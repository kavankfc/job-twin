Convert a Markdown resume or cover letter to Calibri DOCX + PDF (requires LibreOffice for PDF).

    python3 formatter/format_resume.py data/YYYYMM/company_role/artifacts/resumes/targeted_resume_vNNN.md --out-dir data/YYYYMM/company_role/artifacts/formatted
    python3 formatter/format_cover_letter.py data/YYYYMM/company_role/artifacts/cover_letters/cover_letter_vNNN.md --out-dir data/YYYYMM/company_role/artifacts/formatted

Outputs use stable names `resume_<user_name>.*` and `cover_letter_<user_name>.*`, with `user_name` read from the gitignored root `config.json` ({"user_name": "first_last"}). Without --out-dir, outputs go to ../formatted relative to the input.

Resume formatting stops when its alignment preflight fails. Add `--force` to format the Markdown file anyway while still printing the validation report.

Self-checks: python3 test_output_naming.py, test_cover_letter_spacing.py, test_convert_pdf_profile.py (run from formatter/).
