#!/usr/bin/env bash
# 最终验证（colcon 安装后）：启动 -> 话题/TF -> 前进 -> 横移 -> SIGINT 干净退出 -> 无残留进程
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
cleanup() { pkill -x gzserver 2>/dev/null; }
trap cleanup EXIT

setsid ros2 launch robot_control gazebo.launch.py \
  gui:=false rviz:=false teleop:=none >"$OUT/launch.log" 2>&1 &
LAUNCH_PID=$!
echo "launch_pid=$LAUNCH_PID" | tee "$OUT/run_summary.txt"

for i in $(seq 1 180); do
  timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom ready after $i x0.5s" | tee -a "$OUT/run_summary.txt"; break; }
  sleep 0.5
done
sleep 1
{
  echo '===== ros2 topic list ====='
  timeout 10 ros2 topic list
  echo; echo '===== /clock ====='
  timeout 10 ros2 topic echo --once /clock
  echo; echo '===== /joint_states (完整) ====='
  timeout 10 ros2 topic echo --once /joint_states
  echo; echo '===== TF odom -> base_footprint ====='
  timeout 8 ros2 run tf2_ros tf2_echo odom base_footprint 2>&1 | head -6
  echo; echo '===== 初始位姿 gz model -p (x y z r p yaw) ====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 初始 /odom ====='
  timeout 10 ros2 topic echo --once /odom | head -20
} >"$OUT/01_startup.txt" 2>&1

echo '=== 前进 linear.x=0.3, 3s ===' | tee -a "$OUT/run_summary.txt"
(timeout 4 ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}" >/dev/null 2>&1) &
sleep 3.2
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
{
  echo '===== 前进后 gz model -p ====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 前进后 /odom ====='
  timeout 10 ros2 topic echo --once /odom | head -20
} >"$OUT/02_forward.txt" 2>&1

echo '=== 横移 linear.y=0.3, 3s ===' | tee -a "$OUT/run_summary.txt"
(timeout 4 ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {y: 0.3}}" >/dev/null 2>&1) &
sleep 3.2
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
{
  echo '===== 横移后 gz model -p ====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 横移后 /odom ====='
  timeout 10 ros2 topic echo --once /odom | head -20
  echo; echo '===== 模型名/静态标志 ====='
  timeout 10 gz model -m zhirong_robot -i | head -8
} >"$OUT/03_strafe.txt" 2>&1

echo '=== 发 SIGINT 关闭 launch（模拟 Ctrl-C）==='
kill -INT "$LAUNCH_PID" 2>/dev/null
for i in $(seq 1 40); do
  if ! kill -0 "$LAUNCH_PID" 2>/dev/null; then echo "[ok] ros2 launch 已退出（等待 $i x0.5s）" | tee -a "$OUT/run_summary.txt"; break; fi
  sleep 0.5
done
sleep 2
{
  echo '===== 关闭后残留进程检查（期望为空）====='
  ps -ef | grep -E 'gzserver|gzclient|spawn_entity|robot_state_publisher|ros2 launch' | grep -v grep || echo '（无残留进程）'
  echo
  echo '===== launch 退出日志尾部 ====='
  tail -25 "$OUT/launch.log"
} >"$OUT/04_shutdown.txt" 2>&1
