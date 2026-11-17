#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="${CWS_OVERRIDE:-$WS/competition_ws}"
LOG=$WS/verification/logs/gl_view
mkdir -p "$LOG"
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home"
export ROS_LOG_DIR="$LOG/ros_logs"
export ROS_DOMAIN_ID=120
unset GAZEBO_MASTER_URI
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1

echo "### 1) DISPLAY=:1（GL 损坏）上跑 demo.launch.py，应在数秒内给出清晰报错而不是卡住 ###"
cd /home/nepenthe/zmf/linux_code/competitions 2>/dev/null || cd "$CWS"
t0=$(date +%s)
DISPLAY=:1 timeout 60 ros2 launch bring_up demo.launch.py > "$LOG/demo_gl.log" 2>&1
echo "退出码=$? 用时=$(( $(date +%s) - t0 ))s"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/demo_gl.log" | grep -aE "无法创建 OpenGL|view_sim|bring_up.launch|ZHIRONG_SKIP_GL_CHECK" | head -6

echo
echo "### 2) view_sim.sh 实时查看（Xvfb 软渲染 + 相机 + rqt） ###"
DISPLAY=:1 USER_DISPLAY=:1 timeout 120 bash "$CWS/scripts/view_sim.sh" > "$LOG/view_sim.log" 2>&1 &
VPID=$!
sleep 30
echo "--- view_sim 日志 ---"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/view_sim.log" | grep -aE "启动|OK|等待|打开|实时查看|错误|警告" | head -12
echo "--- 图像话题 ---"
timeout 8 ros2 topic list 2>/dev/null | grep -E "view_cam|clock|odom"
echo "--- 抓一帧验证相机渲染 ---"
timeout 30 python3 "$WS/verification/save_camera_frame.py" /view_cam/image/image_raw "$LOG/live_frame.png" 20 2>&1 | tail -1
echo "--- rqt 进程 ---"
pgrep -a rqt_image_view | head -2
kill -INT $VPID 2>/dev/null; sleep 4
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; pkill -x Xvfb 2>/dev/null
sleep 1
echo "--- 清理后残留 gzserver: $(pgrep -xc gzserver 2>/dev/null || echo 0) ---"
