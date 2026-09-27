#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$ROOT"
ACTIVE="ros2_ws/src/maintenance_lidar_demo/config/lab_active.yaml"
git rev-parse -q --verify refs/tags/v1.3 >/dev/null || { echo "ERROR: tag v1.3 not found; run prepare_git_history.sh first." >&2; exit 3; }
git restore --source v1.3 -- "$ACTIVE"
INSTALLED="$ROOT/ros2_ws/install/maintenance_lidar_demo/share/maintenance_lidar_demo/config/lab_active.yaml"
if [[ -e "$INSTALLED" && "$(readlink -f "$ACTIVE")" != "$(readlink -f "$INSTALLED")" ]]; then cp "$ACTIVE" "$INSTALLED"; fi
echo "LAB state reset to broken v1.3."
