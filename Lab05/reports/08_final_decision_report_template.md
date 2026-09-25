# 업그레이드 최종 판단 보고서

> 관련 슬라이드: 15 — 업그레이드 GO / NO-GO 판단

## 1. 기본 정보

| 항목 | 내용 |
|---|---|
| 프로젝트 / 시스템명 | |
| 대상 장비 | Jetson Orin Nano |
| 운영체제 | Ubuntu 22.04 |
| JetPack | |
| ROS 2 배포판 | Humble |
| Robot Application | |
| 현재 Baseline Tag / Commit | |
| 대상 Target Tag / Commit | |
| 점검 일시 | |
| 점검자 | |
| 검토자 | |

## 2. Upgrade Scope

### 변경 대상

- [ ] `myagv_bringup` 일부 변경
- [ ] `myagv_monitor` 신규 모듈 추가
- [ ] 관련 ROS 2 Node / Topic

### 변경하지 않는 대상

- [ ] Ubuntu 22.04
- [ ] JetPack 6.x
- [ ] ROS 2 Humble
- [ ] Jetson Firmware / BSP

### 변경 목적

> 

## 3. 현재 Baseline 요약

| 항목 | 확인 결과 | Evidence / 비고 |
|---|---|---|
| Board | Jetson Orin Nano | |
| Ubuntu | | |
| Jetson Linux | | |
| JetPack | | |
| ROS 2 | Humble | |
| Git Commit | | |
| Git Tag | | |
| Sensor | 정상 / 비정상 / 미확인 | |
| Motor | 정상 / 비정상 / 미확인 | |
| Network | 정상 / 비정상 / 미확인 | |

## 4. 최종 점검 체크리스트

| 구분 | 최종 점검 항목 | YES | NO | 확인 근거 |
|---|---|---:|---:|---|
| Baseline | 현재 정상 상태가 기록되어 있는가? | [ ] | [ ] | |
| Baseline | 현재 Git Commit / Tag가 확인되어 있는가? | [ ] | [ ] | |
| Compatibility | 대상 버전이 현재 ROS 2 Humble 환경과 동작 가능한지 확인했는가? | [ ] | [ ] | |
| Compatibility | 변경 대상과 변경하지 않는 대상이 명확한가? | [ ] | [ ] | |
| Backup | 소스 코드와 설정 파일의 Backup이 준비되어 있는가? | [ ] | [ ] | |
| Backup | Baseline 결과와 주요 로그가 보관되어 있는가? | [ ] | [ ] | |
| Rollback | Baseline으로 되돌아가는 방법이 정의되어 있는가? | [ ] | [ ] | |
| Rollback | 복귀 후 재빌드·환경 반영·재검증 절차가 정해져 있는가? | [ ] | [ ] | |
| Upgrade Plan | 현재 버전과 대상 버전이 명시되어 있는가? | [ ] | [ ] | |
| Upgrade Plan | 변경 이유와 영향 범위가 작성되어 있는가? | [ ] | [ ] | |
| Upgrade Plan | 변경 순서와 최소 검증 항목이 정의되어 있는가? | [ ] | [ ] | |
| 운영 준비 | 문제 발생 시 담당자와 대응 방법이 정해져 있는가? | [ ] | [ ] | |

## 5. 최종 3문장 점검

### 현재 상태를 정확하게 알고 있는가?
- [ ] YES
- [ ] NO

근거:

> 

### 문제가 발생해도 이전 정상 상태로 돌아갈 수 있는가?
- [ ] YES
- [ ] NO

근거:

> 

### 무엇을 어떤 순서로 변경할지 명확한가?
- [ ] YES
- [ ] NO

근거:

> 

## 6. 미확인 / 위험 항목

| 번호 | 항목 | 영향 | 조치 계획 | 담당자 | 완료 예정 |
|---:|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

## 7. 최종 판단

- [ ] **GO** — 6회차 업그레이드 실행 가능
- [ ] **NO-GO** — 미확인 또는 위험 항목 보완 후 재판단

### 판단 근거

> 

### GO 실행 조건

- [ ] Upgrade Plan에 정의된 범위만 변경한다.
- [ ] Ubuntu / JetPack / ROS 2 Humble은 유지한다.
- [ ] 변경 후 최소 기능 확인을 수행한다.
- [ ] 문제 발생 시 Rollback 기준에 따라 대응한다.

### NO-GO 보완 사항

> 

## 8. Evidence 목록

| 번호 | Evidence | 파일 / 위치 | 확인 내용 |
|---:|---|---|---|
| 1 | System Baseline | | |
| 2 | ROS Baseline | | |
| 3 | Git Baseline | | |
| 4 | Upgrade Plan | | |
| 5 | GO / NO-GO Checklist | | |

## 9. 최종 승인

| 역할 | 이름 | 판단 / 승인 | 일자 |
|---|---|---|---|
| 점검자 | | | |
| 검토자 | | | |
| 강사 / 승인자 | | | |

## 10. 한 줄 결론

> 현재 시스템은 __________________________________________ 이유로 GO / NO-GO로 판단한다.

---

## 작성 원칙

- GO는 장애가 절대 발생하지 않는다는 보장이 아니라, 계획한 범위에서 변경을 시작할 준비가 되었음을 의미한다.
- 핵심 조건이 확인되지 않았다면 NO-GO로 판단하고 보완 후 재검토한다.
- NO-GO는 실패가 아니라 준비되지 않은 변경을 막기 위한 정상적인 유지보수 판단이다.
