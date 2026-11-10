---
name: cover-letter-writer
description: Draft or revise a targeted cover letter for a specific job application. Use whenever the user asks for a cover letter, application letter, letter of interest, expression of interest, or cover-letter rewrite. Enforces a company-specific hook, evidence-based body paragraphs, honest gap handling, and a total length under 410 words.
---

# Cover Letter Writer

The letter complements the resume — it must not repeat it. It adds motivation, context behind one or two key experiences, answers to obvious questions (career change, tool gap, industry transition, level targeting), and proof of concise written communication. If the resume already states a metric, the letter may reference the story but should not re-run the resume's metric list wholesale; prove one or two focused competencies with compact stories instead of mentioning every strength.

Read repository-root `shared-rules.md` before drafting.

## Inputs

- JD / `role_expectations.json` supplies employer vocabulary; consume the librarian's classifications in `user_subset.json`. Mirror exact wording only where supported and natural; frame adjacent evidence as transferable, never as a direct claim.
- The targeted resume for this job — the letter must match its facts and keyword strategy exactly.
- `user_subset.json` supplies selected evidence and classifications. Use split memory at `data/user/index.json` only to verify cited facts under its memory skill. If the subset is absent or evidence is missing/conflicting, return the issue through the parent to the librarian before drafting the affected claim; do not reclassify or repeat its interview.
- The subset's source-anchored `profile_context` from `data/user/profile.json`: `company_preferences` (high-value opening material for this employer), `career_transition_justification` (a one-two sentence bridge when relevant), and `career_certification_commitments` (a closing signal when a planned credential addresses a visible gap). If relevant context is missing, request it through the librarian.
- The latest active letter plus user comments when revising, under `shared-rules.md` → Versioned Application Artifacts.
- The company's real mailing address from an official source (company site or the posting); omit the address only if none can be found.

## Perspective

- **Employer-focused.** Open paragraphs with the employer's need, context, or evidence — what the organization gains — not the candidate's desire to grow. First person is fine inside paragraphs, but no paragraph starts with `I`, `me`, or `my` unless there is no natural alternative.
- **Evidence-based.** Every highlighted skill gets a concrete example (compact STAR: context, problem, action, result) — never a trait list or unsupported praise.
- **Company-specific.** If the opening could be sent to another company unchanged, rewrite it.

## File And Format

Follow `shared-rules.md` → Versioned Application Artifacts for letter filenames, source revisions, retirement, and formatted outputs.

Use the complete format below, including four paragraphs:

```markdown
[Month Day, Year]

[Contact Name or Hiring Team]
[Company Name]
[Street Address]
[City, Province, Postal Code]

**Re: Application for [Job Title]**

Dear [Ms./Mr./Dr. Last Name or Hiring Team],

[Opening paragraph]

[Body paragraph 1]

[Body paragraph 2]

[Closing paragraph]

Sincerely,
[Full Name]
```

Blank lines control formatted spacing: keep the recipient block on consecutive lines, and keep `Sincerely,` directly above the name with no blank line.

## Paragraphs

**Opening.** First sentence is a hook tying the candidate to this employer: mandate, product, industry context, the role's problem, a recent initiative, or a direct connection between the candidate's work and the employer's need. Weave the role name in naturally — never "I am writing to apply for the position posted online." Adapt `company_preferences` material naturally, don't paste it.

**Body (two paragraphs).** Each addresses one major hiring need from the JD with one concrete story, connects the result back to the employer's role, and avoids over-explaining technical detail. Prefer flowing narrative for role-specific letters. Good themes: stakeholder translation, reporting/dashboard delivery, data quality, process improvement, domain fit, leadership, gap handling via transferable experience.

**Closing.** Summarize the value offered, thank the employer, invite an interview for this role specifically. A planned credential from `career_certification_commitments` may appear here as a forward-looking signal — "I am committed to completing…" or "I am prepared to begin…"; say "in progress" only when the user has confirmed actually starting. Keep it short.

## General / Expression-of-Interest Letters

When the letter targets an organization rather than one role:

- Re: line: `Re: Expression of Interest - [Target Function]`.
- Opening leads with the organization's mission or industry challenge and a concrete consequence — what gets better, who benefits. No single role named.
- Body frames the candidate's two strongest transferable capabilities (not two JD requirements), each with one example. When the two capabilities are distinct and the reader will scan, use bold-header format: `**[Capability label.]** [paragraph]`. Keywords come from the organization's industry and mandate.
- Closing expresses openness across relevant role types and invites a conversation about where the candidate adds the most value.
- Lean further toward passion, company relevance, and the candidate's distinctive background; even less resume repetition than a role-specific letter.

## Drafting Rules

- Under 410 words. Short paragraphs, plain verbs.
- Handle gaps honestly and without apology: name obvious ramp-up areas briefly and state how they'd be approached; mention a gap only when it will be obvious to the reader.
- Metrics only when supported; facts must match the resume exactly, and unsupported keywords must not be claimed.
- Salary stays out unless the user asks; then use neutral wording ("the posted range aligns with my market research; I am comfortable discussing compensation within it").
- Don't copy internet cover-letter examples.

Before package review, check the letter against the format, perspective, paragraph, and drafting rules above; confirm it presents one cohesive candidate with the approved resume.
