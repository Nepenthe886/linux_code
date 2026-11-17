#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="${CWS_OVERRIDE:-$WS/competition_ws}"
LOG=$WS/verification/logs/view_final
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=135
unset GAZEBO_MASTER_URI
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1

echo "### 1) demo.launch.py 在坏 GLX 的 :1 上应快速报错 ###"
cd /home/nepenthe/zmf/linux_code/competitions 2>/dev/null || cd "$CWS"
t0=$(date +%s)
DISPLAY=:1 timeout 60 ros2 launch bring_up demo.launch.py > "$LOG/demo.log" 2>&1
echo "退出码=$? 用时=$(( $(date +%s) - t0 ))s"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/demo.log" | grep -aE "无法创建 OpenGL|view_sim|bring_up.launch|ZHIRONG_SKIP_GL_CHECK" | head -4

echo
echo "### 2) view_sim.sh（Xvfb 软渲染 + rqt 实时画面）###"
DISPLAY=:1 USER_DISPLAY=:1 timeout 120 bash "$CWS/scripts/view_sim.sh" > "$LOG/view.log" 2>&1 &
VPID=$!
for i in $(seq 1 90); do ros2 topic list 2>/dev/null | grep -qx "/view_cam/image/image_raw" && break; sleep 1; done
sleep 3
echo "--- 日志 ---"; sed 's/\x1b\[[0-9;]*m//g' "$LOG/view.log" | grep -aE "启动|等待|spawn|打开|实时查看|错误|警告" | head -10
echo "--- 图像频率 ---"; timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | grep -m1 "average rate" || echo "无图像"
echo "--- 抓帧 ---"; timeout 30 python3 "$WS/verification/save_camera_frame.py" /view_cam/image/image_raw "$LOG/frame.png" 20; echo "rc=$?"; ls -la "$LOG/frame.png" 2>/dev/null
echo "--- rqt 进程 ---"; pgrep -af "rqt_image_view" | grep -v "pgrep" | head -2
echo "--- TF ---"; timeout 8 ros2 run tf2_ros tf2_echo odom base_footprint 2>/dev/null | grep -m1 Translation
kill -INT $VPID 2>/dev/null; sleep 6
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null
sleep 2
echo "残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0)"
