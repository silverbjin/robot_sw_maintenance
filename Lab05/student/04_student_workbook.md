# 5회차 학생용 Workbook
## 로봇 소프트웨어 업그레이드 전 준비와 GO / NO-GO 판단

> 목표 상태: **READY FOR UPGRADE**

---

## 실습 전 확인

이번 회차에서는 Ubuntu, JetPack, ROS 2 Humble, Firmware를 변경하지 않는다. 실제 Robot Application의 Target Version 적용은 6회차에서 수행한다.

### 최종 산출물

- Upgrade Baseline
- Git Baseline (`pre-upgrade-v1`)
- Upgrade Plan
- GO / NO-GO Checklist
- 최종 판단 보고서

---

# LAB-01 — 업그레이드하지 않고 업그레이드를 준비한다

## 목적

현재 시스템을 먼저 설명할 수 있는 상태로 만들고, 이번 실습의 범위를 구분한다.

## 실습 범위 판단

이번 회차에서 수행하는 항목에 `[x]`를 표시한다.

- [ ] JetPack을 새 버전으로 변경한다.
- [ ] ROS 2 Humble을 다른 배포판으로 변경한다.
- [ ] Robot Application Target Version을 적용한다.
- [ ] 현재 OS / Jetson / ROS 2 / Git 상태를 조사한다.
- [ ] Upgrade Baseline을 작성한다.
- [ ] Upgrade Plan을 작성한다.
- [ ] GO / NO-GO를 판단한다.

### 학생 기록

이번 회차의 목적을 한 문장으로 작성한다.

> ____________________________________________________________________

### 판단 질문

오늘 실습의 종료 상태는 무엇인가?

- [ ] Upgrade Completed
- [ ] Ready for Upgrade

### 완료 체크

- [ ] 실제 업그레이드 실행과 사전 준비를 구분할 수 있다.
- [ ] 최종 산출물을 알고 있다.

---

# LAB-02 — OS와 Jetson 환경 확인

## 목적

현재 정상 동작 중인 Ubuntu와 Jetson Linux 상태를 Baseline으로 기록한다.

## STEP 1. Ubuntu 확인

### 명령

```bash
lsb_release -a
```

### 왜 실행하는가?

현재 운영체제의 배포판, Release, Codename을 확인하기 위해 실행한다.

### 예상 결과 패턴

```text
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.x LTS
Release:        22.04
Codename:       jammy
```

실제 세부 패치 버전은 환경에 따라 다를 수 있다.

### 학생 기록

| 항목 | 실제 확인값 |
|---|---|
| Distributor ID | |
| Description | |
| Release | |
| Codename | |

## STEP 2. Jetson Linux 확인

### 명령

```bash
cat /etc/nv_tegra_release
```

### 왜 실행하는가?

현재 Jetson Linux(L4T)의 Release와 Revision을 기록하기 위해 실행한다.

### 예상 결과 패턴

```text
# R36 (release), REVISION: x.x, ...
```

### 학생 기록

| 항목 | 실제 확인값 |
|---|---|
| Release (Rxx) | |
| Revision | |

### Evidence 수집

```bash
bash evidence/collect_system_baseline.sh
```

배포 폴더 밖에서 작업한다면 강사가 안내한 실제 스크립트 경로를 사용한다.

### 판단 질문

왜 “최신 버전인지”보다 “현재 정상 상태의 실제 값”을 먼저 기록해야 하는가?

> ____________________________________________________________________

### 완료 체크

- [ ] Ubuntu 정보를 실제 출력에서 기록했다.
- [ ] Jetson Linux Release/Revision을 기록했다.

---

# LAB-03 — JetPack과 ROS 2 버전 확인

## 목적

JetPack과 ROS 2를 각각 확인하고, 현재 정상적으로 동작 중인 버전 조합으로 기록한다.

## STEP 1. JetPack 관련 패키지 확인

```bash
apt list --installed 2>/dev/null | grep nvidia-jetpack
```

### 왜 실행하는가?

현재 시스템에서 `nvidia-jetpack` 메타 패키지가 보이는지 확인하기 위해 실행한다.

### 예상 결과 패턴

```text
nvidia-jetpack/... arm64 [installed]
```

