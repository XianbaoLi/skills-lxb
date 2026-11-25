# Workflows

Workflows are task-level orchestration recipes built from the Skills in this repository.

- A **Skill** provides a capability and specialist instructions.
- A **Workflow** defines when to use capabilities, their order, hand-offs, checkpoints, outputs, and failure paths.
- A workflow is documentation for the host Agent. It is **not** an executable pipeline, plugin, daemon, or guarantee that every host tool is available.

## Workflow catalogue

| ID | Purpose | Main Skills | Primary output |
|---|---|---|---|
| [WF-DOC-01](scan-pdf-to-source-markdown.md) | OCR and faithfully transcribe a scanned/image-heavy PDF | mineru; optional stem-notes | Original-language source Markdown |
| [WF-TR-01](source-markdown-to-chinese-candidate.md) | Translate a checked source transcript into a Chinese candidate | mathtranslations | Chinese candidate Markdown |
| [WF-DOC-TR-01](scanned-pdf-to-chinese-candidate.md) | Compose OCR, source transcription, and candidate translation | mineru, stem-notes, mathtranslations | Source Markdown + Chinese candidate |
| [WF-TR-02](review-and-accept-translation.md) | Review a candidate and, only with explicit approval, promote it | mathtranslations; optional mineru | Review record + accepted translation |

## Selection

- Scanned/image-heavy PDF, original-language transcription only → WF-DOC-01.
- Existing, checked source Markdown → WF-TR-01.
- Scanned PDF and a requested Chinese candidate → WF-DOC-TR-01.
- Existing Chinese candidate requiring review or acceptance → WF-TR-02.
- If the PDF has already been parsed, reuse its valid MinerU document ID/locator and parsed output. Do not reparse merely because a new workflow starts.
- For a full book, process coherent chapters/sections and maintain checkpoints. Do not automatically invoke book-to-skill unless the user wants a reusable, queryable knowledge Skill.

## Shared rules

1. Read the working directory's AGENTS.md first when present. User instructions and project-specific rules take precedence over these generic recipes.
2. Preserve the original source. Never modify or replace the source PDF.
3. Treat the visible source PDF page as the authority for what was printed. MinerU output is a structured recognition result, not ground truth.
4. Reuse existing local parsing results and environments. Do not install, upgrade, reconfigure, restart services, invalidate caches, or delete data without the user's approval.
5. Use MinerU locally first. Never add --remote or upload source documents without explicit permission. If the available local tier cannot satisfy the task, stop and present the actual choices rather than silently switching tools.
6. Keep intermediate files under _work/ and deliverables under output/. Do not place logs or raw parse payloads in the final reading document.
7. Keep source transcription, translation candidate, review notes, and accepted translation as distinct artifacts.
8. A file named *.candidate.md is not approved or final. Never rename, overwrite, or promote it automatically.
9. Do not invent illegible text, missing equations, image labels, citations, or page numbers. Record uncertainty with a source-page reference.
10. Workflows are selective: invoke only the Skills needed for the current stage. Do not mechanically run every Skill in the repository.

## Standard project layout

Create only directories that the current task needs:

```text
project/
├── AGENTS.md                         # optional project-specific rules
├── source/                            # original user materials; read-only
├── _work/
│   └── <document-id>/
│       ├── mineru/                    # raw MinerU output and structured responses
│       ├── pages/                     # page renders / visual inspection material
│       ├── figures/                   # extracted or cropped source figures
│       ├── glossary.en-zh.md          # project terminology decisions
│       ├── ocr-issues.md              # unresolved OCR/source issues
│       └── translation-review.md      # candidate review record
└── output/
    └── <document-id>/
        ├── <unit>.source.md
        ├── <unit>.zh-CN.candidate.md
        ├── <unit>.zh-CN.md             # only after explicit acceptance
        └── assets/
            └── <unit>/
```

Use the user's existing folder structure when it is already clear and safe. The layout above is a default, not a requirement to create empty folders.

## Status model

Use explicit artifact status in front matter or a sidecar manifest:

- parsed — MinerU produced a parse result; visual/content review is incomplete.
- transcribed — source-language Markdown has been assembled; checks may remain.
- source-reviewed — the requested source range has been compared with the PDF and known issues recorded.
- translation-candidate — Chinese translation exists but has not been accepted.
- reviewed-candidate — a review pass is complete; unresolved issues remain listed. In candidate front matter, this can be represented by review_status: reviewed while translation_status remains candidate.
- accepted — the user explicitly approved promotion to the accepted filename.

Do not infer a later status from the existence of a file.

## How to invoke

- "按 WF-DOC-01，把这份扫描 PDF 的第 12–18 页忠实转写成英文 Markdown。"
- "基于已经校验的 2.4.source.md，按 WF-TR-01 生成候选中文版。"
- "按 WF-DOC-TR-01，把这本扫描教材的第 2.4 节转写并生成候选中文版。"
- "按 WF-TR-02 对照英文原文复核这份候选译文；先不要定稿。"

## Maturity

These workflows are versioned specifications. They have not yet been validated end-to-end against a representative scan-heavy textbook on every supported Agent host. Treat host-specific tool differences and OCR quality as explicit validation items, not as proven capabilities.
