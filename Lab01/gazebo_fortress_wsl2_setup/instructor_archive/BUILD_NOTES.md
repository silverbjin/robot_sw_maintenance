# Ogre WSLg Patch Build Record

## Baseline

- Host: Windows 11 + WSL2 / WSLg
- Guest: Ubuntu 22.04
- ROS: ROS 2 Humble
- Gazebo: Fortress / Ignition Gazebo 6.18.x
- Rendering: Ogre2
- Ogre-Next baseline: `2.2.5+dfsg3-0ubuntu2`
- GPU path: Mesa D3D12

## Original failure

```text
Ogre::UnimplementedException
GL3PlusTextureGpu::copyTo
```

## OpenGL capability observed during diagnosis

```text
GL_ARB_copy_image : unavailable
GL_NV_copy_image  : available
```

## Resolution

Ogre-Next 2.2.5 ABI를 유지하면서 upstream의 `GL_NV_copy_image` fallback 수정만 backport.

Upstream reference:

```text
Commit: e438c809835542cfaa47cb3111cff52ad7a5f912
Subject: GL3Plus: If GL_ARB_copy_image is not available, use GL_NV_copy_image
```

## Verification

```bash
strings /usr/lib/x86_64-linux-gnu/OGRE-Next/RenderSystem_GL3Plus.so \
  | grep glCopyImageSubDataNV
```

그리고:

```bash
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
ign gazebo -v 4 shapes.sdf
```

정상 결과:

```text
Gazebo Ogre2 GUI PASS
GL3PlusTextureGpu::copyTo crash 없음
```

## Project-specific GUI issue

실제 project world에서는 SDF 내부 GUI configuration 때문에 회색 빈 GUI가 나타날 수 있었으며, 다음 방식으로 정상 GUI config를 강제하여 해결함.

```text
--gui-config ~/.ignition/gazebo/6/gui.config
```

ROS 2 Python launch에서는 `~` 대신 `Path.home()`으로 절대 경로를 구성해야 함.

## Distributed runtime package

학생에게 배포할 실제 파일:

```text
libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb
```

이 저장소에는 해당 `.deb`를 포함하지 않으며, 강사가 별도로 `packages/`에 복사한 뒤 SHA-256을 생성합니다.
