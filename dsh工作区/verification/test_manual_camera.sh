#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/manual_camera
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=127
export GAZEBO_MASTER_URI=http://127.0.0.1:11417
pkill -x gzserver 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
export DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1
export GAZEBO_MODEL_PATH="$CWS/install/zhirong_maps/share/zhirong_maps/models"
export GAZEBO_PLUGIN_PATH="/opt/ros/humble/lib:${GAZEBO_PLUGIN_PATH:-}"
world="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$world" --verbose > "$LOG/gzserver.log" 2>&1 & SP=$!
sleep 8
echo "=== 渲染日志 ==="; sed 's/\x1b\[[0-9;]*m//g' "$LOG/gzserver.log" | grep -aiE "render|display|camera|sensor" | head -8
gz model -f "$CWS/install/bring_up/share/bring_up/config/view_camera.sdf" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 >> "$LOG/gzserver.log" 2>&1
sleep 5
echo "=== gz topic camera 相关 ==="; timeout 8 gz topic -l 2>/dev/null | grep -i "view_cam\|camera" | head -6
echo "=== gz camera -l ==="; timeout 8 gz camera -l 2>&1 | head -5
echo "=== ros image hz ==="; timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | head -3
echo "=== gzserver 中 camera 输出 ==="; sed 's/\x1b\[[0-9;]*m//g' "$LOG/gzserver.log" | grep -aiE "camera|render|sensor" | tail -8
kill -INT $SP 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
