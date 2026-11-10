---
name: resume-writer
description: Create or revise a targeted resume/CV for a specific job from user_subset.json, the split user memory, a JD, or role expectations. Use whenever the user asks for a targeted CV/resume, professional profile, skills section, core competencies, employment-history bullets, or a resume rewrite. This is the single CV-writing skill for targeted applications.
---

# Resume Writer

This skill owns the CV writing: profile, skills, optional core competencies, employment history, projects, and education/certifications. The parent follows `instruction.md` for the surrounding pipeline; `shared-rules.md` owns shared safeguards, artifact versioning, and formatting rules.

Read repository-root `shared-rules.md` before drafting.

## Sources

1. `user_subset.json` — selected evidence and supported/adjacent/unsupported classifications owned by the librarian. If absent, request it through the parent before drafting.
2. Split user memory rooted at `data/user/index.json` — verification of cited facts, using its memory skill; do not independently select or reclassify evidence.
3. `jd.md` / `role_expectations.json` — employer priorities and vocabulary, not candidate proof. Consume the subset's classifications and verify that each claim has its cited support.
4. `data/user/resume_preferences.json` — the user's display defaults (skills labels, section order) and writing-style signals.
5. The latest active resume plus user comments when revising, under `shared-rules.md` → Versioned Application Artifacts.

## Truth Rules

- Claim nothing unsupported: tools, platforms, domains, certifications, seniority.
- Keep direct and adjacent evidence separate. For adjacent evidence, name the actual supported capability, tool, or method; do not name the missing requirement or append meta-language such as "transferable experience."
- Preserve supported metrics exactly. Never invent metrics. If two sources disagree, keep the range.
- Don't inflate ownership: use "supported" or "helped" when ownership was partial.
- No copied JD boilerplate. Use supported JD keywords unchanged only where they describe the actual work and read naturally.

## Evidence Issues

If an important requirement lacks evidence or a subset classification conflicts with its source, return the exact issue through the parent to `candidate_evidence_librarian`. The librarian owns interviews and subset corrections; do not repeat its interview or draft the affected claim until resolved. Apply verified updates when the librarian returns the subset.

## Pre-Draft Resume Plan

Before writing prose, add a compact `resume_plan` to `user_subset.json`:

```json
{
  "resume_plan": {
    "voice_brief": ["Use plain verbs.", "Keep named stakeholders.", "Preserve supported metrics."],
    "keyword_placements": [
      {
        "keyword": "business requirements",
        "priority": "must_cover",
        "evidence_anchor": "Product requirements workshop",
        "planned_wording": "business requirements",
        "primary_section": "employment_history",
        "treatment": "exact"
      }
    ]
  }
}
```

- Add a 3-5 item `voice_brief` drawn from user-approved resume wording and `resume_preferences.json`: preferred diction, ownership language, sentence cadence, terminology to preserve, and phrases to avoid.
- For every supported JD keyword, record `priority` (`must_cover` or `supporting`), a specific `evidence_anchor`, `planned_wording`, `primary_section` (`professional_profile`, `employment_history`, `projects`, or `skills`), and `treatment` (`exact`, `variant`, or `omit_with_reason`). Record a reason for every variant or omission.
- Use one primary location per keyword. Repeat it only when one occurrence labels the capability and another adds distinct proof.
- Draft evidence stories first and apply recognition terms second. The JD may supply concise canonical nouns; the candidate supplies the claim framing, accurate verb, ownership, syntax, stakeholders, tools, and outcome.
- Treat Skills and headings as surface coverage. Important `must_cover` terms need a profile, employment, or project evidence anchor unless an omission is explicitly justified.

## Output Modes And Files

Use the smallest mode that satisfies the request: full CV, profile only, core competencies only, or single-section revision (replace only the requested section). Contact details appear only in a full CV header.

Follow `shared-rules.md` → Versioned Application Artifacts for resume-family filenames, source revisions, retirement, and formatted outputs. Run `python3 formatter/resume_validation.py <resume-path>` on every draft; format only after the independent standout `PASS`.

Full CV structure unless the user asks otherwise:

```markdown
**[Name]**    www.linkedin.com/in/[profile-slug]/
**[Target Title]**    [Email]
[Location]    Phone #: [Phone]

**PROFESSIONAL PROFILE**

[3-5 sentence targeted profile.]

**SKILLS**

**[Skill Group]:** [comma-separated skills]
**[Skill Group]:** [comma-separated skills]

**EMPLOYMENT HISTORY**

**[Title]** - [Organization], *[Location]*    [Dates]

* [Bullet.]
* [Bullet.]

**EDUCATION/CERTIFICATIONS**
```

### LinkedIn Display

- Show the complete LinkedIn profile URL as plain text so the reader can see and reproduce the address.
- Never use `LinkedIn` as generic display text and never wrap the LinkedIn URL in Markdown hyperlink syntax.
- Use the exact display value from `data/user/resume_preferences.json` when one is provided. Otherwise, derive the visible address from `candidate.linkedin`, remove the `http://` or `https://` scheme, preserve the profile slug, and use the readable form `www.linkedin.com/in/[profile-slug]/`.

## Professional Profile

