# Lab11 — 로봇 소프트웨어 유지보수 절차 수행

이 패키지는 11회차 Slide 12~15의 시연을 학생이 그대로 따라할 수 있도록 구성한 실습 자료입니다.

## 핵심 학습 흐름

1. **Slide 12 — 이상 발견**: 정상 기준 `/scan ≈ 10 Hz`와 현재 상태를 비교한다.
2. **Slide 13 — STEP 1**: Node → Topic → Data → Resource 순으로 점검하여 이상 영역을 좁힌다.
3. **Slide 14 — STEP 2**: `/scan` Publisher를 확인하고, `lidar_node` 수준에서 최소 범위 복구를 수행한다.
4. **Slide 15 — STEP 3**: 복구 전·후를 동일한 기준으로 비교하고 일정 시간 정상 유지 여부를 검증한다.

> 교육 목적상 실제 LiDAR 고장을 만들지 않습니다. 강사용 스크립트가 데모 `lidar_node`의 `/scan` 발행 주기를 10 Hz에서 2.5 Hz로 낮춰 동일한 장애를 재현합니다.

## 권장 환경

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python 3.10
- `colcon`
- Terminal

## 빠른 시작

### 1) 데모 빌드

```bash
cd Lab11_maintenance_procedure
bash scripts/build_demo.sh
```

### 2) 데모 시작 — 정상 상태 10 Hz

```bash
bash scripts/start_demo.sh
```

### 3) 강사: 장애 주입 — 2.5 Hz

```bash
bash instructor/inject_slow_scan.sh
```

### 4) 학생: Workbook의 Slide 12~15 절차 수행

```bash
ros2 topic hz /scan
ros2 node list
ros2 topic list
free -h
df -h
ros2 topic info /scan -v
```

### 5) 학생: 최소 범위 복구

```bash
bash scripts/restart_lidar_demo.sh
```

### 6) 복구 후 재검증

```bash
ros2 topic hz /scan
```

### 7) 종료

```bash
bash scripts/stop_demo.sh
```

## 학생 자료

- `student/Lab11_Workbook.md` — Slide 12~15 단계별 실습지
- `student/Lab11_Result_Report.md` — 최종 실습 결과 보고서
- `student/evidence/` — 캡처 파일 저장 위치

## 강사 자료

- `instructor/Instructor_Guide.md` — 운영 순서, 장애 주입/복구, 문제 대응
- `instructor/answer_key.md` — Workbook 정답·판정 기준
- `instructor/inject_slow_scan.sh` — `/scan` 2.5 Hz 장애 주입
- `instructor/reset_demo.sh` — 정상 10 Hz로 즉시 초기화

## 안전 주의

본 데모는 교육용 LaserScan 메시지만 생성하며 모터 제어 명령을 발행하지 않습니다. 실제 myAGV에서 적용할 경우에는 반드시 로봇을 안전 정지한 뒤 진단하십시오.
