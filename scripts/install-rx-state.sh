#!/usr/bin/env bash
set -eu
PY="$HOME/.rx-kb/venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "No $PY — run scripts/kb-init.sh first if you need the shared venv."
  exit 0
fi
ROOT=/mnt/c/Users/louis/rx
if command -v uv >/dev/null 2>&1; then
  uv pip install --python "$PY" -e "$ROOT"
else
  "$PY" -m ensurepip --upgrade || true
  "$PY" -m pip install -e "$ROOT"
fi
"$PY" -c 'from rx_state.grill import SharedUnderstanding; print("rx_state OK", "diff_mechanism" in SharedUnderstanding.__dataclass_fields__)'
