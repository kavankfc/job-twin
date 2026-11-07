Start from the repository root and read `instruction.md` before processing job descriptions or creating targeted application materials. That file is the source of truth for the job intake workflow, including how to turn random Markdown files in `data/raw/` into normalized `data/YYYYMM/company_role_title/jd.md` folders.

When editing the split user memory rooted at `data/user/index.json`, first read and follow `.agents/skills/user-json-memory/SKILL.md`.

When creating targeted job application materials, follow `instruction.md` first. For CVs/resumes, use `.agents/skills/resume-writer/SKILL.md`; for cover letters, use `.agents/skills/cover-letter-writer/SKILL.md` in this workspace.

When creating or updating application status history, follow `.agents/skills/application-log/SKILL.md`.

## Active application working set

Treat `data/` as Codex's active working set. Keep only the latest source version of each resume/CV family and the latest cover-letter source in each active job folder. When creating a new revision, move the previous active Markdown source first to the matching root-level `retired/YYYYMM/company_role_title/artifacts/{resumes,cover_letters}/` path, preserving its filename, then write the new active source. Never retire `jd.md`, `role_expectations.json`, `user_subset.json`, methodology summaries, current formatted deliverables, or factual memory under `data/user/`. Do not read or use `retired/` for drafting, reviewing, or finalizing unless the user explicitly asks for historical comparison or recovery.

## Codex delegation

The parent orchestrator must dispatch the job-application pipeline in this order:

1. `job_description_evaluator` reads the normalized JD and writes employer-side role expectations.
2. `candidate_evidence_librarian` reads those expectations and the relevant split user memory, then writes the factual candidate subset.
3. `resume_writer` creates the evidence-grounded resume draft.
4. `application_reviewer` independently applies the senior-HR standout gate to the current resume without rewriting it. If the verdict is `REDRAFT_REQUIRED`, the parent sends the prioritized findings back to the same `resume_writer`, which creates the next version; repeat the gate. Allow at most two reviewer-led redrafts (three drafts total) per request. If the resume still fails because the evidence is insufficient, stop and ask the user for missing evidence instead of inventing claims or continuing cosmetic rewrites.
5. After the resume receives `PASS`, `cover_letter_writer` may draft from that approved current resume.
6. `application_reviewer` independently reviews the complete package for cross-artifact accuracy and alignment without rewriting it. For a CV-only request, this package pass is not required.
7. `application_finisher` applies only the narrow corrections requested by the parent and performs the final validation/formatting pass for the requested artifacts. If it changes resume wording or content after a `PASS`, the parent must send that exact new version through the senior-HR standout gate again before final formatting or delivery; formatting-only changes do not require another content review.

Do not run the evaluator and librarian in parallel: the librarian depends on the evaluator's role expectations. Select the most specific role for each task, prefer this pipeline over ad-hoc delegation, and never delegate one task to multiple writers. Every handoff must return paths, facts and assumptions, validation performed, and unresolved blockers.
