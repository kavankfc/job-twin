# Targeted Application Instructions

Use this repo-level instruction file when turning a job description and the split user memory rooted at `data/user/index.json` into targeted application materials. Agents should read this file from the repository root before processing new job descriptions, normalizing raw job postings, analyzing fit, or creating resumes/CVs and cover letters.

This file owns the repeatable application pipeline. CV-specific writing knowledge belongs in `.agents/skills/resume-writer/SKILL.md`; cover-letter-specific writing knowledge belongs in `.agents/skills/cover-letter-writer/SKILL.md`.

## Agent Starting Goal

When starting from the repository root, first determine whether there are new raw job descriptions waiting under `data/raw/`.

- If `data/raw/*.md` exists, create a normalized job folder for each raw JD before drafting materials.
- If a job already has a folder with `jd.md`, work inside that job folder and follow the targeted application workflow below.
- Create an application-specific `methodology_summary.md` inside each normalized job folder. Keep reusable process rules in this root `instruction.md`.

## Raw JD Intake

Users may create Markdown files with arbitrary filenames under `data/raw/`. Treat each raw Markdown file as a new job description that needs a stable folder for downstream agents.

For each new `data/raw/*.md` file:

1. Read the JD content and infer the company name and role title.
2. Create a concise, lowercase, snake_case folder name from the company and role, such as `company_role_title`.
3. Create the current month folder using `YYYYMM` format based on today's date (e.g., `data/202607/` for July 2026).
4. Create the destination folder at `data/YYYYMM/company_role_title/`.
5. Copy or move the raw JD content into `data/YYYYMM/company_role_title/jd.md`, preserving the original posting text.
6. Create `data/YYYYMM/company_role_title/methodology_summary.md` for job-specific notes, including the source raw file, inferred company and role, normalized folder path, generated artifacts, fit positioning, and any gaps or assumptions future agents should preserve.
7. Continue the targeted application workflow from that new job folder so later agents know where to pick up the work.

Do not use the random raw filename as the job folder name unless it already clearly matches the company and role. Do not create new job folders under legacy month folder names that do not match `YYYYMM`.

## Git Versioning Policy

Keep this repository safe to publish by default. The public repo should contain reusable tooling, instructions, formatters, and skills, not personal application data.

- Do not track `data/`, `user.json`, `jobs/`, `drafts/`, `accepted/`, `inputs/`, or `private-applications/` in this public repo.
- Treat raw JDs, generated resumes/CVs, cover letters, fit assessments, role analysis JSON, candidate subsets, and job-folder notes as private application data.
- If you want version history for generated CVs and cover letters, use a separate private/local Git repo for those artifacts. In this workspace, `data/` is ignored by the public repo and can be used as that private local Git repo.
- Keep the private versioning repo organized by job folder so tools can compare revisions with normal Git commands such as `git diff`, `git log -p`, or visual diff tools.
- In the private `data/` repo, keep raw JDs and analysis JSON ignored while tracking generated resumes/CVs, cover letters, fit assessments, and job-folder methodology notes.
- If private files were already tracked before this policy existed, remove them from the public Git index without deleting the local files before publishing.

## Source Inputs

- Job description file, usually `jd.md` or `job_description.md` inside `data/YYYYMM/company_role_title/`.
- Split user memory rooted at `data/user/index.json`, with canonical files under `data/user/`.
  - Use `data/user/profile.json` for candidate identity, professional identity, company preferences, career-transition context, and planned credential commitments.
  - Use `data/user/skills.json` as the factual skill index.
  - Use `data/user/experience/*.json` for role-level STAR evidence.
  - Use `data/user/resume_preferences.json` for user-specific display and voice/style preferences. Keep reusable agent methodology in this file and the artifact-specific skills.
- Existing extracted role files, if present.
- Existing active resume/CV or cover-letter artifacts for the same job, if present. Do not read or use `retired/` unless the user explicitly asks for a historical comparison or recovery.
- Existing skills, if available:
  - `.agents/skills/user-json-memory/SKILL.md`
  - `.agents/skills/resume-writer/SKILL.md`
  - `.agents/skills/cover-letter-writer/SKILL.md`
  - `.agents/skills/application-log/SKILL.md`
- Job-folder `methodology_summary.md`, creating it if it does not already exist.

## Application Log

