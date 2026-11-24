# STEM teaching skill collection

2026-11-24 · Upstream snapshots, not a new integrated teaching pipeline. Read `third-party-skills.json` for exact commits and selected paths.

| Skill | Role | Origin |
|---|---|---|
| `mineru` | Document parsing, OCR and page/block locators | MinerU |
| `book-to-skill` | Long-document knowledge structuring | book-to-skill |
| `stem-notes` | STEM notes, worked solutions, figures and LaTeX handbooks | stem-notes |
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
for s in mineru book-to-skill stem-notes study-atlas scientific-writing scientific-visualization scientific-schematics scientific-critical-thinking peer-review citation-management; do
  dest="$HOME/.agents/skills/$s"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    printf 'SKIP existing: %s\n' "$dest"
  else
    cp -a "skills/$s" "$dest" || exit 1
  fi
done
```

Restart Codex and verify discovery. Installing the skill directory does not install Python/Node/LaTeX packages or the MinerU CLI/models. Check dependency availability separately. Do not run third-party scripts, install dependencies, submit documents to remote APIs, or overwrite existing skills without explicit approval. `scientific-schematics` requires network/API credentials for generation; avoid transmitting private material. `stem-notes` uses Claude-specific `AskUserQuestion`/`Skill` conventions; adapt to available Codex tools if necessary rather than assuming identical runtime behavior.

## Upstream-only reference

`GalacticQuasar/claude-study-skills` provides `course-ingest`, `reference-sheet`, and `teach-me`. At the pinned commit no license file was found; no upstream files are redistributed here. The upstream README documents direct installation. To inspect the exact version, obtain it directly from the original repository and review its terms and host requirements:

```bash
git clone https://github.com/GalacticQuasar/claude-study-skills.git
git -C claude-study-skills checkout --detach 957cc593d1cb88ec53db46c386a219c1bbfae2fb
```

## Verification and boundaries

All 173 selected upstream file paths matched destination Git blob SHA and file mode; the six copies of K-Dense's MIT license were also checked. Source content has not been modified. The collection excludes unrelated website/CI/test/demo assets where listed in the manifest. No execution, installation, dependency resolution, or Codex end-to-end teaching-quality test was performed. The components remain separate and are not a MinerU-integrated workflow. Each included third-party skill retains its own upstream license; the root repository MIT license does not relicense third-party code. MinerU has additional license terms.
