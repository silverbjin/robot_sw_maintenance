#!/usr/bin/env bash
set -u
fail=0
for cmd in ros2 colcon ign python3; do
  if command -v "$cmd" >/dev/null 2>&1; then echo "[OK] $cmd: $(command -v "$cmd")"; else echo "[MISSING] $cmd"; fail=1; fi
done
printf '[INFO] ROS_DISTRO=%s\n' "${ROS_DISTRO:-<unset>}"
if [[ "${ROS_DISTRO:-}" != "humble" ]]; then echo "[WARN] Desktop demo is designed for ROS 2 Humble."; fi
if [[ -f /etc/os-release ]]; then . /etc/os-release; echo "[INFO] OS=${PRETTY_NAME:-unknown}"; fi
exit "$fail"
