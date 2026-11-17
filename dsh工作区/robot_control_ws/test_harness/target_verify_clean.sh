#!/usr/bin/env bash
# Clean regression against the deployed Zhirong Cup workspace:
#  1) headless launch + drive check (no GUI/RViz)
#  2) GUI launch + real X11 keys + screenshots + /odom check
# All long-running processes are started with setsid and killed as a process
# group so no stale nodes can survive and pollute later measurements.
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
export PYTHONDONTWRITEBYTECODE=1
export ROS_LOCALHOST_ONLY=1

start_launch() {  # $1=domain $2=log $3...=launch args
  local domain="$1" log="$2"; shift 2
  ROS_DOMAIN_ID="$domain" setsid ros2 launch robot_control teleop_gui.launch.py "$@" > "$log" 2>&1 &
  LAUNCH=$!
  for _ in $(seq 1 40); do
    grep -q "mecanum_sim 启动" "$log" 2>/dev/null && break
    sleep 0.5
  done
  sleep 2
}
stop_launch() {
  kill -INT -- -"$LAUNCH" 2>/dev/null || true
  sleep 3
  kill -TERM -- -"$LAUNCH" 2>/dev/null || true
  sleep 1
  kill -KILL -- -"$LAUNCH" 2>/dev/null || true
  sleep 1
}

echo "=========== 1) 无界面 launch + 麦轮驱动链路 ==========="
ROS_DOMAIN_ID=91 setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false gui:=false > "$WS/target_headless_clean.log" 2>&1 &
LAUNCH=$!
for _ in $(seq 1 40); do grep -q "mecanum_sim 启动" "$WS/target_headless_clean.log" 2>/dev/null && break; sleep 0.5; done
sleep 2
ROS_DOMAIN_ID=91 python3 "$WS/test_harness/check_drive.py"
stop_launch

echo "=========== 2) GUI launch + 真实 X11 按键 + 截图 ==========="
start_launch 92 "$WS/target_gui_clean.log" rviz:=false
python3 "$WS/test_harness/send_key.py" "麦伦机器人" w 2.0 30 &
KEY=$!
sleep 1.2
python3 "$WS/test_harness/grab_window.py" "$WS/preview/deployed_final_forward.png" "麦伦机器人"
wait "$KEY"
sleep 0.7
python3 "$WS/test_harness/send_key.py" "麦伦机器人" a 2.0 30 &
KEY=$!
sleep 1.2
python3 "$WS/test_harness/grab_window.py" "$WS/preview/deployed_final_strafe.png" "麦伦机器人"
wait "$KEY"
sleep 0.5
python3 "$WS/test_harness/send_key.py" "麦伦机器人" Up 1.5 30
sleep 0.6
echo "-- /odom（GUI 按键驱动后）"
ROS_DOMAIN_ID=92 python3 "$WS/test_harness/odom_probe.py" 3
echo "-- launch 错误检查"
grep -E "\[ERROR\]|Traceback" "$WS/target_gui_clean.log" | head -5 || true
stop_launch
echo "=========== 完成 ==========="
