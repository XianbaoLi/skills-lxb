---
workflow_id: WF-DOC-TR-01
name: Scanned PDF to source transcript and Chinese candidate
version: 1.0.0
status: specification
composes:
  - WF-DOC-01
  - WF-TR-01
required_skills:
  - mineru
  - mathtranslations
conditional_skills:
  - stem-notes
input: scanned or image-heavy PDF and requested page/section range
output: checked source-language Markdown plus Chinese translation candidate
---

# WF-DOC-TR-01 — Scanned PDF to Chinese translation candidate

## Purpose

Provide one end-to-end route for a user who has an English scanned/image-heavy textbook or exercise PDF and wants:

1. a faithful, page-traceable source-language Markdown transcription; and
2. a separate Chinese translation candidate based on that checked transcript.

This workflow composes WF-DOC-01 and WF-TR-01. It does not replace their detailed rules.

## Default deliverables

For a requested unit such as section 2.4:

- 2.4.source.md — checked English transcription.
- 2.4.zh-CN.candidate.md — Chinese candidate, not final.
- assets/2.4/ — source figures/crops actually referenced by either document.
- _work/<document-id>/ — reusable MinerU parse, page mapping, glossary, and issue records.

Do not generate a PDF, Word file, solved problem set, summary, or knowledge Skill unless requested.

## Orchestration

### Stage 0 — Scope and reuse

1. Read the project AGENTS.md and this workflow.
2. Confirm source PDF and requested section/page range.
3. Check for existing MinerU output, source Markdown, image assets, and glossary.
4. Resume from the earliest incomplete stage. Do not rerun OCR or redo translation that is already checked and unchanged.
5. For a long book, work chapter/section by section and maintain a small manifest/checkpoint. Do not load the entire book into the Agent context by default.

### Stage 1 — Parse and transcribe

Follow [WF-DOC-01](scan-pdf-to-source-markdown.md) exactly.

- Use the existing local MinerU environment and its configured normal-quality tier.
- Parse the requested range; use JSON control-flow output and follow MinerU continuation locators.
- Compare OCR against original page images for uncertain, image-only, formula-heavy, or table-heavy content.
- Preserve source language, formulas, numbering, diagrams, tables, and page provenance.
- Create the source Markdown and record any unresolved OCR/source issues.

### Stage 2 — Source quality gate

Before translation begins, classify the source unit:

- **READY** — all content that affects meaning is readable and checked.
- **READY_WITH_NOTES** — minor uncertainty remains but does not change mathematical conditions or key content; carry the issue into the candidate review record.
- **BLOCKED** — an illegible equation, operator, number, negation, condition, diagram label, or missing page could change the meaning.

Do not translate a BLOCKED unit as though its source were certain. Resolve it from the page image or keep the unit explicitly provisional and ask the user only for the unresolved source evidence.

### Stage 3 — Build terminology and translate

Follow [WF-TR-01](source-markdown-to-chinese-candidate.md).

- Use mathtranslations for mathematical semantics, glossary decisions, and review principles, adapted to Markdown.
- Translate only from the checked source Markdown, consulting the original PDF where the OCR/transcription is ambiguous.
- Preserve all mathematical expressions and question conditions.
- Do not solve questions or insert teaching explanations.
- Keep the Chinese output separate and label it as a candidate.

### Stage 4 — Cross-artifact verification

Check source and candidate side by side:

| Check | Source Markdown | Chinese candidate |
|---|---|---|
| Page/section coverage | Matches requested PDF range | Same scope as source |
| Heading/problem numbering | Matches source | Preserved |
| Paragraph and list coverage | Complete | No omitted meaning |
| Equations and symbols | Checked against page image | Semantically unchanged |
| Numbers, units, inequalities | Checked against PDF | Identical meaning |
| Figures and tables | Original assets and structure preserved | Links/structure preserved; captions translated |
| Uncertainty | OCR issues recorded | No unsupported guess; affected translation flagged |
| Terminology | Original terms identifiable | Consistent with project glossary |

Do not treat matching paragraph counts alone as proof of completeness. Compare meaning and structure.

### Stage 5 — Handoff

Report:
- source PDF and processed section/page range;
- source Markdown path and its review status;
- Chinese candidate path and its review status;
- image asset directory;
- unresolved OCR, source, or translation issues;
- whether any parsing fallback was used (and whether it was explicitly authorized).

Do not call the Chinese candidate "final" or imply user acceptance.

## Stop conditions

- No compatible MinerU environment or no acceptable local quality route: stop and ask before install, upgrade, alternative parser, or remote upload.
- Critical source ambiguity: stop translation for the affected unit or clearly mark it provisional.
- Missing figure/page asset: preserve a placeholder and issue note; never invent a replacement.
- Existing accepted translation: never overwrite it. Create a new candidate/version.

## Invocation

"按 WF-DOC-TR-01 处理这份扫描版英文教材的 2.4 节：先识别并忠实转写英文原文，再生成独立的候选中文版。保留公式、图片、题目条件和页码，不解题，不生成 PDF。"
