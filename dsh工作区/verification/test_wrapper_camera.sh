#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/wrapper_camera
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=134
CAM="$CWS/install/bring_up/share/bring_up/config/view_camera.sdf"
WORLD="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
export GAZEBO_MASTER_URI=http://127.0.0.1:11427
export DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1
export GAZEBO_MODEL_PATH="$CWS/install/robot_control/share/robot_control/models:$CWS/install/zhirong_maps/share/zhirong_maps/models"
export GAZEBO_PLUGIN_PATH="/opt/ros/humble/lib"
# 完全复刻 launch 的 bash -c 包装命令
bash -c 'world="$1"; shift; if [ ! -f "$world" ]; then echo ERR >&2; exit 2; fi; if [ "${ZHIRONG_KEEP_DISPLAY:-0}" = "1" ]; then :; else unset DISPLAY; fi; exec gzserver "$@" "$world"' \
  gazebo.launch.py "$WORLD" --verbose -s libgazebo_ros_init.so -s libgazebo_ros_factory.so \
  > "$LOG/wrapper.log" 2>&1 & WP=$!
for i in $(seq 1 30); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
echo "wrapper gzserver pid=$(pgrep -x gzserver | head -1)"
gz model -f "$CAM" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn.log" 2>&1
sleep 4
timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | grep -m1 "average rate" || echo "ros 无图像"
kill -INT $WP 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
