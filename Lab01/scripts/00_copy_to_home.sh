#!/usr/bin/env bash
set -euo pipefail
SRC=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
DST="$HOME/ros2_humble_fortress_lidar_lab"
if [ "$SRC" = "$DST" ]; then echo "Already in $DST"; exit 0; fi
mkdir -p "$DST"
cp -a "$SRC/." "$DST/"
echo "Copied to $DST"
