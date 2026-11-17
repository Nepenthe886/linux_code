#!/usr/bin/env bash
# 基线实验：空世界 spawn 原始 URDF，观察落地高度与基础话题
# 关键环境：unset DISPLAY（GLX 坏）、GAZEBO_MASTER_URI 专用端口、补 gazebo_msgs python 路径
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
cd "$WS"
source tools/gazebo_env.sh
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
export PYTHONPATH="$PREFIX/opt/ros/humble/local/lib/python3.10/dist-packages:${PYTHONPATH:-}"
LOG="$WS/preview/robot_gazebo/baseline"
mkdir -p "$LOG"
cleanup() { pkill -x gzserver 2>/dev/null; }
trap cleanup EXIT

gzserver --verbose -s libgazebo_ros_init.so -s libgazebo_ros_factory.so \
  "$PREFIX/opt/ros/humble/share/gazebo_ros/worlds/empty.world" >"$LOG/gzserver.log" 2>&1 &
for i in $(seq 1 60); do
  timeout 5 ros2 topic list 2>/dev/null | grep -q '^/clock$' && { echo "clock ready after ${i}x0.5s"; break; }
  sleep 0.5
done
echo "=== gz model -m robot? (无模型时) ==="
timeout 5 gz model -m nothing -i 2>&1 | head -2
echo "=== topics ==="
timeout 10 ros2 topic list 2>&1 | head -20
echo "=== spawn ==="
timeout 60 ros2 run gazebo_ros spawn_entity.py \
  -file "$WS/competition_ws/src/robot/robot_description/urdf/omni_robot.urdf" \
  -entity zhirong_robot -x 0.5 -y 0.2 -z 0.06 -Y 1.57 -timeout 60 2>&1 | tail -15
sleep 3
echo "=== pose after settle ==="
timeout 5 gz model -m zhirong_robot -p 2>&1
echo "=== topics after spawn ==="
timeout 10 ros2 topic list 2>&1 | head -20
echo "=== gzserver warnings ==="
grep -iE 'warn|error|inertial|mass|lump|urdf' "$LOG/gzserver.log" | head -40
echo "=== gzserver log tail ==="
tail -25 "$LOG/gzserver.log"
