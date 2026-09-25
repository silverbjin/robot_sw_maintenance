# 로봇 소프트웨어 업그레이드 실습 결과 보고서

## 1. 실습 정보

- 성명:
- 실습 일시:
- 실습명: Robot Application Upgrade & Rollback
- 환경: Ubuntu 22.04 / ROS 2 Humble
- Repository: `robot_sw_maintenance / Lab06`

## 2. 실습 목적

이번 실습의 목적을 2~3문장으로 작성한다.

> 작성 예: 계획된 Target Version을 적용하고 Dependency, Build, Source, 최소 실행 절차를 수행한다. 문제가 있다고 가정한 뒤 사전에 지정한 Tag로 Rollback하고 Clean Rebuild를 통해 실행 환경까지 복원한다.

## 3. Baseline 확인 결과

| 항목 | 결과 |
|---|---|
| Branch | |
| Commit | |
| Baseline Tag | |
| Package 구성 | |
| Working Tree | |

### Evidence
- Evidence 파일/캡처:
- 관찰 내용:

## 4. Upgrade 실행 결과

| 단계 | 수행 내용 | 결과 |
|---|---|---|
| Target Version | | 성공 / 실패 |
| Dependency | | 성공 / 실패 |
| Build | | 성공 / 실패 |
| Source | | 완료 / 미완료 |
| 신규 모듈 실행 | | 성공 / 실패 |

### Evidence
- Evidence 파일/캡처:
- 관찰 내용:

## 5. Rollback 실행 결과

| 단계 | 수행 내용 | 결과 |
|---|---|---|
| Tag 복귀 | | 성공 / 실패 |
| Source 구성 확인 | | 성공 / 실패 |
| Build 결과 정리 | | 성공 / 실패 |
| Clean Rebuild | | 성공 / 실패 |
| Baseline 실행 | | 성공 / 실패 |
| 신규 Package 제거 확인 | | 성공 / 실패 |

### Evidence
- Evidence 파일/캡처:
- 관찰 내용:

## 6. 발생 문제 및 조치

| 증상 | 발생 단계 | 조치 | 결과 |
|---|---|---|---|
| | | | |

문제가 없었다면 `특이사항 없음`으로 작성한다.

## 7. 최종 판단

- [ ] Upgrade Execution 절차를 완료함
- [ ] Rollback 절차를 완료함
- [ ] Baseline 실행 환경 복원을 확인함
- [ ] 상세 System Validation은 다음 회차에서 수행함

## 8. 학습자 정리

1. Build와 Source가 다른 이유:
2. Rollback에서 Clean Rebuild가 필요한 이유:
3. 이번 실습에서 가장 중요한 안전 원칙:
