#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo " WSLg GPU Check"
echo "========================================"

if ! command -v glxinfo >/dev/null 2>&1; then
    echo "FAIL: glxinfo가 없습니다."
    echo "설치: sudo apt install mesa-utils"
    exit 1
fi

echo
echo "[1/3] Current renderer"
glxinfo -B | grep -E 'Device|OpenGL renderer|OpenGL version' || true

echo
echo "[2/3] NVIDIA forced renderer"
MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA glxinfo -B \
  | grep -E 'Device|OpenGL renderer|OpenGL version'

echo
echo "[3/3] Verify NVIDIA selection"
RENDERER="$(MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA glxinfo -B | grep 'OpenGL renderer string' || true)"
if echo "$RENDERER" | grep -qi 'NVIDIA'; then
    echo "PASS: NVIDIA adapter 선택 성공"
else
    echo "FAIL: NVIDIA adapter가 선택되지 않았습니다."
    echo "$RENDERER"
    echo
    echo "Windows에 NVIDIA GPU가 존재하고 WSLg에서 노출되는지 확인하십시오."
    exit 1
fi
