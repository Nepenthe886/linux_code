#!/usr/bin/env bash
# 俯视渲染某个 world，并与 Word 图2 拼成对比图（用于场景布局校对）
# 用法: render_world_topdown.sh <world> <out_compare.png> [maps_models_dir]
set -eo pipefail
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
WORLD="${1:?用法: render_world_topdown.sh <world> <out.png> [maps_models]}"
OUT="${2:?用法: render_world_topdown.sh <world> <out.png> [maps_models]}"
MAPS_MODELS="${3:-$WS/competition_ws/src/maps/zhirong_maps/models}"
LOG="$(dirname "$OUT")/topdown_render.log"
mkdir -p "$(dirname "$OUT")" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$WS/competition_ws/install/setup.bash" 2>/dev/null || true
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$WS/verification/logs/topdown_ros" ROS_DOMAIN_ID=150
export GAZEBO_MASTER_URI="http://127.0.0.1:11541"
pkill -x gzserver 2>/dev/null || true; pkill -x gzclient 2>/dev/null || true; sleep 1
XVFB="$WS/gazebo_userland/usr/bin/Xvfb"
"$XVFB" :96 -screen 0 1200x1200x24 +extension GLX +render -noreset > "$(dirname "$OUT")/xvfb.log" 2>&1 & XP=$!
sleep 3
DISPLAY=:96 LIBGL_ALWAYS_SOFTWARE=1 \
GAZEBO_MODEL_PATH="$MAPS_MODELS" \
GAZEBO_PLUGIN_PATH="/opt/ros/humble/lib:${GAZEBO_PLUGIN_PATH:-}" \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$WORLD" > "$LOG" 2>&1 & SP=$!
for _ in $(seq 1 60); do ros2 topic list 2>/dev/null | grep -qx /clock && break; sleep 1; done
# 正俯视相机（北朝上：yaw=π/2）
gz model -f "$WS/verification/cam_rig.sdf" -m top_cam -x 0 -y 0 -z 7.6 -R 0 -P 1.570796 -Y 1.570796 > /dev/null 2>&1
sleep 3
python3 "$WS/verification/save_camera_frame.py" /overview_cam/image/image_raw "$OUT.tmp_frame.png" 25 >/dev/null 2>&1
# 与图2 拼接对比
python3 - "$OUT.tmp_frame.png" "$WS/preview/docx_media/image2.png" "$OUT" <<'PY'
import sys
from PIL import Image, ImageDraw
sim = Image.open(sys.argv[1]).convert("RGB")
fig = Image.open(sys.argv[2]).convert("RGB")
h = 900
def fit(im, h):
    w = round(im.width * h / im.height)
    return im.resize((w, h), Image.LANCZOS)
sim2, fig2 = fit(sim, h), fit(fig, h)
pad = 20
out = Image.new("RGB", (fig2.width + pad + sim2.width, h + 40), "white")
out.paste(fig2, (0, 40)); out.paste(sim2, (fig2.width + pad, 40))
d = ImageDraw.Draw(out)
d.text((5, 10), "Word figure 2 (reference)", fill=(0, 0, 0))
d.text((fig2.width + pad + 5, 10), "Gazebo top-down render", fill=(0, 0, 0))
out.save(sys.argv[3])
print("compare ->", sys.argv[3])
PY
rm -f "$OUT.tmp_frame.png"
kill -INT $SP 2>/dev/null; sleep 2
pkill -x gzserver 2>/dev/null || true; kill $XP 2>/dev/null || true
ls -la "$OUT"
