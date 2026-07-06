#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:?usage: kb-sync.sh <PROJECT_DIR> [KB_DIR]}"
KB_DIR="${2:-$HOME/.rx-kb}"
PREFIX="$(basename "$PROJECT_DIR")"

promote() {
  local src="$1" dst="$2"
  [ -d "$src" ] || return 0
  mkdir -p "$dst"
  shopt -s nullglob
  for f in "$src"/*; do
    [ -f "$f" ] || continue
    cp -f "$f" "$dst/${PREFIX}__$(basename "$f")"
  done
}

promote "$PROJECT_DIR/notes/pitfalls"  "$KB_DIR/pitfalls"
promote "$PROJECT_DIR/notes/learnings" "$KB_DIR/learnings"

echo "Synced notes from $PREFIX into $KB_DIR"
