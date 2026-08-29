#!/usr/bin/env bash
# Budget gate over ccusage: exits 1 when agent spend crosses a threshold.
# Costs are API-rate equivalents from local transcript parsing (all agents
# ccusage detects: Claude Code, Codex, Hermes, ...), not a bill.
#
# Usage:
#   cost-gate.sh --max-usd 25              # today (default window)
#   cost-gate.sh --max-usd 200 --window month
#
# ccusage is version-pinned: this script can run unattended (cron/CI), so a
# compromised or breaking ccusage release must not silently change gate
# behavior. Bump deliberately.
set -euo pipefail

CCUSAGE="ccusage@20.0.20"
MAX=""
WINDOW="today"

while [ $# -gt 0 ]; do
  case "$1" in
    --max-usd) MAX="$2"; shift 2 ;;
    --window)  WINDOW="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done
[ -n "$MAX" ] || { echo "usage: cost-gate.sh --max-usd N [--window today|month]" >&2; exit 2; }

case "$WINDOW" in
  today) SINCE=$(date +%Y%m%d) ;;
  month) SINCE=$(date +%Y%m01) ;;
  *) echo "unknown window: $WINDOW (today|month)" >&2; exit 2 ;;
esac

SPENT=$(npx -y "$CCUSAGE" daily --json --since "$SINCE" 2>/dev/null | jq -r '.totals.totalCost // 0')

if [ "$(printf '%s\n' "$SPENT > $MAX" | bc -l)" = "1" ]; then
  printf 'OVER BUDGET: $%.2f spent since %s (limit $%s)\n' "$SPENT" "$SINCE" "$MAX" >&2
  exit 1
fi
printf 'ok: $%.2f spent since %s (limit $%s)\n' "$SPENT" "$SINCE" "$MAX"
