# Changelog

## Unreleased

- Define documentation-only Workflows: one Markdown file per task, stable semantic IDs, explicit capability/Skill/input/output metadata, and no workflow-specific executable code.
- Add document transcription, mathematical/physics translation, combined OCR-to-Chinese-candidate, and translation-review workflows.
- Update the Workflow catalogue and repository README.

## 2.5.0 — 2026-11-05

- Center the skill on discovering needs from vague ideas, before choosing project architecture or a learning route.
- Require an explicit help option in each choice question, not a hidden Other fallback.
- Queue help selections as needs-explanation and teach the question first on the next round; preserve unrelated answers.
- Keep help separate from business choices in multi-select; command approvals are not interview questions.

## 2.4.0 — 2026-11-05

- Separate understanding, preference, scoped authorization and verified execution.
- Keep native approvals authoritative; preserve existing grants and treat skipped new grants as unresolved.
- Teach unfamiliar concepts with plain language, a concrete example and option consequences; resume one question at a time.
- Decouple intensity from explanation depth; allow deferral, skipping and requests for help.
- Require explicit current interview intent; reading the skill for maintenance does not start an interview.
- Separate interview, understanding, authorization, memory-write and execution state in the session template.
- Replace profile-specific examples with generic teaching/approval cases; add static contract regressions.

## 2.3.1 — 2026-11-04

- Publish the portable grill-me skill in XianbaoLi/skills-lxb.
