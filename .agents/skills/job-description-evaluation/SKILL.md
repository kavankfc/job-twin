---
name: job-description-evaluation
description: Evaluate a normalized job description and write employer-side role_expectations.json. Route raw postings through parent-led intake; candidate fit belongs to candidate-evidence-retrieval.
---

# Job Description Evaluation

## Trigger

Use for employer-side JD analysis. For raw postings or candidate-fit requests, route the dependent work to the parent and evidence librarian under `shared-rules.md`.

## Required workflow

1. Read repository-root `shared-rules.md`.
2. Require a normalized job folder containing `jd.md`. If the input is still raw, return it to the parent for intake rather than creating folders or methodology notes here. Preserve normalized JD text and existing artifacts.
3. Write `role_expectations.json` with posting metadata, company/industry context, role purpose, duties, requirements, assets/provisos, seniority signals, inferred day-to-day expectations, success measures, and concise JD-only keywords. Mark inference explicitly.
   - Use exact or near-exact JD wording for high-signal role capabilities, tools, methods, domain expertise, and success signals. Keep generic responsibility phrases in duties or notes, not the keyword list.
4. Keep employer facts separate from candidate evidence. Do not read candidate memory, classify candidate matches, score fit, or give positioning/gap advice; the librarian owns those decisions.

## Output

`data/YYYYMM/company_role_title/role_expectations.json`

Return this path to the librarian through the parent. Do not draft application artifacts or write the fit assessment or methodology notes.
