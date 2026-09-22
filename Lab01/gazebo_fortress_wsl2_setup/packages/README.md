# Packages

이 디렉터리에는 강사가 미리 빌드한 patched Ogre runtime package를 배치합니다.

## 필요한 파일

```text
libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb
```

이 파일은 본 생성물에 의도적으로 포함되어 있지 않습니다.

강사 PC에서 복사:

```bash
cp ~/ogre_wslg_fix/libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb \
  gazebo_fortress_wsl2_setup/packages/
```

그 다음 상위 디렉터리에서:

```bash
./scripts/99_prepare_distribution.sh
```

을 실행하여 `SHA256SUMS`를 갱신하십시오.

## 학생 배포에 포함하지 않는 빌드 산출물

다음 파일은 이번 runtime patch 설치에 필요하지 않습니다.

```text
libogre-next-dev_*.deb
libogrenexthlmspbs2.2.5_*.deb
libogrenexthlmsunlit2.2.5_*.deb
libogrenextmeshlodgenerator2.2.5_*.deb
libogrenextoverlay2.2.5_*.deb
libogrenextplanarreflections2.2.5_*.deb
libogrenextsceneformat2.2.5_*.deb
*.ddeb
ogre-next-tools_*.deb
ogre-next-doc_*.deb
blender-ogrexml-next_*.deb
```
