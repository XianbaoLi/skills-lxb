# STEM teaching skill collection

2026-11-25 · Upstream Skill snapshots plus documentation-only Workflow definitions. Each Workflow is one Markdown file describing supported capabilities, task modes, mode-specific Skill metadata, inputs/outputs, and task coordination; there is no executable orchestrator. Read `third-party-skills.json` for exact commits and selected paths.

| Skill | Role | Origin |
|---|---|---|
| `mineru` | Document parsing, OCR and page/block locators | MinerU |
| `book-to-skill` | Long-document knowledge structuring | book-to-skill |
| `stem-notes` | STEM notes, worked solutions, figures and LaTeX handbooks | stem-notes |
| `mathtranslations` | Rigorous mathematical translation into Chinese and translation review | mathtranslations-skill |
| `study-atlas` | Practice tests, drills, study guides and offline HTML | study-atlas |
| `scientific-writing` | Evidence-backed writing | K-Dense |
| `scientific-visualization` | Scientific figures | K-Dense |
| `scientific-schematics` | AI-assisted schematic drafts | K-Dense |
| `scientific-critical-thinking` | Research reasoning and bias checks | K-Dense |
| `peer-review` | Evidence and reporting review | K-Dense |
| `citation-management` | Citation workflows | K-Dense |

## Install in WSL Codex

Clone the repository at the desired branch or commit, inspect the individual `SKILL.md` and scripts, then copy selected directories under `skills/` to `~/.agents/skills/` or use the existing `install.sh` (which replaces existing same-name directories). The following example deliberately skips an already-installed skill instead of overwriting it:

```bash
mkdir -p ~/.agents/skills
for s in mineru book-to-skill stem-notes mathtranslations study-atlas scientific-writing scientific-visualization scientific-schematics scientific-critical-thinking peer-review citation-management; do
  dest="$HOME/.agents/skills/$s"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    printf 'SKIP existing: %s\n' "$dest"
  else
    cp -a "skills/$s" "$dest" || exit 1
  fi
done
```

Restart Codex and verify discovery. Installing the skill directory does not install Python/Node/LaTeX packages or the MinerU CLI/models. Check dependency availability separately. Do not run third-party scripts, install dependencies, submit documents to remote APIs, or overwrite existing skills without explicit approval. `scientific-schematics` requires network/API credentials for generation; avoid transmitting private material. `stem-notes` uses Claude-specific `AskUserQuestion`/`Skill` conventions; adapt to available Codex tools if necessary rather than assuming identical runtime behavior.

## MathTranslations usage notes

`mathtranslations` is an unmodified upstream snapshot (workflow version 2026.09.03). Its native deliverable is Chinese LaTeX/PDF. For faithful Markdown translation of textbooks and exercises, use its source-fidelity, mathematical meaning, terminology and review guidance, while following the user's project-level format requirements. Do not apply the upstream personal-cover/logo, fixed reviewer attribution, TeX-template, or PDF-compilation requirements to unrelated Markdown work. Reverse translation is not the native workflow; only applicable principles transfer. The full upstream LICENSE and NOTICE, templates, assets, scripts and tests are retained. No external terminology service is required for local Markdown work.

## Upstream-only reference

`GalacticQuasar/claude-study-skills` provides `course-ingest`, `reference-sheet`, and `teach-me`. At the pinned commit no license file was found; no upstream files are redistributed here. The upstream README documents direct installation. To inspect the exact version, obtain it directly from the original repository and review its terms and host requirements:

```bash
git clone https://github.com/GalacticQuasar/claude-study-skills.git
git -C claude-study-skills checkout --detach 957cc593d1cb88ec53db46c386a219c1bbfae2fb
```

## Verification and boundaries

All 196 selected upstream file paths matched destination Git blob SHA and file mode; the six copies of K-Dense's MIT license were also checked. Source content has not been modified. The collection excludes unrelated website/CI/test/demo assets where listed in the manifest. No execution, installation, dependency resolution, or Codex end-to-end teaching-quality test was performed. The Skills remain independent packages. The workflows directory contains one Markdown specification per Workflow. WF-DOC-PROCESS consolidates related transcription, translation, and review modes in a single document; it adds no executable integration or runtime. Each included third-party skill retains its own upstream license; the root repository MIT license does not relicense third-party code. MinerU has additional license terms.
