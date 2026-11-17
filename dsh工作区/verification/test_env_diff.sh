#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/env_diff
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=131
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
# 手动方式
GAZEBO_MASTER_URI=http://127.0.0.1:11422 DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so \
  "$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world" > "$LOG/manual.log" 2>&1 & MP=$!
sleep 6
# launch 方式
GAZEBO_MASTER_URI=http://127.0.0.1:11423 DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1 \
  ros2 launch bring_up bring_up.launch.py gui:=false rviz:=false teleop:=none verbose:=true > "$LOG/launch.log" 2>&1 & LP=$!
for i in $(seq 1 40); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
GP=$(pgrep -x gzserver | grep -v "^$MP$" | head -1)
echo "manual pid=$MP launch pid=$GP"
tr '\0' '\n' < /proc/$MP/environ 2>/dev/null | sort > "$LOG/env_manual.txt"
tr '\0' '\n' < /proc/$GP/environ 2>/dev/null | sort > "$LOG/env_launch.txt"
echo "=== 仅 launch 有的环境变量 ==="; comm -13 "$LOG/env_manual.txt" "$LOG/env_launch.txt" | grep -vE "^(GAZEBO_MASTER_URI|ROS_DOMAIN_ID|ZHIRONG_KEEP_DISPLAY)=" | head -15
echo "=== 仅 manual 有的环境变量 ==="; comm -23 "$LOG/env_manual.txt" "$LOG/env_launch.txt" | head -10
kill -INT $MP 2>/dev/null; kill -INT $LP 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
