#!/usr/bin/env bash
# 空世界运动学验证：前进 / 横移 / 原地旋转，确定性 publisher，不含障碍物碰撞干扰
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
cd "$WS"
source tools/gazebo_env.sh
. competition_ws/install/setup.bash
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
OUT="$WS/preview/robot_gazebo/evidence"
mkdir -p "$OUT"
TW="$WS/competition_ws/install/robot_control/share/robot_control/worlds/test/gazebo_test.world"
cleanup() { pkill -x gzserver 2>/dev/null; }
trap cleanup EXIT

setsid ros2 launch robot_control gazebo.launch.py \
  world:="$TW" x:=0.0 y:=0.0 z:=0.05 yaw:=0.0 gui:=false rviz:=false teleop:=none \
  >"$OUT/testworld_launch.log" 2>&1 &
LAUNCH_PID=$!
for i in $(seq 1 180); do
  timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && break
  sleep 0.5
done
sleep 2

{
  echo '===== 初始 gz model -p ====='; timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 初始 /odom ====='; timeout 10 ros2 topic echo --once /odom | head -16
} >"$OUT/tw_01_startup.txt" 2>&1

echo '=== 前进 vx=0.3 2.0s ==='
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.3 0.0 0.0 2.0 2>&1 | tail -1
sleep 0.5
{
  echo '===== 前进后 gz model -p（期望 x +0.6, y≈0, yaw≈0）====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 前进后 /odom ====='; timeout 10 ros2 topic echo --once /odom | head -16
} >"$OUT/tw_02_forward.txt" 2>&1

echo '=== 横移 vy=0.3 2.0s ==='
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.0 0.3 0.0 2.0 2>&1 | tail -1
sleep 0.5
{
  echo '===== 横移后 gz model -p（期望 y +0.6, x≈不变, yaw≈0）====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 横移后 /odom ====='; timeout 10 ros2 topic echo --once /odom | head -16
} >"$OUT/tw_03_strafe.txt" 2>&1

echo '=== 原地旋转 wz=0.5 2.0s ==='
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.0 0.0 0.5 2.0 2>&1 | tail -1
sleep 0.5
{
  echo '===== 旋转后 gz model -p（期望 yaw +1.0）====='
  timeout 10 gz model -m zhirong_robot -p
} >"$OUT/tw_04_rotate.txt" 2>&1

kill -INT -"$LAUNCH_PID" 2>/dev/null
for i in $(seq 1 60); do kill -0 "$LAUNCH_PID" 2>/dev/null || break; sleep 0.5; done
sleep 1
{
  echo '===== 关闭后残留（期望为空）====='
  ps -ef | grep -E 'gzserver|gzclient|ros2 launch|robot_state_publisher' | grep -v grep || echo '（无残留进程）'
} >"$OUT/tw_05_shutdown.txt" 2>&1
