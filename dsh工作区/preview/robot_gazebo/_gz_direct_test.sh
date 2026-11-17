#!/usr/bin/env bash
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
cd "$WS"; source tools/gazebo_env.sh; . competition_ws/install/setup.bash
unset DISPLAY; export GAZEBO_MASTER_URI=http://127.0.0.1:11392; export ROS_DOMAIN_ID=42
LOG="$WS/preview/robot_gazebo/evidence/gz_direct.log"
cleanup(){ pkill -x gzserver 2>/dev/null; }; trap cleanup EXIT
gzserver --verbose -s libgazebo_ros_init.so -s libgazebo_ros_factory.so \
  "$WS/competition_ws/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world" >"$LOG" 2>&1 &
GZPID=$!
echo "gzserver pid=$GZPID"
for i in $(seq 1 40); do
  if ! kill -0 "$GZPID" 2>/dev/null; then echo "[FAIL] gzserver 已退出"; break; fi
  if timeout 3 gz model -m spawn_marker -p >/dev/null 2>&1; then echo "[ok] world ready after $i x0.5s"; break; fi
  sleep 0.5
done
echo '--- 直接查模型（带 timeout 3，观察 rc）---'
for m in spawn_marker definitely_not_a_model; do
  out=$(timeout 3 gz model -m "$m" -p 2>&1); rc=$?
  echo "name=$m rc=$rc out=[$(echo "$out" | tr '\n' ' ')]"
done
echo '--- gzserver log 前 30 行 ---'
head -30 "$LOG"
echo '--- gzserver 状态 ---'; kill -0 "$GZPID" 2>/dev/null && echo alive || echo dead
