#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <evidence-session-directory>" >&2
  exit 2
fi
session_dir="$1"
if [[ ! -d "$session_dir" ]]; then
  echo "ERROR: evidence directory not found: $session_dir" >&2
  exit 3
fi
if [[ ! -f "$session_dir/SHA256SUMS" ]]; then
  echo "ERROR: SHA256SUMS not found: $session_dir" >&2
  exit 4
fi
(
  cd "$session_dir"
  sha256sum -c SHA256SUMS
)
