# 05. 사용자 실습 수행 결과 보고서

> 4회차 — 로봇 시스템 설정 및 초기화

---

## 1. 기본 정보

| 항목 | 작성 내용 |
|---|---|
| 교육생 | |
| 교육 일자 | |
| 로봇 | myAGV 2023 Jetson Nano |
| Jetson ROS 2 | Galactic |
| Desktop OS | Ubuntu 22.04 LTS |
| Desktop ROS 2 | Humble |
| 점검 담당자 | |

---

## 2. 실습 목적

다음 문장을 참고하여 2~3문장으로 작성한다.

> 설치된 로봇 소프트웨어가 장치, 데이터, 네트워크, 실제 동작과 안전 기능까지 정상적으로 동작하는지 확인한다.

작성:

```text


```

---

# 3. LAB 15 — 저속 제어 결과

| 항목 | 결과 | 관찰 내용 |
|---|---|---|
| 속도 0 | 정상 / 이상 | |
| 저속 전진 | 정상 / 이상 | |
| 저속 후진 | 정상 / 이상 | |
| 저속 회전 | 정상 / 이상 | |
| 최종 정지 | 정상 / 이상 | |
| `/odom` 일치 | 정상 / 이상 | |
| `/imu` 일치 | 정상 / 이상 | |

### 판단

```text


```

---

# 4. LAB 16 — 센서 검증 결과

| 센서 | 데이터 수신 | 실제 상태 반영 | 최종 |
|---|---|---|---|
| LiDAR `/scan` | 정상 / 이상 | 정상 / 이상 | |
| IMU `/imu` | 정상 / 이상 | 정상 / 이상 | |
| Odometry `/odom` | 정상 / 이상 | 정상 / 이상 | |
| Battery `/voltage` | 정상 / 이상 | 정상 / 이상 | |

### RViz 결과

```text
Fixed Frame:
LaserScan:
실제 환경과의 일치:
특이사항:
```

### Evidence

> **[E02 이미지 삽입 위치 — RViz 또는 /scan Hz]**

---

# 5. LAB 17 — Gateway 결과

| 확인 항목 | 결과 |
|---|---|
| Jetson Gateway 실행 | 정상 / 이상 |
| Desktop Gateway 실행 | 정상 / 이상 |
| TCP 연결 | 정상 / 이상 |
| Heartbeat | 정상 / 이상 |
| Command Channel | 정상 / 이상 |
| Status Channel | 정상 / 이상 |
| `/gateway/odom` | 정상 / 이상 |
| `/gateway/imu` | 정상 / 이상 |
| `/gateway/voltage` | 정상 / 이상 |
| `/gateway/scan_health` | 정상 / 이상 |

### Evidence

> **[E03 이미지 삽입 위치 — Connected / Heartbeat]**

---

# 6. 제어 경로 검증

```text
Desktop Command
→ Gateway
→ Jetson
→ /cmd_vel
→ Motor
→ Robot
```

| 단계 | 확인 결과 |
|---|---|
| Desktop 명령 생성 | |
| TCP 전송 | |
| Jetson `/cmd_vel` | |
| 실제 이동 | |
| odom/imu 변화 | |
| STOP | |

### Evidence

> **[E04 이미지 삽입 위치 — 이동 또는 상태 변화]**

---

# 7. 안전 기능 검증

## Command Timeout

```text
결과:
정지 여부:
로그:
```

## Heartbeat Timeout

```text
결과:
정지 여부:
로그:
```

### Evidence

> **[E05 이미지 삽입 위치 — timeout → STOP]**

---

# 8. 오류 및 조치 기록

| 순번 | 증상 | 확인한 계층 | 원인 | 조치 | 재검증 |
|---:|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

오류가 없었다면:

```text
오류 없음
```

이라고 작성한다.

---

# 9. 최종 체크

- [ ] Hardware
- [ ] Driver
- [ ] Data
- [ ] Network
- [ ] Actual Motion
- [ ] STOP
- [ ] Timeout
- [ ] Evidence 저장

---

# 10. 최종 판정

```text
[ ] 운영 가능
[ ] 추가 점검 필요
[ ] 시험 중단
```

### 판정 근거

```text



```

---

# 11. 배운 점

이번 실습에서 가장 중요한 판단 기준을 2~3문장으로 작성한다.

```text



```

---

# 12. 부록 — Evidence

## E01. Jetson 장치·ROS 상태

> 로그 파일 또는 캡처 삽입

## E02. Sensor / RViz

> 이미지 삽입

## E03. Gateway

> 이미지 삽입

## E04. Motion

> 이미지 삽입

## E05. Safety

> 이미지 삽입
