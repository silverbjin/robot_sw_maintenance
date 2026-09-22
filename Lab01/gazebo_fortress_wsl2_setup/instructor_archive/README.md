# Instructor Archive

이 디렉터리는 학생 실습용이 아니라 강사의 재현성 / 감사(audit) 기록을 위한 공간입니다.

학생에게는 일반적으로 이 디렉터리를 배포할 필요가 없습니다.

## 권장 보관 자료

현재 강사 빌드 디렉터리 `~/ogre_wslg_fix`에서 다음 실제 파일을 보관하는 것을 권장합니다.

```text
backup/RenderSystem_GL3Plus.so
ogre-next_2.2.5+dfsg3-0ubuntu2_amd64.buildinfo
ogre-next_2.2.5+dfsg3-0ubuntu2_amd64.changes
```

또한 upstream patch는 바이너리 배포본에 복사하지 않고 원본 commit URL과 commit SHA를 기록하는 것을 권장합니다.

```text
Commit: e438c809835542cfaa47cb3111cff52ad7a5f912
URL: https://github.com/OGRECave/ogre-next/commit/e438c809835542cfaa47cb3111cff52ad7a5f912
```

## 자동 수집

```bash
./collect_build_artifacts.sh ~/ogre_wslg_fix
```

이 스크립트는 사용자의 실제 빌드 결과물을 이 디렉터리의 `collected/` 아래에 복사합니다.
