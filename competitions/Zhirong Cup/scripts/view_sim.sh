#!/usr/bin/env bash
# =============================================================================
# 无 OpenGL 桌面的实时可视化（本机 nvidia GLX 异常时使用）
#
#   本机 DISPLAY（rqt_image_view，Qt 无需 OpenGL）
#        ↑ ROS 图像 /view_cam/image/image_raw
#   Xvfb(软件 OpenGL) 里的 gzserver：Gazebo 比赛场景 + 机器人 + 观察相机
#
# 说明：gzserver 由本脚本**直接启动**（不经 ros2 launch），因为实测在本机环境中
#       经 launch 启动的 gzserver 相机渲染不出图；直接启动 + Gazebo ROS 插件
#       方式与 `bring_up` 使用同一世界/模型/插件，仅进程启动方式不同。
#
# 用法:
#   bash scripts/view_sim.sh
#   CAM_POS="-4.6 -4.6 4.4" CAM_PITCH=0.62 CAM_YAW=0.785 bash scripts/view_sim.sh
# 停止: Ctrl-C（自动清理 gzserver / robot_state_publisher / Xvfb / rqt）
# =============================================================================
set -eo pipefail

ROS_DISTRO="${ROS_DISTRO:-humble}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$HERE/.." && pwd)"
LOGDIR="${LOGDIR:-$WS/log/view_sim}"
mkdir -p "$LOGDIR" /tmp/.X11-unix

source "/opt/ros/${ROS_DISTRO}/setup.bash"
if [ ! -f "$WS/install/setup.bash" ]; then
  echo "[view_sim][错误] 还没构建，请先运行: bash $WS/scripts/build.sh"
  exit 1
fi
source "$WS/install/setup.bash"

IMAGE_TOPIC="/view_cam/image/image_raw"
USER_DISPLAY="${USER_DISPLAY:-${DISPLAY:-:1}}"
read -r CAM_X CAM_Y CAM_Z <<< "${CAM_POS:-0 -6.0 5.2}"
CAM_PITCH="${CAM_PITCH:-0.714}"
CAM_YAW="${CAM_YAW:-1.5708}"

# ---- 资源路径 ----
MAPS_SHARE="$WS/install/zhirong_maps/share/zhirong_maps"
ROBOT_DESC_SHARE="$WS/install/robot_description/share/robot_description"
ROBOT_CTRL_SHARE="$WS/install/robot_control/share/robot_control"
WORLD="$MAPS_SHARE/worlds/zhirong_arena.world"
[ -f "$WORLD" ] || { echo "[view_sim][错误] 找不到世界文件: $WORLD"; exit 1; }
CAM_SDF="$WS/install/bring_up/share/bring_up/config/view_camera.sdf"
[ -f "$CAM_SDF" ] || CAM_SDF="$WS/src/bring_up/config/view_camera.sdf"
[ -f "$CAM_SDF" ] || { echo "[view_sim][错误] 找不到相机模型: $CAM_SDF"; exit 1; }

# ---- 定位 Xvfb（系统优先，回退用户态安装） ----
find_xvfb() {
  if command -v Xvfb >/dev/null 2>&1; then command -v Xvfb; return 0; fi
  local cand
  for cand in /usr/bin/Xvfb \
      "${GAZEBO_USERLAND_PREFIX:-/home/nepenthe/zmf/linux_code/dsh工作区/gazebo_userland}/usr/bin/Xvfb"; do
    if [ -x "$cand" ]; then echo "$cand"; return 0; fi
  done
  return 1
}
XVFB_BIN="$(find_xvfb)" || {
  echo "[view_sim][错误] 找不到 Xvfb。请安装：sudo apt install -y xvfb"
  echo "             （或 sudo bash $WS/scripts/install_environment.sh）"
  exit 1
}
XVFB_DISPLAY=""
for n in $(seq 99 109); do
  [ -e "/tmp/.X11-unix/X${n}" ] || { XVFB_DISPLAY=":${n}"; break; }
done
[ -n "$XVFB_DISPLAY" ] || { echo "[view_sim][错误] 找不到空闲 X display"; exit 1; }

XVFB_PID=""; GZSERVER_PID=""; RSP_PID=""; RQT_PID=""
cleanup() {
  echo; echo "[view_sim] 清理中 ..."
  [ -n "$RQT_PID" ] && kill -TERM "$RQT_PID" 2>/dev/null || true
  [ -n "$RSP_PID" ] && kill -TERM "$RSP_PID" 2>/dev/null || true
  [ -n "$GZSERVER_PID" ] && kill -TERM "$GZSERVER_PID" 2>/dev/null || true
  sleep 1
  pkill -x gzserver 2>/dev/null || true
  [ -n "$XVFB_PID" ] && kill -TERM "$XVFB_PID" 2>/dev/null || true
  echo "[view_sim] 已退出。"
}
trap cleanup EXIT INT TERM

# ---- 清理上次残留 ----
if pgrep -x gzserver >/dev/null 2>&1; then
  echo "[view_sim] 检测到残留 gzserver，先清理 ..."
  bash "$HERE/kill_sim.sh" || true
fi

# ---- 1) 虚拟显示（软件 OpenGL） ----
echo "[view_sim] 启动 Xvfb ${XVFB_DISPLAY}（${XVFB_BIN}）..."
"$XVFB_BIN" "$XVFB_DISPLAY" -screen 0 1600x1000x24 +extension GLX +render -noreset \
  > "$LOGDIR/xvfb.log" 2>&1 &
