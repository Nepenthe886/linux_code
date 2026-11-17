#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
LOG=$WS/verification/logs/rviz_display
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export DISPLAY=:1
echo "=== 原生 rviz2（10s）==="
timeout 12 rviz2 -d "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup/install/robot_control/share/robot_control/rviz/teleop.rviz" > "$LOG/rviz_native.log" 2>&1 &
P=$!; sleep 8
kill -0 $P 2>/dev/null && echo "rviz2 存活" || echo "rviz2 已退出"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/rviz_native.log" | grep -aiE "error|glx|opengl|fail|cannot|unable" | head -8
wait $P 2>/dev/null
echo
echo "=== LIBGL_ALWAYS_SOFTWARE=1 rviz2（10s）==="
LIBGL_ALWAYS_SOFTWARE=1 timeout 12 rviz2 -d "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup/install/robot_control/share/robot_control/rviz/teleop.rviz" > "$LOG/rviz_soft.log" 2>&1 &
P=$!; sleep 8
kill -0 $P 2>/dev/null && echo "rviz2 存活" || echo "rviz2 已退出"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/rviz_soft.log" | grep -aiE "error|glx|opengl|fail|cannot|unable" | head -8
wait $P 2>/dev/null
pkill -x rviz2 2>/dev/null
