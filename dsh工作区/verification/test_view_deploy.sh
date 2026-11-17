#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
TARGET="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
LOG=$WS/verification/logs/view_deploy
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$TARGET/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=137
unset GAZEBO_MASTER_URI
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1
DISPLAY=:1 USER_DISPLAY=:1 LOGDIR="$LOG/view_sim_logs" \
  timeout 120 bash "$TARGET/scripts/view_sim.sh" > "$LOG/view.log" 2>&1 &
VPID=$!
for i in $(seq 1 90); do ros2 topic list 2>/dev/null | grep -qx "/view_cam/image/image_raw" && break; sleep 1; done
sleep 3
echo "--- 日志 ---"; sed 's/\x1b\[[0-9;]*m//g' "$LOG/view.log" | grep -aE "启动|等待|spawn|打开|实时查看|错误|警告" | head -10
echo "--- 图像频率 ---"; timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | grep -m1 "average rate" || echo "无图像"
echo "--- 抓帧 ---"; timeout 30 python3 "$WS/verification/save_camera_frame.py" /view_cam/image/image_raw "$LOG/frame.png" 20; echo "rc=$?"; ls -la "$LOG/frame.png" 2>/dev/null
echo "--- 机器人位姿 ---"; timeout 5 gz model -m zhirong_robot -p 2>&1 | head -1
kill -INT $VPID 2>/dev/null; sleep 6
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 2
echo "残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0)"
