#!/usr/bin/env bash
set -euo pipefail

# Install or link sec-paper skills into a target project (.agents/skills),
# Codex user skills (~/.codex/skills), or OpenCode user skills (~/.config/opencode/skills).
# Does NOT modify upstream ARIS tracked files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TARGET_DIR=""
PROJECT_DIR=""
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
      [[ $# -ge 2 && -d "$2" ]] || { echo "--project requires an existing directory" >&2; exit 1; }
      PROJECT_DIR="$(cd "$2" && pwd)"
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

if [[ -n "$PROJECT_DIR" ]]; then
  python3 "$REPO_ROOT/tools/project.py" init --project "$PROJECT_DIR"
fi

for skill_path in "$REPO_ROOT"/skills/*/SKILL.md; do
  skill="$(basename "$(dirname "$skill_path")")"
  if [[ -e "$TARGET_DIR/$skill" && ! -L "$TARGET_DIR/$skill" ]]; then
    echo "Refusing to overwrite a real directory: $TARGET_DIR/$skill" >&2
    exit 1
  fi
  ln -sfn "$REPO_ROOT/skills/$skill" "$TARGET_DIR/$skill"
  echo "Linked: $TARGET_DIR/$skill -> $REPO_ROOT/skills/$skill"
done

if $OVERRIDE_GENERIC; then
  for pair in "idea-creator:sec-idea-creator" "idea-discovery:sec-idea-discovery" "research-pipeline:sec-research-pipeline"; do
    name="${pair%%:*}"; target="${pair##*:}"
    if [[ -e "$TARGET_DIR/$name" && ! -L "$TARGET_DIR/$name" ]]; then
      echo "Refusing to overwrite a real directory: $TARGET_DIR/$name" >&2
      exit 1
    fi
    ln -sfn "$REPO_ROOT/skills/$target" "$TARGET_DIR/$name"
    echo "Linked override: $TARGET_DIR/$name -> $REPO_ROOT/skills/$target"
  done
fi
