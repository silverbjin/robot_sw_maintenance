#!/usr/bin/env bash
set -u

if ! command -v ros2 >/dev/null 2>&1; then
  echo "UNAVAILABLE: ROS 2 runtime is not available; final runtime verification was not executed." >&2
  exit 2
fi

fail=0
pass() { echo "PASS: $*"; }
fail_check() { echo "FAIL: $*"; fail=1; }

nodes=$(ros2 node list 2>&1) || nodes=""
grep -qx '/lidar_node' <<<"$nodes" && pass "lidar_node is running" || fail_check "lidar_node is missing"
grep -qx '/navigation_scan_monitor' <<<"$nodes" && pass "navigation_scan_monitor is running" || fail_check "navigation_scan_monitor is missing"

info=$(ros2 topic info /lidar/scan -v 2>&1) || info=""
grep -Eq 'Publisher count:[[:space:]]*1' <<<"$info" && pass "/lidar/scan publisher count = 1" || fail_check "/lidar/scan publisher count is not 1"
grep -Eq 'Subscription count:[[:space:]]*1' <<<"$info" && pass "/lidar/scan subscriber count = 1" || fail_check "/lidar/scan subscriber count is not 1"

if timeout 5s ros2 topic echo /lidar/scan --once >/tmp/lab07_scan_once.$$ 2>&1; then
  pass "LaserScan message received"
else
  fail_check "LaserScan message not received within 5 seconds"
fi
rm -f /tmp/lab07_scan_once.$$

hz_output=$(timeout 4s ros2 topic hz /lidar/scan 2>&1 || true)
if grep -Eq 'average rate:[[:space:]]*[0-9]+' <<<"$hz_output"; then
  rate=$(sed -nE 's/.*average rate:[[:space:]]*([0-9.]+).*/\1/p' <<<"$hz_output" | tail -1)
  if python3 - "$rate" <<'PY'
import sys
rate=float(sys.argv[1])
raise SystemExit(0 if 8.0 <= rate <= 12.0 else 1)
PY
  then
    pass "LaserScan frequency is approximately 10 Hz (${rate} Hz)"
  else
    fail_check "LaserScan frequency outside expected 8-12 Hz window (${rate} Hz)"
  fi
else
  fail_check "Could not measure LaserScan frequency"
fi

if [[ $fail -eq 0 ]]; then
  echo "FINAL: PASS"
  exit 0
fi
echo "FINAL: FAIL"
exit 1
