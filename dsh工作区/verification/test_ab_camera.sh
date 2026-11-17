#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/ab_camera
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=132
CAM="$CWS/install/bring_up/share/bring_up/config/view_camera.sdf"
WORLD="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
check_cam () { # $1=标签 $2=master端口
  sleep 3
  timeout 6 gz topic -e --duration 3 -t "/gazebo/zhirong_arena/view_cam/link/cam/image" > "$LOG/gzimg_$1.txt" 2>&1
  echo "[$1] gz 图像字节=$(wc -c < "$LOG/gzimg_$1.txt")"
  timeout 6 ros2 topic hz /view_cam/image/image_raw 2>&1 | grep -m1 "average rate" || echo "[$1] ros 无图像"
}
echo "=== A：手动 gzserver ==="
export GAZEBO_MASTER_URI=http://127.0.0.1:11424
GAZEBO_MODEL_PATH="$CWS/install/zhirong_maps/share/zhirong_maps/models" \
GAZEBO_PLUGIN_PATH="/opt/ros/humble/lib" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$WORLD" > "$LOG/manual.log" 2>&1 & MP=$!
for i in $(seq 1 30); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
gz model -f "$CAM" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn_manual.log" 2>&1
check_cam manual
kill -INT $MP 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; sleep 1

echo "=== B：bring_up launch ==="
export GAZEBO_MASTER_URI=http://127.0.0.1:11425
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1 \
  ros2 launch bring_up bring_up.launch.py gui:=false rviz:=false teleop:=none verbose:=true > "$LOG/launch.log" 2>&1 & LP=$!
for i in $(seq 1 40); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
gz model -f "$CAM" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn_launch.log" 2>&1
check_cam launch
kill -INT $LP 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
