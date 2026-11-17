#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="${CWS_OVERRIDE:-$WS/competition_ws}"
LOG=$WS/verification/logs/view_sim2
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export ROS_DOMAIN_ID=121
unset GAZEBO_MASTER_URI
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1

DISPLAY=:1 USER_DISPLAY=:1 timeout 150 bash "$CWS/scripts/view_sim.sh" > "$LOG/view_sim.log" 2>&1 &
VPID=$!
# 等待 /clock 与图像话题
for i in $(seq 1 60); do ros2 topic list 2>/dev/null | grep -qx "/view_cam/image/image_raw" && break; sleep 1; done
echo "=== 关键日志 ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/view_sim.log" | grep -aE "启动|OK|等待|打开|实时查看|错误|警告" | head -10
echo "=== 话题 ==="; timeout 8 ros2 topic list 2>/dev/null | grep -E "view_cam|/clock|/odom"
echo "=== 图像频率（3s）==="; timeout 6 ros2 topic hz /view_cam/image/image_raw 2>&1 | head -3
echo "=== 抓帧 ==="; timeout 40 python3 "$WS/verification/save_camera_frame.py" /view_cam/image/image_raw "$LOG/frame.png" 25; echo "rc=$?"
ls -la "$LOG/frame.png" 2>/dev/null
echo "=== rqt 进程 ==="; pgrep -af rqt_image_view | head -2
echo "=== rqt 日志 ==="; tail -5 "$CWS/log/view_sim/rqt.log" 2>/dev/null
echo "=== 收尾 ==="
kill -INT $VPID 2>/dev/null
sleep 6
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; pkill -x Xvfb 2>/dev/null
sleep 2
echo "残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0)"
