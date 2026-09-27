#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$SCRIPT_DIR/../ros2_ws" && pwd)"
source /opt/ros/humble/setup.bash
cd "$WS"
colcon build --symlink-install
printf '\n[OK] Build complete. Next: source %s/install/setup.bash\n' "$WS"
