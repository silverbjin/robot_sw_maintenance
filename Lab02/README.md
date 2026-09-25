# Lab02 — 로봇 소프트웨어 설치 전 환경 점검

과정명: **지속 가능한 로봇 운영을 위한 소프트웨어 유지보수 이해**  
관련 슬라이드: **3-2, 12, 13, 14, 14-2**

이 패키지는 **학생 실습용 배포본**입니다. 강사용 시연이나 ROS 2 데모 없이, 학생이 자신의 개발 PC에서 설치 환경을 점검하고 Evidence를 수집한 뒤 결과 보고서를 작성하는 흐름으로 구성되어 있습니다.

## 실습 목표

소프트웨어를 설치하기 전에 다음 항목을 확인하고 **READY / NOT READY**를 판단합니다.

```text
OS → CPU Architecture → Memory → Storage → Network → 통신 확인 → 최종 판정
```

## 학습의 핵심

> **설치 명령보다 먼저, 설치할 환경이 준비되어 있는지 확인한다.**

- 개발 PC와 로봇은 하드웨어가 달라도 설치 전 점검 원리는 거의 같습니다.
- 차이는 CPU 아키텍처, OS 이미지, 장치 드라이버, 설치 매체에서 주로 발생합니다.
- 네트워크 실습은 개발 PC 한 대에서 수행하지만, 실제 로봇에서도 **상대 주소가 로봇 IP로 바뀔 뿐 확인 원리는 같습니다.**


## 개발환경 사양

본 실습은 **Windows 개발 PC 한 대에서 WSL 2 + Ubuntu 22.04 LTS를 사용하여**
로봇 소프트웨어 설치 전 환경 점검 과정을 학습하도록 구성되어 있습니다.

실제 로봇은 사용하지 않으며, 네트워크 실습에서는 하나의 개발 PC 안에서
Client와 Server를 실행하여 개발 PC ↔ 로봇 통신 실습을 수행 합니다.

실습의 핵심은 고성능 하드웨어가 아니라 **OS → CPU → Memory → Storage → Network 상태를 확인하고 설치 가능 여부를 판단하는 것**입니다.

---

### WSL 환경

설치된 WSL과 Ubuntu 버전은 PowerShell에서 다음 명령으로 확인합니다.

```powershell
wsl --version
wsl --status
wsl -l -v
```


## 배포 파일 구조

```text
Lab02_student_distribution_v1.0/
├── README.md
├── student/
│   ├── 04_student_workbook.md
│   └── quick_commands.md
├── evidence/
│   ├── EVIDENCE_GUIDE.md
│   ├── collect_developer_evidence.sh
│   └── collect_evidence.py
├── reports/
│   └── 05_result_report_template.md
└── results/
    └── .gitkeep
```

### 파일 용도

| 파일 | 용도 |
|---|---|
| `student/04_student_workbook.md` | 학생이 순서대로 수행하는 본 실습 Workbook |
| `student/quick_commands.md` | 실습 명령어 빠른 참고 |
| `evidence/collect_developer_evidence.sh` | Evidence 수집 실행 스크립트 |
| `evidence/collect_evidence.py` | 환경 정보를 수집하고 READY/NOT READY를 판정하는 도구 |
| `evidence/EVIDENCE_GUIDE.md` | Evidence 수집 방법과 결과 확인 방법 |
| `reports/05_result_report_template.md` | 학생 제출용 결과 보고서 템플릿 |
| `results/` | Evidence 결과가 자동 저장되는 디렉터리 |

---

# 진행 순서

이 실습은 아래 **3단계만** 진행합니다.

```text
① Workbook 수행
        ↓
② Evidence 수집
        ↓
③ 결과 보고서 작성
```

## ① 학생 — Workbook 수행

먼저 다음 파일을 엽니다.

```text
student/04_student_workbook.md
```

Workbook의 Mission을 처음부터 순서대로 수행합니다.

주요 확인 항목:

```text
WSL 2 / Ubuntu 22.04
        ↓
Ubuntu Version
        ↓
CPU Architecture
        ↓
Memory
        ↓
Storage
        ↓
Network Interface / IPv4
        ↓
Loopback Ping
        ↓
한 PC에서 TCP Client ↔ Server 통신
        ↓
장애 재현 → 원인 확인 → 복구 → 재검증
```

명령어만 빠르게 확인해야 할 때는 다음 파일을 참고합니다.

```text
student/quick_commands.md
```

> Workbook의 빈칸, 체크박스, 판단 근거를 실습 중 직접 작성합니다.

---

## ② 학생/강사 — Evidence 수집

Workbook 실습을 마친 후 Ubuntu 터미널에서 **이 패키지의 최상위 디렉터리**로 이동합니다.

예:

```bash
cd ~/Lab02_student_distribution_v1.0
```

처음 한 번 실행 권한을 설정합니다.

```bash
chmod +x evidence/collect_developer_evidence.sh
```

Evidence를 수집합니다.

```bash
./evidence/collect_developer_evidence.sh
```

정상적으로 실행되면 다음과 비슷하게 표시됩니다.

```text
[RESULT] READY
[PATH] .../results/20260925_153000
```

또는 점검 기준을 통과하지 못한 항목이 있다면:

