# 3회차 실습 워크북
## ROS 2 Humble 전체 설치 따라하기

> 기반 슬라이드: **슬라이드 6-2. 실습: ROS 2 Humble 전체 설치 따라하기**  
> 실습 환경: Ubuntu 22.04 LTS Desktop PC 또는 Ubuntu 22.04를 지원하는 ARM64 SBC

---

# 1. 실습 목표

실습을 마친 후 다음을 수행할 수 있어야 합니다.

1. Ubuntu 22.04 환경에 ROS 2 Humble을 설치한다.
2. ROS 2 개발 도구와 관련 패키지를 설치한다.
3. `source`와 `ROS_DISTRO`를 이용하여 ROS 2 환경 설정 상태를 확인한다.
4. Talker와 Listener를 실행하여 정상 통신 여부를 검증한다.
5. Desktop PC와 SBC의 공통 설치 절차와 차이를 구분한다.

---

# 2. 전체 실습 흐름

```
    A[Ubuntu 확인]
    --> B[UTF-8 Locale]
    --> C[Universe]
    --> D[ROS 2 apt 저장소]
    --> E[apt update / upgrade]
    --> F[ROS 2 Humble Desktop]
    --> G[ros-dev-tools]
    --> H[source]
    --> I[ROS_DISTRO]
    --> J[Talker / Listener]
    --> K[최종 검증]
```

> **실습 규칙:** 각 단계가 정상인지 확인한 후 다음 단계로 진행합니다.

---

# 실습 1. Ubuntu 환경 확인

## 1-1. Ubuntu 버전

```bash
lsb_release -a
```

정상 기준:

```text
Release: 22.04
Codename: jammy
```

## 1-2. CPU 아키텍처

```bash
uname -m
```

대표 결과:

```text
Desktop PC : x86_64
ARM64 SBC  : aarch64
```

## 기록

| 항목 | 결과 | 판정 |
|---|---|---|
| Release | | □ 정상 □ 오류 |
| Codename | | □ 정상 □ 오류 |
| Architecture | | |

완료 조건:

```text
□ Ubuntu 22.04
□ Jammy
□ CPU Architecture 확인
```

---

# 실습 2. UTF-8 Locale 확인 및 설정

## 2-1. 현재 Locale 확인

```bash
locale
```

`UTF-8`이 포함되어 있는지 확인합니다.

예:

```text
LANG=en_US.UTF-8
```

또는:

```text
LANG=ko_KR.UTF-8
```

이미 UTF-8이면 다음 실습으로 이동할 수 있습니다.

## 2-2. UTF-8 설정이 필요한 경우

```bash
sudo apt update
sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

확인:

```bash
locale
```

## 기록

```text
실습 전 LANG : ___________________________
실습 후 LANG : ___________________________
```

---

# 실습 3. Universe 저장소 활성화

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

완료:

```text
□ 오류 없이 종료
```

---

# 실습 4. ROS 2 apt 저장소 등록

## 4-1. curl 설치

```bash
sudo apt update
sudo apt install curl -y
```

## 4-2. 최신 ros2-apt-source 버전 확인

아래 명령을 한 줄로 실행합니다.

```bash
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
```

확인:

```bash
echo $ROS_APT_SOURCE_VERSION
```

정상 기준:

```text
빈 줄이 아니라 버전 문자열이 출력됨
```

## 4-3. 설치 파일 다운로드

```bash
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
```

확인:

```bash
ls -lh /tmp/ros2-apt-source.deb
```

## 4-4. 설치

```bash
sudo dpkg -i /tmp/ros2-apt-source.deb
```

기록:

```text
ROS_APT_SOURCE_VERSION = ______________________

