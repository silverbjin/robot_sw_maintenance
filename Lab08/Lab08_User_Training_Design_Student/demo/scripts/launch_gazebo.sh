#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORLD="$(cd "$SCRIPT_DIR/../gazebo/worlds" && pwd)/training_world.sdf"
if ! command -v ign >/dev/null 2>&1; then echo '[ERROR] ign command not found. Install/configure Gazebo Fortress first.' >&2; exit 2; fi
exec ign gazebo -r "$WORLD"
