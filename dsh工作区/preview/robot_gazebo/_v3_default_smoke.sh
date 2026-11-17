#!/usr/bin/env bash
# v3 默认模式复测（不带 ZHIRONG_MAPS_ROOT）：world/models 走 install share（symlink-install 指向 v3 源码），
# 验证 spawn、42 个 include 点名、/clock、/odom、/cmd_vel 前进、SIGINT 干净退出。
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
MAPS="$WS/competition_ws/src/maps/zhirong_maps"
cd "$WS"
source tools/gazebo_env.sh
. competition_ws/install/setup.bash
unset DISPLAY
unset ZHIRONG_MAPS_ROOT
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
OUT="$WS/preview/robot_gazebo/evidence"
mkdir -p "$OUT"
cleanup() { pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; }
trap cleanup EXIT

setsid ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none \
  >"$OUT/v3_default_launch.log" 2>&1 &
PID=$!
for i in $(seq 1 180); do timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom ready ($i x0.5s)"; break; }; sleep 0.5; done
READY=0
for i in $(seq 1 120); do
  out=$(timeout 5 gz model -m zhirong_robot -p 2>&1); set -- $out
  [ $# -eq 6 ] && { READY=1; echo "[ok] world+robot ready after $i x0.5s"; break; }; sleep 0.5
done
[ "$READY" = 1 ] || { echo "[FAIL] world 未就绪"; tail -25 "$OUT/v3_default_launch.log"; exit 1; }

{
echo '=== world 解析（应指向源码 v3）==='
grep -E 'world =|gazebo.launch.py' "$OUT/v3_default_launch.log" | head -4
echo
echo '=== gzserver GAZEBO_MODEL_PATH（含 zhirong 的条目）==='
GZPID=$(pgrep -x gzserver | head -1)
tr '\0' '\n' < /proc/"$GZPID"/environ | grep '^GAZEBO_MODEL_PATH=' | tr ':' '\n' | grep zhirong || echo '(未找到!)'
echo
echo '=== 源码 v3 版本线索 ==='
echo "world mtime: $(stat -c %y "$MAPS/worlds/zhirong_arena.world")"
echo "models 数: $(ls "$MAPS/models" | wc -l)  桔区: $(ls "$MAPS/models" | grep -i orange | tr '\n' ' ')"
echo "include 数: $(grep -c '<include>' "$MAPS/worlds/zhirong_arena.world")"
echo
echo '=== 机器人 spawn 位姿 ==='
timeout 10 gz model -m zhirong_robot -p
echo
echo '=== /clock ==='
timeout 10 ros2 topic echo --once /clock | head -4
echo
echo '=== /odom ==='
timeout 10 ros2 topic echo --once /odom | sed -n '1,12p'
echo
echo '=== v3 world 全量点名（42 个 include 实例）==='
VALID=0; INVALID=0; BAD=""
for m in $(grep -oE '<name>[^<]+' "$MAPS/worlds/zhirong_arena.world" | sed 's/<name>//'); do
  out=$(timeout 8 gz model -m "$m" -p 2>&1); set -- $out
  if [ $# -eq 6 ]; then VALID=$((VALID+1)); else INVALID=$((INVALID+1)); BAD="$BAD $m"; fi
done
echo "结果: 存在=$VALID 缺失=$INVALID${BAD:+  缺失名单:$BAD}"
echo
echo '=== v3 关键变化抽查 ==='
for m in zone_orange_ramp_1 zone_orange_ramp_2 ramp_1 ramp_2 zone_yellow zone_red; do
  out=$(timeout 8 gz model -m "$m" -p 2>&1); set -- $out
  if [ $# -eq 6 ]; then printf '  %-20s 存在  pose=%s\n' "$m" "$*"; else printf '  %-20s 缺失\n' "$m"; fi
done
echo "旧实体 zone_orange_disc: $(grep -c 'zone_orange_disc' "$MAPS/worlds/zhirong_arena.world") 次出现（应为 0）"
echo
echo '=== missing model / SDF 错误 ==='
grep -E 'Unable to find model|Unable to find uri|Could not find|\[Err\]' "$OUT/v3_default_launch.log" | grep -v 'open display' | head -10 || true
echo
echo '=== /cmd_vel 前进 0.3 m/s x 2 s ==='
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.3 0.0 0.0 2.0 2>&1 | tail -1
sleep 0.5
echo '--- 前进后 gz model -p ---'; timeout 10 gz model -m zhirong_robot -p
echo '--- 前进后 /odom ---'; timeout 10 ros2 topic echo --once /odom | sed -n '1,12p'
} >"$OUT/v3_default_source.txt" 2>&1
cat "$OUT/v3_default_source.txt"

echo '=== SIGINT 关闭 ==='
kill -INT -"$PID" 2>/dev/null
for i in $(seq 1 60); do kill -0 "$PID" 2>/dev/null || break; sleep 0.5; done
sleep 1
{ echo '=== 残留进程 / 端口 ==='
  ps -ef | grep -E 'gzserver|gzclient|ros2 launch' | grep -v grep || echo '（无残留进程）'
  ss -lntu 2>/dev/null | grep -E ':11392|:11345' || echo '（11345/11392 空闲）'
} | tee -a "$OUT/v3_default_source.txt"
