#!/usr/bin/env bash
set -euo pipefail

KB_DIR="${1:-$HOME/.rx-kb}"
mkdir -p "$KB_DIR"/{system,secrets,pitfalls,learnings,env}

# gitignore secrets
if ! grep -qxF "secrets/" "$KB_DIR/.gitignore" 2>/dev/null; then
  echo "secrets/" >> "$KB_DIR/.gitignore"
fi

# capture system + GPU info (best-effort; never fail the script)
SYS="$KB_DIR/system/system.md"
{
  echo "# System info"
  echo
  echo "Captured: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "## GPU"
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null || echo "nvidia-smi query failed"
  else
    echo "no nvidia-smi found"
  fi
  echo
  echo "## CPU / RAM"
  echo "cores: $(nproc 2>/dev/null || echo '?')"
  echo "mem:   $(free -h 2>/dev/null | awk '/Mem:/ {print $2}' || echo '?')"
} > "$SYS"

# manifest
if [ ! -f "$KB_DIR/index.md" ]; then
  cat > "$KB_DIR/index.md" <<'EOF'
# RX Knowledge Base

Centralized, shared across all research projects.

- system/    — hardware & driver snapshot (GPU, CPU, RAM)
- secrets/   — API config (gitignored; referenced, never copied)
- pitfalls/  — shareable mistakes & gotchas
- learnings/ — reusable techniques that worked
- env/       — shared uv cache config
EOF
fi

echo "KB ready at $KB_DIR"
