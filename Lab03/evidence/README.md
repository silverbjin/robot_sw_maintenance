# Evidence 저장 안내

실습 결과 화면을 이 폴더에 저장합니다.

권장 파일명:

```text
01_os_ros_environment.png
02_ros2_install_complete.png
03_colcon_build.png
04_overlay_package.png
05_talker_listener.png
06_topic_info.png
07_environment_error.png
08_environment_recovery.png
```

## 필수 Evidence

1. `printenv ROS_DISTRO`와 `ros2 --help`
2. `Summary: 1 package finished`
3. `ros2 pkg prefix maintenance_check_pkg`
4. Talker의 `Publishing`과 Listener의 `I heard`
5. `ros2 topic info /chatter`
6. 오류 상태와 동일 명령 복구 성공 결과
