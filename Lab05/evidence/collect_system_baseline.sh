#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="${RESULTS_DIR:-$ROOT/results/$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$RESULTS_DIR"
OUT="$RESULTS_DIR/01_system_baseline.txt"
{
  echo '=== SYSTEM BASELINE ==='
  echo "timestamp=$(date -Is)"
  echo "hostname=$(hostname)"
  echo "architecture=$(uname -m)"
  echo
  echo '[OS]'
  if command -v lsb_release >/dev/null 2>&1; then
    lsb_release -a 2>/dev/null || true
  elif [[ -r /etc/os-release ]]; then
    cat /etc/os-release
  else
    echo 'NOT_AVAILABLE: OS release information'
  fi
  echo
  echo '[Jetson Linux]'
  if [[ -r /etc/nv_tegra_release ]]; then
    cat /etc/nv_tegra_release
  else
    echo 'NOT_AVAILABLE: /etc/nv_tegra_release'
  fi
  echo
  echo '[JetPack meta package]'
  if command -v apt >/dev/null 2>&1; then
    line="$(apt list --installed 2>/dev/null | grep '^nvidia-jetpack/' || true)"
    if [[ -n "$line" ]]; then echo "$line"; else echo 'NOT_FOUND: nvidia-jetpack meta package'; fi
  else
    echo 'NOT_AVAILABLE: apt command'
  fi
} > "$OUT"
cat "$OUT"
echo "Saved: $OUT" >&2
