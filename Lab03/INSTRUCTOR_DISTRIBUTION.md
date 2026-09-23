# 강사용 배포 안내

## 배포 파일

학생에게 다음 폴더를 그대로 제공합니다.

```text
provided_files/
└── maintenance_check_pkg/
```

학생은 코드를 작성하거나 수정하지 않습니다.

## 학생 배치 위치

```bash
mkdir -p ~/robot_ws/src
cp -r maintenance_check_pkg ~/robot_ws/src/
```

또는 압축 파일을 풀어 다음 구조가 되도록 합니다.

```text
~/robot_ws/src/maintenance_check_pkg/package.xml
~/robot_ws/src/maintenance_check_pkg/setup.py
~/robot_ws/src/maintenance_check_pkg/setup.cfg
~/robot_ws/src/maintenance_check_pkg/maintenance_check_pkg/status_node.py
```

## 강의 목적

이 패키지는 코딩 실습용이 아니라 다음 검증을 위한 도구입니다.

1. `colcon`이 프로젝트 패키지를 인식하는가?
2. 패키지를 정상적으로 빌드할 수 있는가?
3. `install/setup.bash`를 Overlay로 적용할 수 있는가?
4. 현재 터미널에서 패키지를 검색할 수 있는가?
5. 환경 설정 오류를 재현하고 복구할 수 있는가?
