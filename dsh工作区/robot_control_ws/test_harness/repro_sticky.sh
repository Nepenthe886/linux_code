#!/usr/bin/env bash
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws"
TARGET="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
source /opt/ros/humble/setup.bash
cd "$TARGET"; source install/setup.bash
set -u
export DISPLAY=:1 ROS_HOME="$WS/ros_home" ROS_LOG_DIR="$WS/ros_logs" ROS_DOMAIN_ID=83 ROS_LOCALHOST_ONLY=1
ros2 launch robot_control teleop_gui.launch.py rviz:=false > "$WS/repro_sticky.log" 2>&1 &
LAUNCH=$!
cleanup() { kill -INT "$LAUNCH" 2>/dev/null || true; sleep 3; kill -INT "$LAUNCH" 2>/dev/null || true; sleep 1; kill -9 "$LAUNCH" 2>/dev/null || true; }
trap cleanup EXIT
sleep 10
python3 "$WS/test_harness/wheel_timeline.py" 8 > "$WS/repro_timeline.txt" 2>&1 &
TL=$!
sleep 1.0
echo "-- press Left 1.0s, release" 
python3 "$WS/test_harness/send_key.py" "麦伦机器人" Left 1.0 30
sleep 2.5
echo "-- press W 0.6s, release (to check recovery)"
python3 "$WS/test_harness/send_key.py" "麦伦机器人" w 0.6 30
wait $TL
cat "$WS/repro_timeline.txt"
