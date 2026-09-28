#!/usr/bin/env bash
set -euo pipefail
# Run locally on myAGV_JN_2023. This script does not bridge Galactic to Humble.
source /opt/ros/galactic/setup.bash
if [[ -n "${MYAGV_WS_SETUP:-}" && -f "$MYAGV_WS_SETUP" ]]; then source "$MYAGV_WS_SETUP"; fi
echo "=== environment ==="
echo "ROS_DISTRO=${ROS_DISTRO:-unset}"
uname -a
echo "=== nodes ==="
ros2 node list | sort
echo "=== topics ==="
ros2 topic list | sort
echo "=== note ==="
echo "Record observations only. Do not change packages/settings during this Lab08 exercise."
