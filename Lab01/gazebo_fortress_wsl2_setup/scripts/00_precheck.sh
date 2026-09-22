#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo " Gazebo Fortress WSL2 Pre-check"
echo "========================================"

echo
echo "[1/6] Ubuntu"
if command -v lsb_release >/dev/null 2>&1; then
    lsb_release -ds
else
    grep '^PRETTY_NAME=' /etc/os-release || true
fi

. /etc/os-release
if [[ "${VERSION_ID:-}" != "22.04" ]]; then
    echo "WARNING: 이 배포본은 Ubuntu 22.04 기준입니다. 현재: ${VERSION_ID:-unknown}"
fi

echo
echo "[2/6] Architecture"
ARCH="$(dpkg --print-architecture)"
echo "Architecture: $ARCH"
if [[ "$ARCH" != "amd64" ]]; then
    echo "FAIL: amd64 환경이 아닙니다."
    exit 1
fi

echo
echo "[3/6] Gazebo"
if ! command -v ign >/dev/null 2>&1; then
    echo "FAIL: ign 명령을 찾을 수 없습니다."
    exit 1
fi
ign gazebo --version || true

echo
echo "[4/6] Ogre-Next"
if ! dpkg-query -W -f='${Status}\n' libogrenextmain2.2.5 2>/dev/null | grep -q 'install ok installed'; then
    echo "FAIL: libogrenextmain2.2.5가 설치되어 있지 않습니다."
    exit 1
fi
dpkg-query -W -f='${Package} ${Version}\n' libogrenextmain2.2.5

echo
echo "[5/6] glxinfo"
if ! command -v glxinfo >/dev/null 2>&1; then
    echo "FAIL: glxinfo가 없습니다."
    echo "설치: sudo apt install mesa-utils"
    exit 1
fi
glxinfo -B | grep -E 'Device|OpenGL renderer|OpenGL version' || true

echo
echo "[6/6] WSLg-related OpenGL extensions"
glxinfo | grep -E 'GL_ARB_copy_image|GL_NV_copy_image' || true

echo
echo "PASS: 기본 환경 확인 완료"
