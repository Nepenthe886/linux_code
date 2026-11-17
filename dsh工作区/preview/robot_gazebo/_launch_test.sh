#!/usr/bin/env bash
# gazebo.launch.py 源码目录直跑验证（headless）：启动 -> 话题/TF -> /cmd_vel 前进/横移
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
PKG="$WS/competition_ws/src/robot/robot_control"
cd "$WS"
source tools/gazebo_env.sh
unset DISPLAY                       # 本机 X :1 GLX 坏，headless
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
LOG="$WS/preview/robot_gazebo/launch"
mkdir -p "$LOG"
cleanup() {
  kill -TERM -"$LAUNCH_PID" 2>/dev/null
  sleep 1
  pkill -x gzserver 2>/dev/null
  pkill -x gzclient 2>/dev/null
}
trap cleanup EXIT

setsid ros2 launch "$PKG/launch/gazebo.launch.py" >"$LOG/launch.log" 2>&1 &
LAUNCH_PID=$!
echo "launch pid=$LAUNCH_PID"

wait_topic() {
  for i in $(seq 1 120); do
    if timeout 5 ros2 topic list 2>/dev/null | grep -qx "$1"; then echo "[ok] 话题 $1 出现（等待 $((i)) x0.5s）"; return 0; fi
    sleep 0.5
  done
  echo "[FAIL] 等不到话题 $1"; return 1
}
wait_topic /clock || exit 1
wait_topic /joint_states || exit 1
wait_topic /odom || exit 1
sleep 1

echo '=== launch log: 关键行 ==='
grep -E 'gazebo.launch.py|spawn_entity|Spawn|error|Error|错误|警告' "$LOG/launch.log" | head -20

echo '=== /clock 采样 ==='
timeout 10 ros2 topic echo --once /clock 2>&1 | head -8

echo '=== /joint_states 采样 ==='
timeout 10 ros2 topic echo --once /joint_states 2>&1 | head -12

echo '=== /odom 初始 ==='
timeout 10 ros2 topic echo --once /odom 2>&1 | head -24

echo '=== TF odom -> base_footprint ==='
timeout 8 ros2 run tf2_ros tf2_echo odom base_footprint 2>&1 | grep -A3 -m1 'At time' | head -6

echo '=== 初始位姿（gz model -p: x y z roll pitch yaw）==='
timeout 10 gz model -m zhirong_robot -p 2>&1

echo '=== 发送 /cmd_vel 前进 0.3 m/s x 3s ==='
(timeout 4 ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}" >/dev/null 2>&1) &
sleep 3.2
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
echo '--- 位姿 ---'; timeout 10 gz model -m zhirong_robot -p 2>&1
echo '--- /odom ---'; timeout 10 ros2 topic echo --once /odom 2>&1 | head -24

echo '=== 发送 /cmd_vel 左移 -0.3 m/s x 3s ==='
(timeout 4 ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {y: 0.3}}" >/dev/null 2>&1) &
sleep 3.2
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
echo '--- 位姿 ---'; timeout 10 gz model -m zhirong_robot -p 2>&1
echo '--- /odom ---'; timeout 10 ros2 topic echo --once /odom 2>&1 | head -24

echo '=== gzservice 模型列表 ==='
timeout 10 gz model -m zhirong_robot -i 2>&1 | head -12

echo '=== launch log tail ==='
tail -30 "$LOG/launch.log"
