#!/usr/bin/env bash
# 用「虚拟 X + Gazebo 相机」渲染比赛场地与机器人的实景截图（headless 服务器可用）。
# 用法: capture_arena_views.sh [world文件] [输出目录]
set -o pipefail
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
WORLD="${1:-$WS/competition_ws/src/maps/zhirong_maps/worlds/zhirong_arena.world}"
OUTDIR="${2:-$WS/verification/shots}"
DISP=":98"
PORT="11394"
export GAZEBO_MASTER_URI="http://127.0.0.1:${PORT}"
source "$WS/tools/gazebo_env.sh"
export DISPLAY="$DISP" LIBGL_ALWAYS_SOFTWARE=1
# 比赛地图包的模型目录（model:// 解析）
export GAZEBO_MODEL_PATH="$WS/competition_ws/src/robot/robot_control/models:$WS/competition_ws/src/maps/zhirong_maps/models:${GAZEBO_MODEL_PATH:-}"
export ROS_DOMAIN_ID=94
mkdir -p "$OUTDIR"
LOG="$OUTDIR/shots.log"
: > "$LOG"

Xvfb "$DISP" -screen 0 1600x1000x24 +extension GLX +render -noreset > "$OUTDIR/xvfb.log" 2>&1 &
XPID=$!
sleep 2
gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$WORLD" --verbose > "$OUTDIR/gzserver.log" 2>&1 &
SPID=$!
sleep 10

# 生成 Gazebo 可直接加载的 URDF（package:// -> 未编码 file://，Gazebo 不做 percent-decode）
RD="$WS/competition_ws/src/robot/robot_description"
python3 - "$RD/urdf/omni_robot.urdf" "$RD" "$OUTDIR/urdf_gazebo.urdf" <<'PYEOF'
import sys
src, pkg, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding="utf-8").read()
s = s.replace("package://robot_description/", "model://robot_description/")
open(dst, "w", encoding="utf-8").write(s)
print("urdf ->", dst)
PYEOF
timeout 30 ros2 run gazebo_ros spawn_entity.py -file "$OUTDIR/urdf_gazebo.urdf" -entity zhirong_robot \
  -x 2.9 -y 1.6 -z 0.05 -Y 3.14159 >> "$OUTDIR/spawn.log" 2>&1
sleep 2

# 让机器人向场内开一点，截图更有内容（/cmd_vel -> planar_move）
timeout 10 ros2 topic pub -r 20 -t 4 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.35}, angular: {z: 0.0}}" >> "$OUTDIR/cmdvel.log" 2>&1
# 显式发零速停车（planar_move 不会因遥控源退出而自动停车）
timeout 8 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}" >> "$OUTDIR/cmdvel.log" 2>&1
sleep 2

# 取景函数：capture_view <name> <cam_x cam_y cam_z> <tgt_x tgt_y tgt_z> [fixed_pitch fixed_yaw]
capture_view () {
  local name=$1 x=$2 y=$3 z=$4 tx=$5 ty=$6 tz=$7 fp=${8:-} fy=${9:-}
  local pitch yaw
  if [ -n "$fp" ]; then pitch=$fp; yaw=$fy; else
    read -r pitch yaw <<< "$(cam_angles "$x" "$y" "$z" "$tx" "$ty" "$tz")"
  fi
  gz model -f "$WS/verification/cam_rig.sdf" -m "overview_cam" -x "$x" -y "$y" -z "$z" \
     -R 0 -P "$pitch" -Y "$yaw" >> "$OUTDIR/spawn_cam.log" 2>&1
  sleep 2
  timeout 40 python3 "$WS/verification/save_camera_frame.py" \
     /overview_cam/image/image_raw "$OUTDIR/arena_${name}.png" 25 >> "$OUTDIR/capture.log" 2>&1
  gz model -m overview_cam -d >> "$OUTDIR/spawn_cam.log" 2>&1
  sleep 1
}

cam_angles () {  # $1..3=相机位置  $4..6=目标点  -> "pitch yaw"
  python3 -c "
import math,sys
x,y,z=map(float,sys.argv[1:4]); tx,ty,tz=map(float,sys.argv[4:7])
d=(tx-x,ty-y,tz-z); n=math.sqrt(sum(c*c for c in d)); d=[c/n for c in d]
print(f'{math.asin(-d[2]):.6f} {math.atan2(d[1],d[0]):.6f}')\
" "$@"
}

# 机器人实际位姿（用于特写取景）
ROBOT_POSE=$(timeout 5 gz model -m zhirong_robot -p 2>/dev/null)
RX=$(echo "$ROBOT_POSE" | awk '{print $1}')
RY=$(echo "$ROBOT_POSE" | awk '{print $2}')
echo "robot pose after drive: $ROBOT_POSE" >> "$OUTDIR/capture.log"

# 全景（斜俯视 / 正俯视）
capture_view overview  0 -6.0 5.2   0 0 0
capture_view sw_oblique -5.0 -5.0 4.6  0 0 0
capture_view se_oblique 5.0 -5.0 5.4  0 0 0
capture_view topdown   0 0 7.6      0 0 0   1.570796 1.570796

# 机器人特写：以实际位姿为中心取景
if [ -n "$RX" ] && [ -n "$RY" ]; then
  CX=$(python3 -c "print($RX-0.9)")
  CY=$(python3 -c "print($RY-1.4)")
  capture_view robot_closeup "$CX" "$CY" 2.5 "$RX" "$RY" 0.18
fi

kill -TERM $RPID 2>/dev/null
pkill -TERM -f "view_robot[.]launch[.]py" 2>/dev/null
pkill -TERM -f "joint_state_publisher" 2>/dev/null
kill $SPID $XPID 2>/dev/null
sleep 1
pkill -f 'gzserver[ ]-s[ ]libgazebo_ros_init' 2>/dev/null
echo "截图完成: $OUTDIR"
ls -la "$OUTDIR"/*.png 2>/dev/null
