# ROS 2 Humble + Gazebo Fortress LiDAR 유지보수 실습

이 저장소는 **설치 자체보다 장애 관찰 → 계층별 진단 → 브리지 수정 → 재검증 → 기록**에 집중하는 실습 패키지입니다.

- Docker image: `silverbjin/ros2-humble-fortress-lab:1.0`
- Host: Windows 11 + Docker Desktop(WSL 2 backend)
- Container: Ubuntu 22.04 + ROS 2 Humble + Gazebo Fortress + RViz2 + ros_gz_bridge
- GUI: 브라우저 noVNC (`http://localhost:6080/vnc.html`)
- VNC password: `student`

## 학생 시작 순서

1. 사전에 Docker Desktop을 설치합니다: [`docs/00_DOCKER_DESKTOP_SETUP.md`](docs/00_DOCKER_DESKTOP_SETUP.md)
2. PowerShell에서 저장소 루트로 이동합니다.
3. 아래 명령을 실행합니다.

```powershell
docker pull silverbjin/ros2-humble-fortress-lab:1.0
docker compose up -d
docker compose ps
```

4. 브라우저에서 `http://localhost:6080/vnc.html`을 열고 비밀번호 `student`로 접속합니다.
5. Container Desktop에서 **Terminator**를 실행합니다.
6. 환경 확인:

```bash
ros2 run maintenance_fortress_demo check_environment.sh
```

`Environment READY`가 나오면 실습을 시작합니다.

## 실습 핵심 흐름

```text
장애 관찰
  ↓
ROS 2 /scan 확인
  ↓
Gazebo /lidar_scan 확인
  ↓
정상/비정상 경계 결정
  ↓
ros_gz_bridge 설정 비교
  ↓
브리지 수정·재시작
  ↓
/scan 메시지·주기·RViz 재검증
  ↓
유지보수 기록
```

## 문서 안내

| 문서 | 대상 | 목적 |
|---|---|---|
| [`docs/00_DOCKER_DESKTOP_SETUP.md`](docs/00_DOCKER_DESKTOP_SETUP.md) | 학생 | Docker Desktop 사전 설치 |
| [`docs/01_DOCKER_COMMAND_GUIDE.md`](docs/01_DOCKER_COMMAND_GUIDE.md) | 학생 | PowerShell / Docker 최소 명령 |
| [`docs/02_ROS2_COMMAND_GUIDE.md`](docs/02_ROS2_COMMAND_GUIDE.md) | 학생 | 실습에서 사용하는 ROS 2 / Gazebo 명령 |
| [`docs/03_SLIDE_LAB_GUIDE.md`](docs/03_SLIDE_LAB_GUIDE.md) | 학생·강사 | 슬라이드 11~16 실습 절차 |
| [`student/DIAGNOSIS_WORKSHEET.md`](student/DIAGNOSIS_WORKSHEET.md) | 학생 | 관찰 결과 기록 |
| [`docs/04_PROJECT_STRUCTURE.md`](docs/04_PROJECT_STRUCTURE.md) | 강사·개발자 | Git 저장소 구성 |
| [`docs/05_INSTRUCTOR_GUIDE.md`](docs/05_INSTRUCTOR_GUIDE.md) | 강사 | 사전 점검·시연·정답·운영 |
| [`README_BUILD_AND_PUBLISH.md`](README_BUILD_AND_PUBLISH.md) | 강사 | Docker image build/push/offline export |

## 정상/장애 판단 기준

| Gazebo `/lidar_scan` | ROS `/scan` | 우선 의심 |
|---|---|---|
| 없음 | 없음 | Gazebo sensor 계층 |
| 존재하지만 데이터 없음 | 없음 | sensor/rendering 계층 |
| **데이터 정상** | **메시지 없음** | **ros_gz_bridge 계층** |
| 데이터 정상 | 데이터 정상, RViz 미표시 | TF / QoS / RViz |
| 데이터 정상 | 데이터 정상, RViz 정상 | 복구 완료 |

> `/scan`이라는 이름이 보여도 실제 메시지가 수신되지 않으면 정상으로 판정하지 않습니다.
