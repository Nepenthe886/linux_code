#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/launch_camera_gz
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=128
export GAZEBO_MASTER_URI=http://127.0.0.1:11418
pkill -x gzserver 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1 \
  ros2 launch bring_up bring_up.launch.py gui:=false rviz:=false teleop:=none verbose:=true \
  > "$LOG/launch.log" 2>&1 & LP=$!
for i in $(seq 1 40); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
gz model -f "$CWS/install/bring_up/share/bring_up/config/view_camera.sdf" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn.log" 2>&1
sleep 5
echo "=== gzserver 进程环境 ==="
GP=$(pgrep -x gzserver | head -1); tr '\0' '\n' < /proc/$GP/environ | grep -E "^DISPLAY=|^LIBGL_ALWAYS|^GAZEBO_PLUGIN_PATH" | head -4
echo "=== gz camera -l ==="; timeout 6 gz camera -l 2>&1 | head -3
echo "=== gz topic -l camera ==="; timeout 8 gz topic -l 2>/dev/null | grep -i "cam/image" | head -3
echo "=== gz 图像消息计数（5s，直接走 gazebo transport） ==="
timeout 6 gz topic -e -t "/gazebo/zhirong_arena/view_cam/link/cam/image" 2>/dev/null | head -c 0 && true
timeout 6 gz topic -e --duration 4 -t "/gazebo/zhirong_arena/view_cam/link/cam/image" > "$LOG/gz_image.txt" 2>&1; echo "gz_image bytes: $(wc -c < "$LOG/gz_image.txt" 2>/dev/null)"
echo "=== ros2 topic hz ==="; timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | head -3
echo "=== launch.log 渲染相关（完整搜索）==="
grep -aiE "RenderEngine|Unable to create X|rendering will be disabled|Unable to initialize" "$LOG/launch.log" | head -5
kill -INT $LP 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
