#!/usr/bin/env python3
"""Create a Lab09 student result report prefilled only with collected evidence.

The generated report intentionally leaves judgment, FAQ choice, user action,
and final VERIFY/REPORT decision for the learner to complete.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def read_kv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def build_report(session_dir: Path) -> str:
    summary = read_kv(session_dir / "summary.txt")
    system = read_kv(session_dir / "system_info.txt")
    node = summary.get("Node", "UNKNOWN")
    topic = summary.get("Topic", "UNKNOWN")
    data = summary.get("Data", "UNKNOWN")
    captured = system.get("captured_at", "unknown")
    ros_distro = system.get("ROS_DISTRO", "unknown")
    mode = system.get("LAB09_MODE", "unknown")
    scan_topic = system.get("SCAN_TOPIC", "/scan")
    session = summary.get("session", session_dir.name)

    return f"""# Lab09 사용자 실습 수행 결과 보고서 — Evidence 연동본

> 자동 입력 영역은 `collect_evidence.sh`가 수집한 사실만 반영합니다.  
> **증상 해석, FAQ 선택, 기본 조치, 최종 VERIFY/REPORT 판단은 학습자가 직접 작성하십시오.**

## 1. 기본 정보

- Evidence 세션: `{session}`
- Evidence 수집 시각: `{captured}`
- ROS_DISTRO: `{ros_distro}`
- 실습 모드: `{mode}`
- Scan Topic: `{scan_topic}`
- 학습자: ____________________

## 2. 발생한 증상

발생한 증상:

```text
____________________________________________________________
```

발생 시점: ____________________

## 3. 자동 수집된 상태 Evidence

Node 확인 결과: **{node}**

Topic 확인 결과: **{topic}**

Data 확인 결과: **{data}**

> 위 값은 보고서 생성 시점의 상태입니다. 문제 발생 시점에 별도로 기록한 결과와 구분하십시오.

문제 발생 시점의 Node/Topic/Data 기록:

```text
Node  : ____________________
Topic : ____________________
Data  : ____________________
```

현재 Evidence로 좁힌 문제 영역:

```text
____________________________________________________________
```

## 4. FAQ 선택

선택한 FAQ: ____________________

선택 근거:

```text
____________________________________________________________
____________________________________________________________
```

## 5. 수행한 기본 조치

수행한 기본 조치:

```text
1. __________________________________________________________
2. __________________________________________________________
3. __________________________________________________________
```

사용자 허용 범위를 벗어난 변경을 수행하지 않았는지 확인:

- [ ] config 임의 수정 없음
- [ ] 드라이버/패키지 임의 설치·삭제 없음
- [ ] 코드 수정 없음
- [ ] OS 업데이트 없음
- [ ] 하드웨어 분해 없음

## 6. 조치 후 결과

조치 후 결과:

```text
Node  : ____________________
Topic : ____________________
Data  : ____________________
RViz  : ____________________
```

재검증 Evidence:

```text
____________________________________________________________
```

## 7. 최종 판단 — VERIFY / REPORT

- [ ] **VERIFY** — 정상 복구를 Evidence로 확인함
- [ ] **REPORT** — 사용자 범위에서 해결되지 않아 담당자에게 보고함

판단 근거:

```text
____________________________________________________________
```

## 8. 미해결 시 담당자 보고

- 발생한 증상: ____________________
- 발생 시점: ____________________
- Node 확인 결과: ____________________
- Topic 확인 결과: ____________________
- Data 확인 결과: ____________________
- 선택한 FAQ: ____________________
- 수행한 기본 조치: ____________________
- 조치 후 결과: ____________________
- Evidence 저장 위치: `{session_dir}`

## 9. Evidence 첨부

Evidence 저장 디렉토리: `{session_dir}`

- `system_info.txt`
- `node_list.txt`
- `topic_list.txt`
- `topic_info.txt`
- `scan_hz.txt`
- `lidar_state.txt`
- `normal_state.txt`
- `summary.txt`
- `SHA256SUMS`

> `SHA256SUMS`는 원본 Evidence 파일을 대상으로 생성됩니다. 이 `result_report.md`는 학생이 작성·수정하는 문서이므로 해시 목록에서 제외됩니다.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_dir", type=Path)
    args = parser.parse_args()
    session_dir = args.session_dir.resolve()
    required = [session_dir / "summary.txt", session_dir / "system_info.txt"]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        parser.error("missing evidence file(s): " + ", ".join(missing))
    output = session_dir / "result_report.md"
    output.write_text(build_report(session_dir), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
