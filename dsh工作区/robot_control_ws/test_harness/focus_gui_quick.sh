#!/usr/bin/env bash
# Short, clean GUI focus-mode check (no long waits / less shared-display noise).
set +u
WS="$(cd "$(dirname "$0")/.." && pwd)"
PREV="$WS/preview"
source /opt/ros/humble/setup.bash
source /home/nepenthe/zmf/linux_code/competitions/Zhirong\ Cup/install/setup.bash
set -u
export DISPLAY=:1 ROS_HOME="$WS/ros_home" ROS_LOG_DIR="$WS/ros_logs" PYTHONDONTWRITEBYTECODE=1 ROS_LOCALHOST_ONLY=1
DOMAIN=156
LAUNCH=""
OTHER=""
cleanup() {
  [ -n "$OTHER" ] && kill "$OTHER" 2>/dev/null || true
  [ -n "$LAUNCH" ] && { kill -INT -- -"$LAUNCH" 2>/dev/null || true; sleep 2; kill -KILL -- -"$LAUNCH" 2>/dev/null || true; }
}
trap cleanup EXIT
ROS_DOMAIN_ID=$DOMAIN setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false > "$WS/focus_gui_quick.log" 2>&1 &
LAUNCH=$!
for _ in $(seq 1 40); do python3 "$WS/test_harness/focus_window.py" "遥控操作台" >/dev/null 2>&1 && break; sleep 1; done
sleep 2
ROS_DOMAIN_ID=$DOMAIN python3 "$WS/test_harness/wheel_timeline.py" 10 > "$PREV/focus_gui_quick_timeline.txt" 2>&1 &
TL=$!
python3 "$WS/test_harness/focus_window.py" "遥控操作台"
python3 "$WS/test_harness/send_key.py" "遥控操作台" k 0.15 0
sleep 0.8
python3 "$WS/test_harness/grab_window.py" "$PREV/focus_target_badge.png" "遥控操作台"
python3 "$WS/test_harness/other_app.py" 14 FocusTest-OtherApp > /dev/null 2>&1 &
OTHER=$!
sleep 1.2
python3 "$WS/test_harness/focus_window.py" FocusTest-OtherApp
sleep 0.2
python3 "$WS/test_harness/grab_window.py" "$PREV/focus_target_other_app.png"
python3 "$WS/test_harness/send_key.py" FocusTest-OtherApp w 1.5 30
sleep 0.5
python3 "$WS/test_harness/send_key.py" FocusTest-OtherApp k 0.15 0
sleep 0.8
python3 "$WS/test_harness/send_key.py" FocusTest-OtherApp w 1.0 30
sleep 0.2
wait "$TL"
wait "$OTHER"; OTHER=""
echo "--- timeline ---"
cat "$PREV/focus_gui_quick_timeline.txt"
echo "--- focus log ---"
grep -E "专注模式" "$WS/focus_gui_quick.log" | tail -4
