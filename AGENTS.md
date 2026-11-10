# Application Work

The parent starts from the repository root and reads `instruction.md` before job intake or application work. That file owns normalization, delegation order, review gates, logging, and job-folder methodology notes.

Delegated agents read `shared-rules.md`, their assigned skill, and the required task inputs. They do not need the full `instruction.md` unless the parent assigns work from it. Shared factual, privacy, versioning, retirement, formatting, and handoff rules live in `shared-rules.md`.

Use the most specific agent and skill for each stage, as defined in `instruction.md`. Keep skill instructions in their existing `.agents/skills/` files; do not copy them into handoffs or load unrelated skills.

Before reading or editing the split user memory rooted at `data/user/index.json`, follow `.agents/skills/user-json-memory/SKILL.md`.

Before creating or updating application status history, follow `.agents/skills/application-log/SKILL.md`.
