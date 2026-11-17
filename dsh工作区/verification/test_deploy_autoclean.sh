#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
TARGET="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
LOG=$WS/verification/logs/deploy_autoclean
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$TARGET/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11408"
export ROS_DOMAIN_ID=108
unset DISPLAY
pkill -x gzserver 2>/dev/null; sleep 1
echo "### 制造残留 gzserver（占住 11408）###"
gzserver --verbose /usr/share/gazebo-11/worlds/empty.world > "$LOG/occupier.log" 2>&1 &
sleep 4
pgrep -ax gzserver | head -2
echo
echo "### 直接 launch（应报端口占用，中文提示）###"
cd /home/nepenthe/zmf/linux_code/competitions
timeout 30 ros2 launch robot_control gazebo.launch.py > "$LOG/direct_launch.log" 2>&1
echo "退出码=$?"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/direct_launch.log" | grep -aE "已被占用" | head -2
echo
echo "### 用 run_sim.sh（应自动清理并启动成功）###"
cd "$TARGET"
timeout 60 bash scripts/run_sim.sh gui:=false rviz:=false teleop:=none > "$LOG/run_sim.log" 2>&1 &
RPID=$!
sleep 18
sed 's/\x1b\[[0-9;]*m//g' "$LOG/run_sim.log" | grep -aE "检测到残留|已清理干净|world =|process has died" | head -5
echo "=== topics ==="; timeout 10 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states)$"
echo "=== robot pose ==="; timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
kill -INT $RPID 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null; sleep 1
echo "=== 残留: $(pgrep -xc gzserver 2>/dev/null || echo 0) ==="
