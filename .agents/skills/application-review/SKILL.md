---
name: application-review
description: Independently review a targeted resume or complete application package for factual support, role alignment, senior-HR standout quality, keyword coverage, versioning, and writing quality.
---

# Application Review

## Trigger

Use after every resume/CV draft for the mandatory senior-HR standout gate. Use again after a cover-letter draft exists for the complete-package pre-finalization audit. A missing cover letter is not an error for a CV-only request or the initial resume gate.

## Inputs

Read `shared-rules.md` first, then inspect the normalized job folder:

- `jd.md` and `role_expectations.json`
- `user_subset.json`
- the selected version under `artifacts/resumes/`
- the selected version under `artifacts/cover_letters/`, when the requested scope includes a cover letter
- `methodology_summary.md`; inspect prior versions only when the user explicitly requests historical comparison

## Review scope

Compare the artifacts and return prioritized findings only. Check:

1. **Truth and consistency:** names, titles, employers, dates, locations, metrics, tools, ownership, certifications, and claims agree with the subset and source memory.
2. **Claim support:** every material resume or letter claim has a candidate evidence anchor; adjacent evidence is not presented as direct experience; unsupported JD terms are not claimed.
3. **Keyword evidence coverage:** compare JD-only keywords and role expectations with supported/adjacent/unsupported classifications. Distinguish evidence-bearing coverage from Skills or heading-only mentions and flag missing high-signal terms.
4. **Cross-artifact alignment, when a cover letter is in scope:** resume and cover letter use the same facts, version strategy, target role, gap handling, and employer context without duplicating stories unnecessarily.
5. **Versioning and paths:** confirm zero-padded source versions, no overwritten prior drafts, and placement under the paths required by `shared-rules.md`.
6. **Writing quality:** flag unsupported specificity, JD copying, vague or inflated wording, unclear ownership, repetition, awkward phrasing, and obvious format or length violations. Apply the dedicated writer skills' checks without rewriting their content.

## Senior-HR Standout Gate

Review the resume as a senior HR professional accustomed to screening thousands of CVs per year. Simulate both a 10-second first scan and a careful follow-up read. Judge only role-relevant presentation and evidence; "standout" does not mean flashy design, exaggerated claims, or non-job-related personal characteristics.

Score each dimension from 1 to 5:

1. **Immediate target fit:** the intended role and level are unmistakable.
2. **Top-third strength:** the opening quickly communicates a credible differentiator and relevant value.
3. **Evidence and impact:** the strongest claims are specific, supported, outcome-oriented, and easy to locate.
4. **Role prioritization:** space and ordering reflect the employer's highest-value needs rather than the candidate's full history.
5. **Scan clarity:** headings, density, sentence structure, and repetition support fast comprehension.
6. **Credible voice and differentiation:** the resume sounds like a specific candidate, not a generic template or lightly rewritten JD.

Return `PASS` only when the total is at least 24/30, no dimension is below 3, and there is no blocking or high-severity truth/support issue. Otherwise return `REDRAFT_REQUIRED`. Do not lower the truth bar to improve the score. If missing evidence creates the ceiling, state the exact evidence needed from the user.

## Output

Begin with:

- `HR_STANDOUT_VERDICT: PASS` or `HR_STANDOUT_VERDICT: REDRAFT_REQUIRED`
- the six dimension scores and total out of 30
- a one-sentence hiring-screen conclusion: whether this CV would advance to the hiring manager and why

Then return findings ordered by severity (`blocking`, `high`, `medium`, `low`), each with the artifact/path, location or claim, issue, concise rationale, and an evidence-safe revision direction. On `REDRAFT_REQUIRED`, identify the three changes most likely to improve the next version. Report missing inputs separately. Findings only means no replacement prose, no patch, and no direct file edits.

The existing `.agents/skills/resume-writer/SKILL.md` and `.agents/skills/cover-letter-writer/SKILL.md` own drafting rules; this skill reviews their outputs and does not duplicate or replace them.
