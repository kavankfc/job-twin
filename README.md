# Job Twin

An agent workflow I used to tailor my CV for job applications that led to offers from multinational corporations and large enterprises.

## Quick Start

Run this prompt in Claude Code or Codex, replacing `<link of job description>` with the job posting URL:

```text
By following the instructions at https://github.com/kavankfc/job-twin, create a CV for <link of job description>. Use ~/job-twin as the default workspace.
```

The default workspace is `job-twin` inside your home directory (`~/job-twin`).

Keep personal data and generated applications out of the public repository.

## Setup

Use Python 3.11+ and install LibreOffice with `soffice` or `libreoffice` on your PATH for PDF generation.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp config.example.json config.json
```

Set `user_name` in `config.json` to your output filename suffix, such as `first_last`. Open the project as a Git repository; run `git init` if you copied it rather than cloned it.

To install the workflow into an empty project, run this from this checkout, then follow Setup in the destination:

```bash
python3 scripts/install.py /path/to/project
```

The installer copies reusable tooling and instructions, excludes private data, and refuses to overwrite different existing files.

## Documentation

- [Application workflow](instruction.md): authoritative rules for intake, evidence, reviews, versioning, and deliverables.
- [Agent instructions](AGENTS.md): repository entry point and delegation rules.
- [Skills](.agents/skills/): task-specific writing, evidence, review, and finalization guidance.
- [Formatter](formatter/readme.md): commands, output naming, and formatter checks.
