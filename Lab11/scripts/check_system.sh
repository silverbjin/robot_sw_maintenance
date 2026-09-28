#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
source_ros

section() { printf '\n===== %s =====\n' "$1"; }

section "Node"
ros2 node list || true

section "Topic"
ros2 topic list || true

section "/scan info"
ros2 topic info /scan -v || true

section "/scan rate (5 sec)"
timeout 5 ros2 topic hz /scan || true

section "Memory"
free -h || true

section "Disk"
df -h / || true
