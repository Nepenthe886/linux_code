#!/bin/bash
# 复现：系统安装 Gazebo 后，从 competitions 父目录用 install 环境执行 launch
WS=/home/nepenthe/zmf/linux_code/dsh工作区
TARGET="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
LOG=$WS/verification/logs/system_gazebo
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$TARGET/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11406"
export ROS_DOMAIN_ID=106
unset DISPLAY
pkill -x gzserver 2>/dev/null; sleep 1
cd /home/nepenthe/zmf/linux_code/competitions
timeout 60 ros2 launch robot_control gazebo.launch.py verbose:=true gui:=false rviz:=false teleop:=none > "$LOG/launch.log" 2>&1 &
LPID=$!
sleep 20
echo "=== launch alive: $(kill -0 $LPID 2>/dev/null && echo YES || echo NO) ==="
echo "=== 关键日志 ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aE "自动注入|world =|process has died|Error|error|not found|\[bash-1\]|\[Err\]" | head -15
echo "=== gzserver 进程 ==="; pgrep -ax gzserver | head -2
echo "=== topics ==="; timeout 8 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states)$"
kill -INT $LPID 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null
