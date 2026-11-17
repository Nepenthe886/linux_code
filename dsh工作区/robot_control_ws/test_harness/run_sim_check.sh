#!/usr/bin/env bash
# Headless check of the simulated drivetrain (no colcon install needed).
set +u
WS="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WS/src/robot_control"
source /opt/ros/humble/setup.bash
set -u
export ROS_HOME="$WS/ros_home"
export ROS_LOG_DIR="$WS/ros_logs"
export ROS_DOMAIN_ID=79
export ROS_LOCALHOST_ONLY=1
mkdir -p "$ROS_HOME" "$ROS_LOG_DIR"
python3 -m robot_control.sim_node > "$WS/sim_standalone.log" 2>&1 &
SIM=$!
cleanup() { kill -INT "$SIM" 2>/dev/null; sleep 1; kill -9 "$SIM" 2>/dev/null; }
trap cleanup EXIT
sleep 2.5
python3 "$WS/test_harness/check_drive.py"
RC=$?
echo "check_rc=$RC"
echo "--- sim log tail ---"
tail -6 "$WS/sim_standalone.log"
exit $RC
