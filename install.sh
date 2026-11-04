#!/usr/bin/env bash
# install.sh — offline installer for the skills in this repo.
# Copies every skill under ./skills/ into agent skill directories.
#
# Usage:
#   bash install.sh                    # global scope, all detected agents
#   bash install.sh codex claude-code  # global scope, only these agents
#   bash install.sh --project codex    # install into current project
#
# Agent dirs follow https://github.com/vercel-labs/skills (docs/agents.md).
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$HERE/skills"
SCOPE="global"
AGENTS=()

for a in "$@"; do
  case "$a" in
    -g|--global) SCOPE="global" ;;
    -p|--project) SCOPE="project" ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) AGENTS+=("$a") ;;
  esac
done

SKILLS=()
for d in "$SKILLS_ROOT"/*/; do
  if [ -f "$d/SKILL.md" ]; then
    SKILLS+=("$(basename "$d")")
  fi
done
if [ "${#SKILLS[@]}" -eq 0 ]; then
  echo "error: no skills found under $SKILLS_ROOT" >&2
  exit 1
fi

global_dir() {
  case "$1" in
    claude-code|claude)                      echo "$HOME/.claude/skills" ;;
    codex|cursor|github-copilot|copilot|gemini-cli|gemini|opencode|cline|amp|universal|agents|zed)
                                             echo "$HOME/.agents/skills" ;;
    windsurf)                                echo "$HOME/.codeium/windsurf/skills" ;;
    hermes-agent|hermes)                     echo "${HERMES_SKILLS_DIR:-$HOME/.hermes/skills}" ;;
    *)                                       echo "" ;;
  esac
}

project_dir() {
  case "$1" in
    claude-code|claude) echo ".claude/skills" ;;
    windsurf)           echo ".windsurf/skills" ;;
    hermes-agent|hermes) echo ".hermes/skills" ;;
    *)                  echo ".agents/skills" ;;
  esac
}

detect_agents() {
  if [ -d "$HOME/.claude" ]; then echo "claude-code"; fi
  if [ -d "$HOME/.cursor" ]; then echo "cursor"; fi
  if [ -d "$HOME/.gemini" ]; then echo "gemini-cli"; fi
  if [ -d "$HOME/.copilot" ]; then echo "github-copilot"; fi
  if [ -d "$HOME/.config/opencode" ]; then echo "opencode"; fi
  if [ -d "$HOME/.codex" ] || [ -d "$HOME/.agents" ]; then echo "codex"; fi
  if [ -d "$HOME/.codeium/windsurf" ]; then echo "windsurf"; fi
  if [ -d "$HOME/.hermes" ] || [ -n "${HERMES_SKILLS_DIR:-}" ]; then echo "hermes-agent"; fi
}

if [ "${#AGENTS[@]}" -eq 0 ]; then
  while IFS= read -r line; do
    if [ -n "$line" ]; then AGENTS+=("$line"); fi
  done < <(detect_agents)
fi

if [ "${#AGENTS[@]}" -eq 0 ]; then
  echo "no agents detected. pass names explicitly, e.g.:  bash install.sh claude-code codex" >&2
  echo "known names: claude-code codex cursor github-copilot gemini-cli opencode windsurf hermes-agent" >&2
  exit 1
fi

echo "scope=$SCOPE  skills: ${SKILLS[*]}"
FAILED=0
for agent in "${AGENTS[@]}"; do
  if [ "$SCOPE" = "project" ]; then
    DEST="$(project_dir "$agent")"
  else
    DEST="$(global_dir "$agent")"
  fi
  if [ -z "$DEST" ]; then
    echo "skip (unknown agent): $agent"; continue
  fi
  mkdir -p "$DEST" 2>/dev/null || { echo "FAILED (mkdir): $DEST" >&2; FAILED=1; continue; }
  for s in "${SKILLS[@]}"; do
    rm -rf "$DEST/$s" 2>/dev/null
    if cp -R "$SKILLS_ROOT/$s" "$DEST/$s" 2>/dev/null; then
      echo "installed -> $DEST/$s   [$agent]"
    else
      echo "FAILED (copy): $DEST/$s   [$agent]" >&2; FAILED=1
    fi
  done
done

if [ "$FAILED" -eq 0 ]; then
  echo "done."
else
  exit 1
fi
