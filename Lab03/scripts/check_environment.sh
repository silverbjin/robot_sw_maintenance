#!/usr/bin/env bash
set -u

echo "=== Lab03 ROS 2 Humble Environment Check ==="
echo

echo "[1] OS"
if command -v lsb_release >/dev/null 2>&1; then
  lsb_release -ds
  lsb_release -cs
else
  grep -E 'PRETTY_NAME|VERSION_CODENAME' /etc/os-release || true
fi

echo
echo "[2] Architecture"
uname -m

echo
echo "[3] ROS install path"
if [ -d /opt/ros/humble ]; then
  echo "PASS: /opt/ros/humble exists"
else
  echo "FAIL: /opt/ros/humble not found"
fi

echo
echo "[4] setup.bash"
if [ -f /opt/ros/humble/setup.bash ]; then
  echo "PASS: /opt/ros/humble/setup.bash exists"
else
  echo "FAIL: setup.bash not found"
fi

echo
echo "[5] Current ROS_DISTRO"
echo "${ROS_DISTRO:-<not set>}"

echo
echo "[6] ros2"
if command -v ros2 >/dev/null 2>&1; then
  echo "PASS: $(command -v ros2)"
else
  echo "INFO: ros2 not visible in current shell"
  echo "Try: source /opt/ros/humble/setup.bash"
fi

echo
echo "[7] colcon"
command -v colcon || true

echo
echo "[8] rosdep"
command -v rosdep || true
