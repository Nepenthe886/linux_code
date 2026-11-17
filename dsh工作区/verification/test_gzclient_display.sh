#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
LOG=$WS/verification/logs/gzclient_display
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export GAZEBO_MASTER_URI="http://127.0.0.1:11411"
export ROS_DOMAIN_ID=111
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1

echo "=== 当前显示环境 ==="
echo "DISPLAY=$DISPLAY"
timeout 5 xdpyinfo -display :1 2>&1 | grep -E "dimensions|GLX" | head -3
echo
echo "=== 起 gzserver（headless 无渲染）==="
world="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
GAZEBO_MODEL_PATH="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup/install/zhirong_maps/share/zhirong_maps/models" \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$world" > "$LOG/gzserver.log" 2>&1 &
sleep 6
echo "gzserver: $(pgrep -x gzserver | head -1)"

echo
echo "=== 测试 A：DISPLAY=:1 起 gzclient（10s 后检查是否响应）==="
DISPLAY=:1 timeout 12 gzclient > "$LOG/gzclient_native.log" 2>&1 &
CPID=$!
sleep 8
if kill -0 $CPID 2>/dev/null; then echo "gzclient 进程存活"; else echo "gzclient 已退出(崩溃)"; fi
sed 's/\x1b\[[0-9;]*m//g' "$LOG/gzclient_native.log" | grep -aiE "error|glx|opengl|render|fail|unable" | head -6
wait $CPID 2>/dev/null
echo "-- 原生 gzclient 退出码: $? --"

echo
echo "=== 测试 B：DISPLAY=:1 + LIBGL_ALWAYS_SOFTWARE=1 ==="
DISPLAY=:1 LIBGL_ALWAYS_SOFTWARE=1 timeout 12 gzclient > "$LOG/gzclient_soft.log" 2>&1 &
CPID=$!
sleep 8
if kill -0 $CPID 2>/dev/null; then echo "gzclient 进程存活"; else echo "gzclient 已退出(崩溃)"; fi
sed 's/\x1b\[[0-9;]*m//g' "$LOG/gzclient_soft.log" | grep -aiE "error|glx|opengl|render|fail|unable" | head -6
wait $CPID 2>/dev/null
echo "-- 软渲染 gzclient 退出码: $? --"

pkill -x gzclient 2>/dev/null
pkill -x gzserver 2>/dev/null
