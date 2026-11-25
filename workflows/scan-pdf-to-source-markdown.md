---
workflow_id: WF-DOC-01
name: Scan PDF to faithful source Markdown
version: 1.0.0
status: specification
required_skills:
  - mineru
optional_skills:
  - stem-notes
input: scanned or image-heavy PDF, optional page/section range
output: original-language source Markdown and referenced source assets
---

# WF-DOC-01 — Scan PDF to faithful source Markdown

## Purpose

Turn a scanned or image-heavy PDF range into a readable, source-language Markdown transcription while preserving original content, mathematical meaning, figures, tables, numbering, and page provenance.

This workflow does **not** translate, summarize, solve exercises, or rewrite the author's argument. It creates a checked source transcript that can later be translated or reorganized.

## Inputs

Required:
- Original PDF path.
- Requested page range, chapter, section, or whole-document scope.

Optional:
- Existing MinerU document ID/locator or parse output.
- Existing project AGENTS.md, output style, and previously transcribed sections.
- Editable source (TeX/Word) as supporting evidence; the published PDF remains the visible-content authority.

## Skill responsibilities

- mineru: parse/OCR the PDF, continue long documents, retrieve page/block images, preserve stable locators.
- stem-notes: use only relevant guidance for figure extraction, mathematical transcription, source-page checking, and technical layout. Do not automatically follow its default MCQ intake or LaTeX-output route when the user requested Markdown.
- Do not invoke book-to-skill unless the user separately requests a reusable knowledge Skill for a whole book.

## Non-negotiable rules

1. Keep the original PDF unchanged.
2. Prefer the already configured local MinerU environment. Do not hard-code a drive letter, Python environment name, or machine-specific path.
3. Do not install or upgrade MinerU, change persistent configuration, start/restart services, or invalidate caches without approval.
4. Do not use remote parsing or upload the PDF without explicit user permission.
5. Do not silently fall back to another OCR/parser when MinerU reports a recoverable engine, quality, or configuration problem.
6. A parsed Markdown block is not proof that the OCR is correct. The PDF page image is the source for resolving uncertain characters, equations, and layout.
7. Preserve the source language. Translation is a separate workflow.

## Procedure

### 1. Read the local rules and inventory the source

- Read the project AGENTS.md if present and this workflow.
- Locate the exact PDF and determine the requested scope.
- Record the source filename, file size, page count if available, edition/revision if known, and the difference between PDF page index and printed page number.
- Check whether an existing MinerU parse or previous source transcript already covers the requested pages. Reuse valid results.
- Do not ask for details that can be determined from the file. Ask only if the source or requested range is genuinely ambiguous.

### 2. Check MinerU without changing the environment

Check the active environment:

```bash
command -v mineru
mineru version --json
```

MinerU Skill currently requires version >=4.0,<5 and Python >=3.11,<3.15. If mineru version --json is unsupported, try mineru --version as the Skill specifies.

- If the CLI is missing or the version is unsupported/unknown after that check, stop and report the finding. Ask before installing or upgrading.
- Use mineru server status --json only when the current local parsing tier/engine needs diagnosis.
- Reuse the current local quality configuration. The MinerU Skill's normal reading default is standard, then basic when available. Do not use flash as the final transcription tier unless the user explicitly accepts preview-level quality.
- If no acceptable local quality tier is available, explain the available options and wait: configure/download a local engine, explicitly accept flash, explicitly authorize another local parser, or explicitly authorize remote parsing. Do not decide on the user's behalf.

### 3. Parse only the requested range

For a known PDF page range, use the MinerU Skill's page-range syntax (1-based, inclusive) and structured JSON output:

```bash
mineru parse "<source.pdf>" --pages "<start>-<end>" --json
```

- For a small document or explicit whole-book request, parse the required full range; otherwise work in bounded page windows.
- Save the structured response and raw parse artifacts under _work/<document-id>/mineru/.
- Preserve the MinerU document ID, selected tier, page/block locators, and continuation information in a manifest.
- If MinerU returns next_request or a <!-- Next: ... --> command, follow that exact continuation. Do not restart at page 1 or guess the next page.
- Use mineru read <locator> for a page/block already parsed; do not reparse the entire PDF to inspect one uncertain item.
- Use mineru read <locator> --format image only when a page/block image is needed for visual verification or figure extraction.

