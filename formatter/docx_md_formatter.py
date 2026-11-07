#!/usr/bin/env python3
"""Small Markdown-to-DOCX/PDF formatter for resumes and cover letters."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable
from xml.sax.saxutils import escape


WORD_NS = (
    'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:o="urn:schemas-microsoft-com:office:office" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
    'xmlns:v="urn:schemas-microsoft-com:vml" '
    'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:w10="urn:schemas-microsoft-com:office:word" '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
    'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
    'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
    'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
    'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
    'mc:Ignorable="w14 w15 wp14"'
)


@dataclass
class Span:
    text: str
    bold: bool = False
    italic: bool = False
    href: str | None = None


@dataclass
class Paragraph:
    kind: str
    spans: list[Span] = field(default_factory=list)
    parts: list[list[Span]] | None = None
    # cover letters: line is part of a block (address, signature) with no blank
    # line after it, so it sits tight against the next line.
    tight: bool = False


@dataclass(frozen=True)
class FormatSpec:
    doc_type: str
    margin_twips: int
    right_tab_twips: int
    body_size: int
    line_twips: int
    body_after: int
    bullet_after: int
    section_after: int
    section_before: int
    header_after: int
    page_bottom: int | None = None


RESUME_SPEC = FormatSpec(
    doc_type="resume",
    margin_twips=720,
    right_tab_twips=10800,
    body_size=22,
    line_twips=240,
    body_after=20,
    bullet_after=40,
    section_after=80,
    section_before=80,
    header_after=0,
    page_bottom=720,
)

COVER_LETTER_SPEC = FormatSpec(
    doc_type="cover_letter",
    margin_twips=1440,
    right_tab_twips=9915,
    body_size=22,
    line_twips=278,
    body_after=160,
    bullet_after=120,
    section_after=160,
    section_before=120,
    header_after=160,
    page_bottom=1440,
)


def clean_markdown_text(text: str) -> str:
    return (
        text.replace("\\#", "#")
        .replace("\\-", "-")
        .replace("\\*", "*")
        .replace("\\_", "_")
    )


def parse_inline(text: str) -> list[Span]:
    text = clean_markdown_text(text)
    spans: list[Span] = []
    i = 0
    bold = False
    italic = False
    while i < len(text):
        if text.startswith("**", i):
            bold = not bold
            i += 2
            continue
        if text[i] == "*" and not text.startswith("**", i):
            italic = not italic
            i += 1
            continue
        if text[i] == "[":
            match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", text[i:])
            if match:
                spans.append(Span(match.group(1), bold, italic, match.group(2)))
                i += match.end()
                continue
        next_marks = [p for p in (text.find("**", i), text.find("*", i), text.find("[", i)) if p != -1]
        j = min(next_marks) if next_marks else len(text)
        if j > i:
            spans.append(Span(text[i:j], bold, italic))
        i = j
    return merge_adjacent_spans(spans)


def merge_adjacent_spans(spans: Iterable[Span]) -> list[Span]:
    merged: list[Span] = []
    for span in spans:
        if not span.text:
            continue
        if (
            merged
            and merged[-1].bold == span.bold
            and merged[-1].italic == span.italic
            and merged[-1].href == span.href
        ):
            merged[-1].text += span.text
        else:
            merged.append(span)
    return merged


def paragraph_text(paragraph: Paragraph) -> str:
    if paragraph.parts is not None:
        return "\t".join("".join(span.text for span in part) for part in paragraph.parts)
    return "".join(span.text for span in paragraph.spans)


def is_bold_only(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("**") and stripped.endswith("**") and stripped.count("**") == 2


def unbold(line: str) -> str:
    return line.strip()[2:-2].strip()


def is_section_heading(line: str) -> bool:
    if not is_bold_only(line):
        return False
    text = unbold(line)
    letters = [ch for ch in text if ch.isalpha()]
    return bool(letters) and text.upper() == text


def parse_markdown(markdown: str, doc_type: str) -> list[Paragraph]:
    paragraphs: list[Paragraph] = []
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    header_lines = 3 if doc_type == "resume" else 2
    seen_nonblank = 0

    for raw_line in lines:
        line = raw_line.rstrip()
        # ponytail: skill markdown separates columns with runs of spaces, not tabs.
        line = re.sub(r" {3,}", "\t", line)
        stripped = line.strip()
        if not stripped:
            paragraphs.append(Paragraph("blank"))
            continue

        seen_nonblank += 1
        if "\t" in line:
            parts = [parse_inline(part.strip()) for part in line.split("\t")]
            kind = "header" if seen_nonblank <= header_lines else "tab"
            paragraphs.append(Paragraph(kind, parts=parts))
            continue

        if stripped.startswith(("* ", "- ")):
            paragraphs.append(Paragraph("bullet", parse_inline(stripped[2:].strip())))
            continue

        if is_section_heading(stripped):
            paragraphs.append(Paragraph("section", parse_inline(unbold(stripped))))
            continue

        if is_bold_only(stripped):
            paragraphs.append(Paragraph("subheading", parse_inline(unbold(stripped))))
            continue

        paragraphs.append(Paragraph("body", parse_inline(stripped)))

    if doc_type == "resume":
        # Keep a role heading with its first bullet; a blank paragraph between
        # them would consume the heading's keep-next setting.
        paragraphs = [
            paragraph
            for index, paragraph in enumerate(paragraphs)
            if not (
                paragraph.kind == "blank"
                and index > 0
                and index + 1 < len(paragraphs)
                and paragraphs[index - 1].kind == "tab"
                and paragraphs[index + 1].kind == "bullet"
            )
        ]
    if doc_type == "cover_letter":
        paragraphs = collapse_cover_letter_blanks(paragraphs)
    return trim_blank_edges(paragraphs)


def collapse_cover_letter_blanks(paragraphs: list[Paragraph]) -> list[Paragraph]:
    # A line not followed by a blank line is part of a block (recipient address,
    # signature) and should sit tight against the next line. Blank lines only
    # mark block boundaries; they are dropped from the output.
    kept: list[Paragraph] = []
    for index, paragraph in enumerate(paragraphs):
        if paragraph.kind == "blank":
            continue
        following = paragraphs[index + 1 :]
        next_para = next((p for p in following if p.kind != "blank"), None)
        no_blank_before_next = following and following[0].kind != "blank"
        if next_para is not None and no_blank_before_next:
            paragraph.tight = True
        kept.append(paragraph)
    return kept


def trim_blank_edges(paragraphs: list[Paragraph]) -> list[Paragraph]:
    while paragraphs and paragraphs[0].kind == "blank":
        paragraphs.pop(0)
    while paragraphs and paragraphs[-1].kind == "blank":
        paragraphs.pop()
    return paragraphs


class DocxBuilder:
    def __init__(self, spec: FormatSpec):
        self.spec = spec
        self.relationships: list[tuple[str, str]] = []
        self.next_rel_id = 6
        self.para_id = 1

    def build(self, paragraphs: list[Paragraph]) -> bytes:
        body = "\n".join(self.paragraph_xml(paragraph) for paragraph in paragraphs)
        sect = self.section_properties()
        document_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f"<w:document {WORD_NS}><w:body>{body}{sect}</w:body></w:document>"
        )
        return package_docx(
            document_xml=document_xml,
            relationships=self.relationships,
            font_size=self.spec.body_size,
            font_name="Calibri",
        )

    def paragraph_xml(self, paragraph: Paragraph) -> str:
        kind = paragraph.kind
        if kind == "blank":
            return self.p([], after=0, before=0, size=6)
        if kind == "header":
            return self.p(
                paragraph.parts or [paragraph.spans],
                after=self.spec.header_after,
                right_tab=True,
                bottom_border=self.spec.doc_type == "resume",
                bold_first_part=True,
                size=24 if self.spec.doc_type == "resume" else self.spec.body_size,
            )
        if kind == "tab":
            return self.p(
                paragraph.parts or [paragraph.spans],
                after=self.spec.body_after,
                right_tab=True,
                keep_next=self.spec.doc_type == "resume",
            )
        if kind == "section":
            return self.p(
                [paragraph.spans],
                after=self.spec.section_after,
                before=self.spec.section_before,
                bottom_border=True,
                bold=True,
                keep_next=True,
                size=24,
            )
        if kind == "subheading":
            # In a cover letter the only subheading is the "Re:" line; it needs a
            # gap before the salutation. Resume subheadings stay tight (keep_next).
            after = self.spec.body_after if self.spec.doc_type == "cover_letter" else 0
            return self.p(
                [paragraph.spans],
                after=after,
                before=80,
                bold=True,
                keep_next=self.spec.doc_type != "cover_letter",
            )
        if kind == "bullet":
            return self.p([paragraph.spans], after=self.spec.bullet_after, bullet=True)
        after = 0 if paragraph.tight else self.spec.body_after
        return self.p([paragraph.spans], after=after)

    def p(
        self,
        parts: list[list[Span]],
        *,
        after: int,
        before: int = 0,
        right_tab: bool = False,
        bottom_border: bool = False,
        bold: bool = False,
        bold_first_part: bool = False,
        bullet: bool = False,
        keep_next: bool = False,
        size: int | None = None,
    ) -> str:
        pid = self.para_id
        self.para_id += 1
        ppr = self.ppr(
            after=after,
            before=before,
            right_tab=right_tab,
            bottom_border=bottom_border,
            bullet=bullet,
            keep_next=keep_next,
            size=size,
        )
        runs: list[str] = []
        for part_index, spans in enumerate(parts):
            if part_index:
                runs.append("<w:r><w:tab/></w:r>")
            for span in spans:
                run_span = Span(
                    span.text,
                    bold=span.bold or bold or (bold_first_part and part_index == 0),
                    italic=span.italic,
                    href=span.href,
                )
                runs.append(self.run_xml(run_span, size=size))
        if not runs:
            runs.append("<w:r/>")
        return (
            f'<w:p w14:paraId="{pid:08X}" w:rsidR="00000000" w:rsidRDefault="00000000">'
            f"{ppr}{''.join(runs)}</w:p>"
        )

    def ppr(
        self,
        *,
        after: int,
        before: int,
        right_tab: bool,
        bottom_border: bool,
        bullet: bool,
        keep_next: bool,
        size: int | None,
    ) -> str:
        parts = ["<w:pPr>"]
        if keep_next:
            parts.append("<w:keepNext/>")
        if bullet:
            parts.append('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>')
        if bottom_border:
            parts.append('<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="000000"/></w:pBdr>')
        if right_tab:
            parts.append(f'<w:tabs><w:tab w:val="right" w:leader="none" w:pos="{self.spec.right_tab_twips}"/></w:tabs>')
        parts.append(f'<w:spacing w:after="{after}" w:before="{before}" w:line="{self.spec.line_twips}" w:lineRule="auto"/>')
        if bullet:
            parts.append('<w:ind w:left="720" w:hanging="360"/>')
        if size:
            parts.append(f'<w:rPr><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>')
        parts.append("</w:pPr>")
        return "".join(parts)

    def run_xml(self, span: Span, size: int | None = None) -> str:
        text_parts = []
        pieces = re.split("(\t)", span.text)
        for piece in pieces:
            if piece == "\t":
                text_parts.append("<w:tab/>")
            elif piece:
                text_parts.append(f'<w:t xml:space="preserve">{escape(piece)}</w:t>')
        body = "".join(text_parts)
        rpr = self.rpr(span, size=size)
        run = f"<w:r>{rpr}{body}</w:r>"
        if span.href:
            rel_id = self.add_hyperlink(span.href)
            return f'<w:hyperlink r:id="{rel_id}">{run}</w:hyperlink>'
        return run

    def rpr(self, span: Span, size: int | None = None) -> str:
        parts = ['<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>']
        if span.bold:
            parts.append("<w:b/><w:bCs/>")
        if span.italic:
            parts.append("<w:i/><w:iCs/>")
        if span.href:
            parts.append('<w:color w:val="1155CC"/><w:u w:val="single"/>')
        if size:
            parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
        parts.append("</w:rPr>")
        return "".join(parts)

    def add_hyperlink(self, href: str) -> str:
        target = href
        if "@" in href and not href.startswith(("http://", "https://", "mailto:")):
            target = f"mailto:{href}"
        rel_id = f"rId{self.next_rel_id}"
        self.next_rel_id += 1
        self.relationships.append((rel_id, target))
        return rel_id

    def section_properties(self) -> str:
        bottom = self.spec.page_bottom or self.spec.margin_twips
        margin = self.spec.margin_twips
        return (
            "<w:sectPr>"
            '<w:pgSz w:w="12240" w:h="15840" w:orient="portrait"/>'
            f'<w:pgMar w:top="{margin}" w:right="{margin}" w:bottom="{bottom}" w:left="{margin}" '
            'w:header="720" w:footer="720" w:gutter="0"/>'
            "</w:sectPr>"
        )


def package_docx(
    *, document_xml: str, relationships: list[tuple[str, str]], font_size: int, font_name: str
) -> bytes:
    with tempfile.TemporaryFile() as tmp:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as docx:
            docx.writestr("[Content_Types].xml", content_types_xml())
            docx.writestr("_rels/.rels", package_rels_xml())
            docx.writestr("word/document.xml", document_xml)
            docx.writestr("word/styles.xml", styles_xml(font_name, font_size))
            docx.writestr("word/numbering.xml", numbering_xml())
            docx.writestr("word/settings.xml", settings_xml())
            docx.writestr("word/fontTable.xml", font_table_xml(font_name))
            docx.writestr("word/theme/theme1.xml", theme_xml(font_name))
            docx.writestr("word/_rels/document.xml.rels", document_rels_xml(relationships))
        tmp.seek(0)
        return tmp.read()


def content_types_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
  <Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
</Types>"""


