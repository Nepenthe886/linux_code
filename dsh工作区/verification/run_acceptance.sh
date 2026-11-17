#!/usr/bin/env bash
# 比赛工作区 Gazebo 启动验收（headless）
# 1) colcon 构建 3 个包  2) 一把 ros2 launch 起 Gazebo+机器人
# 3) 检查 /clock /joint_states /odom /tf  4) 发 /cmd_vel 验证全向运动
# 5) 检查场景关键模型是否加载  6) 收尾清理进程
set -o pipefail
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
CWS="${CWS_OVERRIDE:-$WS/competition_ws}"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOGD="$WS/verification/logs/$STAMP"
mkdir -p "$LOGD"
source "$WS/tools/gazebo_env.sh"
unset DISPLAY
# 动态选一个空闲 master 端口，避免上一次残留 gzserver 占端口导致误判
GZ_PORT=$(python3 - <<'PYEOF'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PYEOF
)
export GAZEBO_MASTER_URI="http://127.0.0.1:${GZ_PORT}"
export ROS_DOMAIN_ID=$(( (GZ_PORT % 100) + 60 ))
echo "[acceptance] 本次使用 Gazebo master 端口 ${GZ_PORT}, ROS_DOMAIN_ID=${ROS_DOMAIN_ID}"
export RCUTILS_LOGGING_BUFFERED_STREAM=1
PASS=0; FAIL=0
note() { echo "$*" | tee -a "$LOGD/summary.txt"; }
check() { # $1 描述, $2 0/非0
  if [ "$2" -eq 0 ]; then PASS=$((PASS+1)); note "[PASS] $1";
  else FAIL=$((FAIL+1)); note "[FAIL] $1"; fi
}

note "===== Gazebo 启动验收 $STAMP ====="
note "日志目录: $LOGD"

# ---------- 0. 清理残留（按进程名精确清理，避免匹配不到带 --verbose 的 argv） ----------
pkill -x gzserver 2>/dev/null
pkill -x gzclient 2>/dev/null
sleep 1
STALE=$(pgrep -xc gzserver 2>/dev/null || true)
if [ "${STALE:-0}" -ne 0 ]; then
  note "[WARN] 仍有 ${STALE} 个 gzserver 残留，强制结束"
  pkill -9 -x gzserver 2>/dev/null; sleep 1
fi
note "启动前 gzserver 残留: $(pgrep -xc gzserver 2>/dev/null || echo 0)"

# ---------- 1. colcon 构建 ----------
if [ "${SKIP_BUILD:-0}" = "1" ]; then
  note "----- [1/6] 跳过 colcon build（SKIP_BUILD=1，使用已有 install）-----"
else
  note "----- [1/6] colcon build -----"
  ( cd "$CWS" && source /opt/ros/humble/setup.bash && \
    colcon build --packages-select robot_description robot_control zhirong_maps \
        --symlink-install --event-handlers console_direct+ ) > "$LOGD/build.log" 2>&1
  check "colcon build 成功" $?
  tail -3 "$LOGD/build.log" | tee -a "$LOGD/summary.txt"
fi

# ---------- 2. 启动 launch ----------
note "----- [2/6] ros2 launch robot_control gazebo.launch.py -----"
( cd "$CWS" && source install/setup.bash && \
  exec ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none \
       verbose:=true ) > "$LOGD/launch.log" 2>&1 &
LPID=$!
sleep 2
note "launch pid=$LPID"

# 等待 /clock（最多 90s）
CLOCK_OK=1
for i in $(seq 1 90); do
  if timeout 3 ros2 topic echo /clock --once >/dev/null 2>&1; then CLOCK_OK=0; note " /clock 在 ${i}s 后可用"; break; fi
  sleep 1
done
check "gzserver 发布 /clock（仿真时钟运行）" $CLOCK_OK

# ---------- 3. 模型加载检查 ----------
note "----- [3/6] 场景模型 & 机器人加载检查 -----"
EXPECTED="zhirong_robot ground arena_floor cell_grid boundary_red zone_yellow zone_orange_ramp_1 zone_orange_ramp_2 zone_red wall_l_095_061 wall_l_130_052 wall_l_113_049 wall_a_frame_041_027 wall_horiz_100x006 wall_t_073_058_nw wall_t_073_058_sw wall_z_112_060 wall_l_114_048 wall_thin_085_008 wall_t_143_057 ramp_1 ramp_2 obstacle_i_089_049 red_barrier_left red_barrier_right target_hostage_1 target_chest_1 target_qr_1 target_hostage_2 target_chest_2 target_qr_2 ring_1 ring_2 ring_3 ring_4 ring_5 sign_entrance sign_exit gate_entrance_n gate_entrance_s gate_exit_n gate_exit_s spawn_marker"
MISS=0
for m in $EXPECTED; do
  if ! timeout 5 gz model -m "$m" -p > "$LOGD/model_$m.txt" 2>&1; then
    MISS=$((MISS+1)); note "  模型缺失: $m"; fi
done
check "场景+机器人关键模型全部加载（缺 $MISS 个）" $MISS
timeout 5 gz model -m zhirong_robot -p | tee "$LOGD/robot_pose_start.txt" | sed 's/^/ robot 初始位姿: /' | tee -a "$LOGD/summary.txt"

# ---------- 4. 控制闭环检查 ----------
note "----- [4/6] /cmd_vel 全向运动闭环检查 -----"
( cd "$CWS" && source install/setup.bash && \
  timeout 120 python3 "$WS/verification/check_gazebo_drive.py" ) > "$LOGD/drive_check.log" 2>&1
check "全向运动闭环（前进/横移/自转）" $?
cat "$LOGD/drive_check.log" | tee -a "$LOGD/summary.txt"
timeout 5 gz model -m zhirong_robot -p | tee "$LOGD/robot_pose_end.txt" | sed 's/^/ robot 结束位姿: /' | tee -a "$LOGD/summary.txt"

# ---------- 5. 话题/TF 汇总 ----------
note "----- [5/6] 话题 & TF 汇总 -----"
( cd "$CWS" && source install/setup.bash && timeout 10 ros2 topic list ) > "$LOGD/topics.txt" 2>&1
for t in /clock /odom /joint_states /cmd_vel /tf /robot_description; do
  if grep -qx "$t" "$LOGD/topics.txt"; then note "  话题存在: $t"; else note "  [警告] 话题缺失: $t"; fi
done
( cd "$CWS" && source install/setup.bash && timeout 10 ros2 run tf2_ros tf2_echo odom base_footprint ) > "$LOGD/tf_echo.log" 2>&1 &
TFPID=$!
sleep 6
kill $TFPID 2>/dev/null
if grep -q "Translation" "$LOGD/tf_echo.log"; then note "  TF odom->base_footprint: OK"; else note "  [警告] TF 未打印"; fi

# ---------- 6. 收尾 ----------
note "----- [6/6] 收尾 -----"
kill -TERM -"$LPID" 2>/dev/null || kill -TERM "$LPID" 2>/dev/null
sleep 3
pkill -TERM -x gzserver 2>/dev/null
pkill -TERM -x gzclient 2>/dev/null
sleep 2
pkill -KILL -x gzserver 2>/dev/null
REMAIN=$(pgrep -xc gzserver 2>/dev/null || true)
note "残留 gzserver: ${REMAIN:-0}"

note ""
note "===== 结果: PASS=$PASS FAIL=$FAIL ====="
[ "$FAIL" -eq 0 ] && note "ACCEPTANCE: PASS" || note "ACCEPTANCE: FAIL"
echo "$LOGD"
