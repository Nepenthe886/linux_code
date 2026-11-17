#!/usr/bin/env bash
# 重建后的最小冒烟：默认参数（自动加载比赛地图）-> /odom -> 前进 -> Ctrl-C 退出 -> 无残留
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
  >"$OUT/final_smoke.log" 2>&1 &
PID=$!
for i in $(seq 1 180); do
  timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom ready ($i x0.5s)"; break; }
  sleep 0.5
done
sleep 2
grep -E 'world =|gazebo.launch.py' "$OUT/final_smoke.log" | head -3
echo '--- 初始位姿 ---'; timeout 10 gz model -m zhirong_robot -p
timeout 10 ros2 topic echo --once /clock | head -3
timeout 30 python3 "$WS/preview/robot_gazebo/twist_phase.py" 0.3 0.0 0.0 2.0 2>&1 | tail -1
sleep 0.5
echo '--- 前进后位姿 ---'; timeout 10 gz model -m zhirong_robot -p
timeout 10 ros2 topic echo --once /odom | sed -n '1,10p'
echo '--- SIGINT 关闭 ---'
START=$(date +%s.%N)
kill -INT -"$PID" 2>/dev/null
for i in $(seq 1 60); do kill -0 "$PID" 2>/dev/null || break; sleep 0.5; done
END=$(date +%s.%N)
python3 -c "print('shutdown_seconds=%.1f' % ($END-$START))"
sleep 2
echo '--- 残留进程 ---'
ps -ef | grep -E 'gzserver|gzclient|ros2 launch|robot_state_publisher|spawn_entity' | grep -v grep || echo '（无残留进程）'
echo '--- 端口 11392 ---'
ss -lntu 2>/dev/null | grep 11392 || echo '（11392 已释放）'
echo '--- launch log 错误/警告 ---'
grep -E '\[Err\]|\[Wrn\]|\[ERROR\]' "$OUT/final_smoke.log" | grep -v "open display" | head -10 || true
