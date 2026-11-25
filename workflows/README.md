# Workflows

A Workflow is a **single Markdown document** describing a repeatable task that an Agent completes by coordinating existing Skills. It is a declarative task recipe, not an executable program.

- **Skill** = specialist capability and its usage instructions.
- **Workflow** = supported task, required/optional Skills, inputs, outputs, constraints, and the order in which the Agent coordinates them.
- **Agent** = interprets the Workflow, selects relevant Skills, adapts to available host tools, and performs the work.

No Python, shell, MCP server, plugin, or other executable code is required to define a Workflow. Add code only when a deterministic operation cannot be handled reliably by the Agent and there is a concrete maintenance reason to automate it.

## Naming convention

Use stable, semantic names. Do not use sequence numbers such as WF-01 or names tied to a particular Skill implementation.

- **Workflow ID:** WF-<DOMAIN>-<ACTION> in uppercase. Use a short domain and one or more action words. IDs are stable once published.
- **Filename:** <domain>-<action>.md in lowercase kebab-case. The filename mirrors the ID without the WF- prefix.
- **Display name:** concise human-readable name; use Chinese as the primary name in this repository.
- **Version:** increment when supported capabilities, inputs/outputs, constraints, or process materially change.
- Do not put Skill names or version numbers in the Workflow ID. Skills can be replaced without changing task identity.
- A combined Workflow uses a clear compound action, not a vague name such as all-in-one.

Examples:
- WF-DOC-TRANSCRIBE → doc-transcribe.md
- WF-DOC-TRANSLATE → doc-translate.md
- WF-DOC-TRANSCRIBE-TRANSLATE → doc-transcribe-translate.md
- WF-DOC-REVIEW-TRANSLATION → doc-review-translation.md

## Required document structure

Each Workflow is self-contained and has YAML front matter followed by explanatory Markdown.

| Metadata | Meaning |
|---|---|
| workflow_id | Stable unique ID |
| name | Human-readable name |
| name_en | Optional English name |
| version | Workflow document version |
| status | draft, active, or deprecated |
| category | Task domain |
| execution_model | Normally agent-guided |
| implementation | Normally documentation-only |
| capabilities | What the Workflow supports |
| skills.required | Skills essential to the task |
| skills.optional | Skills used only when helpful |
| inputs | Required or optional source material |
| outputs | Expected artifacts |
| not_supported | Explicit scope boundaries |
| approval_gates | Actions requiring explicit user approval |

The body should explain purpose and trigger conditions, Skill responsibilities, process and hand-offs, constraints, outputs, failure handling, and natural-language invocation examples.

Do not duplicate the complete contents of referenced Skill instructions. Describe the orchestration and link to the relevant Skill.

## Workflow catalogue

| Workflow ID | Name | File | Main Skills | Input → Output |
|---|---|---|---|---|
| WF-DOC-TRANSCRIBE | 扫描版 PDF 忠实转写 | doc-transcribe.md | mineru; stem-notes (optional) | Scanned PDF → source-language Markdown |
| WF-DOC-TRANSLATE | 数学与物理资料专业翻译 | doc-translate.md | mathtranslations | Checked source Markdown → Chinese candidate |
| WF-DOC-TRANSCRIBE-TRANSLATE | 扫描版 PDF 转写并生成候选中文版 | doc-transcribe-translate.md | mineru; mathtranslations; stem-notes (optional) | Scanned PDF → source Markdown + Chinese candidate |
| WF-DOC-REVIEW-TRANSLATION | 中文译文对照复核与验收 | doc-review-translation.md | mathtranslations; mineru (optional) | Source + candidate → review record; accepted copy only after approval |

## Shared conventions

- Read the project AGENTS.md first when present. User instructions and project-specific rules take precedence.
- Reuse existing Skill installations, environments, parse results, terminology decisions, and project structure.
- A Workflow selects only the Skills needed for its task. Do not invoke every Skill in the repository.
- A Workflow describes what is supported, not an unconditional command sequence. The Agent adapts to source format, scope, host, and available tools.
- Never silently install/upgrade dependencies, change persistent configuration, upload source documents, or overwrite existing user artifacts.
- Keep source, intermediate work, candidate outputs, and accepted outputs distinct.
- A candidate is not final. Acceptance must be explicit when the Workflow defines an approval gate.
- A Workflow is not production-validated merely because its Markdown is complete. Record real-world validation separately.

## File organization

The workflows directory contains one Markdown file per Workflow plus this catalogue. It should not contain copied Skill packages, raw documents, generated deliverables, or executable orchestration code.

For task-specific working files, follow project AGENTS.md or the Workflow's output convention. Generic default:

~~~text
project/
├── AGENTS.md
├── source/              # original user materials, read-only
├── _work/               # parse results, locators, glossaries, issue notes
└── output/              # requested deliverables
~~~

## Maturity

The current Workflows are draft specifications. Their structure and safety boundaries have been reviewed statically; end-to-end OCR and translation quality has not yet been benchmarked across representative documents or Agent hosts.
