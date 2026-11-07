---
name: job-description-evaluation
description: Evaluate a job description during intake, normalize raw postings, create employer-side role_expectations.json, and produce an evidence-based fit assessment without drafting application artifacts.
---

# Job Description Evaluation

## Trigger

Use for new job/JD intake, JD normalization, employer-side role analysis, or a fit assessment.

## Required workflow

1. From the repository root, read `instruction.md` before processing the JD.
2. Check `data/raw/*.md`. Normalize every new raw Markdown posting first, following `instruction.md`:
   - infer company and role;
   - create `data/YYYYMM/company_role_title/` using lowercase snake case;
   - preserve the posting as `jd.md`;
   - create or update that folder's `methodology_summary.md`.
3. If a normalized folder already exists, use its `jd.md` and preserve existing artifacts.
4. Keep `role_expectations.json` strictly employer-side. Record posting metadata, role purpose, duties, requirements, assets/provisos, seniority signals, inferred day-to-day expectations, success measures, and concise JD-only keywords. Mark inference explicitly.
5. If comparing against the candidate, read `.agents/skills/user-json-memory/SKILL.md` before reading `data/user/`. Cite source files and distinguish evidence from inference.
6. Produce a separate fit assessment based mainly on requirements. Classify each material requirement or keyword as `supported`, `adjacent`, or `gap` (use `unsupported` when a term has no candidate evidence). Explain the evidence or missing evidence and any score.

## Outputs

- `data/YYYYMM/company_role_title/role_expectations.json`
- `data/YYYYMM/company_role_title/fit_assessment.md` (or the existing job-folder fit-assessment convention)
- `data/YYYYMM/company_role_title/methodology_summary.md` for job-specific intake notes

Maintain a hard boundary: employer facts and marked inferences belong in `role_expectations.json`; candidate facts, classifications, and fit reasoning belong in the fit assessment. Do not put candidate evidence, fit scores, application strategy, or gap advice in `role_expectations.json`.

## Non-goals

Do not draft or revise a resume/CV, cover letter, or other candidate artifact. The existing `.agents/skills/resume-writer/SKILL.md` and `.agents/skills/cover-letter-writer/SKILL.md` own all drafting rules.
