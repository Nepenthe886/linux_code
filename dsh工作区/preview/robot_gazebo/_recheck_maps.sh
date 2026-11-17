#!/usr/bin/env bash
# scene-builder 包定稿后复测：当前 world（41 include）+ 我的 launch 默认参数
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
cd "$WS"
source tools/gazebo_env.sh
. competition_ws/install/setup.bash
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
OUT="$WS/preview/robot_gazebo/evidence"
cleanup() { pkill -x gzserver 2>/dev/null; }
trap cleanup EXIT

setsid ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none \
  >"$OUT/recheck_maps.log" 2>&1 &
PID=$!
for i in $(seq 1 180); do timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && break; sleep 0.5; done
sleep 2
echo '=== world 解析 ==='
grep -E 'world =|gazebo.launch.py' "$OUT/recheck_maps.log" | head -3
echo '=== spawn 位姿 ==='; timeout 10 gz model -m zhirong_robot -p
echo '=== 场景模型抽查（应有 41 个 include）==='
ok=0; fail=0
for m in ground arena_floor spawn_marker gate_entrance_n gate_entrance_s zone_yellow zone_orange_ramp_1 ramp_1 ramp_2 target_hostage_1 target_qr_1 ring_1 ring_5 wall_l_095_061 wall_t_143_057 obstacle_i_089_049 sign_entrance sign_exit cell_grid boundary_red; do
  if timeout 8 gz model -m "$m" -p >/dev/null 2>&1; then ok=$((ok+1)); else fail=$((fail+1)); echo "MISSING: $m"; fi
done
echo "抽查结果: ok=$ok missing=$fail"
echo '=== missing model / SDF 警告 ==='
grep -E 'Unable to find model|Could not find|\[Err\]' "$OUT/recheck_maps.log" | grep -v 'open display' | head -10 || true
echo '=== /clock /joint_states /odom 存在性 ==='
timeout 10 ros2 topic list | grep -E '^/(clock|joint_states|odom)$'
echo '=== 前进 0.3m/s 2s ==='
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.3 0.0 0.0 2.0 2>&1 | tail -1
sleep 0.5; timeout 10 gz model -m zhirong_robot -p
kill -INT -"$PID" 2>/dev/null
for i in $(seq 1 60); do kill -0 "$PID" 2>/dev/null || break; sleep 0.5; done
sleep 1
echo '=== 残留进程 ==='
ps -ef | grep -E 'gzserver|gzclient|ros2 launch' | grep -v grep || echo '（无残留进程）'
