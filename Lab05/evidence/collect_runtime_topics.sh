#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="${RESULTS_DIR:-$ROOT/results/$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$RESULTS_DIR"
OUT="$RESULTS_DIR/04_runtime_topics.txt"
{
  echo '=== READ-ONLY ROS 2 RUNTIME SNAPSHOT ==='
  echo "timestamp=$(date -Is)"
  if command -v ros2 >/dev/null 2>&1; then
    echo '[nodes]'
    ros2 node list 2>&1 || true
    echo
    echo '[topics]'
    ros2 topic list 2>&1 || true
  else
    echo 'NOT_EXECUTED: ros2 command is not available in the current shell.'
    echo 'hint=source /opt/ros/humble/setup.bash'
  fi
} > "$OUT"
cat "$OUT"
echo "Saved: $OUT" >&2
