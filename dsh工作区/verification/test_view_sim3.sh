#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="${CWS_OVERRIDE:-$WS/competition_ws}"
LOG=$WS/verification/logs/view_sim3
mkdir -p "$LOG"
mkdir -p /tmp/.X11-unix   # sandbox 每次调用 /tmp 是空的；真实系统已有该目录
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export ROS_DOMAIN_ID=122
unset GAZEBO_MASTER_URI
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1

DISPLAY=:1 USER_DISPLAY=:1 timeout 120 bash "$CWS/scripts/view_sim.sh" > "$LOG/view_sim.log" 2>&1 &
VPID=$!
for i in $(seq 1 60); do ros2 topic list 2>/dev/null | grep -qx "/view_cam/image/image_raw" && break; sleep 1; done
sleep 3
echo "=== X 显示 ==="; ls /tmp/.X11-unix/ 2>/dev/null | head -3
echo "=== 渲染/显示相关日志 ==="
sed 's/\x1b\[[0-9;]*m//g' "$CWS/log/view_sim/launch.log" | grep -aiE "RenderEngine|display|rendering|sensor" | head -6
echo "=== 图像频率（5s）==="; timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | head -4
echo "=== 抓帧 ==="; timeout 40 python3 "$WS/verification/save_camera_frame.py" /view_cam/image/image_raw "$LOG/frame.png" 25; echo "rc=$?"
ls -la "$LOG/frame.png" 2>/dev/null
kill -TERM $VPID 2>/dev/null; sleep 6
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; pkill -x Xvfb 2>/dev/null
sleep 2
echo "残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0)"
