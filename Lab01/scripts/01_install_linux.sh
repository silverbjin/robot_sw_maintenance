#!/usr/bin/env bash
set -euo pipefail

if ! grep -q '22.04' /etc/os-release; then
  echo "[ERROR] This lab requires Ubuntu 22.04 (Jammy)."
  exit 1
fi

echo "[1/6] Base packages and UTF-8 locale"
sudo apt update
sudo apt install -y locales software-properties-common curl gnupg lsb-release x11-apps mesa-utils
sudo locale-gen en_US en_US.UTF-8 >/dev/null
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

echo "[2/6] Enable Ubuntu universe repository"
sudo add-apt-repository universe -y

echo "[3/6] Configure ROS 2 apt repository"
sudo mkdir -p /usr/share/keyrings
sudo curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
ARCH=$(dpkg --print-architecture)
CODENAME=$(. /etc/os-release && echo "$UBUNTU_CODENAME")
echo "deb [arch=${ARCH} signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu ${CODENAME} main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list >/dev/null

echo "[4/6] Install ROS 2 Humble + Gazebo Fortress integration"
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-ros-gz \
  ros-humble-ros-ign-bridge \
  python3-colcon-common-extensions \
  python3-rosdep \
  git

echo "[5/6] Configure shell"
LINE='source /opt/ros/humble/setup.bash'
grep -qxF "$LINE" "$HOME/.bashrc" || echo "$LINE" >> "$HOME/.bashrc"

# rosdep may already have been initialized on some images.
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
  sudo rosdep init || true
fi
rosdep update || true

echo "[6/6] Verification"
set +u
source /opt/ros/humble/setup.bash
set -u
printf 'ROS_DISTRO=%s\n' "${ROS_DISTRO:-unset}"
command -v ros2 >/dev/null && echo "[PASS] ros2"
command -v ign >/dev/null && echo "[PASS] ign (Gazebo Fortress CLI)"
ros2 pkg prefix ros_gz_bridge >/dev/null && echo "[PASS] ros_gz_bridge"
command -v rviz2 >/dev/null && echo "[PASS] rviz2"

echo
echo "Installation complete. Open a new WSL terminal, then run scripts/02_build_lab.sh"
