#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:?usage: bootstrap.sh <PROJECT_DIR> <PROJECT_NAME> [KB_DIR]}"
PROJECT_NAME="${2:?project name required}"
KB_DIR="${3:-$HOME/.rx-kb}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ensure KB exists
bash "$SCRIPT_DIR/kb-init.sh" "$KB_DIR" >/dev/null

mkdir -p "$PROJECT_DIR"/{experiments,notes,paper/arxiv,paper/anon}
mkdir -p "$PROJECT_DIR"/.rx/{questions,evidence,claims,experiments}

# state.json (must match rx_state.store.default_state)
cat > "$PROJECT_DIR/.rx/state.json" <<EOF
{
  "project": "$PROJECT_NAME",
  "kb_path": "$KB_DIR",
  "stage": "ideate",
  "loop": {
    "enabled": false,
    "iteration": 0,
    "max_iterations": 20,
    "no_improve_count": 0,
    "no_improve_limit": 5
  },
  "artifacts": {"questions": [], "evidence": [], "claims": [], "experiments": []}
}
EOF

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
.venv/
experiments/**/checkpoints/
EOF

# fresh git repo
git -C "$PROJECT_DIR" init -q

# per-project venv from shared uv cache (skip gracefully if uv missing)
if command -v uv >/dev/null 2>&1; then
  ( cd "$PROJECT_DIR" && uv venv >/dev/null 2>&1 || true )
fi

git -C "$PROJECT_DIR" add -A
git -C "$PROJECT_DIR" -c user.email=rx@local -c user.name=rx \
    commit -q -m "chore: bootstrap $PROJECT_NAME research project"

echo "Project ready at $PROJECT_DIR"
