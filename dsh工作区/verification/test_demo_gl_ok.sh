#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/demo_gl_ok
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=136
export GAZEBO_MASTER_URI=http://127.0.0.1:11430
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 1
# 用 Xvfb 模拟“有可用 OpenGL 的显示器”
"$WS/gazebo_userland/usr/bin/Xvfb" :98 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
cd /home/nepenthe/zmf/linux_code/competitions 2>/dev/null || cd "$CWS"
timeout 45 env DISPLAY=:98 LIBGL_ALWAYS_SOFTWARE=1 ros2 launch bring_up demo.launch.py > "$LOG/demo.log" 2>&1 &
LPID=$!
sleep 25
echo "launch alive: $(kill -0 $LPID 2>/dev/null && echo YES || echo NO)"
sed 's/\x1b\[[0-9;]*m//g' "$LOG/demo.log" | grep -aE "无法创建 OpenGL|process started|process has died|world =" | head -10
echo "=== gzclient/rviz 进程 ==="; pgrep -x gzclient | head -1; pgrep -x rviz2 | head -1
echo "=== 话题 ==="; timeout 8 ros2 topic list 2>/dev/null | grep -E "^/(clock|odom|joint_states)$"
kill -INT $LPID 2>/dev/null; sleep 4
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; pkill -x rviz2 2>/dev/null; kill $XP 2>/dev/null