```text
[RESULT] NOT_READY
[FAILED] ...
```

### 생성되는 파일

```text
results/YYYYMMDD_HHMMSS/
├── evidence.json
└── evidence.md
```

- `evidence.json`: 자동 수집된 원본 Evidence
- `evidence.md`: 사람이 읽기 쉬운 요약

학생 또는 강사는 다음 파일을 열어 결과를 확인합니다.

```text
results/YYYYMMDD_HHMMSS/evidence.md
```

### 교육용 READY 기준

기본 기준은 다음과 같습니다.

```text
Ubuntu Release       = 22.04
Architecture         = x86_64
Available Memory     >= 1 GiB
Root Storage Use     < 90%
Loopback Ping        = PASS
Loopback TCP         = PASS
```

> 이 기준은 **수업용 판정 기준**이며 실제 제품이나 로봇의 운영 요구사항을 의미하지 않습니다.

`NOT_READY`가 표시되더라도 Evidence 수집 프로그램이 고장 났다는 뜻은 아닙니다. 하나 이상의 점검 항목이 교육용 기준을 통과하지 못했다는 뜻입니다.

자세한 내용은 다음 파일을 참고합니다.

```text
evidence/EVIDENCE_GUIDE.md
```

---

## ③ 학생 — 결과 보고서 작성

다음 파일을 복사하거나 직접 작성합니다.

```text
reports/05_result_report_template.md
```

보고서에는 최소한 다음 내용을 기록합니다.

```text
1. WSL 2 상태
2. Ubuntu 버전
3. CPU Architecture
4. Available Memory
5. Storage Use%
6. Network Interface / IPv4
7. Loopback Ping 결과
8. TCP 정상 통신 결과
9. 잘못된 Port를 사용한 장애 재현 결과
10. 수정 후 재검증 결과
11. Evidence 경로
12. READY / NOT READY 최종 판단과 근거
```

Evidence 경로 예:

```text
results/20260925_153000/evidence.json
results/20260925_153000/evidence.md
```

보고서의 Evidence 이미지 항목에는 Workbook 수행 중 캡처한 화면을 첨부합니다.

---

# 네트워크 실습에서 반드시 기억할 점

이번 실습은 실제 로봇 없이 **개발 PC 한 대**에서 수행합니다.

```text
Terminal 2                       Terminal 1
Client                           Server
개발 PC 역할                     Robot 역할
    │                               │
    └──────── TCP :8000 ────────────┘
```

이번 실습에서는 다음 주소를 사용합니다.

```text
127.0.0.1
```

실제 로봇에서는 이 주소가 로봇의 IP로 바뀝니다.

```text
실습:      Client → 127.0.0.1 → Server
실제 로봇: 개발 PC → Robot IP → Robot
```

확인 원리는 동일합니다.

```text
IP 확인 → Interface 확인 → 상대 주소 확인 → 통신 요청 → 응답 확인
```

---

# 개발 PC와 Robot의 공통점 / 차이점

## 공통적으로 확인하는 항목

```text
OS
CPU Architecture
Memory
Storage
Network Interface
IP Address
통신 상태
```

## 주로 달라지는 항목

| 개발 PC | Robot SBC |
|---|---|
| 보통 `x86_64` | 보통 `aarch64` |
| WSL / USB 설치 | SD / eMMC / NVMe Image |
| PC 범용 드라이버 | Robot / Sensor / Motor 드라이버 |
| 일반 Ubuntu 환경 | 제조사 이미지가 사용될 수 있음 |

따라서 **하드웨어는 달라도 점검 방법은 유사하지만 설치 파일과 드라이버는 같다고 가정하면 안 됩니다.**

---

# 실습 종료 체크

제출 전에 확인합니다.

- [ ] `student/04_student_workbook.md`의 모든 Mission을 수행했다.
- [ ] `wsl -l -v`에서 Ubuntu 22.04와 WSL VERSION 2를 확인했다.
- [ ] OS / CPU / Memory / Storage / Network 결과를 기록했다.
- [ ] `127.0.0.1` Loopback Ping을 수행했다.
- [ ] TCP Port 8000 정상 통신을 확인했다.
- [ ] Port 9000 장애를 재현하고 원인을 기록했다.
- [ ] Port 8000으로 복구 후 재검증했다.
- [ ] Evidence를 수집했다.
- [ ] `evidence.json`과 `evidence.md` 생성 여부를 확인했다.
- [ ] `reports/05_result_report_template.md`를 작성했다.
- [ ] READY / NOT READY 판단과 근거를 기록했다.

---

# 문제가 발생했을 때

먼저 Workbook의 해당 Mission으로 돌아가 명령과 결과를 다시 확인합니다.

Evidence 수집 중 `NOT_READY`가 나타난 경우에는 다음 순서로 확인합니다.

```text
FAILED 항목 확인
      ↓
Workbook의 해당 점검 단계 확인
      ↓
문제 조치
      ↓
명령으로 재검증
      ↓
Evidence 다시 수집
```

Evidence를 다시 수집하면 `results/` 아래에 **새로운 시간 디렉터리**가 생성됩니다. 기존 Evidence는 삭제하지 말고, 최종 보고서에는 최종 검증 결과의 경로를 기록합니다.
