#!/bin/bash
# 测试 1：master 端口被占时，launch 是否给出清晰中文错误
# 测试 2：run_sim.sh 是否会自动清理残留 gzserver
WS=/home/nepenthe/zmf/linux_code/dsh工作区
TARGET="${TARGET_WS:-/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup}"
LOG=$WS/verification/logs/port_conflict
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$TARGET/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11407"
export ROS_DOMAIN_ID=107
unset DISPLAY
pkill -x gzserver 2>/dev/null; sleep 1

echo "### 场景 1：先起一个 gzserver 占住端口，再 launch（应给出清晰错误） ###"
gzserver --verbose /usr/share/gazebo-11/worlds/empty.world > "$LOG/occupier.log" 2>&1 &
OPID=$!
sleep 5
cd /home/nepenthe/zmf/linux_code/competitions
timeout 30 ros2 launch robot_control gazebo.launch.py > "$LOG/conflict_launch.log" 2>&1
echo "launch 退出码: $?"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/conflict_launch.log" | grep -aE "已被占用|pkill|run_sim|GAZEBO_MASTER_URI|RuntimeError" | head -6

echo
echo "### 场景 2：run_sim.sh 自动清理残留并正常启动 ###"
cd "$TARGET"
timeout 60 bash scripts/run_sim.sh gui:=false rviz:=false teleop:=none verbose:=false > "$LOG/run_sim.log" 2>&1 &
RPID=$!
sleep 18
sed 's/\x1b\[[0-9;]*m//g' "$LOG/run_sim.log" | grep -aE "检测到残留|kill_sim|已清理|world =|process has died" | head -8
echo "=== topics ==="; timeout 10 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states)$"
kill -INT $RPID 2>/dev/null; sleep 2
pkill -x gzserver 2>/dev/null
sleep 1
echo "=== 清理后残留: $(pgrep -xc gzserver 2>/dev/null || echo 0) ==="
