#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/sys_camera
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=123
export GAZEBO_MASTER_URI=http://127.0.0.1:11413
unset GAZEBO_MODEL_PATH
pkill -x gzserver 2>/dev/null; sleep 1
/usr/bin/Xvfb :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 2
world="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
GAZEBO_MODEL_PATH="$CWS/install/zhirong_maps/share/zhirong_maps/models" \
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$world" > "$LOG/gzserver.log" 2>&1 & SP=$!
sleep 8
echo "=== render logs ==="; sed 's/\x1b\[[0-9;]*m//g' "$LOG/gzserver.log" | grep -aiE "render|display|error" | head -5
gz model -f "$CWS/install/bring_up/share/bring_up/config/view_camera.sdf" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn.log" 2>&1
sleep 4
echo "=== topics ==="; timeout 8 ros2 topic list 2>/dev/null | grep view_cam
echo "=== hz ==="; timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | head -3
timeout 30 python3 $WS/verification/save_camera_frame.py /view_cam/image/image_raw "$LOG/frame.png" 20; echo "rc=$?"
ls -la "$LOG/frame.png" 2>/dev/null
kill $SP $XP 2>/dev/null; pkill -x gzserver 2>/dev/null; sleep 1
