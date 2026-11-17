#!/usr/bin/env bash
# =============================================================================
# 戎智杯反恐搜救 —— 系统依赖一键安装（Gazebo Classic 11 + ROS 2 Humble 桥接）
#
# 目的：把仿真环境统一装进系统（/opt/ros + /usr），使本工作空间可以整体
#       拷贝/迁移到任何 Ubuntu 22.04 + ROS 2 Humble 机器后，只需运行本脚本即可。
#
# 用法（需要 sudo 密码）：
#   sudo bash scripts/install_environment.sh
#
# 安装内容：
#   gazebo / gazebo-common                                   Gazebo Classic 11 仿真器
#   xvfb / mesa-utils                                        软件 OpenGL 虚拟显示 + GL 诊断（无 GPU 机器实时查看用）
#   ros-humble-gazebo-ros-pkgs / gazebo-plugins / gazebo-ros ROS 2 与 Gazebo 的桥接与插件
#   rosdep install --from-paths src                          按各包 package.xml 补齐其它依赖
# =============================================================================
set -eo pipefail

ROS_DISTRO="${ROS_DISTRO:-humble}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$HERE/.." && pwd)"

if [ "$(id -u)" -ne 0 ]; then
  echo "[错误] 本脚本需要 root 权限安装系统包，请用： sudo bash $0"
  exit 1
fi

echo "==============================================================="
echo "[1/3] 安装 Gazebo Classic 11 与 ROS 2 gazebo 桥接包 (ROS_DISTRO=$ROS_DISTRO)"
echo "==============================================================="
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  gazebo gazebo-common \
  "ros-${ROS_DISTRO}-gazebo-ros-pkgs" \
  "ros-${ROS_DISTRO}-gazebo-plugins" \
  "ros-${ROS_DISTRO}-gazebo-ros" \
  xvfb mesa-utils

echo "==============================================================="
echo "[2/3] 校验系统 Gazebo 与 ROS 桥接是否可用"
echo "==============================================================="
# shellcheck disable=SC1090
source "/opt/ros/${ROS_DISTRO}/setup.bash"
if ! command -v gzserver >/dev/null 2>&1; then
  echo "[错误] 系统里仍找不到 gzserver，请检查 apt 安装是否成功"
  exit 1
fi
if ! ros2 pkg prefix gazebo_ros >/dev/null 2>&1; then
  echo "[错误] ros2 找不到 gazebo_ros 包，请检查 ros-${ROS_DISTRO}-gazebo-ros 是否安装"
  exit 1
fi
echo "  gzserver: $(command -v gzserver)"
echo "  gazebo_ros: $(ros2 pkg prefix gazebo_ros)/share/gazebo_ros"

echo "==============================================================="
echo "[3/3] rosdep 补齐各包 package.xml 声明的其它依赖（以普通用户执行）"
echo "==============================================================="
USER_NAME="${SUDO_USER:-$(logname 2>/dev/null || echo "")}"
if [ -n "$USER_NAME" ] && [ "$USER_NAME" != "root" ]; then
  su - "$USER_NAME" -c "cd '$WS' && \
    source /opt/ros/${ROS_DISTRO}/setup.bash && \
    (rosdep install --from-paths src --ignore-src -r -y || \
     (echo '[提示] rosdep 失败（可能未初始化），可跳过：' ; \
      echo '  sudo rosdep init && rosdep update && rosdep install --from-paths src --ignore-src -r -y'))" || true
else
  echo "[提示] 未识别普通用户，跳过 rosdep；如缺依赖请手动执行："
  echo "  rosdep install --from-paths $WS/src --ignore-src -r -y"
fi

echo "==============================================================="
echo "[4/4] 创建 Python 虚拟环境并按 requirements.txt 安装依赖（以普通用户执行）"
echo "==============================================================="
if [ -n "$USER_NAME" ] && [ "$USER_NAME" != "root" ]; then
  su - "$USER_NAME" -c "bash '$WS/scripts/setup_python_env.sh'" || true
else
  bash "$WS/scripts/setup_python_env.sh" || true
fi

echo "==============================================================="
echo "安装完成。后续使用："
echo "  bash $WS/scripts/build.sh      # 构建工作空间"
echo "  bash $WS/scripts/run_sim.sh    # 启动比赛场景 + 机器人"
echo "  bash $WS/scripts/run_sim.sh gui:=true   # 有显示器时开 gzclient"
echo "  source $WS/.venv/bin/activate  # Python 依赖环境（requirements.txt）"
echo "==============================================================="
