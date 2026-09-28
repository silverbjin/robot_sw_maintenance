# Lab09 사용자 FAQ — LiDAR 상태 확인과 기본 대응

이 FAQ는 **Node → Topic → Data → RViz** 결과를 바탕으로 다음 행동을 선택하기 위한 자료입니다.

## 빠른 찾기

| 관찰 상태 | FAQ |
|---|---|
| 관련 Node가 보이지 않음 | FAQ-01 |
| Node는 있으나 `/scan`이 없음 | FAQ-02 |
| `/scan`은 있으나 Data가 수신되지 않음 | FAQ-03 |
| Data는 정상이나 RViz에 표시되지 않음 | FAQ-04 |

여러 상태가 비정상이라면 **Node → Topic → Data 순서에서 처음 FAIL인 지점**부터 확인합니다.

---

## FAQ-01. 관련 Node가 보이지 않는다

### 증상

```text
Node  : FAIL
Topic : 확인 전 또는 FAIL
Data  : 확인 전 또는 FAIL
```

### 먼저 확인

1. 로봇/센서 전원 상태
2. 정상 시작 절차 수행 여부
3. 올바른 ROS 환경인지 확인

```bash
echo $ROS_DISTRO
ros2 node list
```

### 기본 조치

- 사용자 매뉴얼에서 허용한 시작 절차를 1회 수행
- 허용된 경우에만 프로그램을 1회 재실행

### 정상 결과

관련 Node가 다시 보입니다. 그 다음 `/scan`을 확인합니다.

### 해결되지 않으면

증상, 발생 시점, Node 목록, ROS_DISTRO, 수행 조치를 담당자에게 보고합니다.

---

## FAQ-02. Node는 있으나 `/scan` Topic이 없다

### 증상

```text
Node  : PASS
Topic : FAIL
Data  : 확인 불가
```

### 먼저 확인

```bash
ros2 node list
ros2 topic list
```

- 실제 장비의 Topic 이름이 `/scan`인지 매뉴얼 확인
- 교육 실습에서는 기준 Topic이 `/scan`인지 확인

### 기본 조치

- 허용된 LiDAR 시작 절차 재확인
- 매뉴얼에서 허용한 경우에만 프로그램 1회 재실행

### 정상 결과

```text
/scan
```

이 나타난 뒤 Data를 확인합니다.

### 해결되지 않으면

Node 이름, 전체 Topic 목록, 기대 Topic 이름, 수행 조치를 보고합니다.

---

## FAQ-03. `/scan`은 존재하지만 Data가 수신되지 않는다

### 증상

```text
Node  : PASS
Topic : PASS
Data  : FAIL
```

### 먼저 확인

실제 장비라면:

1. LiDAR 전원
2. 케이블 연결
3. USB 연결
4. 네트워크 연결
5. 사용자가 확인 가능한 상태 LED

교육용 Mock 환경에서는 장비를 임의로 분리하지 말고 교육자 안내를 따릅니다.

### 기본 조치

- 외부 연결을 다시 확인
- 매뉴얼에 허용된 경우 LiDAR 프로그램 1회 재실행
- 조치 후 반드시 Data를 다시 확인

```bash
timeout 4s ros2 topic hz /scan
```

### 정상 결과

메시지가 다시 주기적으로 수신됩니다.

### 해결되지 않으면

Node/Topic/Data 결과, 외부 연결 상태, 수행 조치, 조치 후 결과를 담당자에게 전달합니다.

---

## FAQ-04. `/scan` Data는 정상이나 RViz 2에 표시되지 않는다

### 증상

```text
Node  : PASS
Topic : PASS
Data  : PASS
RViz  : FAIL
```

### 먼저 확인

1. RViz LaserScan Display가 활성화되어 있는지 확인
2. LaserScan Topic이 `/scan`인지 확인
3. Fixed Frame이 교육자가 지정한 Frame인지 확인
4. RViz Status에 Error/Warning이 있는지 확인

### 기본 조치

- GUI에서 교육자가 지정한 Topic/Fixed Frame으로 되돌림
- Display를 다시 활성화
- 사용자가 임의로 ROS config 파일이나 TF 코드를 수정하지 않음

### 정상 결과

Data는 계속 수신되며 RViz에 LaserScan이 다시 표시됩니다.

### 해결되지 않으면

`/scan` Data 결과, RViz Topic, Fixed Frame, RViz Status 메시지를 보고합니다.

---

# 공통 금지 작업

```text
config 파일 임의 변경 ×
드라이버 임의 재설치 ×
소스 코드 변경 ×
패키지 임의 삭제/설치 ×
OS 업데이트 ×
하드웨어 분해 ×
```

핵심 원칙:

> **확인·허용된 복구·검증·보고 = 사용자 영역**  
> **변경·수정 = 유지보수 담당자 영역**