### 4. Assemble the source transcript

Create output/<document-id>/<unit>.source.md.

Preserve:
- Original language and meaning.
- Chapter/section/subsection hierarchy.
- Paragraph order, lists, examples, exercises, options, notes, footnotes, captions, and cross-references.
- Formula content, inline/display status where meaningful, equation tags/numbers, symbols, units, and punctuation connected to equations.
- Table row/column relationships and all meaningful values.
- Figure numbers, captions, labels, and the relation between each figure and its surrounding explanation.

Use Markdown headings and lists. Use LaTeX for mathematical expressions. Do not turn a formula into prose or a screenshot.

Add unobtrusive source-page markers at meaningful boundaries, for example:

```markdown
<!-- Source: PDF page 14; printed page 9; MinerU locator: doc:.../page:14 -->
```

Keep PDF page number and printed page number distinct. If printed page numbering is absent or unreadable, record that rather than guessing.

### 5. Verify page images, figures, and mathematical content

- Visually inspect all pages where the OCR is uncertain, image-only, formula-heavy, table-heavy, or layout-sensitive.
- For a high-fidelity full-section transcription, compare every page in the requested range against the rendered source page; at minimum, never leave a known OCR uncertainty unchecked without recording it.
- Compare every non-trivial equation for signs, subscripts, superscripts, Greek letters, vector/operator marks, delimiters, integrals, sums, matrices, cases, and equation numbers.
- Verify exercise numbers, all givens, units, inequalities, quantifiers, conditions, answer choices, and figure references.
- For a diagram/plot that is a meaningful part of the content, preserve the original image or make a faithful crop from the source page. Do not replace it with an AI-generated image.
- If a figure is extracted/cropped, save it under output/<document-id>/assets/<unit>/ and use a relative link from the Markdown file.
- Use stem-notes selectively when its figure or STEM-specific visual guidance is useful. Do not generate unrelated formula sheets, summaries, solutions, or PDFs.

### 6. Record uncertainty instead of guessing

- Correct an OCR error only when the source page provides sufficient evidence.
- If the source itself appears to contain a typo, preserve the printed content and record the suspected source error separately.
- If a symbol, word, figure label, or page fragment remains illegible, mark it visibly in the source transcript as [待核对：PDF 第 N 页] and add a concise entry to _work/<document-id>/ocr-issues.md.
- Do not fill missing text from domain intuition or a similar edition without marking the evidence and uncertainty.

### 7. Run the completion check

Before marking the source transcript source-reviewed:
- Every requested page is accounted for, including blank/figure-only pages when relevant.
- Heading and problem numbering match the source.
- No paragraph, equation, table, figure, footnote, or answer option has silently disappeared.
- Equations and numerical values have been visually checked where necessary.
- Every local image link resolves relative to the Markdown file.
- OCR/source issues are either resolved or explicitly listed.

## Outputs

Minimum deliverables:
- output/<document-id>/<unit>.source.md — source-language transcription.
- output/<document-id>/assets/<unit>/ — only the figures/crops actually referenced by the Markdown.
- _work/<document-id>/mineru/ — reusable raw parse results and locators.
- _work/<document-id>/manifest.json — source path/name, scope, MinerU version/tier, document ID, page mapping, and artifact status.
- _work/<document-id>/ocr-issues.md — only when uncertainties or suspected source errors exist.

The source transcript must not contain shell logs, model reasoning, installation notes, or unrelated commentary.

## Failure and stop conditions

Stop and report rather than silently degrade when:
- MinerU is missing, incompatible, or cannot provide an acceptable local parsing route.
- The only available route would upload the source without explicit permission.
- The source file is corrupt or the requested pages cannot be located.
- A critical equation or condition is illegible and cannot be verified from the source image.

## Invocation examples

- "按 WF-DOC-01 转写这份扫描 PDF 的第 20–28 页，保留英文原文。"
- "继续使用之前的 MinerU 解析结果，完成 2.4 节的 source Markdown。"
- "只识别并重排这些习题，不翻译、不解题。"
