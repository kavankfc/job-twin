"""Self-check for sandbox-safe LibreOffice conversion.

Run: python3 test_convert_pdf_profile.py
"""

from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
from unittest.mock import patch

from docx_md_formatter import convert_pdf


def main() -> None:
    seen_command: list[str] = []

    def fake_run(command, **_kwargs):
        seen_command[:] = command
        outdir = Path(command[command.index("--outdir") + 1])
        docx = Path(command[-1])
        (outdir / f"{docx.stem}.pdf").write_bytes(b"%PDF-1.4\n")
        return CompletedProcess(command, 0, "", "")

    with TemporaryDirectory() as tmp:
        docx_path = Path(tmp) / "resume.docx"
        pdf_path = Path(tmp) / "resume.pdf"
        docx_path.write_bytes(b"docx")

        with patch("docx_md_formatter.shutil.which", return_value="/usr/bin/soffice"):
            with patch("docx_md_formatter.subprocess.run", side_effect=fake_run):
                assert convert_pdf(docx_path, pdf_path) is True

    assert any(arg.startswith("-env:UserInstallation=file://") for arg in seen_command)
    assert "--headless" in seen_command
    assert "--nofirststartwizard" in seen_command
    print("ok")


if __name__ == "__main__":
    main()
