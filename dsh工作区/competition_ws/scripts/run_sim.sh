#!/usr/bin/env bash
# 启动比赛场景 + 机器人（Gazebo Classic 11）
# 用法:
#   bash scripts/run_sim.sh                     # headless（无 gzclient / rviz）
#   bash scripts/run_sim.sh gui:=true           # 有显示器时打开 gzclient
#   bash scripts/run_sim.sh gui:=true rviz:=true teleop:=keyboard
set -eo pipefail
ROS_DISTRO="${ROS_DISTRO:-humble}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$HERE/.." && pwd)"

# shellcheck disable=SC1090
source "/opt/ros/${ROS_DISTRO}/setup.bash"
if [ ! -f "$WS/install/setup.bash" ]; then
  echo "[错误] 还没构建，请先运行: bash $WS/scripts/build.sh"
  exit 1
fi
# shellcheck disable=SC1091
source "$WS/install/setup.bash"

# 清理上一次仿真残留（否则 Gazebo master 端口被占，新 gzserver 会以退出码 255 死掉）
if pgrep -x gzserver >/dev/null 2>&1 || pgrep -x gzclient >/dev/null 2>&1; then
  echo "[run_sim] 检测到残留 Gazebo 进程，先清理（详见 scripts/kill_sim.sh）..."
  bash "$HERE/kill_sim.sh"
fi

# 系统未装 Gazebo 时给出明确提示（gazebo.launch.py 也会自动检测用户态前缀并提示）
if ! ros2 pkg prefix gazebo_ros >/dev/null 2>&1; then
  echo "[警告] 当前环境找不到 gazebo_ros。统一安装请运行:"
  echo "       sudo bash $WS/scripts/install_environment.sh"
  echo "       （本机若已有用户态 Gazebo 前缀，launch 会自动注入并继续）"
fi

# 优先使用 bring_up 一键启动包（统一入口）；未构建时回退 robot_control 的 launch
if ros2 pkg prefix bring_up >/dev/null 2>&1; then
  exec ros2 launch bring_up bring_up.launch.py "$@"
else
  echo "[run_sim][提示] 没找到 bring_up 包，回退 robot_control/gazebo.launch.py（先 bash scripts/build.sh 可获得一键启动包）"
  exec ros2 launch robot_control gazebo.launch.py "$@"
fi
