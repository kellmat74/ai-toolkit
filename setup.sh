#!/usr/bin/env bash
# Idempotent: symlinks ai-toolkit contents into ~/.claude and ~/.hermes.
# Safe to re-run. Won't touch existing files unless they're already symlinks
# pointing somewhere else (in which case it relinks).
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
echo "Wiring ai-toolkit from: $REPO"

# ---------- Claude Code ----------
mkdir -p ~/.claude/{skills,agents,commands}

link_if_exists() {
  local src="$1" dest="$2"
  if [ -e "$src" ]; then
    ln -sfn "$src" "$dest"
    echo "  linked $dest -> $src"
  fi
}

link_if_exists "$REPO/claude/CLAUDE.md"        ~/.claude/CLAUDE.md
link_if_exists "$REPO/claude/settings.json"    ~/.claude/settings.json
link_if_exists "$REPO/claude/keybindings.json" ~/.claude/keybindings.json

for d in skills agents commands; do
  if [ -d "$REPO/claude/$d" ]; then
    for f in "$REPO/claude/$d"/*; do
      [ -e "$f" ] || continue
      [ "$(basename "$f")" = "README.md" ] && continue
      ln -sfn "$f" "$HOME/.claude/$d/$(basename "$f")"
      echo "  linked ~/.claude/$d/$(basename "$f")"
    done
  fi
done

# ---------- Hermes ----------
mkdir -p ~/.hermes/skills
link_if_exists "$REPO/hermes/config.yaml" ~/.hermes/config.yaml

if [ -d "$REPO/hermes/skills" ]; then
  for f in "$REPO/hermes/skills"/*; do
    [ -e "$f" ] || continue
    ln -sfn "$f" "$HOME/.hermes/skills/$(basename "$f")"
    echo "  linked ~/.hermes/skills/$(basename "$f")"
  done
fi

# ---------- MCP config (both surfaces) ----------
# Renders claude/mcp-servers-template.json into the Mac app config AND the
# CLI's ~/.claude.json. Needs gh auth + ~/.claude/secrets.json; skip if absent.
if command -v gh >/dev/null && [ -f ~/.claude/secrets.json ]; then
  python3 "$REPO/claude/restore-mcp-config.py" || echo "  WARN: MCP config render failed; run claude/restore-mcp-config.py manually"
else
  echo "  Skipped MCP config render (needs gh CLI auth + ~/.claude/secrets.json)"
fi

# ---------- Secrets check ----------
echo ""
missing=()
[ -f ~/.claude/.env ] || missing+=("~/.claude/.env")
[ -f ~/.hermes/.env ] || missing+=("~/.hermes/.env")

if [ ${#missing[@]} -gt 0 ]; then
  echo "Next: populate these from .env.example"
  for m in "${missing[@]}"; do echo "  - $m"; done
  echo ""
  echo "Use credentials you OWN (personal Anthropic key, personal GitHub PAT, etc.)"
  echo "so the toolchain follows you across employers."
else
  echo "Secrets present. You're good."
fi
