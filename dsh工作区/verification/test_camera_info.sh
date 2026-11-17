#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/camera_info
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=126
export GAZEBO_MASTER_URI=http://127.0.0.1:11416
pkill -x gzserver 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1 \
  ros2 launch bring_up bring_up.launch.py gui:=false rviz:=false teleop:=none verbose:=true \
  > "$LOG/launch.log" 2>&1 & LP=$!
for i in $(seq 1 40); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
gz model -f "$CWS/install/bring_up/share/bring_up/config/view_camera.sdf" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn.log" 2>&1
echo "spawn rc=$?"; sleep 5
echo "=== launch.log 中 view_cam/camera 相关 ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aiE "view_cam|camera|sensor" | head -10
echo "=== topic info ==="
timeout 10 ros2 topic info -v /view_cam/image/image_raw 2>&1 | head -20
echo "=== gz model -m view_cam -i (前 25 行) ==="
timeout 5 gz model -m view_cam -i 2>&1 | head -25
kill -INT $LP 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
