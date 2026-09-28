# Evidence 캡처 가이드

자동 수집된 텍스트 Evidence는 `evidence/`에 저장됩니다. 강사가 스크린샷 제출을 요구하는 경우 다음 화면을 추가로 캡처합니다.

## 권장 캡처 5종

1. **원인/변경 증거** — `git diff`에서 `/dev/ttyUSB0 → /dev/ttyUSB1` 변경이 보이는 화면
2. **노드 상태** — `ros2 node list`에서 `/lab12_lidar_publisher`, `/lab12_monitor`가 보이는 화면
3. **통신 상태** — `ros2 topic hz /lidar_scan`에서 약 10 Hz가 보이는 화면
4. **Git 기준선** — `git log --oneline --decorate -5`에서 `stable-2026-08`가 보이는 화면
5. **기능 상태** — `ros2 topic echo /lab12/function_status --once`에서 `FUNCTION_TEST=PASS`가 보이는 화면

## 캡처 원칙

- 실행 명령과 결과가 한 화면에 보이게 한다.
- 불필요한 다른 로그는 최소화한다.
- 파일명 예: `E04_topic_hz.png`
- 캡처만 제출하지 말고 Workbook과 보고서에 **그 캡처가 무엇을 증명하는지** 기록한다.
