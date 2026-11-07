#!/usr/bin/env python3
"""Format a Markdown resume as Calibri DOCX and PDF."""

from docx_md_formatter import RESUME_SPEC, main
from resume_validation import preflight_job_resume


if __name__ == "__main__":
    raise SystemExit(
        main(
            None,
            RESUME_SPEC,
            "Convert a Markdown resume to a Calibri-formatted Word document and PDF.",
            preflight_job_resume,
        )
    )
