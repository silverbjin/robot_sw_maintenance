# ⑤ 로봇 소프트웨어 설치 환경 점검 결과 보고서

## 1. 기본 정보

| 항목 | 내용 |
|---|---|
| 과정명 | 지속 가능한 로봇 운영을 위한 소프트웨어 유지보수 이해 |
| 실습명 | 로봇 소프트웨어 설치 전 환경 점검 |
| 작성자 | |
| 실습일 | |
| 대상 PC | |

## 2. 최종 결론

- [ ] READY — 소프트웨어 설치 진행 가능
- [ ] NOT READY — 문제 조치 후 재검증 필요

**판단 근거 요약**

> 

## 3. 환경 점검 결과

| 점검 항목 | 명령 | 결과 | 판정 |
|---|---|---|---|
| WSL | `wsl -l -v` | | 정상/확인 |
| Ubuntu | `lsb_release -a` | | 정상/확인 |
| Architecture | `uname -m` | | 정상/확인 |
| Memory | `free -h` | | 정상/확인 |
| Storage | `df -h /` | | 정상/확인 |
| Interface/IP | `ip addr` | | 정상/확인 |
| Loopback Ping | `ping -c 4 127.0.0.1` | | 정상/확인 |
| TCP 통신 | `curl 127.0.0.1:8000` | | 정상/확인 |

## 4. 장애 재현 및 복구

### 장애 내용

- 실행 명령: `curl http://127.0.0.1:9000`
- 관찰된 오류:

> 

### 원인

> 

### 조치

> 

### 재검증

- 실행 명령: `curl http://127.0.0.1:8000`
- 결과:

> 

## 5. 개발 PC와 Robot 설치 환경 비교

### 공통점

> 

### 차이점

> 

## 6. Evidence 파일

- `evidence.json`: `results/________________/evidence.json`
- `evidence.md`: `results/________________/evidence.md`

## 7. 증거 이미지 첨부 위치

### E-01 — WSL 2 상태

> `wsl -l -v` 결과 캡처 삽입

### E-02 — Ubuntu / Architecture

> `lsb_release -a`, `uname -m` 결과 캡처 삽입

### E-03 — Memory / Storage

> `free -h`, `df -h /` 결과 캡처 삽입

### E-04 — Network

> `ip addr`, `ping -c 4 127.0.0.1` 결과 캡처 삽입

### E-05 — TCP 정상/장애/복구

> `curl :8000` 성공, `curl :9000` 실패, 다시 `:8000` 성공 결과 캡처 삽입

## 8. 최종 점검 체크리스트

- [ ] OS 버전을 확인했다.
- [ ] CPU 아키텍처를 확인했다.
- [ ] Available Memory를 확인했다.
- [ ] Storage Use%를 확인했다.
- [ ] Network interface와 IPv4를 확인했다.
- [ ] Loopback Ping을 확인했다.
- [ ] TCP 통신을 확인했다.
- [ ] 장애를 재현하고 원인을 설명했다.
- [ ] 수정 후 재검증했다.
- [ ] READY/NOT READY 판단 근거를 기록했다.

## 9. 학습자 의견

### 설치 전에 가장 먼저 확인해야 한다고 생각한 항목

> 

### 실제 로봇에서는 추가로 확인해야 할 항목

>
