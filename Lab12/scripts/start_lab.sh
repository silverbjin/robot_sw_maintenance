#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/common.sh"
source_ros

if [ ! -f "$WS/install/setup.bash" ]; then
  echo "[ERROR] Workspace not built. Run: bash scripts/prepare_lab.sh" >&2
  exit 1
fi

echo "[INFO] Starting Lab12 recovered runtime. Press Ctrl+C to stop."
exec ros2 launch lab12_maintenance_demo lab12_demo.launch.py