아무 결과도 나오지 않으면 JetPack이 없다고 바로 단정하지 않는다. 앞서 확인한 Jetson Linux 정보를 기록하고 강사에게 확인한다.

### 학생 기록

| 항목 | 실제 확인값 |
|---|---|
| nvidia-jetpack 표시 여부 | |
| 표시된 버전 | |

## STEP 2. ROS 2 배포판 확인

```bash
printenv ROS_DISTRO
```

### 예상 결과

```text
humble
```

아무것도 출력되지 않는다면 강사 지시에 따라 현재 셸의 ROS 환경 설정을 확인한다.

### 학생 기록

| 항목 | 실제 확인값 |
|---|---|
| ROS_DISTRO | |

### Evidence 수집

```bash
bash evidence/collect_ros_baseline.sh
```

### 버전 조합 기록

```text
Ubuntu       : __________________
Jetson Linux : __________________
JetPack      : __________________
ROS 2        : __________________
```

### 판단 질문

왜 네 개의 버전을 각각 아는 것만으로는 충분하지 않은가?

> ____________________________________________________________________

### 완료 체크

- [ ] JetPack 정보를 기록했다.
- [ ] ROS 2 배포판을 기록했다.
- [ ] 전체 조합으로 판단해야 하는 이유를 설명할 수 있다.

---

# LAB-04 Robot Application 버전은 Git으로 남긴다

> Git이 처음이라면 먼저 `student/appendix_git_github_beginner.md`를 읽는다. 이번 로컬 실습에는 GitHub 계정이 없어도 된다.

## 목적

현재 정상 동작 중인 Robot Application을 다시 찾을 수 있도록 Commit과 Tag 기준점으로 기록한다.

## STEP 1. 현재 Git 상태 확인

```bash
git status
```

### 예상 결과 패턴

```text
On branch main
nothing to commit, working tree clean
```

### 학생 기록

- 현재 Branch: __________________
- Working Tree가 clean인가? YES / NO

## STEP 2. 최근 Commit 확인

```bash
git log --oneline -5
```

현재 HEAD Commit ID:

> ________________________________

## STEP 3. Tag 확인

```bash
git tag
```

현재 Tag:

> ____________________________________________________________________

## STEP 4. Baseline Tag 확인

강사가 준비한 데모 저장소에서는 다음 Tag를 사용한다.

```text
pre-upgrade-v1
```

확인:

```bash
git show --no-patch --decorate pre-upgrade-v1
```

실제 프로젝트에서 임의로 Tag를 추가·삭제하지 않는다. 강사가 별도 연습을 지시한 경우에만 Tag 생성 실습을 수행한다.

### Evidence 수집

Git 저장소 최상위에서 실행한다.

```bash
REPO_DIR="$PWD" bash evidence/collect_git_baseline.sh
```

### 판단 질문

단순히 “현재 코드가 있다”고 기록하는 것보다 Commit/Tag를 기록해야 하는 이유는 무엇인가?

> ____________________________________________________________________

### 완료 체크

- [ ] `git status`의 의미를 이해한다.
- [ ] 현재 Commit ID를 기록했다.
- [ ] `pre-upgrade-v1`이 Rollback 기준점임을 이해한다.

---

# LAB-05 — 슬라이드 14-2. 6회차용 Upgrade Plan 작성

## 목적

다음 회차의 변경 범위를 제한하고, 현재 버전부터 Rollback 방법까지 계획한다.

## 변경하지 않는 범위

- Ubuntu 22.04
- JetPack 6.x
- ROS 2 Humble
- Jetson Firmware / BSP

## 변경 예정 범위

- `myagv_bringup`: 일부 변경
- `myagv_monitor`: 신규 추가
- 관련 ROS 2 Node / Topic

## Upgrade Plan 작성

`reports/06_upgrade_plan_template.md`를 열어 다음 6개 항목을 작성한다.

### 1. 현재 버전

```text
ROS 2: Humble
Robot Application: pre-upgrade-v1
Current Commit: __________________
```

### 2. 대상 버전

강사가 제공한 6회차 Target Tag/Commit을 기록한다.

> ________________________________

### 3. 변경 이유

> ____________________________________________________________________

### 4. 영향 범위

변경하는 항목에 체크한다.

