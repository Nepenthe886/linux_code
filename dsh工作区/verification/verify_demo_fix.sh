#!/bin/bash
# 验证修复：demo.launch.py（gui+rvis+teleop 全开）在 Xvfb 上，gzclient 不应再卡在
# "Waiting for model database update to complete..."，且画面正常渲染。
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="${CWS_OVERRIDE:-$WS/competition_ws}"
LOG=$WS/verification/logs/demo_fix
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=143
export GAZEBO_MASTER_URI="http://127.0.0.1:11531"
unset GAZEBO_MODEL_PATH
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 timeout 120 ros2 launch bring_up demo.launch.py > "$LOG/launch.log" 2>&1 &
LPID=$!
sleep 30
echo "=== launch 存活: $(kill -0 $LPID 2>/dev/null && echo YES || echo NO) ==="
echo "=== launch 日志（错误/关键）==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aE "启动|process started|process has died|Error|错误" | head -12
echo "=== gzclient 进程 ==="; pgrep -x gzclient | head -1
echo "=== gzclient 的模型路径环境 ==="
GP=$(pgrep -x gzclient | head -1); tr '\0' '\n' < /proc/$GP/environ 2>/dev/null | grep "^GAZEBO_MODEL_PATH=" | cut -c1-160
echo "=== gzclient transport 日志关键行 ==="
tail -15 "$HOME/.gazebo/client-11531/default.log" 2>/dev/null | sed 's/^/  /'
echo "=== 是否出现卡死标志（应为 0 次 model-database 阻塞 + 无 No mesh specified）==="
echo -n "  Waiting for model database: "; grep -ac "Waiting for model database update to complete" "$HOME/.gazebo/client-11531/default.log" 2>/dev/null || true
echo -n "  No mesh specified: "; grep -ac "No mesh specified" "$HOME/.gazebo/client-11531/default.log" 2>/dev/null || true
echo "=== 截图 ==="
xwd -root -display :99 -out "$LOG/demo.png.xwd" >/dev/null 2>&1
python3 "$WS/tools/xwd2png.py" "$LOG/demo.png.xwd" "$LOG/demo.png" >/dev/null 2>&1 && ls -la "$LOG/demo.png"
echo "=== 收尾 ==="
kill -INT $LPID 2>/dev/null; sleep 6
pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; pkill -x rviz2 2>/dev/null; pkill -x Xvfb 2>/dev/null
sleep 2
echo "残留 gzserver/gzclient: $(pgrep -xc gzserver 2>/dev/null || echo 0)/$(pgrep -xc gzclient 2>/dev/null || echo 0)"
