#!/bin/bash
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS=$WS/competition_ws
LOG=$WS/verification/logs/ab2_camera
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=133
CAM="$CWS/install/bring_up/share/bring_up/config/view_camera.sdf"
WORLD="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
RD="$CWS/install/robot_description/share/robot_description"
pkill -x gzserver 2>/dev/null; pkill -x Xvfb 2>/dev/null; sleep 1
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3
# 生成 model:// 的 URDF（不依赖 rsp）
python3 - "$RD/urdf/omni_robot.urdf" "$LOG/robot_gazebo.urdf" <<'PY'
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read().replace("package://robot_description/","model://robot_description/")
open(dst,'w',encoding='utf-8').write(s)
PY
export GAZEBO_MASTER_URI=http://127.0.0.1:11426
GAZEBO_MODEL_PATH="$CWS/install/zhirong_maps/share/zhirong_maps/models:$CWS/install/robot_control/share/robot_control/models" \
GAZEBO_PLUGIN_PATH="/opt/ros/humble/lib" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$WORLD" > "$LOG/manual.log" 2>&1 & MP=$!
for i in $(seq 1 30); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
echo "=== 手动 gzserver + spawn 机器人 + spawn 相机 ==="
timeout 30 ros2 run gazebo_ros spawn_entity.py -file "$LOG/robot_gazebo.urdf" -entity zhirong_robot -x 2.9 -y 1.6 -z 0.05 -Y 3.14159 > "$LOG/spawn_robot.log" 2>&1
tail -1 "$LOG/spawn_robot.log"
gz model -f "$CAM" -m view_cam -x 0 -y -6 -z 5.2 -R 0 -P 0.714 -Y 1.5708 > "$LOG/spawn_manual.log" 2>&1
sleep 4
timeout 8 ros2 topic hz /view_cam/image/image_raw 2>&1 | grep -m1 "average rate" || echo "ros 无图像"
echo "=== gzserver 日志中 mesh/robot/render 错误 ==="
sed 's/\x1b\[[0-9;]*m//g' "$LOG/manual.log" | grep -aiE "mesh|No mesh|render|OGRE" | head -6
kill -INT $MP 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null; kill $XP 2>/dev/null
