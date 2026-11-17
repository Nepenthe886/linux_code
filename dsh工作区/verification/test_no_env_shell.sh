#!/bin/bash
# 模拟用户终端：只 source ROS 与工作空间 install，不 source tools/gazebo_env.sh
WS=/home/nepenthe/zmf/linux_code/dsh工作区
LOG=$WS/verification/logs/no_env_test
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$WS/competition_ws/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11396"
export ROS_DOMAIN_ID=96
unset DISPLAY
pkill -x gzserver 2>/dev/null; sleep 1
cd "$WS/competition_ws"
timeout 120 ros2 launch ./src/robot/robot_control/launch/gazebo.launch.py \
  gui:=false rviz:=false teleop:=none verbose:=true > "$LOG/launch.log" 2>&1 &
LPID=$!
sleep 15
echo "=== launch 是否存活: $(kill -0 $LPID 2>/dev/null && echo YES || echo NO) ==="
echo "=== 启动日志关键行 ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aE "自动注入|world =|gzserver|Error|error|Traceback" | head -8
echo "=== topics ==="
timeout 10 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states|cmd_vel|tf)$" | head
echo "=== robot pose ==="
timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
echo "=== 前进 2s ==="
timeout 6 ros2 topic pub -r 20 -t 2 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}" >/dev/null 2>&1
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
kill -INT $LPID 2>/dev/null; sleep 3
pkill -x gzserver 2>/dev/null
sleep 1
echo "=== 残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0) ==="
