#!/usr/bin/env bash
# GUI end-to-end: installed launch (GUI + sim, no RViz), inject real X11 keys,
# screenshot while moving, then verify /odom moved.
set +u
WS="$(cd "$(dirname "$0")/.." && pwd)"
source /opt/ros/humble/setup.bash
source "$WS/install/setup.bash"
set -u
export DISPLAY=:1
export ROS_HOME="$WS/ros_home"
export ROS_LOG_DIR="$WS/ros_logs"
export ROS_DOMAIN_ID=79
export ROS_LOCALHOST_ONLY=1
LOG="$WS/gui_chain2.log"
PREV="$WS/preview"
ros2 launch robot_control teleop_gui.launch.py rviz:=false > "$LOG" 2>&1 &
LAUNCH=$!
cleanup() {
  kill -INT "$LAUNCH" 2>/dev/null
  sleep 3
  kill -INT "$LAUNCH" 2>/dev/null; sleep 1
  kill -9 "$LAUNCH" 2>/dev/null
}
trap cleanup EXIT
echo "== waiting for GUI window / nodes (log: $LOG)"
sleep 9
python3 "$WS/test_harness/send_key.py" "麦伦机器人" w 2.0 30 &
KEY1=$!
sleep 1.2
python3 "$WS/test_harness/grab_window.py" "$PREV/teleop_forward.png" "麦伦机器人"
wait "$KEY1"
sleep 0.6
python3 "$WS/test_harness/send_key.py" "麦伦机器人" a 2.0 30 &
KEY2=$!
sleep 1.2
python3 "$WS/test_harness/grab_window.py" "$PREV/teleop_strafe_left.png" "麦伦机器人"
wait "$KEY2"
sleep 0.4
python3 "$WS/test_harness/send_key.py" "麦伦机器人" Up 1.5 30
sleep 0.5
echo "== odom after GUI key driving"
python3 "$WS/test_harness/odom_probe.py" 3
echo "== launch errors"
grep -E "\[ERROR\]|Traceback" "$LOG" | head -10 || true
echo "== windows/done"
