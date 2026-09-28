# 기존 사용자 매뉴얼 발췌 — 개선 전

> 교육용 샘플 문서입니다.

## 3.1 `ping` 사용 방법

로봇과 PC 간 네트워크 연결 상태를 확인한다.

```bash
ping <robot-ip>
```

## 3.2 `ros2 node list` 사용 방법

현재 실행 중인 ROS 2 노드 목록을 확인한다.

```bash
ros2 node list
```

## 3.3 `ros2 topic list` 사용 방법

현재 사용 가능한 ROS 2 토픽 목록을 확인한다.

```bash
ros2 topic list
```

## 3.4 `ros2 topic echo` 사용 방법

지정한 토픽의 데이터를 확인한다.

```bash
ros2 topic echo <topic>
```

## 3.5 시스템 재시작

필요한 경우 시스템 서비스를 재시작한다.

```bash
sudo systemctl restart myagv_bringup
```

---

## 학생 분석 질문

- 개별 명령어 설명은 존재합니까?
- “로봇이 움직이지 않을 때” 어떤 순서로 확인해야 하는지 제시되어 있습니까?
- 정상/비정상 결과를 구분할 기준이 충분합니까?
- 언제 재시작해야 하는지 판단 기준이 있습니까?
- 해결되지 않을 때 무엇을 기록하여 보고해야 하는지 제시되어 있습니까?
