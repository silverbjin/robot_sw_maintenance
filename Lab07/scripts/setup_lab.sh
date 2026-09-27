#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

if ! command -v ros2 >/dev/null 2>&1 && [[ -f /opt/ros/humble/setup.bash ]]; then
  # shellcheck disable=SC1091
  source /opt/ros/humble/setup.bash
fi

if ! command -v ros2 >/dev/null 2>&1; then
  echo "ERROR: ROS 2 CLI not found. Install/source ROS 2 Humble before setup." >&2
  exit 2
fi
if [[ "${ROS_DISTRO:-}" != "humble" ]]; then
  echo "ERROR: expected ROS_DISTRO=humble, got '${ROS_DISTRO:-unset}'." >&2
  exit 3
fi
if ! command -v colcon >/dev/null 2>&1; then
  echo "ERROR: colcon not found. Install colcon before setup." >&2
  exit 4
fi

cd "$ROOT/ros2_ws"
colcon build --symlink-install
cat <<EOF
LAB-07 workspace build complete.
Next terminal steps:
  source /opt/ros/humble/setup.bash
  source "$ROOT/ros2_ws/install/setup.bash"
  cd "$ROOT"
EOF
