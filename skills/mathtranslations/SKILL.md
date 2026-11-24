---
name: mathtranslations
description: Translate mathematical books, papers, notes, and existing LaTeX projects into rigorous Chinese LaTeX, or review and repair an existing mathematical translation, including projects using the MathTranslations template. Use when source fidelity, mathematical correctness, terminology consistency, cross-references, citations, compilation, and PDF-level proofreading all matter. Do not use for ordinary non-mathematical translation.
metadata:
  workflow-version: "2026.09.03"
---

# MathTranslations

Produce a Chinese mathematical translation that can be compiled, checked against
the source, and maintained as a real LaTeX project.

## Canonical Workflow

This installed skill is the sole active workflow. Use the version recorded in
`VERSION`; do not activate V2.1/V2.2 experiment packets or project-local legacy
templates as alternative workflows. Historical files may be read only as
provenance or migration input. Before continuing an older project, migrate its
cover and routing contracts to this current version.

## Establish The Source Of Truth

1. Inventory the supplied PDF, TeX sources, bibliography, figures, fonts,
   templates, and any existing translated files before editing.
2. Treat the published source PDF as the authority for visible mathematical
   content and structure. Use source TeX to recover markup and reduce
   transcription errors, but do not follow it when it conflicts with the
   published PDF.
3. If the source PDF is unavailable, state that limitation and use the best
   available source without pretending that page-level comparison was done.
4. Never silently repair a suspected error in the source. Preserve it by
   default and clearly record the issue; apply a correction only when the user
   requests it or reliable evidence resolves it.
5. Separate content authority from presentation authority. The source PDF
   governs mathematical content; when the user chooses the MathTranslations
   template, `mathtranslations-translation-template.tex` governs typesetting
   conventions.

## Prepare The Project

- Preserve an existing project's document class, packages, file layout, labels,
  citation keys, macros, and build system unless a change is necessary or the
  user explicitly chooses the MathTranslations template.
- For a new project, consult the current MathTranslations guide before choosing
  a template or terminology source. Prefer the latest stable resources linked
  from <https://mathtranslations.org/guide/> over bundled stale copies.
- When a `mathtranslations-translation-template.zip` or
  `mathtranslations-translation-template.tex` is supplied, inspect that exact
  version instead of relying on memory. Archives under the older name
  `MathTranslations-Template.zip` are earlier releases of the same template.
  Read [references/mathtranslations-template.md](references/mathtranslations-template.md)
  before adapting it.
- If the user selects the MathTranslations template but supplies no template
  files, copy `assets/mathtranslations-translation-template.tex` and
  `assets/wuyi-logo.png` into the project. `assets/wuyi-logo.svg` is the
  canonical website source asset; the PNG is the XeLaTeX-ready derivative.
- If the user supplies a newer template, prefer that version after comparing
  its contract with the bundled baseline and recording any meaningful changes.
- Build a small project glossary before translating substantial text. Reuse
  established Chinese mathematical terms; keep named objects and symbols
  stable across chapters.
- Read [references/workflow.md](references/workflow.md) when starting a new
  translation, importing a long source, or deciding how to stage the work.
- For a book-length or multi-chapter job, also read
  [references/long-book-optimization.md](references/long-book-optimization.md)
  before choosing checkpoints, context, or models. It defines the optional
  Sol-medium/Terra-medium routing and the minimal state needed to measure
  whether the routing actually helps.
- When dispatching a routed translation worker, build a bounded unit packet
  with `scripts/build_context_capsule.py`. Give that worker the generated
  `CONTRACT.md` and `TASK.json`; do not also ask it to reread this skill, the
  long-book guide, complete build logs, or the full-book glossary.
- For its blind Sol review, use the same bounded source packet plus
  [references/routed-review-contract.md](references/routed-review-contract.md),
  anonymized candidate files, unit terms, and a short deterministic-findings
  summary. Do not replay either worker's conversation or successful logs.

## Translate

