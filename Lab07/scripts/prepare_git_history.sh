#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$ROOT"
ACTIVE="ros2_ws/src/maintenance_lidar_demo/config/lab_active.yaml"
V12="ros2_ws/src/maintenance_lidar_demo/config/v12_baseline.yaml"
V13="ros2_ws/src/maintenance_lidar_demo/config/v13_broken.yaml"
IDENTITY=(-c user.name='LAB-07 Instructor' -c user.email='lab07@example.invalid')

for file in "$V12" "$V13"; do
  [[ -f "$file" ]] || { echo "ERROR: missing template $file" >&2; exit 5; }
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b main >/dev/null
  git add -A
  git "${IDENTITY[@]}" commit -m 'lab: imported training package' >/dev/null
  echo "Initialized LAB-07 Git repository from the distributed package."
else
  TOP=$(git rev-parse --show-toplevel)
  [[ "$TOP" == "$ROOT" ]] || { echo "ERROR: script must run from its own LAB-07 repository." >&2; exit 2; }
fi

if git rev-parse -q --verify refs/tags/v1.2 >/dev/null || git rev-parse -q --verify refs/tags/v1.3 >/dev/null; then
  echo "ERROR: v1.2 or v1.3 tags already exist. Refusing to rebuild history." >&2
  exit 3
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: prepare_git_history.sh requires a clean worktree. Commit/stash unrelated work first." >&2
  exit 4
fi

sync_installed_config() {
  local installed="$ROOT/ros2_ws/install/maintenance_lidar_demo/share/maintenance_lidar_demo/config/lab_active.yaml"
  if [[ -e "$installed" ]]; then
    local src_real dst_real
    src_real=$(readlink -f "$ACTIVE")
    dst_real=$(readlink -f "$installed")
    if [[ "$src_real" != "$dst_real" ]]; then
      cp "$ACTIVE" "$installed"
    fi
  fi
}

cp "$V12" "$ACTIVE"
git add "$ACTIVE"
git "${IDENTITY[@]}" commit -m 'lab: baseline configuration v1.2' >/dev/null
git "${IDENTITY[@]}" tag -a v1.2 -m 'LAB-07 baseline v1.2'

cp "$V13" "$ACTIVE"
git add "$ACTIVE"
git "${IDENTITY[@]}" commit -m 'lab: upgrade lidar publisher topic' >/dev/null
git "${IDENTITY[@]}" tag -a v1.3 -m 'LAB-07 broken upgrade v1.3'
sync_installed_config

echo "Created deterministic training history: v1.2 -> v1.3"
echo "Current active state: broken v1.3 (publisher=/lidar/scan, subscriber=/scan)"
