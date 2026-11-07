# Job Application Skills and Formatter

An agent workflow for turning job descriptions and private candidate evidence into targeted CVs and cover letters, with independent review and DOCX/PDF formatting.

## Setup

Use Python 3.11 or newer. Install LibreOffice and ensure `soffice` or `libreoffice` is on your PATH to generate PDFs.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp config.example.json config.json
```

Set `user_name` in your local `config.json` to the filename suffix you want, such as `first_last`. Keep personal information in ignored local files.

For the included Codex agent setup, open the project as a Git repository. Its startup hook uses `git rev-parse --show-toplevel` to locate the repository root. Run `git init` if this directory was copied rather than cloned.

## Install into another project

Create an empty target directory, then run this command from this checkout:

```bash
python3 scripts/install.py /path/to/project
```

The installer copies all nine skills, six Codex agents, the startup hook,
instructions, formatter, dependency list, and public configuration template as
one workflow. Python 3.11+ is sufficient to run the installer. Follow Setup above
in the destination to install its Python dependency and configure your name.
Initialize Git there if needed, then start a new Codex session and use Codex's
normal project trust and hook approval flow.

No personal data, retired drafts, generated applications, local `config.json`,
virtual environment, or Git history is copied. Identical files are skipped, so
repeat installs are safe. Different files, custom Codex configuration, or
symlinked destinations stop the install before any files are copied; reconcile
them manually before retrying. Existing files are never overwritten. Use an
empty directory or an unmodified matching workflow checkout.

## Usage

Ask your agent to read `AGENTS.md` and `instruction.md` from the repository root before application work. All nine skills are under `.agents/skills/`; the six agent definitions and startup hook remain under Codex's native `.codex/` directory.

Provide candidate facts privately using the split-memory layout described in `.agents/skills/user-json-memory/SKILL.md` and its JSON schema. Start at `data/user/index.json`; register the profile, skills, preferences, experience, projects, education, and completed certifications there. This project includes no candidate records or application materials.

Validate your local memory before drafting:

```bash
python3 .agents/skills/user-json-memory/validate_user_memory.py
```

Provide a full job posting under `data/raw/`, or give the agent a posting URL. For a URL, the agent must retrieve the complete posting using its available web/browser tools, preserve the source URL in the job methodology notes, and save the posting as `jd.md` in a normalized job folder before evaluation. If retrieval fails, provide the posting text. This repository does not include a web scraper.

The required sequence is evaluator → evidence librarian → resume writer → independent resume review → cover-letter writer → package review → finisher. The cover letter starts only after the current CV passes review. The evaluator defines employer expectations; the librarian owns candidate matching, the fit assessment, and evidence interviews using `grill-me`. Writers use those classifications and return new evidence issues through the parent; the reviewer independently checks the resulting claims.

After the required reviews pass, format the Markdown sources:

```bash
python3 formatter/format_resume.py data/YYYYMM/company_role/artifacts/resumes/targeted_resume_v001.md --out-dir data/YYYYMM/company_role/artifacts/formatted
python3 formatter/format_cover_letter.py data/YYYYMM/company_role/artifacts/cover_letters/cover_letter_v001.md --out-dir data/YYYYMM/company_role/artifacts/formatted
```

Outputs use `resume_<user_name>.docx`/`.pdf` and `cover_letter_<user_name>.docx`/`.pdf`. Inspect the PDFs for page breaks and layout before submission. See `formatter/readme.md` for formatter details.

## Checks and Limits

Run the formatter self-checks from `formatter/`:

```bash
cd formatter
python3 test_output_naming.py
python3 test_cover_letter_spacing.py
python3 test_convert_pdf_profile.py
python3 test_resume_validation.py
```

Run installer and relocated-validator checks from the repository root after
installing `requirements.txt`:

```bash
python3 scripts/test_install.py
```

The PDF self-checks mock LibreOffice; they do not verify actual PDF rendering. The formatter checks resume keyword planning and coverage, while agents must verify factual support, writing quality, and independent review status. Cover-letter length and content also require agent review.

Automatic prior-version comparison searches the active resume directory. Record coverage before retiring a prior source; do not read `retired/` unless the user explicitly requests historical comparison or recovery.

Private data, retired drafts, generated applications, and local configuration are ignored by Git. Do not add them to a public repository.
