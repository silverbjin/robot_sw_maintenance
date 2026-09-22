#!/usr/bin/env bash
set -euo pipefail

export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
unset LIBGL_ALWAYS_SOFTWARE || true
unset LIBGL_DRI3_DISABLE || true
unset MESA_GL_VERSION_OVERRIDE || true
unset QT_QPA_PLATFORM || true

OGRE_PLUGIN="/usr/lib/x86_64-linux-gnu/OGRE-Next/RenderSystem_GL3Plus.so"

echo "========================================"
echo " Gazebo Fortress Ogre2 Verification"
echo "========================================"

echo
echo "[1/4] Ogre patch"
if [[ ! -f "$OGRE_PLUGIN" ]]; then
    echo "FAIL: $OGRE_PLUGIN 를 찾을 수 없습니다."
    exit 1
fi
if strings "$OGRE_PLUGIN" | grep -q 'glCopyImageSubDataNV'; then
    echo "PASS: patched GL3Plus renderer detected"
else
    echo "FAIL: patched Ogre runtime이 아닙니다."
    exit 1
fi

echo
echo "[2/4] GPU"
RENDERER="$(glxinfo -B | grep 'OpenGL renderer string' || true)"
echo "$RENDERER"
if ! echo "$RENDERER" | grep -qi 'NVIDIA'; then
    echo "FAIL: NVIDIA GPU가 사용되지 않습니다."
    exit 1
fi

echo
echo "[3/4] Relevant extensions"
glxinfo | grep -E 'GL_ARB_copy_image|GL_NV_copy_image' || true

echo
echo "[4/4] Starting Gazebo shapes.sdf"
echo "확인: ground / box / sphere / cylinder, blank/flicker/crash 없음"
echo "종료: Ctrl+C"
echo
ign gazebo -v 4 shapes.sdf
