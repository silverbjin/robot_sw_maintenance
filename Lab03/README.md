# 3회차 학생 배포용 실습 패키지
## ROS 2 Humble 설치와 정상 동작 검증

과정명: **지속 가능한 로봇 운영을 위한 소프트웨어 유지보수 이해**  
회차명: **3회차. 로봇 소프트웨어 설치 실습**  
기준 환경: **Ubuntu 22.04 LTS + ROS 2 Humble**

이 패키지는 3회차의 두 학습목표를 실습으로 확인하기 위한 학생 배포용 자료입니다.

1. Ubuntu 22.04 환경에 ROS 2 Humble과 관련 종속 패키지를 설치할 수 있다.
2. ROS 2 설치 오류를 점검하고 필요한 환경 변수를 설정할 수 있다.

---

# 1. 패키지 구성

```text
lab03_ros2_humble_student_package/
├── README.md
├── student/
│   ├── 03_student_workbook.md
│   └── 04_install_validation_workbook.md
├── provided_files/
│   └── maintenance_check_pkg/
│       ├── README.md
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       ├── resource/
│       │   └── maintenance_check_pkg
│       └── maintenance_check_pkg/
│           ├── __init__.py
│           └── status_node.py
├── scripts/
│   ├── check_environment.sh
│   ├── prepare_workspace.sh
│   └── verify_ros2.sh
├── evidence/
│   └── README.md
└── SHA256SUMS
```

---

# 2. 실습 진행 순서

```text
① student/03_student_workbook.md
   ROS 2 Humble 전체 설치
              ↓
② scripts/check_environment.sh
   기본 환경 점검
              ↓
③ provided_files/maintenance_check_pkg
   강사 제공 패키지 배치
              ↓
④ student/04_install_validation_workbook.md
   Build · Overlay · 통신 · 오류 복구
              ↓
⑤ evidence/
   실습 결과 캡처 저장
```

> `maintenance_check_pkg`의 소스 코드는 학생이 작성하지 않습니다.  
> 학생은 **배치 → 빌드 → Overlay 적용 → 실행 → 오류 진단**에 집중합니다.

---

# 3. 실습 1 — ROS 2 Humble 설치

다음 문서를 먼저 수행합니다.

```text
student/03_student_workbook.md
```

이 문서는 **슬라이드 6-2. ROS 2 Humble 전체 설치 따라하기**를 학생용 워크북으로 확장한 자료입니다.

주요 흐름:

```text
Ubuntu 22.04 확인
      ↓
UTF-8 Locale
      ↓
Universe 저장소
      ↓
ROS 2 apt 저장소
      ↓
apt update / upgrade
      ↓
ros-humble-desktop
      ↓
ros-dev-tools
      ↓
source / ROS_DISTRO
      ↓
Talker / Listener
```

각 단계에서 **예상 결과와 실제 결과를 비교하고 기록**합니다.

---

# 4. 실습 2 — 설치 검증과 오류 복구

설치 완료 후 다음 문서를 수행합니다.

```text
student/04_install_validation_workbook.pdf
```

슬라이드와 실습의 대응 관계:

| 실습 | 대응 슬라이드 | 내용 |
|---|---:|---|
| 실습 1 | 10 | 시연 시나리오 준비 |
| 실습 2 | 11 | 운영체제와 ROS 2 환경 확인 |
| 실습 3 | 12 | 워크스페이스 빌드와 Overlay |
| 실습 4 | 13 | Talker/Listener 통신 검증 |
| 실습 5 | 14 | 환경 설정 오류 재현·복구 |
| 실습 6 | 15 | 대표 오류 점검표 |
| 참고 | 15-2 | WSL2 / Jetson Nano 환경 준비 |

---

# 5. 보조 스크립트

실습 폴더에서 다음을 실행합니다.

```bash
chmod +x scripts/*.sh
```

환경 확인:

```bash
./scripts/check_environment.sh
```

강사 제공 패키지 자동 배치:

```bash
./scripts/prepare_workspace.sh
```

설치/Overlay 상태 확인:

```bash
./scripts/verify_ros2.sh
```

보조 스크립트는 실습 절차를 대신하지 않으며, 학생이 수행한 결과를 빠르게 확인하기 위한 도구입니다.

---

# 6. 정상 설치 최종 기준

```text
□ Ubuntu 22.04 Jammy
□ /opt/ros/humble 존재
□ ROS_DISTRO=humble
□ ros2 --help 실행
□ colcon 사용 가능
□ maintenance_check_pkg 빌드 성공
□ Overlay 적용 후 패키지 검색 성공
□ status_node 실행 성공
□ Talker 메시지 발행
□ Listener 메시지 수신
□ /talker, /listener 확인
□ /chatter Publisher 1 / Subscription 1
```

---

# 7. Evidence 저장

실습 화면 캡처는 `evidence/`에 저장합니다.

권장 파일명:

```text
evidence/
├── 01_os_ros_environment.png
├── 02_ros2_install_complete.png
├── 03_colcon_build.png
├── 04_overlay_package.png
├── 05_talker_listener.png
├── 06_topic_info.png
├── 07_environment_error.png
└── 08_environment_recovery.png
```

---

# 8. Windows 사용자의 경우

Windows 11에서는 WSL2 + Ubuntu 22.04 환경을 사용할 수 있습니다.

관리자 PowerShell:

```powershell
wsl --install -d Ubuntu-22.04
wsl --list --verbose
```

Ubuntu 안의 권장 작업 위치:

```text
~/robot_ws
```

---

# 9. myAGV Jetson Nano는 별도 환경

3회차 개발 PC:

```text
Ubuntu 22.04 + ROS 2 Humble
```

4회차 myAGV Jetson Nano:

```text
Ubuntu 20.04 + ROS 2 Galactic
```

Jetson Nano에서는 제조사 시스템 이미지를 사용합니다.

```text
myAGV2023_ubuntu_V20240103_20.04JN_aarch64_shrunk.img.gz
```

다운로드:

https://download-elephantrobotics.oss-cn-shenzhen.aliyuncs.com/Product_software/iMage-ISO/myAGV/myAGV2023_ubuntu_V20240103_20.04JN_aarch64_shrunk.img.gz

이번 3회차의 `ros-humble-desktop` 설치 절차를 해당 Jetson Nano 환경에 그대로 적용하지 않습니다.

---

# 10. 문제 발생 시 판단 순서

```text
설치되어 있는가?
      ↓
환경이 적용되어 있는가?
      ↓
빌드되어 있는가?
      ↓
Overlay가 적용되어 있는가?
      ↓
노드가 실행되는가?
      ↓
노드가 통신하는가?
```

대표 오류:

| 증상 | 먼저 확인 |
|---|---|
| `Unable to locate package` | apt 저장소 |
| `ros2: command not found` | 설치 경로 / `source` |
| `ROS_DISTRO` 출력 없음 | Underlay |
| `Package not found` | Build / Overlay |
| `colcon build` 실패 | 최초 실제 오류 |
| Listener 수신 없음 | Node / Topic / Domain / DDS |

---

# 핵심 원칙

> 설치 명령이 끝났다고 실습이 끝난 것이 아닙니다.  
> 설치 파일 존재 → 환경 적용 → 빌드 → 패키지 검색 → 노드 실행 → 메시지 통신까지 확인해야 정상 설치로 판단합니다.
