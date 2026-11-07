---
name: application-finalization
description: Finalize already-drafted and reviewed resumes, cover letters, or complete application packages by applying only parent-approved corrections, formatting them with the repository formatter, and verifying versions and output paths.
---

# Application Finalization

## Trigger

Use only after every requested artifact exists and its required independent review has been completed. A CV-only request requires a resume with a senior-HR standout `PASS`; a complete package also requires the cross-artifact review. Do not use this skill to begin drafting or independently decide substantive corrections.

## Required workflow

1. Read the repository-root `instruction.md` and `formatter/readme.md`.
2. Confirm the senior-HR standout `PASS`, parent-approved corrections, and exact active source versions under `instruction.md` → Versioned Application Artifacts.
3. Apply only those approved corrections. Preserve factual evidence and approved wording. Do not add claims, infer missing facts, or perform a broad rewrite.
   - When the parent explicitly includes humanization, revise only the named passages to sound natural and specific; preserve their claims, evidence, meaning, and document structure.
   - If any correction changes resume wording or content after the recorded standout `PASS`, validate the corrected source and return it to the parent for another independent senior-HR standout review. Do not format or deliver that changed resume until the exact version receives `PASS`. Formatting-only changes do not require another content review.
4. Apply source revisions, retirement, and current-output rules from `instruction.md` → Versioned Application Artifacts.
5. Run the requested artifacts' formatter commands from that section with its job-folder output directory.

6. Run applicable Markdown/formatter checks described in `formatter/readme.md`. For resume alignment failures, do not bypass `format_resume.py` with `--force` unless the parent explicitly approves that exception. Ensure PDF conversion succeeds.
7. Verify the current `artifacts/formatted/` folder has the stable DOCX/PDF outputs for every requested artifact; a complete package must contain all four resume and cover-letter files. Remove stale formatted copies only as permitted by `instruction.md`. Verify source and output paths, versions, and that no unapproved content changed.

## Report

Report approved corrections applied, checks and commands run, pass/fail results, source versions, and every generated output path. Stop and report a blocker rather than inventing content or fixing unrelated issues.

The existing `.agents/skills/resume-writer/SKILL.md` and `.agents/skills/cover-letter-writer/SKILL.md` own drafting rules. This skill performs controlled finalization only.
