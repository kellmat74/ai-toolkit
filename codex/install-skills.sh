#!/usr/bin/env bash
# Install toolkit-owned skill links without replacing another skill installation.
set -euo pipefail

TOOLKIT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
skill_destination="${1:-${CODEX_HOME:-$HOME/.codex}/skills}"
mkdir -p "$skill_destination"
install_result=0
for source in "$TOOLKIT_ROOT"/codex/skills/*; do
  [ -f "$source/SKILL.md" ] || continue
  target="$skill_destination/$(basename "$source")"
  if [ -e "$target" ] || [ -L "$target" ]; then
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$source" ]; then
      continue
    fi
    echo "Existing skill left unchanged: $target" >&2
    install_result=1
    continue
  fi
  ln -s "$source" "$target"
  echo "Linked $target"
done
exit "$install_result"
