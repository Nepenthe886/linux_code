#!/usr/bin/env bash
# colcon 安装后（install/setup.bash）启动验证 + world 自动解析 / 覆盖 / 报错
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
CWS="$WS/competition_ws"
cd "$WS"
source tools/gazebo_env.sh
. "$CWS/install/setup.bash"
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
export ROS_DOMAIN_ID=42
LOG="$WS/preview/robot_gazebo/installed"
mkdir -p "$LOG"
LAUNCH_PID=""
cleanup() {
  [ -n "$LAUNCH_PID" ] && kill -TERM -"$LAUNCH_PID" 2>/dev/null
  sleep 1
  pkill -x gzserver 2>/dev/null
  pkill -x gzclient 2>/dev/null
}
trap cleanup EXIT

echo "=== ros2 pkg prefix robot_control ==="
ros2 pkg prefix robot_control

echo '=== launch --show-args ==='
timeout 60 ros2 launch robot_control gazebo.launch.py --show-args 2>&1 | head -30

echo '=== 安装版默认启动（world 自动 -> 回退自带测试世界）==='
setsid ros2 launch robot_control gazebo.launch.py >"$LOG/default.log" 2>&1 &
LAUNCH_PID=$!
for i in $(seq 1 120); do
  timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom 出现"; break; }
  sleep 0.5
done
timeout 10 ros2 topic echo --once /clock 2>&1 | head -4
timeout 10 gz model -m zhirong_robot -p 2>&1
echo '--- 前进 0.3m/s 2s ---'
(timeout 3 ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}" >/dev/null 2>&1) &
sleep 2.2
timeout 5 ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}" >/dev/null 2>&1
sleep 1
timeout 10 gz model -m zhirong_robot -p 2>&1
timeout 10 ros2 topic echo --once /odom 2>&1 | sed -n '1,16p'
grep -E 'gazebo.launch.py' "$LOG/default.log" | head -4
kill -TERM -"$LAUNCH_PID" 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null; LAUNCH_PID=""

echo '=== ZHIRONG_MAPS_ROOT 模拟地图包 -> 自动解析 zhirong_maps world ==='
FAKE="$WS/preview/robot_gazebo/fake_maps"
mkdir -p "$FAKE/worlds"
cp "$CWS/src/robot/robot_control/worlds/test/gazebo_test.world" "$FAKE/worlds/zhirong_arena.world"
export ZHIRONG_MAPS_ROOT="$FAKE"
setsid ros2 launch robot_control gazebo.launch.py >"$LOG/maps.log" 2>&1 &
LAUNCH_PID=$!
for i in $(seq 1 120); do
  timeout 5 ros2 topic list 2>/dev/null | grep -qx /odom && { echo "[ok] /odom 出现"; break; }
  sleep 0.5
done
grep -E 'gazebo.launch.py' "$LOG/maps.log" | head -4
kill -TERM -"$LAUNCH_PID" 2>/dev/null; sleep 2; pkill -x gzserver 2>/dev/null; LAUNCH_PID=""
unset ZHIRONG_MAPS_ROOT

echo '=== world:= 不存在的路径 -> 清晰报错 ==='
timeout 30 ros2 launch robot_control gazebo.launch.py world:=/tmp/does_not_exist.world >"$LOG/bad_world.log" 2>&1
echo "exit=$?"
grep -E '错误|不存在|RuntimeError|world' "$LOG/bad_world.log" | head -6
