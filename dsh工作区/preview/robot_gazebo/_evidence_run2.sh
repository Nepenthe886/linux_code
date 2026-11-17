#!/usr/bin/env bash
# 最终验证 v2：确定性 publisher + 组 SIGINT（等价 Ctrl-C）干净退出
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
  gui:=false rviz:=false teleop:=none >"$OUT/launch_v2.log" 2>&1 &
LAUNCH_PID=$!
echo "launch_pid=$LAUNCH_PID" | tee "$OUT/run_summary_v2.txt"
for i in $(seq 1 180); do
  timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom ready after $i x0.5s" | tee -a "$OUT/run_summary_v2.txt"; break; }
  sleep 0.5
done
sleep 2

{
  echo '===== 启动后位姿 gz model -m zhirong_robot -p ====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 启动后 /odom ====='
  timeout 10 ros2 topic echo --once /odom | head -18
  echo; echo '===== TF odom->base_footprint ====='
  timeout 8 ros2 run tf2_ros tf2_echo odom base_footprint 2>&1 | head -6
} >"$OUT/v2_01_startup.txt" 2>&1

echo '=== 前进 vx=0.3, 2.0s（确定性 publisher）===' | tee -a "$OUT/run_summary_v2.txt"
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.3 0.0 0.0 2.0 2>&1 | tail -2
sleep 0.5
{
  echo '===== 前进后 gz model -p ====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 前进后 /odom ====='
  timeout 10 ros2 topic echo --once /odom | head -18
} >"$OUT/v2_02_forward.txt" 2>&1

echo '=== 横移 vy=0.3, 2.0s ===' | tee -a "$OUT/run_summary_v2.txt"
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.0 0.3 0.0 2.0 2>&1 | tail -2
sleep 0.5
{
  echo '===== 横移后 gz model -p ====='
  timeout 10 gz model -m zhirong_robot -p
  echo; echo '===== 横移后 /odom ====='
  timeout 10 ros2 topic echo --once /odom | head -18
} >"$OUT/v2_03_strafe.txt" 2>&1

echo '=== 组内 SIGINT（等价终端 Ctrl-C）===' | tee -a "$OUT/run_summary_v2.txt"
SHUTDOWN_START=$(date +%s.%N)
kill -INT -"$LAUNCH_PID" 2>/dev/null
EXITED=0
for i in $(seq 1 60); do
  if ! kill -0 "$LAUNCH_PID" 2>/dev/null; then EXITED=1; break; fi
  sleep 0.5
done
SHUTDOWN_END=$(date +%s.%N)
SHUTDOWN_SEC=$(python3 -c "print(f'{$SHUTDOWN_END-$SHUTDOWN_START:.1f}')")
if [ "$EXITED" = 1 ]; then
  echo "[ok] ros2 launch 已退出，用时 ${SHUTDOWN_SEC}s" | tee -a "$OUT/run_summary_v2.txt"
else
  echo "[warn] 30s 内 launch 未退出，补 SIGTERM" | tee -a "$OUT/run_summary_v2.txt"
  kill -TERM -"$LAUNCH_PID" 2>/dev/null; sleep 3
fi
sleep 2
{
  echo '===== 关闭后残留进程（期望为空）====='
  ps -ef | grep -E 'gzserver|gzclient|spawn_entity|robot_state_publisher|ros2 launch' | grep -v grep || echo '（无残留进程）'
  echo
  echo '===== launch log 尾部 ====='
  tail -20 "$OUT/launch_v2.log"
  echo
  echo '===== gzserver 启动日志（关闭后 buffer 已刷出）====='
  grep -E 'Loading world|gazebo_ros_init|planar_move|joint_state_publisher|\[Err\]|\[Wrn\]|Unable to find model' "$OUT/launch_v2.log" | head -25
} >"$OUT/v2_04_shutdown.txt" 2>&1
