#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Gateway processes ==="
pgrep -af '[j]etson_gateway.py|[d]esktop_gateway.py' || echo "No gateway process found."
echo
echo "=== Listening TCP sockets ==="
ss -lntp 2>/dev/null | grep -E '(:5000|python)' || true
echo
echo "=== Configuration files ==="
for f in "$ROOT/config/jetson.env" "$ROOT/config/desktop.env"; do
  [[ -f "$f" ]] && echo "$f" || true
done
