#!/usr/bin/env bash
set -euo pipefail
SCENARIO="${1:-normal}"
case "$SCENARIO" in normal|missing_sensor) ;; *) echo "usage: $0 normal|missing_sensor" >&2; exit 2;; esac
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUT_BASE="${2:-$ROOT/student/evidence/runs}"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="$OUT_BASE/${STAMP}_${SCENARIO}"
mkdir -p "$OUT"
{
  echo "timestamp=$(date -Iseconds)"
  echo "scenario=$SCENARIO"
  echo "ROS_DISTRO=${ROS_DISTRO:-unset}"
  echo "uname=$(uname -a)"
} > "$OUT/environment.txt"
ros2 node list | sort > "$OUT/node_list.txt"
python3 "$ROOT/tools/analyze_node_list.py" --input "$OUT/node_list.txt" --scenario "$SCENARIO" --json-out "$OUT/analysis.json"
echo "[OK] Evidence: $OUT"
