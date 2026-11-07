---
name: candidate-evidence-retrieval
description: Match the user's factual experience, certifications, and skills to a normalized role or JD and build an evidence-anchored user_subset.json without inventing claims.
---

# Candidate Evidence Retrieval

## Trigger

Use when selecting candidate evidence for a role/JD, classifying requirement matches, or preparing a candidate subset for later drafting.

## Required workflow

1. Read the repository-root `instruction.md` first.
2. Before reading or editing anything under `data/user/`, read the existing `.agents/skills/user-json-memory/SKILL.md` and follow it. Treat `data/user/index.json` and its registered split files as the factual source of truth.
3. Use the normalized job folder, normally `data/YYYYMM/company_role_title/`, and read `jd.md` plus `role_expectations.json` when available. Do not process a raw JD as if it were normalized; route intake through the JD workflow first.
4. Select only role-relevant skills, experience, projects, education, and completed certifications. Preserve title, organization, location, dates, tools, ownership, and outcomes for every included experience.
5. For every material match, write an explicit evidence anchor: source file and precise JSON field, highlight, or record that supports it. Preserve the role expectation matched, causal driver, method/tools, and measurable or observable outcome for high-value evidence.
6. Classify requirements and keywords as `supported`, `adjacent`, or `unsupported`; record genuine gaps separately. Never turn adjacent evidence into a direct claim.
7. For a material evidence gap, ask the user targeted clarification questions covering context, task, dates, ownership, tools, scale, deliverable, and outcome. Do not fill the gap by inference.

## Output

Create or update:

`data/YYYYMM/company_role_title/user_subset.json`

Include source files, target role focus, selected role-relevant evidence, explicit anchors, classifications, and gap notes. Keep application-specific targeting in this subset, not in durable memory.

Update the split user memory only when the user explicitly requests a durable, application-neutral fact be saved. If they do, follow `.agents/skills/user-json-memory/SKILL.md` and run its prescribed JSON/schema validation. Otherwise make no changes under `data/user/`.

## Non-goals

Do not draft a resume/CV or cover letter. The existing `.agents/skills/resume-writer/SKILL.md` and `.agents/skills/cover-letter-writer/SKILL.md` own drafting rules; this skill supplies factual evidence for them.
