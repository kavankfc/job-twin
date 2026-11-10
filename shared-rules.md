# Shared Application Rules

Read this file before delegated application work, then load only the assigned skill and the inputs needed for the task. The parent reads `instruction.md` for intake and orchestration; subagents do not need that full guide unless the parent assigns work from it.

## Evidence And Scope

- Work in the normalized job folder provided by the parent. Return raw postings to the parent for intake; preserve `jd.md` exactly.
- Keep employer facts, candidate facts, inference, and assumptions distinct. Never invent experience, metrics, tools, ownership, credentials, eligibility, or employer requirements. Adjacent evidence is not a direct match.
- The evaluator owns employer expectations; the librarian owns candidate classifications and gap interviews. Writers return missing or conflicting evidence through the parent to the librarian before drafting affected claims.
- Before reading or editing `data/user/`, follow `.agents/skills/user-json-memory/SKILL.md`. Save durable facts only within the assigned scope and existing user authorization.
- Keep candidate memory, raw postings, analysis, application artifacts, and job notes private. Never add them or local `config.json` to the public repository.
- Modify only assigned files. The parent owns intake, methodology notes, application logging, and pipeline decisions. Load other skills only when their work is required by the assignment.

## Versioned Application Artifacts

`data/` is the active working set. Each active job folder retains only the latest source version of each artifact family: the latest targeted resume, latest chronological resume when present, and latest cover letter. Superseded resume/CV and cover-letter Markdown sources belong in the matching root-level `retired/YYYYMM/company_role_title/artifacts/{resumes,cover_letters}/` directory, preserving their existing filenames. Never retire `jd.md`, `role_expectations.json`, `user_subset.json`, `methodology_summary.md`, current formatted deliverables, or factual memory under `data/user/`. Codex must not read or use `retired/` when drafting, reviewing, or finalizing unless the user explicitly asks for a historical comparison or recovery.

Use this structure:

```text
data/YYYYMM/company_role_title/
  artifacts/
    resumes/
      targeted_resume_v001.md
      chronological_resume_v001.md
    cover_letters/
      cover_letter_v001.md
    formatted/
      resume_<user_name>.docx
      resume_<user_name>.pdf
      cover_letter_<user_name>.docx
      cover_letter_<user_name>.pdf

retired/YYYYMM/company_role_title/
  artifacts/
    resumes/       # superseded source Markdown, original filenames preserved
    cover_letters/ # superseded source Markdown, original filenames preserved
```

Versioning rules:

- Use zero-padded version numbers: `v001`, `v002`, `v003`.
- Never overwrite an existing source or retirement destination.
- Before creating a resume/CV, inspect the active `artifacts/resumes/` and identify the latest relevant version.
- Before creating a cover letter, inspect the active `artifacts/cover_letters/` and identify the latest version.
- If the user asks for a revision, use the latest active artifact plus the user's comments as the starting point, move that previous active source to the matching `retired/` location first, then create the next version.
- If the user asks for a fresh rewrite or a different format, still create the next version and report the reset or format change to the parent for `methodology_summary.md`.
- Keep artifact filenames stable and generic within the job folder; preserve each superseded source filename when moving it to `retired/` so diff tools can compare versions easily.
- Keep `artifacts/resumes/` and `artifacts/cover_letters/` Markdown-only. Put generated `.docx` and `.pdf` files under `artifacts/formatted/`.
- Treat `artifacts/formatted/` as the current ready-to-submit output folder, not a version history folder. Keep only one formatted resume and one formatted cover letter per job, each with DOCX and PDF copies.
- After the resume receives the senior-HR standout `PASS` and all requested artifacts complete their required review, run the formatter in the same workflow pass:
  - Resume/CV: `python3 formatter/format_resume.py data/YYYYMM/company_role_title/artifacts/resumes/targeted_resume_vNNN.md --out-dir data/YYYYMM/company_role_title/artifacts/formatted`
  - Cover letter: `python3 formatter/format_cover_letter.py data/YYYYMM/company_role_title/artifacts/cover_letters/cover_letter_vNNN.md --out-dir data/YYYYMM/company_role_title/artifacts/formatted`
  - The formatter writes the stable filenames itself (`resume_<user_name>.docx`/`.pdf`, `cover_letter_<user_name>.docx`/`.pdf`), reading `<user_name>` from the gitignored root `config.json` (`{"user_name": "first_last"}`). If any older versioned outputs remain in `artifacts/formatted/`, remove them so the folder contains only the current four ready-to-submit files.
- If the formatter creates DOCX but PDF conversion fails, fix the formatter/conversion issue or use its repo-native fallback path before finishing; do not leave a generated application package with only Markdown and DOCX unless the user explicitly accepts that.
- Return newly generated artifact paths and the reason for the new version to the parent for the job-folder `methodology_summary.md`.

## Reviews And Handoffs

- Every resume draft requires independent `application_reviewer` review. Writers cannot self-certify `PASS`. The parent permits at most two reviewer-led redrafts per request; unresolved evidence gaps return to the librarian.
- Cover-letter drafting starts only after the exact current resume receives `PASS`. A complete package also requires cross-artifact review; a CV-only request does not.
- If resume wording or content changes after `PASS`, return that exact version for another independent review before formatting or delivery. Formatting-only changes do not require another content review.
- Return paths created, changed, or reviewed; facts and assumptions; validation performed and results; unresolved blockers; and the exact source version for the next stage. Report version changes and reasons to the parent for `methodology_summary.md`.