설치 결과:
□ 정상
□ 오류
```

---

# 실습 5. Ubuntu 패키지 업데이트

```bash
sudo apt update
```

다음 오류가 있으면 다음 단계로 진행하지 않습니다.

```text
404 Not Found
NO_PUBKEY
repository is not signed
Temporary failure resolving
```

정상이라면:

```bash
sudo apt upgrade
```

질문이 나타나면 `Y`를 입력합니다.

## 기록

| 항목 | 결과 |
|---|---|
| `apt update` | □ 정상 □ 오류 |
| `apt upgrade` | □ 정상 □ 오류 |
| 저장소 오류 | □ 없음 □ 있음 |

---

# 실습 6. ROS 2 Humble Desktop 설치

```bash
sudo apt install ros-humble-desktop
```

설치 완료 후:

```bash
ls /opt/ros
```

정상:

```text
humble
```

세부 확인:

```bash
ls /opt/ros/humble
```

대표 항목:

```text
bin
include
lib
share
setup.bash
```

## 기록

```text
□ /opt/ros/humble 존재
□ setup.bash 존재
```

---

# 실습 7. 개발 도구 설치

```bash
sudo apt install ros-dev-tools
```

확인:

```bash
which colcon
which rosdep
```

## 기록

| 도구 | 출력 |
|---|---|
| colcon | |
| rosdep | |

---

# 실습 8. ROS 2 환경 적용

## 8-1. 적용 전 확인

새 터미널에서:

```bash
printenv ROS_DISTRO
```

아무것도 표시되지 않을 수 있습니다.

## 8-2. Humble 환경 적용

```bash
source /opt/ros/humble/setup.bash
```

## 8-3. 적용 후 확인

```bash
printenv ROS_DISTRO
```

정상:

```text
humble
```

## 기록

```text
source 전 ROS_DISTRO : ______________________
source 후 ROS_DISTRO : ______________________
```

### 질문

왜 두 결과가 다른가?

```text
____________________________________________________
____________________________________________________
```

---

# 실습 9. ROS 2 CLI 확인

```bash
ros2 --help
```

정상 기준:

```text
action
bag
daemon
interface
launch
node
param
pkg
run
service
topic
```

체크:

```text
□ ros2 명령 실행
□ command not found 없음
```

---

# 실습 10. 선택 — 새 터미널 자동 설정

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

확인:

```bash
printenv ROS_DISTRO
grep "source /opt/ros" ~/.bashrc
```

> 다른 ROS 2 배포판이 함께 등록되어 있다면 강사에게 확인합니다.

---

# 실습 11. Talker 실행

터미널 A:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

정상 예:

```text
[INFO] [talker]: Publishing: 'Hello World: 1'
[INFO] [talker]: Publishing: 'Hello World: 2'
```

체크:

```text
□ Publishing 반복
□ 번호 증가
□ 터미널 A 유지
```

---

# 실습 12. Listener 실행

터미널 B:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

정상 예:

```text
[INFO] [listener]: I heard: [Hello World: 1]
[INFO] [listener]: I heard: [Hello World: 2]
```

기록:

```text
Talker   : Hello World: _______
Listener : Hello World: _______
```

```text
□ 메시지 번호가 대응한다.
```

---

# 실습 13. Node / Topic 검증

터미널 C:

```bash
source /opt/ros/humble/setup.bash
ros2 node list
ros2 topic list
ros2 topic info /chatter
```

정상:

```text
/listener
/talker

Type: std_msgs/msg/String
Publisher count: 1
Subscription count: 1
```

메시지 직접 확인:

```bash
ros2 topic echo /chatter
```

중단: `Ctrl+C`

## 기록

| 항목 | 결과 |
|---|---|
| `/talker` | □ |
| `/listener` | □ |
| `/chatter` | □ |
| Publisher count | |
| Subscription count | |

---

# 실습 14. 최종 설치 판정

```text
□ Ubuntu 22.04 Jammy
□ UTF-8 Locale
□ Universe 활성화
□ ROS 2 apt 저장소
□ apt update/upgrade 정상
□ ros-humble-desktop 설치
□ ros-dev-tools 설치
□ /opt/ros/humble 존재
□ ROS_DISTRO=humble
□ ros2 --help 정상
□ Talker Publishing
□ Listener I heard
□ /talker, /listener
□ /chatter
□ Publisher 1
□ Subscription 1
```

최종:

```text
□ 정상 설치
□ 추가 점검 필요
```

---

# 참고 실습. Ubuntu 22.04 SBC의 차이점

공통점:

```text
Ubuntu 22.04
→ 저장소 설정
→ Humble 설치
→ source
→ ROS_DISTRO 확인
→ 노드 통신 검증
```

차이점:

| 항목 | Desktop PC | ARM64 SBC |
|---|---|---|
| CPU | `x86_64` | 주로 `aarch64` |
| GUI | 적극 사용 | 선택적 |
| RViz | 로컬 실행 | PC에서 실행 가능 |
| 저장 공간 | 상대적으로 여유 | 제한 가능 |
| 빌드 시간 | 비교적 빠름 | 더 느릴 수 있음 |
| 장치 | 개발 중심 | USB/Serial/GPIO 중요 |

실행 전용 SBC에서 GUI가 필요 없다면 강사의 지시에 따라 다음을 검토할 수 있습니다.

```bash
sudo apt install ros-humble-ros-base
```

> 본 과정의 **myAGV 2023 Jetson Nano**는 이 Ubuntu 22.04 Humble SBC 실습과 다릅니다.  
> 4회차에서는 제조사 제공 **Ubuntu 20.04 + ROS 2 Galactic 이미지**를 사용합니다.

---

# 학생 최종 자기점검

```text
□ Ubuntu 버전과 CPU 아키텍처를 확인할 수 있다.
□ ROS 2 저장소를 구성할 수 있다.
□ Humble Desktop과 개발 도구를 설치할 수 있다.
□ source 명령의 역할을 설명할 수 있다.
□ ROS_DISTRO가 humble인지 확인할 수 있다.
□ Talker/Listener로 통신을 검증할 수 있다.
□ 설치 파일 존재와 환경 적용을 구분할 수 있다.
□ Desktop과 SBC의 차이를 설명할 수 있다.
```