Keep application status history in `data/application_log.csv`. Before adding or changing rows, read and follow `.agents/skills/application-log/SKILL.md`; that skill owns the CSV schema, ID rules, duplicate-drafted handling, sorting, and parseability checks.

Required columns:

```text
date,application_id,company_name,company_sector,role_name,application_status,note
```

Use one row per application status event, except repeated `drafted` updates for the same company and role, which update the existing drafted row's date. Leave `note` blank unless the user explicitly provides note text.

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
- Before creating a resume/CV, inspect the active `artifacts/resumes/` and identify the latest relevant version.
- Before creating a cover letter, inspect the active `artifacts/cover_letters/` and identify the latest version.
- If the user asks for a revision, use the latest active artifact plus the user's comments as the starting point, move that previous active source to the matching `retired/` location first, then create the next version.
- If the user asks for a fresh rewrite or a different format, still create the next version and note the reset or format change in `methodology_summary.md`.
- Keep artifact filenames stable and generic within the job folder; preserve each superseded source filename when moving it to `retired/` so diff tools can compare versions easily.
- Keep `artifacts/resumes/` and `artifacts/cover_letters/` Markdown-only. Put generated `.docx` and `.pdf` files under `artifacts/formatted/`.
- Treat `artifacts/formatted/` as the current ready-to-submit output folder, not a version history folder. Keep only one formatted resume and one formatted cover letter per job, each with DOCX and PDF copies.
- After the resume receives the senior-HR standout `PASS` and all requested artifacts complete their required review, run the formatter in the same workflow pass:
  - Resume/CV: `python3 formatter/format_resume.py data/YYYYMM/company_role_title/artifacts/resumes/targeted_resume_vNNN.md --out-dir data/YYYYMM/company_role_title/artifacts/formatted`
  - Cover letter: `python3 formatter/format_cover_letter.py data/YYYYMM/company_role_title/artifacts/cover_letters/cover_letter_vNNN.md --out-dir data/YYYYMM/company_role_title/artifacts/formatted`
  - The formatter writes the stable filenames itself (`resume_<user_name>.docx`/`.pdf`, `cover_letter_<user_name>.docx`/`.pdf`), reading `<user_name>` from the gitignored root `config.json` (`{"user_name": "first_last"}`). If any older versioned outputs remain in `artifacts/formatted/`, remove them so the folder contains only the current four ready-to-submit files.
- If the formatter creates DOCX but PDF conversion fails, fix the formatter/conversion issue or use its repo-native fallback path before finishing; do not leave a generated application package with only Markdown and DOCX unless the user explicitly accepts that.
- Record newly generated artifact paths and the reason for the new version in the job-folder `methodology_summary.md`.

## Workflow

1. Read and normalize the job description.
   - Identify the company, industry, role title, level, department, location, work arrangement, employment type, salary range, and close date.
   - Separate company background from the actual role expectations.
   - Focus mainly on duties, requirements, tools, domain knowledge, and success signals.

2. Create `role_expectations.json`.
   - Keep this file strictly employer-side: JD facts plus clearly marked inference only.
   - Include the required concepts, not a rigid schema: source file, posting metadata, company/industry context, role purpose, key duties, requirements, assets/provisos, inferred day-to-day expectations, likely success measures, seniority signals, and keywords.
   - Do not include candidate facts, split user-memory evidence, fit scores, supported/unsupported classifications, application strategy, or gap-handling advice.
   - Add a `keywords` field with exact or near-exact wording from the JD only for high-signal terms that represent the employer's ideal-candidate characteristics, role identity, core capabilities, frameworks, tools, methods, domain expertise, or success signals.
   - Keep `keywords` concise. Do not dump every responsibility phrase, generic stakeholder noun, action verb, interview detail, or low-signal JD wording into this field. Put those details in `duties`, `inferred_day_to_day_expectations`, or notes instead.
   - Keep `keywords` JD-only. Do not split keywords by whether they are supported by the candidate; that comparison belongs in `user_subset.json`.

3. Compare the role against the split user memory.
   - Score fit mainly against job requirements, not generic company appeal.
   - Separate direct matches, adjacent matches, and gaps, especially for missing tools, domain experience, certifications, or seniority.
   - Use simple scoring when useful, such as `L3: 82/100`, `L4: 68/100`, or `Overall: 75/100`.
   - Explain scores with evidence from `data/user/` files, not vibes.

