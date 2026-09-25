#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="${LAB05_WS:-$HOME/lab05_ros2_ws}"
mkdir -p "$WS/src"
if [[ -d "$WS/src/myagv_bringup" ]]; then
  if [[ -d "$WS/.git" ]]; then
    dirty="$(git -C "$WS" status --porcelain -- src/myagv_bringup || true)"
    if [[ -n "$dirty" && "${LAB05_RESET:-0}" != "1" ]]; then
      echo "ERROR: existing lab workspace has changes under src/myagv_bringup." >&2
      echo "Refusing to overwrite learner work. Move/backup the workspace, or set LAB05_RESET=1 intentionally." >&2
      exit 3
    fi
  elif [[ "${LAB05_RESET:-0}" != "1" ]]; then
    echo "ERROR: unmanaged existing src/myagv_bringup found at $WS." >&2
    echo "Refusing to overwrite it. Move/backup it, or set LAB05_RESET=1 intentionally." >&2
    exit 3
  fi
fi
rm -rf "$WS/src/myagv_bringup"
cp -a "$ROOT/src/myagv_bringup" "$WS/src/"
cd "$WS"
if [[ ! -d .git ]]; then
  git init -b main >/dev/null
fi
cat > .gitignore <<'EOF'
build/
install/
log/
results/
EOF
# Avoid mutating the learner's global Git configuration.
git add .gitignore src/myagv_bringup
if ! git diff --cached --quiet; then
  git -c user.name='Course Instructor' -c user.email='instructor@example.invalid' \
    commit -m 'Session 5 stable baseline' >/dev/null
fi
if ! git rev-parse -q --verify refs/tags/pre-upgrade-v1 >/dev/null; then
  git -c user.name='Course Instructor' -c user.email='instructor@example.invalid' \
    tag -a pre-upgrade-v1 -m 'Stable baseline before upgrade'
fi
printf 'Workspace: %s\n' "$WS"
printf 'Baseline tag: pre-upgrade-v1\n'
printf 'No package installation, firmware change, or motor command was performed.\n'
