#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/render_debug2
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=125
export GAZEBO_MASTER_URI=http://127.0.0.1:11415
pkill -x gzserver 2>/dev/null; sleep 1
XVFB="$WS/gazebo_userland/usr/bin/Xvfb"
"$XVFB" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
echo "=== Xvfb 进程: $(kill -0 $XP 2>/dev/null && echo 存活 || echo 死亡) socket: $(ls /tmp/.X11-unix/ 2>/dev/null | tr '\n' ' ')"
echo "=== xdpyinfo :99 ==="; DISPLAY=:99 timeout 5 xdpyinfo 2>&1 | head -3
echo "=== 直接验证 GLX（ctypes） ==="; DISPLAY=:99 python3 -c "import sys; sys.path.insert(0,'$WS/competition_ws/src/robot/robot_control/launch'); import importlib.util; spec=importlib.util.spec_from_file_location('gz','$WS/competition_ws/src/robot/robot_control/launch/gazebo.launch.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print('GLX ok:', m._opengl_available())"
pkill -x gzserver 2>/dev/null
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ZHIRONG_KEEP_DISPLAY=1 \
  ros2 launch bring_up bring_up.launch.py gui:=false rviz:=false teleop:=none verbose:=true \
  > "$LOG/launch.log" 2>&1 & LP=$!
for i in $(seq 1 40); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
echo "=== gzserver 渲染日志 ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/launch.log" | grep -aiE "RenderEngine|display|rendering" | head -6
gz model -f "$CWS/install/bring_up/share/bring_up/config/view_camera.sdf" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn.log" 2>&1
sleep 4
echo "=== hz ==="; timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | head -3
timeout 30 python3 $WS/verification/save_camera_frame.py /view_cam/image/image_raw "$LOG/frame.png" 20; echo "rc=$?"
ls -la "$LOG/frame.png" 2>/dev/null
kill -INT $LP 2>/dev/null; sleep 3; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
