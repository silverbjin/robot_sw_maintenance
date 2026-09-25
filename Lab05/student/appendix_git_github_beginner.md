# 별첨 — Git / GitHub 초보자 시작 가이드

## 1. Git과 GitHub는 다르다

**Git**은 내 PC나 Jetson에서 파일 변경 이력을 관리하는 버전 관리 프로그램이다.  
**GitHub**는 Git 저장소를 인터넷에 저장하고 협업할 수 있게 해 주는 서비스이다.

> 이번 5회차 로컬 Git 실습은 **GitHub 계정이 없어도** 진행할 수 있다.

## 2. Git 설치 여부 확인

```bash
git --version
```

설치되어 있다면 `git version ...`이 표시된다. 설치가 필요하면 강사의 사전 준비 지시를 따른다.

## 3. Git 작성자 정보 확인

```bash
git config --global user.name
git config --global user.email
```

개인 실습 환경에서 비어 있다면 다음 형식으로 설정할 수 있다.

```bash
git config --global user.name "홍길동"
git config --global user.email "student@example.com"
```

교육장 공용 PC에서는 강사 지시에 따른다.

## 4. GitHub 계정은 언제 필요한가?

원격 GitHub 저장소를 clone/push하거나 개인 저장소를 만들 때 필요할 수 있다. 회원가입은 `https://github.com/signup`에서 진행할 수 있다.

이번 실습처럼 강사가 준비한 **로컬 저장소**에서 아래 명령을 사용하는 데에는 GitHub 로그인이 필요하지 않다.

```bash
git status
git log --oneline -5
git tag
git show --no-patch --decorate pre-upgrade-v1
```

## 5. 핵심 용어

### Repository
Git으로 변경 이력을 관리하는 프로젝트 저장소.

### Commit
특정 시점의 파일 상태와 변경 내용을 기록한 단위.

### Commit ID
각 Commit을 식별하는 고유한 값.

### Tag
특정 Commit에 `pre-upgrade-v1` 같은 의미 있는 이름을 붙인 기준점.

### Working Tree
현재 직접 수정하고 있는 파일의 상태.

## 6. 이번 실습의 명령 순서

```text
git status
   ↓
git log --oneline -5
   ↓
git tag
   ↓
git show --no-patch --decorate pre-upgrade-v1
```

## 7. 자주 발생하는 오류

### `fatal: not a git repository`

Git 저장소가 아닌 폴더에 있다.

```bash
pwd
ls -la
```

강사가 지정한 `~/lab05_ros2_ws`로 이동한 뒤 다시 확인한다.

### `Author identity unknown`

직접 Commit이나 annotated Tag를 만드는 실습에서 작성자 정보가 없을 때 나타날 수 있다. `git config` 설정을 확인하고 강사에게 문의한다.

### `pre-upgrade-v1 already exists`

이미 Baseline Tag가 준비되어 있다는 의미일 수 있다. 삭제하지 말고 다음 명령으로 내용을 확인한다.

```bash
git show --no-patch --decorate pre-upgrade-v1
```

## 8. 안전 원칙

- 강사가 제공한 실제 프로젝트의 Tag나 Commit을 임의로 삭제하지 않는다.
- Git 초보자는 강사용 데모 저장소에서 먼저 연습한다.
- 5회차의 목적은 Target Version으로 이동하는 것이 아니라 **현재 기준점을 기록하는 것**이다.
