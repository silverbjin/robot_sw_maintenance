#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
source_ros

cd "$WS_DIR"
echo "[BUILD] maintenance_lidar_demo"
colcon build --symlink-install --packages-select maintenance_lidar_demo

echo
printf '[OK] Build complete. Next: bash %q\n' "$ROOT_DIR/scripts/start_demo.sh"
