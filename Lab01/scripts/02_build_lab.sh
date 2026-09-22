#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
LAB_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
WS="$LAB_ROOT/maintenance_demo_ws"

set +u
source /opt/ros/humble/setup.bash
set -u

cd "$WS"
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble || true
colcon build --symlink-install

set +u
source "$WS/install/setup.bash"
set -u

if ! grep -qxF "source $WS/install/setup.bash" "$HOME/.bashrc"; then
  echo "source $WS/install/setup.bash" >> "$HOME/.bashrc"
fi

echo "[PASS] Workspace built: $WS"
echo "Next: ros2 launch maintenance_fortress_demo base_demo.launch.py"
