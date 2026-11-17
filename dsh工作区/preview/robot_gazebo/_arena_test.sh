#!/usr/bin/env bash
# 与 zhirong_maps 比赛地图联调（源码目录直跑，自动解析地图 world 与 models 路径）
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
PKG="$WS/competition_ws/src/robot/robot_control"
cd "$WS"
source tools/gazebo_env.sh
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
LOG="$WS/preview/robot_gazebo/arena"
mkdir -p "$LOG"
cleanup() {
  kill -TERM -"$LAUNCH_PID" 2>/dev/null
  sleep 1
  pkill -x gzserver 2>/dev/null
}
trap cleanup EXIT

setsid ros2 launch "$PKG/launch/gazebo.launch.py" >"$LOG/launch.log" 2>&1 &
LAUNCH_PID=$!
for i in $(seq 1 180); do
  timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom 出现（等待 $i x0.5s）"; break; }
  sleep 0.5
done
sleep 1
echo '=== world 解析与插件加载 ==='
grep -E 'gazebo.launch.py|gazebo_ros_planar|joint_state_publisher|Spawn status' "$LOG/launch.log" | head -12
echo '=== 出生点 ==='
timeout 10 gz model -m zhirong_robot -p 2>&1
timeout 10 ros2 topic echo --once /odom 2>&1 | sed -n '1,12p'
echo '=== 场地模型抽查（含模型是否加载）==='
for m in ground arena_floor spawn_marker gate_entrance_n; do
  echo "--- $m ---"; timeout 10 gz model -m "$m" -p 2>&1 | head -2
done
echo '=== 前进 0.3m/s 3s ==='
(timeout 4 ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}" >/dev/null 2>&1) &
sleep 3.2
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
timeout 10 gz model -m zhirong_robot -p 2>&1
timeout 10 ros2 topic echo --once /odom 2>&1 | sed -n '1,12p'
echo '=== gzserver 警告（模型缺失等）==='
grep -E 'Unable to find model|Could not find|\[Err\]|\[Wrn\]' "$LOG/launch.log" | grep -v 'open display' | head -15
echo '=== log tail ==='
tail -20 "$LOG/launch.log"
