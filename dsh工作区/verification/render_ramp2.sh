#!/usr/bin/env bash
# 斜坡2 特写渲染（验证 Λ 形）
set -eo pipefail
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
OUT="${1:-$WS/preview/scene/ramp2_closeup.png}"
MAPS="$WS/competition_ws/src/maps/zhirong_maps/models"
WORLD="$WS/competition_ws/src/maps/zhirong_maps/worlds/zhirong_arena.world"
mkdir -p "$(dirname "$OUT")" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$WS/competition_ws/install/setup.bash" 2>/dev/null || true
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$WS/verification/logs/ramp2_ros" ROS_DOMAIN_ID=151
export GAZEBO_MASTER_URI="http://127.0.0.1:11542"
pkill -x gzserver 2>/dev/null || true; pkill -x gzclient 2>/dev/null || true; sleep 1
XVFB="$WS/gazebo_userland/usr/bin/Xvfb"
"$XVFB" :95 -screen 0 1400x1000x24 +extension GLX +render -noreset > "$(dirname "$OUT")/ramp2_xvfb.log" 2>&1 & XP=$!
sleep 3
DISPLAY=:95 LIBGL_ALWAYS_SOFTWARE=1 GAZEBO_MODEL_PATH="$MAPS" \
GAZEBO_PLUGIN_PATH="/opt/ros/humble/lib:${GAZEBO_PLUGIN_PATH:-}" \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$WORLD" > "$(dirname "$OUT")/ramp2_gz.log" 2>&1 & SP=$!
for _ in $(seq 1 60); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
# 相机：从西南上方看斜坡2（中心约 (-0.53,-1.20)）
gz model -f "$WS/verification/cam_rig.sdf" -m top_cam -x -2.6 -y -3.2 -z 1.9 -R 0 -P 0.55 -Y 0.72 >/dev/null 2>&1
sleep 3
python3 "$WS/verification/save_camera_frame.py" /overview_cam/image/image_raw "$OUT" 25
kill -INT $SP 2>/dev/null || true; sleep 2
pkill -x gzserver 2>/dev/null || true; kill $XP 2>/dev/null || true
ls -la "$OUT"
