# Ogre-Next WSLg Patch 정보

## 문제 요약

WSLg / Mesa D3D12 환경에서 Gazebo Fortress의 Ogre2를 실행할 때 다음 예외가 발생할 수 있습니다.

```text
Ogre::UnimplementedException
GL3PlusTextureGpu::copyTo
```

문제가 확인된 환경에서는 OpenGL extension 상태가 다음과 같았습니다.

```text
GL_ARB_copy_image : unavailable
GL_NV_copy_image  : available
```

Ubuntu 22.04의 Ogre-Next 2.2.5는 이 조건에서 필요한 NVIDIA extension fallback을 사용하지 않아 `copyTo()` 경로에서 예외가 발생할 수 있습니다.

## 적용 원칙

이 실습 환경에서는 Ogre 2.3 전체를 설치하지 않습니다.

```text
Gazebo Fortress
  ↓
Ogre-Next 2.2.5 유지
  ↓
GL_NV_copy_image fallback만 backport
  ↓
Mesa D3D12 / WSLg
```

목적은 Gazebo Fortress가 기대하는 Ogre 2.2.5 ABI를 유지하면서 WSLg에서 필요한 texture-copy fallback만 보완하는 것입니다.

## 설치 확인

```bash
strings /usr/lib/x86_64-linux-gnu/OGRE-Next/RenderSystem_GL3Plus.so \
  | grep glCopyImageSubDataNV
```

다음 문자열이 출력되면 patched renderer가 설치된 것입니다.

```text
glCopyImageSubDataNV
```

## Upstream 참고

- Ogre-Next upstream fix: `GL3Plus: If GL_ARB_copy_image is not available, use GL_NV_copy_image`
- Commit: `e438c809835542cfaa47cb3111cff52ad7a5f912`
- Source: https://github.com/OGRECave/ogre-next/commit/e438c809835542cfaa47cb3111cff52ad7a5f912

학생 실습에서는 upstream patch 적용 및 Ogre source build 과정을 수행하지 않습니다. 강사가 미리 빌드한 `.deb`를 설치합니다.
