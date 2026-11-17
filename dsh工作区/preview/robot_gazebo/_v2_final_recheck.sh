#!/usr/bin/env bash
# zhirong_maps v2 定稿复测（当前 launch）：spawn / 42 include 全量点名 / odom / 前进 / 干净退出
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
cleanup() { pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; }
trap cleanup EXIT

setsid ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none \
  >"$OUT/v2_final_launch.log" 2>&1 &
PID=$!
for i in $(seq 1 180); do timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom ready ($i x0.5s)"; break; }; sleep 0.5; done
# 等 world 完全加载（机器人可查询）
READY=0
for i in $(seq 1 120); do
  out=$(timeout 5 gz model -m zhirong_robot -p 2>&1)
  set -- $out
  if [ $# -eq 6 ]; then READY=1; echo "[ok] world+robot ready after $i x0.5s"; break; fi
  sleep 0.5
done
[ "$READY" = 1 ] || { echo "[FAIL] world 未就绪"; tail -20 "$OUT/v2_final_launch.log"; exit 1; }

{
echo '=== world 解析 ==='
grep -E 'world =|gazebo.launch.py' "$OUT/v2_final_launch.log" | head -4
echo
echo '=== gzserver GAZEBO_MODEL_PATH（只列含 zhirong 的条目）==='
GZPID=$(pgrep -x gzserver | head -1)
tr '\0' '\n' < /proc/"$GZPID"/environ | grep '^GAZEBO_MODEL_PATH=' | tr ':' '\n' | grep zhirong || echo '(未找到 zhirong models 条目!)'
echo
echo '=== 机器人 spawn 位姿（gz model -p: x y z r p yaw）==='
timeout 10 gz model -m zhirong_robot -p
echo
echo '=== /clock ==='
timeout 10 ros2 topic echo --once /clock | head -4
echo
echo '=== /odom ==='
timeout 10 ros2 topic echo --once /odom | sed -n '1,12p'
echo
echo '=== v2 world 全量 42 个 include 名点名 ==='
VALID=0; INVALID=0; BAD=""
for m in $(grep -oE '<name>[^<]+' "$WS/competition_ws/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world" | sed 's/<name>//'); do
  out=$(timeout 8 gz model -m "$m" -p 2>&1)
  set -- $out
  if [ $# -eq 6 ]; then VALID=$((VALID+1)); else INVALID=$((INVALID+1)); BAD="$BAD $m"; fi
done
echo "结果: 存在=$VALID 缺失=$INVALID${BAD:+  缺失名单:$BAD}"
echo
echo '=== 旧 v1 名字（预期：不存在）==='
for m in arena_floor_5x5 zone_yellow_cross l_wall_112x060; do
  out=$(timeout 8 gz model -m "$m" -p 2>&1)
  set -- $out
  if [ $# -eq 6 ]; then echo "  $m: 仍存在（与 v2 不符）"; else echo "  $m: 不存在（符合 v2）"; fi
done
echo
echo '=== missing model / SDF 错误 ==='
grep -E 'Unable to find model|Unable to find uri|Could not find|\[Err\]' "$OUT/v2_final_launch.log" | grep -v 'open display' | head -10 || true
echo
echo '=== /cmd_vel 前进 0.3 m/s x 2 s ==='
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.3 0.0 0.0 2.0 2>&1 | tail -1
sleep 0.5
echo '--- 前进后 gz model -p ---'; timeout 10 gz model -m zhirong_robot -p
echo '--- 前进后 /odom ---'; timeout 10 ros2 topic echo --once /odom | sed -n '1,12p'
} >"$OUT/v2_final_recheck.txt" 2>&1
cat "$OUT/v2_final_recheck.txt"

echo '=== SIGINT 关闭（等价 Ctrl-C）==='
kill -INT -"$PID" 2>/dev/null
for i in $(seq 1 60); do kill -0 "$PID" 2>/dev/null || break; sleep 0.5; done
sleep 1
{ echo '=== 残留进程 / 端口 ==='
  ps -ef | grep -E 'gzserver|gzclient|ros2 launch' | grep -v grep || echo '（无残留进程）'
  ss -lntu 2>/dev/null | grep -E ':11392|:11345' || echo '（11345/11392 空闲）'
} | tee -a "$OUT/v2_final_recheck.txt"
