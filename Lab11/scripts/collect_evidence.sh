#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
source_ros

LABEL="${1:-snapshot}"
TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="$ROOT_DIR/student/evidence"
OUT_FILE="$OUT_DIR/${TS}_${LABEL}.txt"
mkdir -p "$OUT_DIR"

{
  echo "Lab11 Evidence"
  echo "timestamp: $(date --iso-8601=seconds)"
  echo "label: $LABEL"
  echo
  echo "===== ros2 node list ====="
  ros2 node list || true
  echo
  echo "===== ros2 topic list ====="
  ros2 topic list || true
  echo
  echo "===== ros2 topic info /scan -v ====="
  ros2 topic info /scan -v || true
  echo
  echo "===== ros2 topic hz /scan (5 sec) ====="
  timeout 5 ros2 topic hz /scan || true
  echo
  echo "===== free -h ====="
  free -h || true
  echo
  echo "===== df -h / ====="
  df -h / || true
} > "$OUT_FILE" 2>&1

echo "[OK] Evidence saved: $OUT_FILE"
