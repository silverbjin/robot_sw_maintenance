#!/usr/bin/env bash
# 이 파일은 실행(./env_gazebo.sh)하지 말고 source 하십시오.
#   source scripts/env_gazebo.sh

export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
unset LIBGL_ALWAYS_SOFTWARE || true
unset LIBGL_DRI3_DISABLE || true
unset MESA_GL_VERSION_OVERRIDE || true
unset QT_QPA_PLATFORM || true

echo "Gazebo WSLg environment loaded."
echo "MESA_D3D12_DEFAULT_ADAPTER_NAME=$MESA_D3D12_DEFAULT_ADAPTER_NAME"
