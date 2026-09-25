#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-$HOME/myagv_tcp_gateway}"
ROS_SETUP="/opt/ros/galactic/setup.bash"

if [[ ! -f "$ROS_SETUP" ]]; then
  echo "ERROR: ROS 2 Galactic setup not found: $ROS_SETUP" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ROS_SETUP"
if [[ "${ROS_DISTRO:-}" != "galactic" ]]; then
  echo "ERROR: expected ROS_DISTRO=galactic, got ${ROS_DISTRO:-<unset>}" >&2
  exit 1
fi
python3 -c 'import rclpy' >/dev/null

mkdir -p "$DEST"
if [[ "$(readlink -f "$SOURCE_ROOT")" != "$(readlink -f "$DEST")" ]]; then
  for item in common jetson desktop tools scripts systemd config docs README.md INSTALL_GUIDE.md STUDENT_LAB.md; do
    if [[ -e "$SOURCE_ROOT/$item" ]]; then
      cp -a "$SOURCE_ROOT/$item" "$DEST/"
    fi
  done
fi

mkdir -p "$DEST/logs"
if [[ ! -f "$DEST/config/jetson.env" ]]; then
  cp "$DEST/config/jetson.env.example" "$DEST/config/jetson.env"
  echo "Created $DEST/config/jetson.env from example."
else
  echo "Keeping existing $DEST/config/jetson.env"
fi
chmod +x "$DEST"/scripts/*.sh "$DEST"/jetson/*.py "$DEST"/desktop/*.py "$DEST"/tools/*.py

MYAGV_WS="${MYAGV_WS:-$HOME/myagv_ros2}"
if [[ ! -f "$MYAGV_WS/install/local_setup.bash" ]]; then
  echo "WARNING: manufacturer workspace setup not found at $MYAGV_WS/install/local_setup.bash"
  echo "         Install/build myagv_ros2 galactic-JN before hardware operation."
fi

cat <<EOF
Jetson gateway installed at: $DEST

Next:
  1) Edit: $DEST/config/jetson.env
  2) Start manufacturer drivers in a separate terminal.
  3) Run: $DEST/scripts/start_jetson.sh
  4) Run: $DEST/scripts/verify_jetson.sh

The installer did NOT modify the manufacturer myagv_ros2 workspace.
EOF
