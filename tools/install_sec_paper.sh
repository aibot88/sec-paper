#!/usr/bin/env bash
set -euo pipefail

# Install or link sec-paper skills into a target project (.agents/skills),
# Codex user skills (~/.codex/skills), or OpenCode user skills (~/.config/opencode/skills).
# Does NOT modify upstream ARIS tracked files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TARGET_DIR=""
OVERRIDE_GENERIC=false

usage() {
  cat <<'EOF'
Usage:
  bash tools/install_sec_paper.sh [--project <path> | --codex | --opencode] [--override-generic]

Options:
  --project <path>          Link skills into <path>/.agents/skills/
  --codex                   Link skills into ~/.codex/skills/
  --opencode                Link skills into ~/.config/opencode/skills/
  --override-generic        Route generic entry points to security variants in the
                            target skill dir: idea-creator, idea-discovery,
                            research-pipeline -> sec-* equivalents
                            (alias: --override-idea-creator)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      TARGET_DIR="$(cd "$2" && pwd)/.agents/skills"
      shift 2
      ;;
    --codex)
      TARGET_DIR="$HOME/.codex/skills"
      shift
      ;;
    --opencode)
      TARGET_DIR="$HOME/.config/opencode/skills"
      shift
      ;;
    --override-generic|--override-idea-creator)
      OVERRIDE_GENERIC=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$TARGET_DIR" ]]; then
  echo "Error: specify one of --project <path>, --codex, or --opencode" >&2
  usage >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

for skill in sec-research-pipeline sec-idea-discovery sec-research-lit sec-idea-creator sec-novelty-check sec-research-review sec-research-refine sec-experiment-plan sec-research-refine-pipeline sec-experiment-bridge sec-auto-review-loop sec-paper-writing; do
  ln -sfn "$REPO_ROOT/skills/$skill" "$TARGET_DIR/$skill"
  echo "Linked: $TARGET_DIR/$skill -> $REPO_ROOT/skills/$skill"
done

if $OVERRIDE_GENERIC; then
  for pair in "idea-creator:sec-idea-creator" "idea-discovery:sec-idea-discovery" "research-pipeline:sec-research-pipeline"; do
    name="${pair%%:*}"; target="${pair##*:}"
    ln -sfn "$REPO_ROOT/skills/$target" "$TARGET_DIR/$name"
    echo "Linked override: $TARGET_DIR/$name -> $REPO_ROOT/skills/$target"
  done
fi
