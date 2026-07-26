#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:?usage: bootstrap.sh <PROJECT_DIR> <PROJECT_NAME> [KB_DIR]}"
PROJECT_NAME="${2:?project name required}"
if ! [[ "$PROJECT_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "error: PROJECT_NAME must match ^[A-Za-z0-9._-]+$ (got: $PROJECT_NAME)" >&2
  exit 2
fi
KB_DIR="${3:-$HOME/.rx-kb}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ensure KB exists
bash "$SCRIPT_DIR/kb-init.sh" "$KB_DIR" >/dev/null

mkdir -p "$PROJECT_DIR"/{experiments,notes,paper/arxiv,paper/anon}
mkdir -p "$PROJECT_DIR"/.rx/{questions,evidence,claims,experiments}

# state.json (must match rx_state.store.default_state)
python3 - "$PROJECT_NAME" "$KB_DIR" "$PROJECT_DIR/.rx/state.json" <<'PY'
import json, sys
project, kb_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
state = {
    "project": project,
    "kb_path": kb_path,
    "stage": "ideate",
    "loop": {"enabled": False, "iteration": 0, "max_iterations": 20,
             "no_improve_count": 0, "no_improve_limit": 5},
    "artifacts": {"questions": [], "evidence": [], "claims": [], "experiments": []},
}
with open(out, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)
PY

cat > "$PROJECT_DIR/PROJECT.md" <<EOF
# $PROJECT_NAME

Research project bootstrapped by rx.

- Knowledge base: \`$KB_DIR\` (system/GPU, pitfalls, learnings, secrets-by-reference)
- Traceability state: \`.rx/state.json\`
- Paper outputs: \`paper/arxiv/\` (preprint) and \`paper/anon/\` (double-blind)

## Research question

_TODO: filled in by rx-ideate._
EOF

cat > "$PROJECT_DIR/.gitignore" <<'EOF'
__pycache__/
*.pyc
.venv
experiments/**/checkpoints/
EOF

# fresh git repo
git -C "$PROJECT_DIR" init -q

# One venv shared across all rx projects, kept in the KB dir (already the one thing every
# project shares). `.venv` in each project is a symlink to it, so `rx_state` and its deps are
# installed once instead of per project. Best-effort: never fail the bootstrap if uv is missing
# or offline.
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SHARED_VENV="${RX_VENV_DIR:-$KB_DIR/venv}"
if command -v uv >/dev/null 2>&1; then
  # rx_state requires Python >=3.11; pin the venv so the editable install resolves.
  if [ ! -d "$SHARED_VENV" ]; then
    uv venv --python '>=3.11' "$SHARED_VENV" >/dev/null 2>&1 || true
  fi
  uv pip install --python "$SHARED_VENV/bin/python" -e "$PLUGIN_ROOT" >/dev/null 2>&1 || true
  ln -sfn "$SHARED_VENV" "$PROJECT_DIR/.venv"
fi

git -C "$PROJECT_DIR" add -A
git -C "$PROJECT_DIR" diff --cached --quiet || \
  git -C "$PROJECT_DIR" -c user.email=rx@local -c user.name=rx \
      commit -q -m "chore: bootstrap $PROJECT_NAME research project"

echo "Project ready at $PROJECT_DIR"
