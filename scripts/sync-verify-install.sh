#!/usr/bin/env bash
set -euo pipefail

echo "=== Claude cache skill markers ==="
WRITE=$(find "$HOME/.claude/plugins/cache" -path '*rx*/rx-write/SKILL.md' | head -1 || true)
GRILL=$(find "$HOME/.claude/plugins/cache" -path '*rx*/rx-grill/SKILL.md' | head -1 || true)
echo "WRITE=$WRITE"
echo "GRILL=$GRILL"
if [[ -n "${WRITE:-}" ]]; then
  grep -n 'conference-outcome-lessons\|novel-but-empty\|Paper structure' "$WRITE" | head -20 || true
fi
if [[ -n "${GRILL:-}" ]]; then
  grep -n 'collision\|evidence_expectations\|conference-outcome' "$GRILL" | head -20 || true
fi

echo "=== settings.json plugin flags ==="
python3 - <<'PY'
import json
from pathlib import Path
p = Path.home() / ".claude" / "settings.json"
d = json.loads(p.read_text())
print("enabledPlugins:", json.dumps(d.get("enabledPlugins", {}), indent=2))
print("extraKnownMarketplaces:", list(d.get("extraKnownMarketplaces", {}).keys()))
PY

echo "=== rx_state install ==="
candidates=(
  "$HOME/.rx-kb/venv/bin/python"
  "/mnt/c/Users/louis/rx/.venv/bin/python"
)
found=0
for py in "${candidates[@]}"; do
  if [[ -x "$py" ]]; then
    found=1
    echo "Using $py"
    "$py" -m pip install -e /mnt/c/Users/louis/rx/shared -q
    "$py" -c 'from rx_state.grill import SharedUnderstanding; print("rx_state OK", "diff_mechanism" in SharedUnderstanding.__dataclass_fields__)'
  fi
done
if [[ "$found" -eq 0 ]]; then
  echo "No shared venv found yet (ok if you have not run kb-init)."
fi
