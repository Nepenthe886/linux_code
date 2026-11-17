#!/bin/bash
# 模拟“迁移后的普通终端”：不 source 任何 Gazebo 环境脚本，只用工作空间 scripts/
WS=/home/nepenthe/zmf/linux_code/dsh工作区
LOG=$WS/verification/logs/scripts_clean
mkdir -p "$LOG"
export HOME="$WS/gazebo_home"          # 沙箱内 HOME 不可写；真实机器用默认 HOME 即可
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11397"
export ROS_DOMAIN_ID=97
unset DISPLAY
pkill -x gzserver 2>/dev/null; sleep 1
cd "$WS/competition_ws"
timeout 120 bash scripts/run_sim.sh gui:=false rviz:=false teleop:=none verbose:=true > "$LOG/launch.log" 2>&1 &
LPID=$!
sleep 15
echo "=== launch alive: $(kill -0 $LPID 2>/dev/null && echo YES || echo NO) ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aE "自动注入|world =|gzserver 启动" | head -4
echo "=== topics ==="; timeout 10 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states|cmd_vel|tf)$"
echo "=== robot pose start ==="; timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
timeout 6 ros2 topic pub -r 20 -t 2 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}" >/dev/null 2>&1
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
echo "=== robot pose after forward ==="; timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
kill -INT $LPID 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; sleep 1
echo "=== 残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0) ==="
