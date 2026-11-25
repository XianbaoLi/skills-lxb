---
workflow_id: WF-TR-02
name: Review and explicitly accept a Chinese translation candidate
version: 1.0.0
status: specification
required_skills:
  - mathtranslations
optional_skills:
  - mineru
input: source Markdown, Chinese candidate, optional original PDF
output: review record; accepted Markdown only after explicit user approval
---

# WF-TR-02 — Review and accept a Chinese translation candidate

## Purpose

Review a Chinese candidate against its source-language transcript and, when available, the original PDF. Keep review findings separate from the translated content. Promote the candidate to an accepted translation only after the user explicitly approves the reviewed version.

## Inputs

- Source-language .source.md.
- Chinese .zh-CN.candidate.md.
- Original PDF and MinerU locators when page-level checking is required.
- Project glossary and previous review notes.

## Review procedure

### 1. Confirm versions and provenance

- Confirm both files refer to the same source edition, section, and page range.
- Check that the candidate was generated from the current source transcript, not a stale revision.
- Preserve hashes or version identifiers in the review record when available.
- Do not overwrite the source or candidate during intake.

### 2. Review completeness

Compare every unit in order:
- heading and paragraph;
- definition, theorem, example, proof, and exercise;
- every sentence, condition, given value, unit, and answer option;
- table row/column, caption, footnote, citation, and cross-reference;
- image and source-page marker.

Flag omissions, additions, duplicated content, and order changes.

### 3. Review mathematical fidelity

Pay particular attention to:
- negation and quantifier scope;
- if / only if / iff;
- necessary versus sufficient;
- unique, exactly, at least, at most, respectively;
- assumptions, boundary/initial conditions, and domain restrictions;
- signs, subscripts, superscripts, indices, vector/operator notation;
- inequalities, units, constants, equation numbers, and referenced figures.

Use the original PDF page image to resolve a source/OCR dispute. Do not silently "correct" the printed source.

### 4. Review Chinese terminology and style

- Check technical terms against glossary.en-zh.md.
- Keep the Chinese concise and natural without weakening the mathematical claim.
- Keep named theorems, acronyms, symbols, and repeated concepts consistent.
- Distinguish a translation problem from a source typo or an author-specific convention.

### 5. Record findings

Write _work/<document-id>/translation-review.md with:
- source and candidate paths/versions;
- reviewed page/section range;
- checks completed;
- findings with source page/paragraph anchors;
- severity: critical / major / minor;
- proposed correction, if any;
- unresolved questions;
- review status.

A review pass is not proof of mathematical correctness beyond the evidence actually checked.

## Acceptance gate

The workflow has three distinct states:

1. candidate — generated, not yet reviewed.
2. reviewed-candidate — review completed; findings and remaining issues recorded.
3. accepted — the user explicitly approves this exact reviewed candidate.

Only after explicit approval may the Agent create:

output/<document-id>/<unit>.zh-CN.md

Promotion rules:

- Never infer acceptance from silence, a request to review, or a successful lint check.
- Never overwrite an existing accepted translation. If one exists, create a versioned successor and preserve the prior file.
- Keep the candidate and review record for traceability unless the user explicitly asks to archive them.
- If the user requests corrections, update the candidate, rerun the relevant checks, and keep it in candidate/reviewed-candidate state until approved.

## Invocation examples

- "按 WF-TR-02 对照原文复核 2.4.zh-CN.candidate.md，先列出问题，不要定稿。"
- "我接受刚才复核的 2.4 候选译文；请按 WF-TR-02 归档为正式中文版。"
