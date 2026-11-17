#!/usr/bin/env bash
# 构建工作空间（系统 ROS 环境；无需任何用户态 Gazebo 环境脚本）
# 用法: bash scripts/build.sh
set -eo pipefail
ROS_DISTRO="${ROS_DISTRO:-humble}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$HERE/.." && pwd)"

# shellcheck disable=SC1090
source "/opt/ros/${ROS_DISTRO}/setup.bash"
cd "$WS"
echo "[build] 工作空间: $WS"
colcon build --symlink-install "$@"
# shellcheck disable=SC1091
source "$WS/install/setup.bash"
echo "[build] 完成。启动仿真： bash $WS/scripts/run_sim.sh"
