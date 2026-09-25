#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-$HOME/myagv_tcp_gateway}"
ROS_SETUP="/opt/ros/humble/setup.bash"

if [[ ! -f "$ROS_SETUP" ]]; then
  echo "ERROR: ROS 2 Humble setup not found: $ROS_SETUP" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ROS_SETUP"
if [[ "${ROS_DISTRO:-}" != "humble" ]]; then
  echo "ERROR: expected ROS_DISTRO=humble, got ${ROS_DISTRO:-<unset>}" >&2
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
if [[ ! -f "$DEST/config/desktop.env" ]]; then
  cp "$DEST/config/desktop.env.example" "$DEST/config/desktop.env"
  echo "Created $DEST/config/desktop.env from example."
else
  echo "Keeping existing $DEST/config/desktop.env"
fi
chmod +x "$DEST"/scripts/*.sh "$DEST"/jetson/*.py "$DEST"/desktop/*.py "$DEST"/tools/*.py

cat <<EOF
Desktop gateway installed at: $DEST

Next:
  1) Edit ROBOT_IP in: $DEST/config/desktop.env
  2) Confirm Jetson gateway is running.
  3) Run: $DEST/scripts/start_desktop.sh
  4) Run: $DEST/scripts/verify_desktop.sh
EOF
