---
name: user-json-memory
description: Use whenever reading, creating, editing, validating, compacting, or extracting from the split user memory rooted at data/user/index.json. That memory is the master factual record of the user's background, experience, skills, projects, education, certifications, and presentation preferences. Always use this skill before modifying the memory.
---

# User JSON Memory

`data/user/index.json` is the entrypoint to the split master memory under `data/user/`. It is durable source material for future agents writing targeted resumes and cover letters. The machine-readable schema is `.agents/skills/user-json-memory/user.schema.json`; the validator is `.agents/skills/user-json-memory/validate_user_memory.py`. Read both before any schema-level change and keep skill, schema, validator, and files aligned. `data/user.json` is deprecated — never recreate it.

## Core Principles

- The memory describes the person, not an application. Never store application intent, targeting logic, positioning, or fields like `objective`, `target_title`, `target_keywords`, `application_focus`.
- Preserve factual breadth: a tailored CV omitting a fact is never a reason to delete it.
- Keep entries compact — short factual claims, not prose crafted for one job. Numbers, scale, deliverables, audiences, tools, and outcomes belong in structured highlight fields, not loose sentences.
- Do not guess. Unsupported claims stay out; empty strings/arrays beat invented context. If sources disagree on a metric, preserve the range (e.g., `"reported accuracy across CV versions of 70%-75%"`).

## File Boundaries

```text
data/user/index.json          entrypoint: schema_version "8.0", memory_format "split_user_memory", files map
data/user/profile.json        candidate identity/contact; professional_identity facts; career_transition_justification;
                              company_preferences; career_certification_commitments
data/user/skills.json         factual skill index only, grouped by theme
data/user/resume_preferences.json  user-specific display preferences only (own schema "1.0"); no writing methodology
data/user/experience/<slug>.json   one role per file: title, organization, url, location, dates, technologies, scale, highlights
data/user/projects.json       factual projects: name, organization, url, location, dates, description, technologies, details
data/user/education.json      credential, institution, location, dates
data/user/certifications.json completed certifications only: name, issuer, date, credential_id, url
```

Agent writing methodology lives in `.agents/skills/resume-writer/SKILL.md`, never in the memory. Avoid new files, groups, or top-level fields unless the user asks or the schema cannot represent a factual item; prefer merging into existing groups. When creating a memory from scratch, follow the schema file for exact shapes and register every experience file in `index.json` under `files.experience`.

Field notes:

- `candidate`: stable identity/contact only (name, alternate_name, credentials, location, email, phone, linkedin, github). No job preferences, salary, availability, or visa assumptions unless the user explicitly asks to store them.
- `professional_identity`: broad reusable facts (years, domains, work types, stakeholders, scale, strengths) — no "targeting X" or per-job marketing copy.
- `company_preferences` / `career_transition_justification` / `career_certification_commitments`: only when the user explicitly asks to preserve them; factual and reusable, not cover-letter paragraphs. Planned credentials never go under `certifications`, and are "in progress" only if the user confirms having started.
- `skills.json`: concise names, evidence-backed, never removed because a tailored CV excluded them; display rules go in `resume_preferences.json`.

## Highlight Shape

Each `experience[].highlights[]` entry requires `situation`, `action`, `outcomes`; `background` and `tasks` are optional; `action` has exactly `methodologies`, `technical_tools`, `description`. Resume verbs are not stored here — they are chosen at drafting time from the approved list in `.agents/skills/resume-writer/verbs.md`, the single source of truth.

**STAR completeness rule:** every highlight must let a reader answer all four STAR questions. S = `situation`; T = `tasks` when present, otherwise the need stated in `situation` plus the ownership stated in `action.description`; A = `action`; R = `outcomes`. So when omitting `tasks`, `situation` must state both the context and what needed to be done or delivered (e.g., "daily routine workflows *that needed automation*"). Include `tasks` only when responsibilities or constraints don't fit in one situation sentence — multiple distinct duties, an explicit constraint like "without larger infrastructure", or a mandate beyond the obvious implication. Never restate the situation or action as imperatives just to fill the field.

```json
{
  "background": { "product": "...", "scale": ["..."], "challenge": ["..."] },
  "situation": "Short context, problem, or operating environment.",
  "tasks": ["Responsibility, requirement, goal, or constraint."],
  "action": {
    "methodologies": ["Medallion data architecture", "Data validation"],
    "technical_tools": ["Python", "AWS S3"],
    "description": "Factual description of what the candidate did — source material, not polished resume prose."
  },
  "outcomes": ["One result, impact, metric, deliverable, or stakeholder value per item."]
}
```

- `background` is a freeform factual object (any supported keys such as `product`, `domain`, `scale`, `challenge`, `audience`, `constraints`, `data_sources`, `operating_environment`); omit it when there is nothing to add — never a prose dump, never an empty `{}`.
- `methodologies` are compact phrases; `technical_tools` only when supported.
- No extra root fields (`description`, `tools`, `outcome`, `verbs`, `text`, `evidence`, …). Merge near-duplicate highlights into one with combined proof.

## Editing Workflow

1. Read `index.json`, the schema, and the validator; then only the memory files relevant to the task plus user-provided sources.
2. Add, merge, or correct facts. Preserve existing facts unless the user asks for removal or they are clear duplicates/errors.
3. Validate:

```bash
jq empty data/user/*.json data/user/experience/*.json
python3 .agents/skills/user-json-memory/validate_user_memory.py   # must print: user memory schema ok
```

Good edits: adding an evidence-backed skill or certification, merging duplicate highlights while preserving all numbers, correcting contact details from accepted documents, converting prose bullets into v8.0 highlights. Bad edits: removing experience a tailored CV omitted, adding employer-specific intent, replacing memory language with cover-letter language, deleting metrics for brevity, inferring unsupported skills, storing job-search strategy.

After editing, state briefly: which file changed, any schema-level change, and the validation result. Don't paste full JSON unless asked.