- Translate mathematical meaning rather than sentence shape. Use natural,
  concise Chinese while preserving definitions, hypotheses, quantifiers,
  logical dependencies, notation, equation content, theorem status, and the
  force of words such as "if", "only if", "unique", and "respectively".
- Keep math in LaTeX. Reuse the source's macros and environments when they are
  sound. Do not convert formulas into prose, screenshots, or Unicode lookalikes.
- Preserve theorem-like environments, equation structure, bibliography links,
  footnotes, figures, tables, and section hierarchy.
- Recreate commutative diagrams, morphism diagrams, category diagrams,
  pullback or pushout squares, and other arrow-and-node mathematical diagrams
  with the `tikz-cd` package and `tikzcd` environment. Do not replace them with
  screenshots or raster images. Preserve every node, label, arrow direction,
  arrow style, and commutative relationship from the source.
- Handle ordinary figures by priority: when the source PDF has good quality
  and the figure is clear, crop a faithful screenshot as the preferred asset;
  redraw simple figures with ordinary TikZ; keep `tikzcd` for arrow-and-node
  diagrams. Record any exception.
- Typeset display formulas uniformly in `align`, `aligned`, or `align*`
  environments. Never place multiple `\[ \]` blocks side by side; merge them
  into a single environment.
- Use the `enumerate` environment for every ordered list; never type the
  numbering manually.
- Write Chinese double quotes with TeX ligatures: two grave accents for the
  opening quote and two straight apostrophes for the closing quote. The
  apostrophe pair alone renders a closing quote, and Unicode curly quotes
  are not used in this template.
- Apply the personal cover standard to every new translation: place the
  official 物译 Phi-style logo (`wuyi-logo.png`) on the first page; show no old
  MathTranslations `logo.pdf` or `mathtranslations.org` branding; omit the
  translator credit and `翻译及重排`; and place the bottom-right metadata in
  this order: publisher line, `Model: \ModelUsed`, `审核：\Reviewer`, then
  `Updated: \TranslationDate`. Define `\Reviewer` as `曹溪能`. Keep the
  reviewer line directly below the model line.
- With the MathTranslations template, introduce a concept once with
  `\newterm{stable-key}{中文术语}{English term}`, write the Chinese term normally
  afterward, and keep `\printterminology` as the final document content.
- Follow the selected template's punctuation policy. The inspected
  MathTranslations template uses Chinese punctuation except for an ASCII `.`
  at the end of Chinese prose sentences.
- Use `\label` plus the project's reference command for numbered objects. Do
  not hard-code theorem, equation, section, figure, table, or page numbers in
  translated prose.
- Do not invent missing proof steps, citations, definitions, labels, or
  references. Mark unresolved source ambiguity explicitly.
- Read [references/latex-quality.md](references/latex-quality.md) when editing
  TeX, resolving ambiguous notation, handling OCR, or repairing references.

## Verify

Verification is part of the translation, not an optional final polish.

1. Compile early and repeatedly with the project's actual build command.
2. Compare the generated PDF with the source PDF section by section.
3. Perform three separate passes: Chinese language and terminology;
   mathematics and structural fidelity; compilation and visual layout.
4. Run `scripts/audit_latex.py <project-or-tex-file>` for deterministic checks.
   Add `--profile mathtranslations` for projects based on the inspected
   MathTranslations template, and use `--strict` when warnings should fail CI.
5. Extract and visually inspect the first PDF page. It must show the official
   物译 Phi-style logo, contain `审核：曹溪能` below the model line, and contain
   neither the old MathTranslations logo nor `mathtranslations.org` branding.
6. Read [references/review-checklist.md](references/review-checklist.md) before
   declaring a chapter or project complete.
7. For model-routed long work, apply the blind Sol-medium sampling and
   downshift stop rules in
   [references/long-book-optimization.md](references/long-book-optimization.md).

## Report The Result

Summarize:

- translated or reviewed scope;
- source files and authority used;
- build command and whether it succeeded;
- checks performed;
- unresolved ambiguities, suspected source errors, missing assets, or visual
  differences that still need human judgment.
