# Lab12 Student — 로봇 소프트웨어 유지보수 결과 관리 및 보고

이 패키지는 **12회차 Slide 12~15 학생 실습용**입니다.

학생은 소스 코드를 작성하지 않습니다. 제공된 Mock ROS 2 데모를 실행하고, 복구된 시스템에서 Evidence를 수집한 뒤 유지보수 결과 보고서와 장기 운영 후속 조치를 작성합니다.

## 실습 목표

1. 유지보수 완료 상태에서 환경·노드·토픽·Git 변경 이력·기능 상태를 확인하여 Evidence를 수집한다.
2. 수집한 Evidence를 근거로 유지보수 결과 보고서와 장기 운영 관리 항목을 작성한다.

## 권장 환경

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python 3
- Git
- colcon

## 실습 흐름

1. **Slide 12** — 복구된 시스템과 비어 있는 기록을 비교한다.
2. **Slide 13** — 환경/노드/토픽/Git/기능 Evidence를 수집한다.
3. **Slide 14** — Evidence를 근거로 유지보수 결과 보고서를 작성한다.
4. **Slide 15** — 보고서의 후속 조치를 장기 운영 전략으로 전환한다.

## 빠른 시작

### 1) 실습 준비 — 최초 1회

```bash
cd Lab12_Student
bash scripts/prepare_lab.sh
```

이 스크립트는 다음을 자동으로 준비합니다.

- ROS 2 워크스페이스 빌드
- 정상 기준선 Git commit/tag 생성
- LiDAR 포트 오류가 포함된 regression commit 생성
- 오류를 수정한 **복구 완료 상태**를 working tree에 준비

따라서 학생은 이미 복구된 상태에서 `git diff`를 통해 무엇이 변경되었는지 확인할 수 있습니다.

### 2) 데모 실행 — 터미널 1

```bash
cd Lab12_Student
bash scripts/start_lab.sh
```

터미널을 종료하지 않고 그대로 둡니다.

### 3) 상태 확인 및 Evidence 수집 — 터미널 2

```bash
cd Lab12_Student
bash scripts/check_runtime.sh
bash scripts/collect_evidence.sh
```

### 4) 학생 문서 작성

순서대로 작성합니다.

1. `student/01_student_workbook.md`
2. `reports/02_maintenance_result_report.md`
3. `reports/03_operations_followup.md`

Evidence는 `evidence/`에 저장됩니다.

## 중요한 원칙

> 명령어를 실행하는 것 자체가 목적이 아닙니다.  
> **무엇을 확인하는가 → 정상 결과는 무엇인가 → 보고서의 어느 판단 근거가 되는가**를 설명할 수 있어야 합니다.

## 실습 종료

데모를 실행 중인 터미널에서 `Ctrl+C`를 누릅니다.
