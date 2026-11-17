#!/bin/bash
# 精确模拟用户终端：source ROS + install，然后执行用户当时的那条命令（不 source 任何 gazebo 环境脚本）
WS=/home/nepenthe/zmf/linux_code/dsh工作区
TARGET="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
LOG=$WS/verification/logs/user_command
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$TARGET/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11398"
export ROS_DOMAIN_ID=98
unset DISPLAY
pkill -x gzserver 2>/dev/null; sleep 1
cd "$TARGET"
timeout 120 ros2 launch robot_control gazebo.launch.py > "$LOG/launch.log" 2>&1 &
LPID=$!
sleep 15
echo "=== launch alive: $(kill -0 $LPID 2>/dev/null && echo YES || echo NO) ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aE "自动注入|world =|ERROR|Traceback|not found" | head -5
echo "=== topics ==="; timeout 10 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states|cmd_vel|tf)$"
echo "=== robot pose ==="; timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
kill -INT $LPID 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; sleep 1
echo "=== 残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0) ==="
