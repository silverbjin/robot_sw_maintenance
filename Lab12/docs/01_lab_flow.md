# Slide 12~15 실습 흐름

## Slide 12 — 상황 판단

현재 시스템은 기능 복구가 완료되었지만 유지보수 이력과 보고서는 작성되지 않은 상태입니다.

판단할 내용:

- 기능 복구는 완료되었는가?
- 결과 관리도 완료되었는가?
- 어떤 근거가 아직 필요한가?

## Slide 13 — Evidence 수집

다음 항목을 확인합니다.

| Evidence | 확인 내용 | 대표 명령 |
|---|---|---|
| E01 | 실행 환경 | `printenv ROS_DISTRO` |
| E02 | ROS 2 노드 | `ros2 node list` |
| E03 | 토픽 존재 | `ros2 topic list` |
| E04 | LiDAR 수신 주기 | `ros2 topic hz /lidar_scan` |
| E05 | Git 변경 상태 | `git status --short` |
| E06 | 실제 변경 내용 | `git diff -- .../config.yaml` |
| E07 | 기준 commit/tag | `git log --oneline --decorate -5` |
| E08 | 최종 기능 상태 | `/lab12/function_status` |

## Slide 14 — 결과 보고서

Evidence를 다음 항목으로 변환합니다.

`증상 → 원인 → 조치 → 변경 → 검증 → 결과 → 후속 조치`

## Slide 15 — 장기 운영 전략

보고서 결과를 다음 관리 항목으로 연결합니다.

- 기준선
- 백업·복구
- 상태 점검
- 이력 검토