4. Create `user_subset.json`.
   - Use the split user memory rooted at `data/user/index.json` as the source of truth.
   - Include the required concepts, not a rigid schema: source files, target role focus, role-relevant skills, selected experience, why each selected experience matters, supported/adjacent/unsupported keyword handling, and gap notes.
   - For high-value selected experience, preserve the resume-writing logic explicitly: role expectation matched, primary causal driver, supporting tools or methodology, and measurable/observable outcome.
   - Include all jobs if requested; otherwise keep only role-relevant experience.
   - Preserve enough role facts for every included job to draft accurately: title, organization, location, dates, relevant skills, relevant evidence, and relevance to the target role.
   - Mark gaps carefully. Do not turn adjacent evidence into direct claims.

5. Draft the targeted resume/CV.
   - Use `.agents/skills/resume-writer/SKILL.md` for all CV-writing rules, structure, and quality checks.
   - Use `user_subset.json` as the main source.
   - Before writing prose, add a compact `resume_plan` to `user_subset.json`. For every supported keyword, record its priority (`must_cover` or `supporting`), evidence anchor, planned wording, primary section, and treatment (`exact`, `variant`, or `omit_with_reason`). An omission or variant requires a reason. Add a short `voice_brief` based on user-approved wording and `resume_preferences.json`.
   - Draft Employment History and relevant Projects from candidate evidence and the `voice_brief` first. Apply planned JD vocabulary to those stories second, then write the profile and skills from the completed evidence. Use exact supported nouns where recognition matters, but keep verbs, sentence structure, ownership, stakeholders, tools, and outcomes candidate-led.
   - Do not add Core Competencies or abstract skill taxonomies solely to carry keywords. A Skills-section or heading mention is surface coverage, not evidence coverage.
   - Before formatting, run the resume alignment preflight. Every supported keyword must be present as planned or explicitly waived; unsupported keywords must not appear; and a revision must not silently lose supported terms from the preceding version. `formatter/format_resume.py` runs this preflight automatically for job-folder resumes and stops before creating DOCX/PDF files when it fails. If the user explicitly wants the Markdown formatted despite those failures, rerun it with `--force`; the validation report is still printed.
   - Inspect the active `artifacts/resumes/` family, move its previous active source to the matching root-level `retired/YYYYMM/company_role_title/artifacts/resumes/` path first, then create the next versioned Markdown filename, such as `targeted_resume_v001.md` or `chronological_resume_v001.md`.
   - If revising an existing resume/CV, read the latest active version first and apply the user's comments to produce the next version; do not use `retired/` unless the user explicitly asks for historical comparison or recovery.
   - Before treating the resume as final, send it to the independent `application_reviewer` for the senior-HR standout gate defined in `.agents/skills/application-review/SKILL.md`. The reviewer must return `PASS` or `REDRAFT_REQUIRED`; the writer must not self-certify this gate.
   - On `REDRAFT_REQUIRED`, return the reviewer's prioritized, evidence-safe directions to the same `resume_writer`. Retire the failed active source, create the next version, and repeat the independent gate. Allow at most two reviewer-led redrafts (three drafts total) per request. If missing evidence prevents a pass, pause for targeted user evidence rather than inventing content or cycling through cosmetic rewrites.
   - During this review/redraft loop, run `python3 formatter/resume_validation.py <resume-path>` on every draft, but create the ready-to-submit formatted copies only after the resume receives `PASS`.
   - Do not duplicate detailed CV guidance in this file; keep CV-specific knowledge in the CV skill.

6. Draft the targeted cover letter.
   - Use `.agents/skills/cover-letter-writer/SKILL.md` for all cover-letter writing rules, structure, and quality checks.
   - Start only after the current resume receives the senior-HR standout `PASS`, and read that approved version before drafting.
   - Use `role_expectations.json.keywords` as the employer's JD-only vocabulary guide, and use `user_subset.json` to decide which keywords are supported, adjacent, or unsupported. Mirror exact wording only where it improves alignment without sounding copied or overclaimed.
   - Inspect the active `artifacts/cover_letters/` family, move its previous active source to the matching root-level `retired/YYYYMM/company_role_title/artifacts/cover_letters/` path first, then create the next versioned Markdown filename, such as `cover_letter_v001.md`.
   - If revising an existing cover letter, read the latest active version first and apply the user's comments to produce the next version; do not use `retired/` unless the user explicitly asks for historical comparison or recovery.
   - Use the company address if available from the JD or official source.
   - Salary should usually stay out of the cover letter unless the user explicitly asks.

