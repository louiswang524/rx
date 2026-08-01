#!/usr/bin/env bash
# Bootstrap a new RX research project under the canonical research tree:
#   $RX_RESEARCH_ROOT/<topic>/<project-name>/
#
# Preferred:
#   bootstrap.sh <PROJECT_NAME> --topic <TOPIC> [KB_DIR]
#   bootstrap.sh --topic <TOPIC> <PROJECT_NAME> [KB_DIR]
#
# Legacy (explicit directory, still supported for tests / special cases):
#   bootstrap.sh <PROJECT_DIR> <PROJECT_NAME> [KB_DIR]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALID_TOPICS="llm-agents llm-reasoning llm-inference recsys multimodal dl-optimization _archive"

usage() {
  cat >&2 <<EOF
usage:
  bootstrap.sh <PROJECT_NAME> --topic <TOPIC> [KB_DIR]
  bootstrap.sh --topic <TOPIC> <PROJECT_NAME> [KB_DIR]
  bootstrap.sh <PROJECT_DIR> <PROJECT_NAME> [KB_DIR]   # legacy explicit path

topics: $VALID_TOPICS

New projects are created under the research root
(\$RX_RESEARCH_ROOT, or ~/.rx-kb/research_root, or ~/research):
  <research-root>/<topic>/<project-name>/
EOF
  exit 2
}

is_valid_topic() {
  local t="$1"
  for x in $VALID_TOPICS; do
    [ "$x" = "$t" ] && return 0
  done
  return 1
}

is_valid_name() {
  [[ "$1" =~ ^[A-Za-z0-9._-]+$ ]]
}

looks_like_path() {
  local s="$1"
  [[ "$s" == /* || "$s" == ./* || "$s" == ../* || "$s" == *"/"* || "$s" == ~* ]]
}

TOPIC=""
PROJECT_NAME=""
PROJECT_DIR=""
KB_DIR=""
POSITIONAL=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    -h|--help) usage ;;
    --topic)
      [ "$#" -ge 2 ] || usage
      TOPIC="$2"
      shift 2
      ;;
    --topic=*)
      TOPIC="${1#--topic=}"
      shift
      ;;
    --)
      shift
      while [ "$#" -gt 0 ]; do POSITIONAL+=("$1"); shift; done
      break
      ;;
    -*)
      echo "error: unknown option: $1" >&2
      usage
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [ -n "$TOPIC" ]; then
  # New mode: name + topic
  if [ "${#POSITIONAL[@]}" -lt 1 ] || [ "${#POSITIONAL[@]}" -gt 2 ]; then
    usage
  fi
  PROJECT_NAME="${POSITIONAL[0]}"
  KB_DIR="${POSITIONAL[1]:-$HOME/.rx-kb}"
  if ! is_valid_name "$PROJECT_NAME"; then
    echo "error: PROJECT_NAME must match ^[A-Za-z0-9._-]+$ (got: $PROJECT_NAME)" >&2
    exit 2
  fi
  if ! is_valid_topic "$TOPIC"; then
    echo "error: unknown topic '$TOPIC' (expected one of: $VALID_TOPICS)" >&2
    exit 2
  fi
  RESEARCH_ROOT="$("$SCRIPT_DIR/research-root.sh" "$KB_DIR")"
  PROJECT_DIR="$RESEARCH_ROOT/$TOPIC/$PROJECT_NAME"
else
  # Legacy / shorthand
  if [ "${#POSITIONAL[@]}" -lt 2 ] || [ "${#POSITIONAL[@]}" -gt 3 ]; then
    usage
  fi
  ARG1="${POSITIONAL[0]}"
  ARG2="${POSITIONAL[1]}"
  ARG3="${POSITIONAL[2]:-}"

  if looks_like_path "$ARG1"; then
    PROJECT_DIR="$ARG1"
    PROJECT_NAME="$ARG2"
    KB_DIR="${ARG3:-$HOME/.rx-kb}"
  elif is_valid_name "$ARG1" && is_valid_topic "$ARG2"; then
    # Shorthand: bootstrap.sh <name> <topic> [kb]
    PROJECT_NAME="$ARG1"
    TOPIC="$ARG2"
    KB_DIR="${ARG3:-$HOME/.rx-kb}"
    RESEARCH_ROOT="$("$SCRIPT_DIR/research-root.sh" "$KB_DIR")"
    PROJECT_DIR="$RESEARCH_ROOT/$TOPIC/$PROJECT_NAME"
  else
    echo "error: when not using --topic, pass an explicit PROJECT_DIR path," >&2
    echo "       or '<name> <topic>' with a known topic." >&2
    usage
  fi

  if ! is_valid_name "$PROJECT_NAME"; then
    echo "error: PROJECT_NAME must match ^[A-Za-z0-9._-]+$ (got: $PROJECT_NAME)" >&2
    exit 2
  fi
fi

# ensure KB exists and remember research root for future bootstraps
bash "$SCRIPT_DIR/kb-init.sh" "$KB_DIR" >/dev/null

if [ -z "${RESEARCH_ROOT:-}" ]; then
  RESEARCH_ROOT="$("$SCRIPT_DIR/research-root.sh" "$KB_DIR")"
fi
# Persist detected/chosen research root (do not overwrite an existing file unless empty)
if [ ! -s "$KB_DIR/research_root" ]; then
  printf '%s\n' "$RESEARCH_ROOT" > "$KB_DIR/research_root"
fi

if [ -e "$PROJECT_DIR" ] && [ -n "$(ls -A "$PROJECT_DIR" 2>/dev/null || true)" ]; then
  echo "error: project directory already exists and is not empty: $PROJECT_DIR" >&2
  exit 2
fi

mkdir -p "$PROJECT_DIR"/{code,writings,experiments,notes,blog,publication/arxiv,publication/anon}
mkdir -p "$PROJECT_DIR"/.rx/{questions,evidence,claims,experiments,notes/papers,reviews,plan}

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

TOPIC_LINE=""
if [ -n "$TOPIC" ]; then
  TOPIC_LINE="- Topic: \`$TOPIC\`"
fi

cat > "$PROJECT_DIR/PROJECT.md" <<EOF
# $PROJECT_NAME

Research project bootstrapped by rx.

- Knowledge base: \`$KB_DIR\` (system/GPU, pitfalls, learnings, secrets-by-reference)
- Traceability state: \`.rx/state.json\`
$TOPIC_LINE
- Status: active
- Layout: \`code/\`, \`writings/\`, \`experiments/\`, \`publication/<venue>/\`
- Publication folders: \`publication/arxiv/\` (preprint) and \`publication/anon/\` (double-blind)

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

# Best-effort: refresh the research catalog if present
CATALOG_SCRIPT="$RESEARCH_ROOT/scripts/refresh_catalog.py"
if [ -f "$CATALOG_SCRIPT" ] && command -v python3 >/dev/null 2>&1; then
  python3 "$CATALOG_SCRIPT" --root "$RESEARCH_ROOT" >/dev/null 2>&1 || true
fi

echo "Project ready at $PROJECT_DIR"
if [ -n "$TOPIC" ]; then
  echo "Topic: $TOPIC"
fi
echo "Research root: $RESEARCH_ROOT"
