#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/launch_cmd
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=130
export GAZEBO_MASTER_URI=http://127.0.0.1:11420
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1 \
  ros2 launch bring_up bring_up.launch.py gui:=false rviz:=false teleop:=none verbose:=true \
  > "$LOG/launch.log" 2>&1 & LP=$!
for i in $(seq 1 40); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
GP=$(pgrep -x gzserver | head -1)
echo "=== 完整 cmdline ==="; tr '\0' ' ' < /proc/$GP/cmdline; echo
echo "=== DISPLAY/X 相关 env ==="; tr '\0' '\n' < /proc/$GP/environ | grep -E "DISPLAY|LIBGL|XAUTH|GAZEBO_RES|HOME=" | head -8
echo "=== 与手动方式对比：直接再起一个 gzserver（不同 master 端口）==="
GAZEBO_MASTER_URI=http://127.0.0.1:11421 DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so \
  "$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world" --verbose > "$LOG/manual.log" 2>&1 & MP=$!
sleep 8
echo "manual gzserver X11 fd:"; ls -l /proc/$MP/fd 2>/dev/null | grep -c "X11\|X99"
echo "launch gzserver X11 fd:"; ls -l /proc/$GP/fd 2>/dev/null | grep -c "X11\|X99"
echo "manual log render:"; sed 's/\x1b\[[0-9;]*m//g' "$LOG/manual.log" | grep -aiE "render|display" | head -4
echo "=== 两个 gzserver 进程后，给 launch 模式也 spawn 相机看是否出图 ==="
kill -INT $MP 2>/dev/null
kill -INT $LP 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