7. Create final formatted deliverable copies.
   - If any resume wording or content changed after its latest senior-HR standout `PASS`, send that exact active source back to `application_reviewer` and require another `PASS` before formatting. Formatting-only changes do not require another content review.
   - Follow the formatting and `artifacts/formatted/` copy rules in Versioned Application Artifacts.

8. Update the job-folder `methodology_summary.md`.
   - Use this file for job-specific notes only.
   - Include the source JD path and normalized job folder.
   - Include inferred company and role.
   - List generated artifacts and note why each new resume/CV or cover-letter version was created.
   - Summarize fit, positioning strategy, explicit gap-handling decisions, the final senior-HR standout verdict and attempt count, and assumptions future agents should preserve.
   - Keep this file job-specific; do not duplicate the full root instructions unless the reusable workflow itself changed.

9. Update `data/application_log.csv` when a new application is identified or its status changes.
   - Use `.agents/skills/application-log/SKILL.md`.
   - Record drafted/submitted/interview/rejected/accepted/withdrawn status changes according to the long-format rules in that skill.

10. Update the split user memory only if a reusable fact emerges.
   - First read `.agents/skills/user-json-memory/SKILL.md`.
   - Add only durable, application-neutral facts.
   - Do not add company-specific intent, one-off cover-letter wording, or unsupported skills.
   - Validate JSON after editing:

```bash
jq empty data/user/*.json data/user/experience/*.json
python3 .agents/skills/user-json-memory/validate_user_memory.py
```

The validator should print `user memory schema ok`.

## Writing Principles

- Use the JD to select priorities; draft sentences from candidate evidence and user-approved voice, not from JD prose.
- Build role expectations before writing application materials.
- Use split user memory facts for evidence and `user_subset.json` for targeting.
- Separate direct evidence from transferable evidence.
- Do not claim tools, platforms, industries, certifications, or seniority that are not supported.
- Make gaps sound manageable, not hidden.
- Keep artifact-specific writing rules in their dedicated skill files.

## Recommended Output Sequence

1. `role_expectations.json`
2. Fit score or match notes
3. `user_subset.json`
4. Versioned targeted resume/CV Markdown under `artifacts/resumes/`
5. Independent senior-HR standout verdict; reviewer-led resume revision(s) when required
6. Versioned targeted cover letter Markdown under `artifacts/cover_letters/`
7. Current ready-to-submit DOCX/PDF copies under `artifacts/formatted/`
8. Job-folder `methodology_summary.md`
9. `data/application_log.csv` update
10. Optional split user-memory update

## Quality Checklist

- The JD was read and distilled before drafting.
- The role expectation file separates duties, requirements, assets, and inferred expectations.
- The candidate subset is grounded in the split user memory.
- Every job included has role-relevant evidence only.
- Direct, adjacent, and gap areas are clearly separated.
- The targeted resume/CV follows `.agents/skills/resume-writer/SKILL.md`.
- The targeted cover letter follows `.agents/skills/cover-letter-writer/SKILL.md`.
- New resume/CV and cover-letter versions are created after the previous active source is moved to the matching `retired/` location, rather than overwriting or retaining superseded sources in the active folder.
- Revisions are based on the latest relevant artifact plus the user's comments.
- Every supported resume keyword has an intentional evidence anchor and treatment in `resume_plan`; adjacent and unsupported terms are not counted as direct coverage.
- Resume alignment was checked by section, and no revision lost a supported term without an explicit reason.
- No sentence, Skills bucket, or Core Competencies section exists solely to carry JD wording.
- The independent senior-HR standout gate returned `PASS`; any `REDRAFT_REQUIRED` verdict produced a substantive, evidence-safe new version rather than synonym-only polishing.
- Formatted PDFs are visually checked so section headings or role headings are not stranded as the last line of a page while their content starts on the next page.
- Job-folder `methodology_summary.md` exists and records the generated artifacts and positioning decisions.
- `data/application_log.csv` records new applications and status changes in long format.
- Tool and domain gaps are handled honestly.
- JSON files parse successfully.