def package_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""


def document_rels_xml(relationships: list[tuple[str, str]]) -> str:
    base = [
        ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles", "styles.xml", None),
        ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings", "settings.xml", None),
        ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable", "fontTable.xml", None),
        ("rId4", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering", "numbering.xml", None),
        ("rId5", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "theme/theme1.xml", None),
    ]
    rows = []
    for rel_id, rel_type, target, mode in base:
        mode_attr = f' TargetMode="{mode}"' if mode else ""
        rows.append(f'<Relationship Id="{rel_id}" Type="{rel_type}" Target="{target}"{mode_attr}/>')
    for rel_id, target in relationships:
        rows.append(
            f'<Relationship Id="{rel_id}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
            f'Target="{escape(target)}" TargetMode="External"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(rows)
        + "</Relationships>"
    )


def styles_xml(font_name: str, font_size: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}" w:eastAsia="{font_name}" w:cs="{font_name}"/>
        <w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/></w:style>
  <w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="1155CC"/><w:u w:val="single"/></w:rPr></w:style>
</w:styles>"""


def numbering_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:multiLevelType w:val="hybridMultilevel"/>
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="bullet"/>
      <w:lvlText w:val="&#x2022;"/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>
      <w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>"""


def settings_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
  <w:compat/>
</w:settings>"""


def font_table_xml(font_name: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:font w:name="{font_name}">
    <w:panose1 w:val="020F0502020204030204"/>
    <w:charset w:val="00"/>
    <w:family w:val="swiss"/>
    <w:pitch w:val="variable"/>
  </w:font>
</w:fonts>"""


def theme_xml(font_name: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Calibri Theme">
  <a:themeElements>
    <a:clrScheme name="Office">
      <a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
      <a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1F497D"/></a:dk2>
      <a:lt2><a:srgbClr val="EEECE1"/></a:lt2>
      <a:accent1><a:srgbClr val="4F81BD"/></a:accent1>
      <a:accent2><a:srgbClr val="C0504D"/></a:accent2>
      <a:accent3><a:srgbClr val="9BBB59"/></a:accent3>
      <a:accent4><a:srgbClr val="8064A2"/></a:accent4>
      <a:accent5><a:srgbClr val="4BACC6"/></a:accent5>
      <a:accent6><a:srgbClr val="F79646"/></a:accent6>
      <a:hlink><a:srgbClr val="0000FF"/></a:hlink>
      <a:folHlink><a:srgbClr val="800080"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Office">
      <a:majorFont><a:latin typeface="{font_name}"/><a:ea typeface="{font_name}"/><a:cs typeface="{font_name}"/></a:majorFont>
      <a:minorFont><a:latin typeface="{font_name}"/><a:ea typeface="{font_name}"/><a:cs typeface="{font_name}"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
</a:theme>"""


def user_name_slug() -> str:
    config_path = Path(__file__).resolve().parent.parent / "config.json"
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))["user_name"]
    except (OSError, KeyError, ValueError):
        return "user"


def write_outputs(input_path: Path, out_dir: Path | None, spec: FormatSpec) -> tuple[Path, Path | None]:
    markdown = input_path.read_text(encoding="utf-8")
    paragraphs = parse_markdown(markdown, spec.doc_type)
    output_dir = out_dir or input_path.parent.parent / "formatted"
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{spec.doc_type}_{user_name_slug()}" if spec.doc_type in ("resume", "cover_letter") else input_path.stem
    docx_path = output_dir / f"{stem}.docx"
    pdf_path = output_dir / f"{stem}.pdf"

    builder = DocxBuilder(spec)
    docx_path.write_bytes(builder.build(paragraphs))

    pdf_ok = convert_pdf(docx_path, pdf_path)
    return docx_path, pdf_path if pdf_ok else None


def convert_pdf(docx_path: Path, pdf_path: Path) -> bool:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("LibreOffice/soffice is required to generate PDFs.")
    pdf_path.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="lo-profile-") as profile_dir:
        profile_uri = Path(profile_dir).resolve().as_uri()
        result = subprocess.run(
            [
                soffice,
                f"-env:UserInstallation={profile_uri}",
                "--headless",
                "--nologo",
                "--nofirststartwizard",
                "--norestore",
                "--nodefault",
                "--convert-to",
                "pdf",
                "--outdir",
                str(pdf_path.parent),
                str(docx_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    converted = pdf_path.parent / f"{docx_path.stem}.pdf"
    if result.returncode == 0 and converted.exists():
        return True
    details = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    if details:
        print(f"LibreOffice/soffice conversion failed:\n{details}", file=sys.stderr)
    else:
        print(f"LibreOffice/soffice conversion failed with exit code {result.returncode}.", file=sys.stderr)
    pdf_path.unlink(missing_ok=True)
    return False


def parse_args(argv: list[str] | None, description: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input", type=Path, help="Markdown file to format")
    parser.add_argument("-o", "--out-dir", type=Path, help="Output directory. Defaults to the input file directory.")
    parser.add_argument("--force", action="store_true", help="Format even if a configured preflight check fails.")
    return parser.parse_args(argv)


def main(
    argv: list[str] | None,
    spec: FormatSpec,
    description: str,
    preflight: Callable[[Path], bool] | None = None,
) -> int:
    args = parse_args(argv, description)
    if not args.input.exists():
        print(f"Input file not found: {args.input}", file=sys.stderr)
        return 1
    if preflight is not None and not preflight(args.input):
        if not args.force:
            print("Resume content validation failed; formatted files were not created. Use --force to format anyway.", file=sys.stderr)
            return 3
        print("Resume content validation failed; continuing because --force was supplied.", file=sys.stderr)
    docx_path, pdf_path = write_outputs(args.input, args.out_dir, spec)
    print(f"Wrote {docx_path}")
    if pdf_path:
        print(f"Wrote {pdf_path}")
    else:
        print("PDF was not created: LibreOffice/soffice conversion failed.", file=sys.stderr)
        return 2
    return 0
