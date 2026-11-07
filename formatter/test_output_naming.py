"""Self-check for stable formatted artifact names. Run: python3 test_output_naming.py"""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree
from zipfile import ZipFile

from docx_md_formatter import COVER_LETTER_SPEC, RESUME_SPEC, user_name_slug, write_outputs


def fake_convert(_docx_path: Path, pdf_path: Path) -> bool:
    pdf_path.write_bytes(b"%PDF-1.4\n")
    return True


def main() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        resume = root / "artifacts" / "resumes" / "targeted_resume_v003.md"
        cover = root / "artifacts" / "cover_letters" / "cover_letter_v007.md"
        out = root / "artifacts" / "formatted"
        resume.parent.mkdir(parents=True)
        cover.parent.mkdir(parents=True)
        resume.write_text("**Test User**\n\n**PROFILE**\n\nBody\n", encoding="utf-8")
        cover.write_text("July 3, 2026\n\nDear Hiring Team,\n\nBody\n", encoding="utf-8")

        with patch("docx_md_formatter.convert_pdf", side_effect=fake_convert):
            resume_docx, resume_pdf = write_outputs(resume, out, RESUME_SPEC)
            cover_docx, cover_pdf = write_outputs(cover, out, COVER_LETTER_SPEC)

        slug = user_name_slug()
        assert resume_docx == out / f"resume_{slug}.docx"
        assert resume_pdf == out / f"resume_{slug}.pdf"
        assert cover_docx == out / f"cover_letter_{slug}.docx"
        assert cover_pdf == out / f"cover_letter_{slug}.pdf"

        with ZipFile(resume_docx) as docx:
            theme = ElementTree.fromstring(docx.read("word/theme/theme1.xml"))
        namespace = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
        for family in ("majorFont", "minorFont"):
            fonts = theme.find(f".//a:{family}", namespace)
            assert fonts is not None
            for script in ("latin", "ea", "cs"):
                font = fonts.find(f"a:{script}", namespace)
                assert font is not None and font.get("typeface")

    print("ok")


if __name__ == "__main__":
    main()
