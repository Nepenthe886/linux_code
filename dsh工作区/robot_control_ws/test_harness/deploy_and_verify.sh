#!/usr/bin/env bash
# Deploy robot_control into the Zhirong Cup colcon workspace, build it and
# verify the installed launch chain end to end (headless).
set -euo pipefail

WS="/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws"
TARGET="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
SRC="$WS/src/robot_control"
DST="$TARGET/src/robot/robot_control"

echo "== 1/4 部署源码包 -> $DST"
mkdir -p "$DST"
rsync -a --delete \
  --exclude '__pycache__' --exclude '.pytest_cache' --exclude '*.pyc' \
  "$SRC/" "$DST/"
# 目标源码树里可能残留上次验证生成的字节码/测试缓存（--delete 不会删除被
# exclude 的项），显式清理，保证交付目录干净。
find "$DST" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
rm -rf "$DST/.pytest_cache"
find "$DST" -type f | sort | sed 's/^/   /'

echo "== 2/4 目标工作区 colcon build（先清掉旧包构建产物，避免 symlink_data 脏状态）"
cd "$TARGET"
rm -rf "$TARGET/build/robot_control" "$TARGET/install/robot_control"
set +u
source /opt/ros/humble/setup.bash
set -u
export ROS_HOME="$WS/ros_home"
export ROS_LOG_DIR="$WS/ros_logs"
export ROS_DOMAIN_ID=81
export ROS_LOCALHOST_ONLY=1
export PYTHONDONTWRITEBYTECODE=1
colcon --log-base log build --symlink-install --packages-select robot_control 2>&1 | tail -6

echo "== 3/4 目标安装校验 + pytest"
set +u
source install/setup.bash
set -u
echo "robot_control prefix: $(ros2 pkg prefix robot_control)"
echo "robot_description prefix: $(ros2 pkg prefix robot_description)"
cd "$DST"
python3 -m pytest test -q -p no:cacheprovider 2>&1 | tail -3

echo "== 源码与部署副本一致性校验"
diff -r --exclude='__pycache__' "$SRC" "$DST" && echo "   OK: 部署副本与开发工作区一致"

echo "== 4/4 安装后 launch + 麦轮驱动链路验证（无 GUI/RViz）"
cd "$TARGET"
LOG="$WS/target_launch_check.log"
DOMAIN=$(( (RANDOM % 100) + 120 ))
ROS_DOMAIN_ID="$DOMAIN" setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false gui:=false > "$LOG" 2>&1 &
LAUNCH=$!
cleanup() {
  kill -INT -- -"$LAUNCH" 2>/dev/null || true
  sleep 3
  kill -TERM -- -"$LAUNCH" 2>/dev/null || true
  sleep 1
  kill -KILL -- -"$LAUNCH" 2>/dev/null || true
}
trap cleanup EXIT
for _ in $(seq 1 30); do
  grep -q "mecanum_sim 启动" "$LOG" 2>/dev/null && break
  sleep 1
done
sleep 2
ROS_DOMAIN_ID="$DOMAIN" python3 "$WS/test_harness/check_drive.py"
echo "== 目标工作区部署与验证完成"
