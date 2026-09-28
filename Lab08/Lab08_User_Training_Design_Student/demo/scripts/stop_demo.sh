#!/usr/bin/env bash
set -euo pipefail
pkill -f 'lab08_training_demo.*training_component' 2>/dev/null || true
pkill -f 'ros2 launch lab08_training_demo training_demo.launch.py' 2>/dev/null || true
echo '[OK] Lab08 ROS 2 demo stop signal sent.'