XVFB_PID=$!
sleep 2
kill -0 "$XVFB_PID" 2>/dev/null || { echo "[view_sim][错误] Xvfb 启动失败: $LOGDIR/xvfb.log"; exit 1; }

# ---- 2) gzserver（带渲染，直接启动） ----
echo "[view_sim] 启动 Gazebo（Xvfb 软件渲染）..."
DISPLAY="$XVFB_DISPLAY" LIBGL_ALWAYS_SOFTWARE=1 \
GAZEBO_MODEL_PATH="$ROBOT_CTRL_SHARE/models:$MAPS_SHARE/models" \
GAZEBO_PLUGIN_PATH="/opt/ros/${ROS_DISTRO}/lib:${GAZEBO_PLUGIN_PATH:-}" \
  gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$WORLD" --verbose \
  > "$LOGDIR/gzserver.log" 2>&1 &
GZSERVER_PID=$!

echo -n "[view_sim] 等待 Gazebo 就绪 "
for _ in $(seq 1 90); do
  if ros2 topic list 2>/dev/null | grep -qx "/clock"; then echo "OK"; break; fi
  sleep 1
done
ros2 topic list 2>/dev/null | grep -qx "/clock" || { echo "[view_sim][错误] Gazebo 未起来: $LOGDIR/gzserver.log"; exit 1; }

# ---- 3) 机器人：生成 Gazebo 可解析 URDF（model://）并 spawn ----
URDF_SRC="$ROBOT_DESC_SHARE/urdf/omni_robot.urdf"
ROBOT_URDF="$LOGDIR/robot_gazebo.urdf"
python3 - "$URDF_SRC" "$ROBOT_URDF" <<'PYEOF'
import sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
text = text.replace("package://robot_description/", "model://robot_description/")
open(dst, "w", encoding="utf-8").write(text)
PYEOF
echo "[view_sim] spawn 机器人 ..."
ros2 run gazebo_ros spawn_entity.py -file "$ROBOT_URDF" -entity zhirong_robot \
  -x 2.9 -y 1.6 -z 0.05 -Y 3.14159 > "$LOGDIR/spawn_robot.log" 2>&1 || {
    echo "[view_sim][警告] 机器人 spawn 失败: $LOGDIR/spawn_robot.log"; }

# ---- 4) robot_state_publisher（TF；用 params-file 避免多行参数问题） ----
RSP_PARAMS="$LOGDIR/rsp_params.yaml"
python3 - "$URDF_SRC" "$RSP_PARAMS" <<'PYEOF'
import sys, yaml
src, dst = sys.argv[1], sys.argv[2]
urdf = open(src, encoding="utf-8").read().replace(
    "package://robot_description/", "model://robot_description/")
yaml.safe_dump({"robot_state_publisher": {"ros__parameters": {
    "robot_description": urdf, "use_sim_time": True}}},
    open(dst, "w", encoding="utf-8"), allow_unicode=True)
PYEOF
ros2 run robot_state_publisher robot_state_publisher --ros-args \
  --params-file "$RSP_PARAMS" -p use_sim_time:=true > "$LOGDIR/rsp.log" 2>&1 &
RSP_PID=$!

# ---- 5) 观察相机 ----
echo "[view_sim] 添加观察相机 (${CAM_X}, ${CAM_Y}, ${CAM_Z}) ..."
gz model -f "$CAM_SDF" -m view_cam -x "$CAM_X" -y "$CAM_Y" -z "$CAM_Z" \
  -R 0 -P "$CAM_PITCH" -Y "$CAM_YAW" > "$LOGDIR/spawn_cam.log" 2>&1 || {
    echo "[view_sim][警告] 相机 spawn 失败: $LOGDIR/spawn_cam.log"; }

echo -n "[view_sim] 等待图像话题 ${IMAGE_TOPIC} "
for _ in $(seq 1 60); do
  if ros2 topic list 2>/dev/null | grep -qx "$IMAGE_TOPIC"; then echo "OK"; break; fi
  sleep 1
done

# ---- 6) 在用户显示器上查看（Qt，不依赖 OpenGL） ----
echo "[view_sim] 在 DISPLAY=${USER_DISPLAY} 打开 rqt_image_view ..."
DISPLAY="$USER_DISPLAY" ros2 run rqt_image_view rqt_image_view "$IMAGE_TOPIC" \
  > "$LOGDIR/rqt.log" 2>&1 &
RQT_PID=$!
sleep 2
if ! kill -0 "$RQT_PID" 2>/dev/null; then
  echo "[view_sim][警告] rqt_image_view 未保持运行（见 $LOGDIR/rqt.log）"
  echo "           可在其它终端手动查看：ros2 run rqt_image_view rqt_image_view $IMAGE_TOPIC"
fi

cat <<MSG

============================ 实时查看已启动 ============================
  画面：rqt_image_view（DISPLAY=${USER_DISPLAY}），话题 ${IMAGE_TOPIC}
  数据：/clock /odom /joint_states /cmd_vel
  遥控：另开终端 ros2 run robot_control teleop_keyboard，或 ros2 topic pub ...
  Ctrl-C 结束并自动清理（gzserver / rsp / Xvfb / rqt）
  换视角：CAM_POS="-4.6 -4.6 4.4" CAM_PITCH=0.62 CAM_YAW=0.785 bash scripts/view_sim.sh
=======================================================================
MSG

# 等待任一子进程退出（通常是 rqt 关闭或 Ctrl-C）
wait