- [ ] Ubuntu
- [ ] JetPack
- [ ] ROS 2 배포판
- [ ] `myagv_bringup`
- [ ] `myagv_monitor`
- [ ] 관련 Node / Topic
- [ ] Firmware

### 5. Backup

- [ ] 현재 Commit ID
- [ ] `pre-upgrade-v1`
- [ ] 주요 설정 파일
- [ ] Baseline Evidence

### 6. Rollback 계획

빈칸을 채운다.

```text
문제 발생
  ↓
________________ 로 복귀
  ↓
재빌드
  ↓
환경 source
  ↓
기존 기능 ________________
```

### 완료 체크

- [ ] 현재 버전과 대상 버전을 구분했다.
- [ ] 변경하지 않는 범위를 명시했다.
- [ ] Backup과 Rollback 기준점을 작성했다.

---

# LAB-06 — 슬라이드 15. 업그레이드 GO / NO-GO 판단

## 목적

업그레이드 실행 준비가 충분한지 Evidence와 계획서를 근거로 최종 판단한다.

## 최종 체크리스트

`reports/07_go_no_go_checklist.md`를 작성한다.

| 구분 | 질문 | YES | NO |
|---|---|---:|---:|
| Baseline | 현재 정상 상태를 기록했는가? | [ ] | [ ] |
| Compatibility | Target과 현재 ROS 2 Humble 환경의 관계를 확인했는가? | [ ] | [ ] |
| Backup | 복구에 필요한 자료를 확보했는가? | [ ] | [ ] |
| Rollback | `pre-upgrade-v1`로 돌아가는 절차가 명확한가? | [ ] | [ ] |
| Upgrade Plan | 변경 범위·순서·검증 항목이 명확한가? | [ ] | [ ] |

### 판단 규칙

- 다섯 항목이 모두 YES → **GO 검토 가능**
- 하나라도 NO → **NO-GO**, 보완 후 다시 판단

### 최종 3문장 확인

1. 지금 정상 상태를 정확하게 알고 있는가? YES / NO
2. 문제가 생겨도 이전 정상 상태로 돌아갈 수 있는가? YES / NO
3. 무엇을 변경할지 명확한가? YES / NO

### 최종 판단

- [ ] GO — 6회차 진행 가능
- [ ] NO-GO — 미확인 항목 보완 필요

판단 근거:

> ____________________________________________________________________
>
> ____________________________________________________________________

### 완료 체크

- [ ] GO/NO-GO를 추측이 아니라 Evidence로 판단했다.
- [ ] NO-GO도 정상적인 유지보수 판단임을 이해한다.

---

# 최종 제출 체크리스트

- [ ] `01_system_baseline.txt`
- [ ] `02_ros_baseline.txt`
- [ ] `03_git_baseline.txt`
- [ ] `04_runtime_topics.txt` 또는 미실행 사유 기록
- [ ] `05_upgrade_baseline_template.md` 작성본
- [ ] `06_upgrade_plan_template.md` 작성본
- [ ] `07_go_no_go_checklist.md` 작성본
- [ ] `08_final_decision_report_template.md` 작성본
- [ ] 작성한 Upgrade Plan과 GO/NO-GO Checklist를 Evidence 디렉터리에 최종 반영했다.
- [ ] 최종 판단이 GO 또는 NO-GO로 명확하다.
- [ ] 판단 근거를 작성했다.

## 실습 종료 문장

> 현재 시스템의 정상 상태를 __________________ 로 기록하였고, 6회차에서는 ROS 2 Humble을 유지한 채 __________________ 와 __________________ 를 변경할 계획이다. 문제가 발생하면 __________________ 로 복귀하여 기존 기능을 재검증한다.


## Evidence 최종화

`collect_all.sh`로 생성된 run 디렉터리에 작성 완료한 계획서와 체크리스트를 포함시키고 checksum을 다시 만든다.

```bash
bash evidence/finalize_evidence.sh   results/<run_id>   reports/06_upgrade_plan_template.md   reports/07_go_no_go_checklist.md
```

최종 Evidence 디렉터리에는 `05_upgrade_plan.md`, `06_go_no_go.md`, `manifest.sha256`이 함께 있어야 한다.
