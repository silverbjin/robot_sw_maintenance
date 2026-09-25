# Upgrade Plan Template

> 6회차 예정 범위: ROS 2 Humble은 유지하고 Robot Application만 변경한다.

## 1. 현재 버전

- ROS 2: Humble (유지)
- Robot Application Baseline Tag: `pre-upgrade-v1`
- Current Commit ID:

## 2. 대상 버전

- Target Tag / Commit:
- `myagv_bringup`: 일부 변경
- `myagv_monitor`: 신규 모듈 추가

## 3. 변경 이유

> 

## 4. 영향 범위

### 변경함

- [ ] `myagv_bringup`
- [ ] `myagv_monitor`
- [ ] 관련 ROS 2 Node / Topic

### 변경하지 않음

- [ ] Ubuntu 22.04
- [ ] JetPack 6.x
- [ ] ROS 2 Humble
- [ ] Jetson Firmware / BSP

영향 범위 설명:

> 

## 5. Backup

- [ ] Current Commit ID 기록
- [ ] `pre-upgrade-v1` Tag 확인
- [ ] 주요 설정 파일 보관
- [ ] Upgrade Baseline 저장
- [ ] 추가 Backup:

## 6. Rollback 계획

문제 발생 시 기준점:

> `pre-upgrade-v1`

예상 절차:

```text
pre-upgrade-v1 복귀
    ↓
재빌드
    ↓
source install/setup.bash
    ↓
기존 기능 재검증
```

추가 메모:

> 