3-5 short, scannable sentences, each doing distinct work: professional identity and target-fit, core analytical/technical strength, role-relevant tools or methods, scale or impact, stakeholder or communication value. Open with a sentence that signals fit for the requested role and level. Don't list every tool, employer, or domain. Mention Excel only when backed by concrete work; describe visualization tools by purpose (dashboards, decision-ready insights); make stakeholder communication concrete (requirements gathering, adoption, plain-language explanation).

## Skills

- 3-5 grouped lines, buckets organized by role value, one concept per bucket, clean noun labels without `&` (unless part of a formal name).
- Default to the section labels in `data/user/resume_preferences.json` unless the role rewards a narrower or differently framed subset.
- Only supported, role-relevant, meaningful terms — no filler words, soft-skill padding, raw tool inventories, or technically-true-but-irrelevant tools. Requested-but-missing tools go in gap notes, never the CV.
- If user-requested Core Competencies exist, align skill buckets with them so the top half of the CV has one organizing logic.

## Core Competencies

Omit by default. Include only when the user asks, the target format requires it, or it carries distinct signal the other sections cannot. If included: exactly three focused headings (one capability each) ordered by importance in the posting, 3-4 action-verb bullets per heading, capability-led with light evidence anchors (metric, audience, scale, or tool family). Leave full stories and employer names to Employment History; don't repeat the profile or repeat Employment History stories verbatim.

## Employment History

This section carries the detailed proof. Reverse chronological; the most relevant, recent, or heavily weighted role gets the most bullets; cap each role at 7 bullets and give older or less relevant roles fewer (or omit them, unless the user asks for all jobs).

Most bullets should make the following information easy to find, usually in one sentence. Order it for clarity and emphasis instead of forcing every bullet into the same cadence:

1. **Accurate past-tense action verb.** Consult `verbs.md` as a suggestion bank, but prefer the candidate's precise verb over a forced synonym. Vary repeated openings when a natural alternative exists.
2. **Primary causal driver:** make the tool, method, process change, or analysis that produced the outcome clear and prominent. Never flatten an achievement into a list of nearby tools.
3. **Material tools inline:** connect the most role-relevant tools to proof; omit incidental tools that make the sentence read like an inventory.
4. **Concrete effect:** preserve the metric, or failing that state who benefited, what became faster or more reliable, or what risk shrank.

One story = one bullet. Keep an incident's mitigation/root-cause/fix/outcome together; keep requirements-plus-implementation for one product together unless each part has a distinct outcome. Merge weak supporting details into a stronger bullet, a skills line, or omit them — never pad with standalone partial evidence.

Example shape: `Led the improvement of a recurring reporting pipeline through workflow cleanup, validation automation, and parallelization, reducing delivery time from 6 weeks to 3 weeks while maintaining 100% on-time delivery.`

## Education, Certifications, Projects

Keep education factual. Include only certifications and projects relevant to the target role or that explain a qualification signal — don't list every certification, and don't turn certification-only knowledge into an active work skill. A short Selected Projects section is useful when a personal or academic project bridges a JD gap (e.g., home-lab container operations, an energy study for utility roles).

## Style Signals

- When the user edits wording, treat that phrasing as a strong style signal: preserve the sentence shape, tool emphasis, and plain wording in future drafts instead of re-polishing it into generic resume language.
- Before drafting or revising a bullet, understand the full highlight context — problem, what the user actually changed, which tools mattered, what followed. Truth and accurate ownership are hard constraints. Within them, optimize role recognition and candidate voice together; use brevity to remove noise.

## Keyword And Voice Gates

- Every supported keyword has a planned treatment and evidence anchor. Every `must_cover` term appears in its planned evidence-bearing section unless explicitly waived.
- Report exact keyword matches, approved variants, profile-only matches, Skills/headings-only matches, missing terms, adjacent terms present, unsupported terms present, and terms lost since the previous version. Do not use fuzzy similarity: for example, `SIT/UAT` does not automatically satisfy `test cases`.
- A Skills or heading occurrence does not substitute for evidence. Do not introduce Core Competencies solely to raise coverage.
- Compare the draft with the `voice_brief` and user-approved examples. Remove JD-clause copying, abstract-noun chains, forced synonyms, unexplained register changes, duplicated stories, and repeated sentence skeletons.
- Read every line without the JD beside it. It must remain specific, credible, and useful; no sentence should exist solely to carry a keyword.

## Reviewer-Led Redraft

The independent `application_reviewer`, not the writer, owns the final senior-HR standout verdict. When its verdict is `REDRAFT_REQUIRED`:

- Use the reviewer's prioritized findings as revision requirements, but apply only directions supported by `user_subset.json`. Verify source facts and return evidence discrepancies to the librarian before changing claims.
- Make a substantive next version: sharpen the target identity and differentiator in the top third, reorder the strongest evidence toward the role's priorities, replace vague or low-value content with stronger supported proof, and improve scan clarity. Do not satisfy the gate with synonym swaps, inflated language, graphics, or invented claims.
- Preserve valid facts, metrics, ownership boundaries, user-approved voice, and supported keyword coverage from the prior active version.
- Follow the active/retired version policy, validate the new Markdown and alignment, and return it for another independent standout review. Do not self-declare `PASS`.
- Stop after two reviewer-led redrafts in one request. If an evidence gap prevents a pass, return it through the parent to the librarian for its targeted interview; report unavoidable profile limitations honestly.

Before reviewer handoff, apply the section standards and keyword/voice gates above, validate the draft, and confirm any prior reviewer findings were addressed.
