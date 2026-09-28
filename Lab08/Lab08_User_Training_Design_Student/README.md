# Lab08 — 사용자 교육 설계 실습 패키지

과정: **지속 가능한 로봇 운영을 위한 소프트웨어 유지보수 이해**  
회차: **8회차 사용자 교육 개요**  
대상 슬라이드: **12~15**

## 실습 핵심

학생은 로봇 코드를 수정하지 않는다. 강사가 제공한 정상/장애 데모를 관찰하여 다음 흐름으로 **사용자 교육 설계안**을 완성한다.

> 사용자 분석 → 수행 목표 → 업무 흐름형 매뉴얼 → 정상/이상 판단 → 실습·평가 정렬 → 장애 보고

## 운영 환경

- Desktop: Windows 11 + WSL2/WSLg + Ubuntu 22.04 + ROS 2 Humble + Gazebo Fortress
- Robot: myAGV_JN_2023 + Ubuntu MATE 20.04 + ROS 2 Galactic

두 ROS 배포판의 직접 DDS 통신은 본 실습의 성공 조건이 아니다. Desktop에서는 재현 가능한 교육용 시나리오를 실행하고, 실제 로봇에서는 Galactic 로컬 터미널에서 상태를 관찰한다.

## 빠른 시작 — 강사

```bash
cd demo/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash

# Terminal 1
../scripts/run_demo.sh normal

# Terminal 2
ros2 node list | sort
../scripts/collect_evidence.sh normal
```

장애 시나리오:

```bash
../scripts/stop_demo.sh
../scripts/run_demo.sh missing_sensor
```

Gazebo 화면은 별도 터미널에서 실행한다.

```bash
demo/scripts/launch_gazebo.sh
```

## 주요 문서

- `docs/01_final_distribution_structure.md` — 최종 배포 구조
- `student/01_student_workbook.md` — 학생용 Workbook
- `student/02_user_training_design_template.md` — 최종 설계안 템플릿
- `student/03_incident_report_template.md` — 장애 보고 양식
- `student/04_final_checklist.md` — 최종 점검표
- `instructor/01_instructor_operation_guide.md` — 강사용 운영 가이드
- `instructor/02_answer_key.md` — 정답·예시
- `docs/07_verification_report.md` — 검증 결과

## 학생에게 강조할 기준

> 문제를 직접 고치는 것이 목표가 아니다. 일반 운영자의 권한 안에서 **정상/이상 판단 → 업무 시작/중단 결정 → 정보 기록 → 보고**를 정확히 수행하는 것이 목표다.
