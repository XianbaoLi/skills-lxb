---
workflow_id: WF-TR-01
name: Source Markdown to Chinese translation candidate
version: 1.0.0
status: specification
required_skills:
  - mathtranslations
optional_skills:
  - mineru
  - stem-notes
input: checked source-language Markdown, optional original PDF and figures
output: Chinese candidate Markdown, project glossary, review notes
---

# WF-TR-01 — Source Markdown to Chinese translation candidate

## Purpose

Translate an existing source-language Markdown transcription into a technically faithful Chinese **candidate** while preserving mathematical meaning, exercise conditions, structure, equations, numbering, figures, and source references.

The output is a reviewable draft. It is not automatically accepted as a final translation.

## Inputs and preconditions

Required:
- A source-language Markdown file, preferably produced and checked by WF-DOC-01.
- The requested translation range and target language (default: Simplified Chinese, zh-CN).

Strongly recommended:
- Original PDF pages or stable MinerU locators for checking ambiguous source text.
- Existing chapter translations and a project glossary.
- Discipline-specific terminology preferences supplied by the user.

If only a scanned PDF is available, run WF-DOC-01 first or use the combined WF-DOC-TR-01. Do not translate unverified OCR as if it were authoritative.

## Skill responsibilities

- mathtranslations: use its guidance for mathematical meaning, source authority, terminology decisions, uncertainty tracking, and separate language/math review passes.
- mineru: retrieve the original page/block when a source phrase, formula, caption, or OCR result is ambiguous. Do not reparse pages already available.
- stem-notes: optional support for STEM-specific figure context and mathematical transcription.

### Markdown adaptation boundary

The upstream mathtranslations Skill's native workflow targets Chinese LaTeX/PDF projects. This workflow deliberately targets Markdown.

Use its applicable translation principles and references, but do **not** automatically:
- create a MathTranslations LaTeX project or compile a PDF;
- apply its personal cover, logo, fixed reviewer credit, or template-specific punctuation;
- convert the entire Markdown document into TeX;
- invoke optional multi-model routing or external terminology services.

The requested/project Markdown format and AGENTS.md take precedence. Do not run audit_latex.py against a Markdown artifact.

## Translation rules

1. Translate mathematical meaning, not English word order. Use natural, concise Chinese while preserving the exact logical force of the source.
2. Preserve hypotheses, quantifiers, scope, modality, negation, comparisons, exceptions, necessary/sufficient conditions, and dependencies.
3. Treat instruction verbs precisely: prove, show, derive, calculate, evaluate, estimate, sketch, compare, discuss, and explain are not interchangeable.
4. Preserve all formulas and mathematical notation. Do not silently change signs, indices, symbols, units, equation numbers, or mathematical assumptions while translating surrounding prose.
5. Preserve headings, theorem/definition/example types, problem numbers, answer options, tables, captions, footnotes, labels, citations, and cross-references.
6. Do not solve exercises, add hints, explain the solution, simplify the question, or change its difficulty unless the user explicitly requests those additions.
7. Do not omit repeated statements merely because they appear redundant in English; they may carry a condition or referential role.
8. Use established Chinese terminology in the relevant mathematical/physical field. A term's everyday translation is not necessarily its technical translation.
9. Keep one preferred translation for each recurring term. Record context-specific alternatives and exceptions in the glossary rather than switching wording casually.
10. Preserve proper names, named theorems, acronyms, and symbols consistently. Use an English term in parentheses at first occurrence when it prevents ambiguity or is pedagogically useful.
11. Keep source figures unchanged by default. Translate captions and surrounding references. Do not edit text embedded in a figure unless the user explicitly asks for a translated/recreated figure.
12. Do not silently repair a suspected error in the source. Preserve it and record the issue separately.

## Procedure

### 1. Establish the source of truth

- Read project AGENTS.md and the source Markdown.
- Confirm the source file's language, scope, page markers, and status.
- If a source PDF exists, use it as the authority for visible content when OCR and the PDF disagree.
- If the PDF is unavailable, state that page-level verification is not possible; do not imply that it was performed.
- If a source issue changes the meaning of a condition or equation, resolve it from the PDF before translating that unit or mark the translation as blocked/provisional.

### 2. Build or update the glossary

Use _work/<document-id>/glossary.en-zh.md.

Suggested columns:

| English term | Preferred Chinese | Field/context | Alternatives or exceptions | Source |
|---|---|---|---|---|

- Reuse user-approved terms and prior chapter decisions.
- Establish terminology from local definitions and field context, not literal dictionary substitution.
- Record disputed terms and unresolved choices.
- Do not query external terminology services or upload text unless the user authorizes network use.

### 3. Translate in coherent units

- Work by section/subsection or a bounded group of problems.
- Keep the source and target structure aligned so omissions can be detected.
- Translate prose and labels while preserving equations as source-equivalent LaTeX.
- Preserve page/source markers, figure links, table structure, and numbered references.
- For problem statements, translate every sentence, condition, given value, unit, and option. Do not solve the problem.
- If a term has multiple valid meanings, use context and glossary evidence. If still unresolved, retain the English term in parentheses and add a review issue rather than inventing certainty.

### 4. Create the candidate artifact

Write:

output/<document-id>/<unit>.zh-CN.candidate.md

Use front matter to make the status explicit:

```yaml
---
artifact_type: translation
source_artifact: <unit>.source.md
target_language: zh-CN
translation_status: candidate
review_status: pending
---
```

Keep the source-language transcript as a separate file. Do not overwrite it or replace an existing accepted translation.

### 5. Review mathematical and linguistic fidelity

Perform separate checks:

**Completeness**
- Every source heading, paragraph, list item, problem, option, caption, table row, footnote, and meaningful note is represented.
- No sentence or condition has been silently shortened away.

**Mathematical semantics**
- Check if/only if, iff, for all/there exists, unique, respectively, at least/at most, necessary/sufficient, unless, assume, suppose, and boundary/initial conditions.
- Compare every equation, sign, index, unit, constant, inequality, and referenced number against the source.
- Confirm the translated instruction verb asks for the same mathematical operation as the original.

**Terminology**
- Check repeated technical terms against the glossary.
- Distinguish context-specific meanings.
- Preserve names, acronyms, and notation consistently.

**Markdown integrity**
- Check heading hierarchy, lists, tables, LaTeX delimiters, image paths, anchors, citations, and page markers.
- Ensure translated text has not broken a Markdown table or formula boundary.

Record unresolved issues in _work/<document-id>/translation-review.md. Do not bury important uncertainty in polished prose.

## Outputs

- <unit>.source.md — unchanged source-language transcript.
- <unit>.zh-CN.candidate.md — Chinese translation candidate.
- _work/<document-id>/glossary.en-zh.md — project terminology decisions.
- _work/<document-id>/translation-review.md — review status and unresolved issues, when needed.
- Existing source image assets reused through relative paths.

## Completion status

A candidate may be marked review_status: reviewed only after the checks above have been performed. Even then, translation_status remains candidate until the user explicitly accepts it.

## Invocation examples

- "基于 2.4.source.md，按 WF-TR-01 生成候选中文版，不解题。"
- "将这份英文物理习题翻译成中文，保留全部条件和选项，输出 candidate。"
- "沿用 glossary.en-zh.md 的术语，继续翻译下一节。"
