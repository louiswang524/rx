#!/usr/bin/env bash
# Resolve the canonical research root for new RX projects.
# Preference order:
#   1. RX_RESEARCH_ROOT env
#   2. $KB_DIR/research_root file (written by kb-init / first bootstrap)
#   3. Existing candidate directories
#   4. $HOME/research
set -euo pipefail

KB_DIR="${1:-${RX_KB_DIR:-$HOME/.rx-kb}}"

if [ -n "${RX_RESEARCH_ROOT:-}" ]; then
  printf '%s\n' "$RX_RESEARCH_ROOT"
  exit 0
fi

if [ -f "$KB_DIR/research_root" ]; then
  root="$(tr -d '\r\n' < "$KB_DIR/research_root")"
  if [ -n "$root" ]; then
    printf '%s\n' "$root"
    exit 0
  fi
fi

user="${USER:-louis}"
for candidate in \
  "$HOME/research" \
  "/mnt/c/Users/${user}/research" \
  "/mnt/c/Users/louis/research" \
  "/c/Users/${user}/research" \
  "/c/Users/louis/research"
do
  if [ -d "$candidate" ]; then
    printf '%s\n' "$candidate"
    exit 0
  fi
done

printf '%s\n' "$HOME/research"
