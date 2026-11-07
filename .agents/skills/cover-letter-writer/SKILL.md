---
name: cover-letter-writer
description: Draft or revise a targeted cover letter for a specific job application. Use whenever the user asks for a cover letter, application letter, letter of interest, expression of interest, or cover-letter rewrite. Enforces a company-specific hook, evidence-based body paragraphs, honest gap handling, and a total length under 410 words.
---

# Cover Letter Writer

The letter complements the resume — it must not repeat it. It adds motivation, context behind one or two key experiences, answers to obvious questions (career change, tool gap, industry transition, level targeting), and proof of concise written communication. If the resume already states a metric, the letter may reference the story but should not re-run the resume's metric list wholesale; prove one or two focused competencies with compact stories instead of mentioning every strength.

## Inputs

- JD / `role_expectations.json`. `keywords` is JD-only vocabulary: classify each as supported, adjacent, or unsupported against candidate evidence before using it. Mirror exact wording only where supported and natural; frame adjacent evidence as transferable, never as a direct claim.
- The targeted resume for this job — the letter must match its facts and keyword strategy exactly.
- `user_subset.json`, or the split memory at `data/user/index.json` if no subset exists.
- `data/user/profile.json`: `company_preferences` (high-value opening material when it has an entry for this employer), `career_transition_justification` (fold in as a one-two sentence bridge when relevant), `career_certification_commitments` (closing-paragraph signal when a planned credential addresses a visible gap).
- The latest active version under `artifacts/cover_letters/`; when revising, start from it plus the user's comments. Do not read or use `retired/` unless the user explicitly asks for a historical comparison or recovery.
- The company's real mailing address from an official source (company site or the posting); omit the address only if none can be found.

## Perspective

- **Employer-focused.** Open paragraphs with the employer's need, context, or evidence — what the organization gains — not the candidate's desire to grow. First person is fine inside paragraphs, but no paragraph starts with `I`, `me`, or `my` unless there is no natural alternative.
- **Evidence-based.** Every highlighted skill gets a concrete example (compact STAR: context, problem, action, result) — never a trait list or unsupported praise.
- **Company-specific.** If the opening could be sent to another company unchanged, rewrite it.

## File And Format

Save to `artifacts/cover_letters/cover_letter_vNNN.md` (next zero-padded version). When revising, move the previous active source first to the matching root-level `retired/YYYYMM/company_role_title/artifacts/cover_letters/` path while preserving its filename, then write the new active source; never overwrite an existing source. Do not use `retired/` unless the user explicitly asks for a historical comparison or recovery. Then format per `instruction.md`.

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
- Metrics only when supported; facts must match the resume exactly.
- Salary stays out unless the user asks; then use neutral wording ("the posted range aligns with my market research; I am comfortable discussing compensation within it").
- Don't copy internet cover-letter examples.

## Quality Checklist

- Under 410 words; first sentence company- or role-specific; letter unusable for another company unchanged.
- Body uses specific stories, not trait lists; supported keywords appear naturally; unsupported keywords are not claimed.
- No paragraph starts with I/me/my; tone employer-focused; obvious application questions answered briefly.
- Resume and letter present one cohesive candidate; closing is concise and interview-oriented.
- Full format present (date, recipient block, Re: line, greeting, four paragraphs, sign-off); versioning and formatting follow `instruction.md`.
