#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/launch_x11
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=129
export GAZEBO_MASTER_URI=http://127.0.0.1:11419
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
echo "Xvfb alive=$(kill -0 $XP 2>/dev/null && echo yes || echo no) xdpyinfo=$(DISPLAY=:99 xdpyinfo 2>&1 | head -1)"
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1 \
  ros2 launch bring_up bring_up.launch.py gui:=false rviz:=false teleop:=none verbose:=true \
  > "$LOG/launch.log" 2>&1 & LP=$!
for i in $(seq 1 40); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
GP=$(pgrep -x gzserver | head -1)
echo "gzserver pid=$GP"
echo "=== gzserver 的 X11 fd ==="; ls -l /proc/$GP/fd 2>/dev/null | grep -i "X11\|X99" | head -3
echo "=== gzserver 线程数 ==="; ls /proc/$GP/task 2>/dev/null | wc -l
echo "=== 相机 spawn 后检查 ==="
gz model -f "$CWS/install/bring_up/share/bring_up/config/view_camera.sdf" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn.log" 2>&1
sleep 5
timeout 6 gz topic -e --duration 4 -t "/gazebo/zhirong_arena/view_cam/link/cam/image" > "$LOG/gzimg.txt" 2>&1; echo "gz img bytes=$(wc -c < "$LOG/gzimg.txt")"
echo "=== SIGINT 后完整 gzserver 日志 ==="
kill -INT $LP 2>/dev/null; sleep 4
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aiE "RenderEngine|rendering|display|Camera|sensor" | head -12
pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
