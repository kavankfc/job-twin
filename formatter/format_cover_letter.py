#!/usr/bin/env python3
"""Format a Markdown cover letter as Calibri DOCX and PDF."""

from docx_md_formatter import COVER_LETTER_SPEC, main


if __name__ == "__main__":
    raise SystemExit(
        main(
            None,
            COVER_LETTER_SPEC,
            "Convert a Markdown cover letter to a Calibri-formatted Word document and PDF.",
        )
    )
