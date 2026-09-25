#!/usr/bin/env bash
set -euo pipefail
PIDS="$(pgrep -f '[j]etson_gateway.py|[d]esktop_gateway.py' || true)"
if [[ -z "$PIDS" ]]; then
  echo "No gateway process running."
  exit 0
fi
echo "Sending SIGTERM to gateway PID(s): $PIDS"
# shellcheck disable=SC2086
kill -TERM $PIDS
for _ in $(seq 1 20); do
  sleep 0.1
  if ! pgrep -f '[j]etson_gateway.py|[d]esktop_gateway.py' >/dev/null; then
    echo "Gateway stopped."
    exit 0
  fi
done
echo "WARNING: gateway process still present after 2 seconds." >&2
exit 1
