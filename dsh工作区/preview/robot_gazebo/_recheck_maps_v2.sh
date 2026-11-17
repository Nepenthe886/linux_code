#!/usr/bin/env bash
# zhirong_maps v2（42 include / 29 models，分块布局 + 不规则红边界）复测
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
cd "$WS"
source tools/gazebo_env.sh
. competition_ws/install/setup.bash
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
OUT="$WS/preview/robot_gazebo/evidence"
mkdir -p "$OUT"
cleanup() { pkill -x gzserver 2>/dev/null; }
trap cleanup EXIT

setsid ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none \
  >"$OUT/recheck_maps_v2.log" 2>&1 &
PID=$!
for i in $(seq 1 180); do timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom ready ($i x0.5s)"; break; }; sleep 0.5; done
sleep 2

echo '=== world 解析 ==='
grep -E 'world =|gazebo.launch.py' "$OUT/recheck_maps_v2.log" | head -3
echo '=== gzserver 进程的 GAZEBO_MODEL_PATH（验证 launch 自动注入）==='
GZPID=$(pgrep -x gzserver | head -1)
if [ -n "$GZPID" ]; then tr '\0' '\n' < /proc/"$GZPID"/environ | grep '^GAZEBO_MODEL_PATH=' | tr ':' '\n' | head -6; else echo '（gzserver 未找到）'; fi
echo '=== spawn 位姿 ==='; timeout 10 gz model -m zhirong_robot -p
echo '=== /clock ==='; timeout 10 ros2 topic echo --once /clock | head -4
echo '=== /odom ==='; timeout 10 ros2 topic echo --once /odom | sed -n '1,12p'
echo '=== v2 场景模型抽查（42 include）==='
ok=0; fail=0; missing=""
for m in ground arena_floor cell_grid boundary_red zone_yellow zone_orange_ramp_1 zone_orange_ramp_2 zone_red \
         wall_l_095_061 wall_l_130_052 wall_l_113_049 wall_a_frame_041_027 wall_horiz_100x006 \
         wall_t_073_058_nw wall_t_073_058_sw wall_z_112_060 wall_l_114_048 wall_thin_085_008 \
         obstacle_i_089_049 red_barrier_left red_barrier_right wall_t_143_057 \
         target_hostage_1 target_qr_1 target_chest_2 ring_1 ring_5 \
         sign_entrance sign_exit gate_entrance_n gate_entrance_s gate_exit_n gate_exit_s spawn_marker; do
  if timeout 8 gz model -m "$m" -p >/dev/null 2>&1; then ok=$((ok+1)); else fail=$((fail+1)); missing="$missing $m"; fi
done
echo "抽查结果: ok=$ok missing=$fail${missing:+ (缺失:$missing)}"
echo '=== 旧 v1 名字应当查不到（预期全部 no）==='
for m in arena_floor_5x5 zone_yellow_cross l_wall_112x060; do
  if timeout 8 gz model -m "$m" -p >/dev/null 2>&1; then echo "  $m: 存在（意料之外）"; else echo "  $m: 不存在（符合 v2 改名预期）"; fi
done
echo '=== missing model / SDF 错误 ==='
grep -E 'Unable to find model|Could not find|\[Err\]' "$OUT/recheck_maps_v2.log" | grep -v 'open display' | head -10 || true
echo '=== 前进 0.3m/s 2s ==='
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.3 0.0 0.0 2.0 2>&1 | tail -1
sleep 0.5
echo '--- 前进后位姿 ---'; timeout 10 gz model -m zhirong_robot -p
echo '--- 前进后 /odom ---'; timeout 10 ros2 topic echo --once /odom | sed -n '1,12p'
kill -INT -"$PID" 2>/dev/null
for i in $(seq 1 60); do kill -0 "$PID" 2>/dev/null || break; sleep 0.5; done
sleep 1
echo '=== 残留进程 / 端口 ==='
ps -ef | grep -E 'gzserver|gzclient|ros2 launch' | grep -v grep || echo '（无残留进程）'
ss -lntu 2>/dev/null | grep -E ':11392|:11345' || echo '（11345/11392 空闲）'
