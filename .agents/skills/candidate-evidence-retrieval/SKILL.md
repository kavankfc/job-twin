---
name: candidate-evidence-retrieval
description: Own candidate-to-JD matching, evidence-gap interviews, user_subset.json, and fit_assessment.md. Select factual experience, certifications, and skills without inventing claims.
---

# Candidate Evidence Retrieval

## Trigger

Use when selecting candidate evidence, classifying requirement matches, assessing fit, or resolving gaps before drafting. Writers return newly discovered evidence issues here through the parent.

## Required workflow

1. Read the repository-root `shared-rules.md` first.
2. Before reading or editing anything under `data/user/`, read the existing `.agents/skills/user-json-memory/SKILL.md` and follow it. Treat `data/user/index.json` and its registered split files as the factual source of truth.
3. Use the normalized job folder, normally `data/YYYYMM/company_role_title/`, and read `jd.md` plus `role_expectations.json` when available. Do not process a raw JD as if it were normalized; route intake through the JD workflow first.
4. Select only role-relevant skills, experience, projects, education, and completed certifications. Preserve title, organization, location, dates, tools, ownership, and outcomes for every included experience.
5. For every material match, write an explicit evidence anchor: source file and precise JSON field, highlight, or record that supports it. Preserve the role expectation matched, causal driver, method/tools, and measurable or observable outcome for high-value evidence.
6. Classify requirements and keywords as `supported`, `adjacent`, or `unsupported`; record genuine gaps separately. Never turn adjacent evidence into a direct claim.
7. Resolve material, unresolved evidence gaps using Gap Discovery below; record the answer and classification in the subset before returning it to the writer.
8. Produce `fit_assessment.md` from the same classifications: cite requirement-level evidence, distinguish direct/adjacent matches and gaps, and explain any score. Do not assess fit a second time independently of the subset.

## Gap Discovery

Use `.agents/skills/grill-me/SKILL.md` for one-question-at-a-time follow-ups; this skill owns the evidence questions and stopping conditions.

- Read the available evidence first, then probe plausible sources: paid work, internships, school, certifications, side projects, volunteer work, and indirectly used tools.
- Ask for task, context, dates, ownership, tools, scale, deliverables, and outcomes. Seek supported before/after time, volume, error rate, users, dollars, percentage, turnaround, and adoption metrics.
- Do not accept vague answers, suggest candidate answers, or fill gaps by inference. Continue until the requirement is directly supported, adjacently supported, or confirmed as a real gap; do not restart an already resolved interview.
- Record confirmed facts, provenance, and classifications in `user_subset.json`. Durable-memory updates remain subject to the explicit-request rule below.

## Output

Create or update:

- `data/YYYYMM/company_role_title/user_subset.json`
- `data/YYYYMM/company_role_title/fit_assessment.md`

Include source files, target role focus, selected role-relevant evidence, explicit anchors, classifications, and gap notes. Keep application-specific targeting in this subset, not in durable memory.

Include relevant `profile_context` from `data/user/profile.json`: `company_preferences`, `career_transition_justification`, and `career_certification_commitments`, with precise source anchors. Preserve whether a planned credential has actually started; these letter inputs are not completed certifications or proof of work experience.

Update the split user memory only when the user explicitly requests a durable, application-neutral fact be saved. If they do, follow `.agents/skills/user-json-memory/SKILL.md` and run its prescribed JSON/schema validation. Otherwise make no changes under `data/user/`.

## Non-goals

Do not draft a resume/CV or cover letter. The existing `.agents/skills/resume-writer/SKILL.md` and `.agents/skills/cover-letter-writer/SKILL.md` own drafting rules; this skill supplies factual evidence for them.
