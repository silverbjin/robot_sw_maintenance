# 7회차 학생용 실습 패키지

## 로봇 소프트웨어 업그레이드 검증 및 문제 해결

이 패키지는 7회차 슬라이드 **11~15**의 실습을 학생이 순서대로 따라 할 수 있도록 구성한 학생 전용 배포본입니다.

학생은 소스 코드를 직접 작성하지 않습니다. 제공된 ROS 2 패키지와 스크립트를 실행하고, ROS 2/Git 명령으로 Evidence를 확인한 뒤 **비교 → 판단 → 조치 → 재검증 → 기록**을 수행합니다.

## 학습 흐름

```text
LAB-11 문제 재현
  ↓
LAB-12 어디까지 정상인지 확인
  ↓
LAB-13 Git 변경 전후 비교 및 Root Cause 판단
  ↓
LAB-14 Fix / Rollback 판단
  ↓
LAB-15 같은 기준으로 재검증 + Upgrade Record 작성
```

## 기본 실습 환경

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Git
- colcon
- 기본 센서 Backend: **Mock LiDAR**

실제 LiDAR 하드웨어가 없어도 전체 실습을 진행할 수 있습니다.

## 패키지 구성

```text
Lab07_Upgrade_Verification_Student/
├── README.md
├── docs/
│   ├── 01_student_workbook.md
│   ├── 02_command_reference.md
│   └── 03_upgrade_record.md
├── ros2_ws/
│   └── src/
│       └── maintenance_lidar_demo/
├── scripts/
│   ├── setup_lab.sh
│   ├── prepare_git_history.sh
│   ├── reset_to_v13.sh
│   ├── apply_topic_fix.sh
│   ├── rollback_v12.sh
│   ├── collect_evidence.sh
│   └── verify_result.sh
├── evidence/
│   ├── LAB11/
│   ├── LAB12/
│   ├── LAB13/
│   ├── LAB14/
│   └── LAB15/
└── optional_hardware/
    ├── 01_hardware_option.md
    └── myagv_lidar_bringup/
```

## 1. 실습 준비

패키지 루트에서 실행합니다.

```bash
source /opt/ros/humble/setup.bash
./scripts/setup_lab.sh
```

빌드가 끝난 뒤 현재 터미널에서 다음을 실행합니다.

```bash
source ros2_ws/install/setup.bash
```

교육용 Git 이력이 아직 준비되지 않았다면 최초 한 번 실행합니다.

```bash
./scripts/prepare_git_history.sh
```

실습 시작 상태를 깨진 v1.3으로 맞춥니다.

```bash
./scripts/reset_to_v13.sh
```

## 2. 학생이 사용할 문서

1. `docs/01_student_workbook.md` — 실습의 본문입니다. **LAB-11부터 LAB-15까지 순서대로 수행합니다.**
2. `docs/02_command_reference.md` — 사용 명령어의 목적, 예상 결과, 오류 확인 방법을 설명합니다.
3. `docs/03_upgrade_record.md` — LAB-15에서 최종 결과를 기록합니다.

## 3. 대표 장애 시나리오

```text
v1.2 Baseline
Publisher  = /scan
Subscriber = /scan
→ NORMAL

v1.3 Broken
Publisher  = /lidar/scan
Subscriber = /scan
→ Laser scan data timeout

v1.3 Fixed
Publisher  = /lidar/scan
Subscriber = /lidar/scan
→ NORMAL
```

실습의 핵심은 처음부터 정답을 추측하는 것이 아니라 다음 순서로 Evidence를 확보하는 것입니다.

```text
Node → Topic → Publisher/Subscriber → Data → Git Diff → Root Cause
```

## 4. 실습 시작

`docs/01_student_workbook.md`를 열고 **LAB-11**부터 시작합니다.

깨진 v1.3 실행:

```bash
ros2 launch maintenance_lidar_demo lab_current.launch.py
```

다른 터미널에서 상태를 확인할 때는 해당 터미널에서도 다음을 먼저 실행합니다.

```bash
source /opt/ros/humble/setup.bash
source ros2_ws/install/setup.bash
```

## 5. Evidence 저장

Workbook 지시에 따라 다음처럼 Evidence를 저장할 수 있습니다.

```bash
./scripts/collect_evidence.sh LAB12
./scripts/collect_evidence.sh LAB13
./scripts/collect_evidence.sh LAB15
```

저장 위치:

```text
evidence/LABxx/
```

## 6. Fix와 Rollback

이번 대표 시나리오의 기본 판단은 **Fix**입니다.

```bash
./scripts/apply_topic_fix.sh
```

Rollback 대안은 다음 명령으로 확인할 수 있습니다.

```bash
./scripts/rollback_v12.sh
```

수업에서 강사의 지시가 없다면 Workbook의 기본 흐름인 **Fix 경로**를 따릅니다.

## 7. 최종 검증

```bash
./scripts/verify_result.sh
```

그 뒤 `docs/03_upgrade_record.md`를 작성합니다.

## 8. 실제 YDLIDAR 선택 실습

기본 실습에는 실제 LiDAR가 필요하지 않습니다.

강사가 실제 YDLIDAR 실습을 안내한 경우에만 `optional_hardware/01_hardware_option.md`를 참고합니다. 장비별 `port`, `baudrate`, `sample_rate` 등은 강사가 확인한 값을 사용해야 합니다.

## 주의

- Python/YAML 소스 코드를 임의로 수정하지 않습니다.
- LAB-13 이전에는 장애 원인을 정답처럼 단정하지 않습니다.
- LAB-14에서는 “수정할 수 있는가?”보다 **“안전하게 수정할 수 있는가?”**를 판단합니다.
- Fix 또는 Rollback 후에는 반드시 LAB-15의 동일 기준으로 재검증합니다.
