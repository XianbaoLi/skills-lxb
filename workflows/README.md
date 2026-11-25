# Workflows

A Workflow is one Markdown document describing a repeatable task that an Agent completes by coordinating existing Skills. It is a declarative task definition, not an executable program.

- **Skill** provides a specialist capability and usage instructions.
- **Workflow** defines supported capabilities, modes, Skill requirements, inputs, outputs, constraints, and coordination logic.
- **Agent** reads the Workflow, selects the relevant mode and Skills, adapts to available host tools, and performs the task.

No Python, shell, MCP server, plugin, or executable orchestration code is required to define a Workflow. Add code only when a deterministic operation cannot be handled reliably by the Agent and there is a concrete maintenance reason.

## Naming convention

Use stable, semantic names.

- **Workflow ID:** WF-<DOMAIN>-<ACTION>, uppercase, semantic, and stable.
- **Filename:** matching lowercase kebab-case name without the WF- prefix.
- **Display name:** concise; Chinese is primary in this repository.
- **Version:** increment when supported capabilities, inputs/outputs, constraints, or process materially change.
- Do not use sequence numbers or embed Skill names/version numbers in the ID.
- One Workflow may contain multiple modes. Do not split closely related modes into separate files unless their goals, inputs/outputs, Skill sets, and approval boundaries are materially independent.

Examples:
- WF-DOC-PROCESS → doc-process.md
- WF-RESEARCH-REVIEW → research-review.md
- WF-CODE-MAINTAIN → code-maintain.md

## Required metadata

Each Workflow has YAML front matter:

| Field | Meaning |
|---|---|
| workflow_id, name, name_en | Stable ID and display names |
| version, status | Document version and draft/active/deprecated lifecycle |
| category | Task domain |
| execution_model | Normally agent-guided |
| implementation | Normally documentation-only |
| supported_modes | Distinct task modes within this Workflow |
| capabilities | Explicitly supported functions |
| skills.required / skills.optional | Global Skill requirements, when applicable |
| skills.by_mode | Mode-specific required and optional Skills when requirements differ |
| inputs / outputs | Accepted materials and expected artifacts |
| not_supported | Explicit scope boundaries |
| approval_gates | Actions requiring explicit user approval |

The body explains purpose and selection, Skill responsibilities, mode-specific process, constraints, outputs, failure handling, and invocation examples. Link to Skill documentation instead of copying its full instructions.

## Current catalogue

| Workflow ID | Name | File | Purpose |
|---|---|---|---|
| WF-DOC-PROCESS | 教材与学习资料处理 | [doc-process.md](doc-process.md) | PDF/OCR 转写、专业翻译、组合处理及译文复核 |

## Shared conventions

- Read the project AGENTS.md first when present. User instructions and project-specific rules take precedence.
- Reuse existing Skill installations, environments, parse results, terminology decisions, and project structure.
- Select only the Skills needed for the chosen mode. Do not invoke every Skill in the repository.
- A Workflow describes what is supported, not an unconditional command sequence. The Agent adapts to source format, scope, host, and available tools.
- Never silently install/upgrade dependencies, change persistent configuration, upload source documents, or overwrite existing user artifacts.
- Keep source, intermediate work, candidate outputs, and accepted outputs distinct.
- A candidate is not final. Acceptance must be explicit when the Workflow defines an approval gate.
- Workflow status reflects maturity. A complete document is not proof of end-to-end validation.

## Directory rule

The workflows directory contains one Markdown file per Workflow plus this catalogue. It should not contain copied Skill packages, raw documents, generated deliverables, or executable orchestration code.
