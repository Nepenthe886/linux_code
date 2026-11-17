#!/usr/bin/env bash
# Verify the deployed package in the Zhirong Cup workspace: GUI launch + real
# X11 key injection + screenshot + /odom check.
set +u
WS="/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws"
TARGET="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
source /opt/ros/humble/setup.bash
cd "$TARGET"
source install/setup.bash
set -u
export DISPLAY=:1
export ROS_HOME="$WS/ros_home"
export ROS_LOG_DIR="$WS/ros_logs"
export ROS_DOMAIN_ID=82
export ROS_LOCALHOST_ONLY=1
echo "== launch args (installed share)"
ros2 launch robot_control teleop_gui.launch.py --show-args 2>&1 | head -20
LOG="$WS/target_gui_check.log"
ros2 launch robot_control teleop_gui.launch.py rviz:=false > "$LOG" 2>&1 &
LAUNCH=$!
cleanup() {
  kill -INT "$LAUNCH" 2>/dev/null || true
  sleep 3
  kill -INT "$LAUNCH" 2>/dev/null || true; sleep 1
  kill -9 "$LAUNCH" 2>/dev/null || true
}
trap cleanup EXIT
sleep 10
python3 "$WS/test_harness/send_key.py" "麦伦机器人" w 2.0 30 &
KEY=$!
sleep 1.2
python3 "$WS/test_harness/grab_window.py" "$WS/preview/deployed_gui_forward.png" "麦伦机器人"
wait "$KEY"
sleep 0.4
python3 "$WS/test_harness/send_key.py" "麦伦机器人" Left 1.5 30
sleep 0.5
echo "== odom after deployed GUI driving"
python3 "$WS/test_harness/odom_probe.py" 3
echo "== errors in launch log"
grep -E "\[ERROR\]|Traceback" "$LOG" | head -5 || true
