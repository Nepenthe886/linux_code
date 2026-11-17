#!/usr/bin/env bash
# End-to-end launch check: installed teleop_gui.launch.py without GUI/RViz.
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
LOG="$WS/launch_check.log"
ros2 launch robot_control teleop_gui.launch.py rviz:=false gui:=false > "$LOG" 2>&1 &
LAUNCH=$!
cleanup() {
  kill -INT "$LAUNCH" 2>/dev/null
  sleep 3
  kill -INT "$LAUNCH" 2>/dev/null; sleep 1
  kill -9 "$LAUNCH" 2>/dev/null
}
trap cleanup EXIT
echo "== waiting for launch (log: $LOG)"
for i in $(seq 1 30); do
  if grep -q "mecanum_sim 启动" "$LOG" 2>/dev/null; then break; fi
  sleep 1
done
sleep 2
echo "== topics"
ros2 topic list | grep -E '^(/cmd_vel|/wheel_cmd|/joint_states|/odom|/robot_description|/tf|/tf_static)$' | sort
echo "== robot_description length"
ros2 topic echo --once /robot_description --field robot_description 2>&1 | head -2
echo "== TF base_footprint -> wheel_front_left_link"
timeout 12 ros2 run tf2_ros tf2_echo base_footprint wheel_front_left_link 2>&1 | head -6
echo "== drive check"
python3 "$WS/test_harness/check_drive.py"
RC=$?
echo "== launch log grep (errors)"
grep -E "\[ERROR\]|Traceback" "$LOG" | head -10 || true
echo "drive_check_rc=$RC"
exit $RC
