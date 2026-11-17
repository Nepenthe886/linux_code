#!/bin/bash
# 验证 bring_up 一键启动（系统 Gazebo，干净 shell，不 source 用户态环境）
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="${CWS_OVERRIDE:-$WS/competition_ws}"
LOG=$WS/verification/logs/bring_up
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11410"
export ROS_DOMAIN_ID=110
unset DISPLAY
pkill -x gzserver 2>/dev/null; sleep 1

echo "### 1) --show-args ###"
timeout 20 ros2 launch bring_up bring_up.launch.py --show-args 2>&1 | head -18
echo
echo "### 2) 一键启动（headless）###"
cd /home/nepenthe/zmf/linux_code/competitions 2>/dev/null || cd "$CWS"
timeout 120 ros2 launch bring_up bring_up.launch.py > "$LOG/launch.log" 2>&1 &
LPID=$!
sleep 18
echo "launch alive: $(kill -0 $LPID 2>/dev/null && echo YES || echo NO)"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aE "\[bring_up\]|world =|process has died|已自动注入" | head -5
echo "=== topics ==="; timeout 10 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states|cmd_vel|tf)$"
echo "=== robot pose ==="; timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
echo "=== 前进 2s ==="
timeout 6 ros2 topic pub -r 20 -t 2 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}" >/dev/null 2>&1
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
kill -INT $LPID 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; sleep 1
echo "=== 残留: $(pgrep -xc gzserver 2>/dev/null || echo 0) ==="
