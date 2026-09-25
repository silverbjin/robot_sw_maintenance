# Evidence 수집 가이드

## 목적

Workbook 수행 결과를 자동으로 수집하여 **JSON + Markdown Evidence**로 남깁니다.

이 단계는 학생이 직접 수행하거나 강사가 학생 PC에서 함께 수행할 수 있습니다.

---

## 1. 패키지 루트로 이동

Ubuntu 터미널에서 학생 배포 패키지의 최상위 디렉터리로 이동합니다.

예:

```bash
cd ~/Lab02_student_distribution_v1.0
```

현재 위치 확인:

```bash
pwd
ls
```

다음 디렉터리가 보여야 합니다.

```text
student  evidence  reports  results
```

---

## 2. 실행 권한 설정

처음 한 번만 실행합니다.

```bash
chmod +x evidence/collect_developer_evidence.sh
```

---

## 3. Evidence 수집

```bash
./evidence/collect_developer_evidence.sh
```

정상 예:

```text
[RESULT] READY
[PATH] /.../results/20260925_153000
```

교육용 기준을 통과하지 못한 항목이 있다면 다음처럼 표시될 수 있습니다.

```text
[RESULT] NOT_READY
[FAILED] root_storage
```

`NOT_READY`는 프로그램 오류가 아니라 **하나 이상의 점검 항목이 기준을 통과하지 못했다는 의미**입니다.

---

## 4. 생성 결과 확인

```text
results/YYYYMMDD_HHMMSS/
├── evidence.json
└── evidence.md
```

가장 최근 결과 디렉터리 확인:

```bash
ls -dt results/*/ | head -n 1
```

Markdown Evidence 확인:

```bash
cat "$(ls -dt results/*/ | head -n 1)evidence.md"
```

---

## 5. 자동 수집 항목

- Ubuntu release
- Kernel / Architecture
- WSL 감지 여부
- Available Memory
- Root filesystem 사용률
- Network interface
- Routing 정보
- Loopback Ping
- Loopback TCP self-test
- ROS 2 CLI 존재 여부(참고 정보)

---

## 6. 교육용 READY 기준

```text
Ubuntu 22.04
x86_64
Available Memory >= 1 GiB
Root Storage Use < 90%
Loopback Ping PASS
Loopback TCP PASS
```

> 실제 제품 운영 기준이 아니라 본 실습을 위한 교육용 기준입니다.

---

## 7. NOT_READY가 나온 경우

`evidence.md`의 `Checks`와 `Failed checks`를 확인합니다.

예:

```text
Failed checks
root_storage
```

Workbook의 해당 Mission으로 돌아가 조치합니다.

```text
문제 확인
  ↓
조치
  ↓
수동 명령으로 재검증
  ↓
Evidence 다시 수집
```

Evidence를 다시 실행하면 기존 결과를 덮어쓰지 않고 새 디렉터리가 생성됩니다.

```text
results/
├── 20260925_153000/   ← 첫 번째 결과
└── 20260925_154500/   ← 재검증 결과
```

최종 보고서에는 **최종 검증 결과**의 경로를 기록합니다.

---

## 8. 결과 보고서에 기록할 Evidence

```text
results/<최종시간>/evidence.json
results/<최종시간>/evidence.md
```

학생은 다음 템플릿을 작성합니다.

```text
reports/05_result_report_template.md
```

Evidence 파일은 자동 생성된 원본이므로 내용을 임의로 수정하지 않습니다.
