#!/usr/bin/env bash
# Verify "focus mode ON by default" against a deployed install.
#   A) GUI starts with focus mode already on (no click), focus moved to another
#      window -> W still drives the robot; K exits; W then does nothing.
#   B) terminal teleop auto-enters focus mode at startup; global W drives; global
#      K exits; Ctrl-C exits gracefully.
#   C) GUI with focus_mode:=false does NOT grab the keyboard.
set +u
WS="$(cd "$(dirname "$0")/.." && pwd)"
PREV="$WS/preview"
INSTALL_SETUP="${INSTALL_SETUP:-$WS/install/setup.bash}"
source /opt/ros/humble/setup.bash
source "$INSTALL_SETUP"
set -u
export DISPLAY=:1 ROS_HOME="$WS/ros_home" ROS_LOG_DIR="$WS/ros_logs" PYTHONDONTWRITEBYTECODE=1 ROS_LOCALHOST_ONLY=1
GUI_TITLE="遥控操作台"
OTHER_TITLE="FocusTest-OtherApp"
LAUNCH=""
OTHER=""
cleanup() {
  [ -n "$OTHER" ] && kill "$OTHER" 2>/dev/null || true
  if [ -n "$LAUNCH" ]; then
    kill -INT -- -"$LAUNCH" 2>/dev/null || true
    sleep 2
    kill -KILL -- -"$LAUNCH" 2>/dev/null || true
    LAUNCH=""
  fi
}
trap cleanup EXIT

wait_window() {
  for _ in $(seq 1 "${2:-40}"); do
    python3 "$WS/test_harness/window_exists.py" "$1" 2>/dev/null && return 0
    sleep 1
  done
  return 1
}
wait_log() {  # $1 log, $2 pattern, $3 attempts
  for _ in $(seq 1 "${3:-40}"); do grep -q "$2" "$1" 2>/dev/null && return 0; sleep 0.5; done
  return 1
}

echo "================ A) GUI 默认开启专注模式 ================"
DOMAIN_A=166
ROS_DOMAIN_ID=$DOMAIN_A setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false > "$WS/default_gui_launch.log" 2>&1 &
LAUNCH=$!
if ! wait_window "$GUI_TITLE" 40; then echo "GUI 窗口未出现"; tail -20 "$WS/default_gui_launch.log"; exit 1; fi
sleep 2
if grep -q "默认进入专注模式\|已进入专注模式" "$WS/default_gui_launch.log"; then
  echo "[OK] 启动后未点击窗口即自动进入专注模式: $(grep -E '默认进入专注模式|已进入专注模式' "$WS/default_gui_launch.log" | tail -1)"
else
  echo "[FAIL] 启动后没有自动进入专注模式"; grep -E "专注模式" "$WS/default_gui_launch.log" | tail -3
fi
python3 "$WS/test_harness/raise_window.py" "$GUI_TITLE" >/dev/null
python3 "$WS/test_harness/grab_window.py" "$PREV/default_focus_badge.png" "$GUI_TITLE"
ROS_DOMAIN_ID=$DOMAIN_A python3 "$WS/test_harness/wheel_timeline.py" 14 > "$PREV/default_focus_gui_timeline.txt" 2>&1 &
TL=$!
python3 "$WS/test_harness/other_app.py" 16 "$OTHER_TITLE" > /dev/null 2>&1 &
OTHER=$!
sleep 1.2
python3 "$WS/test_harness/focus_window.py" "$OTHER_TITLE"
sleep 0.3
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.5 30
sleep 0.5
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" k 0.15 0
sleep 0.8
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.0 30
sleep 0.4
wait "$TL"; wait "$OTHER"; OTHER=""
echo "--- A 时间线（焦点在其它窗口时按 W）---"
cat "$PREV/default_focus_gui_timeline.txt"
echo "--- A 专注模式日志 ---"
grep -E "专注模式" "$WS/default_gui_launch.log" | tail -4
cleanup
sleep 1

echo "================ B) 终端遥控默认开启专注模式 ================"
DOMAIN_B=167
STATE="$PREV/default_focus_terminal_state.txt"; rm -f "$STATE"
ROS_DOMAIN_ID=$DOMAIN_B setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false gui:=false > "$WS/default_sim_launch.log" 2>&1 &
LAUNCH=$!
sleep 6
ROS_DOMAIN_ID=$DOMAIN_B python3 "$WS/test_harness/wheel_timeline.py" 28 > "$PREV/default_focus_terminal_timeline.txt" 2>&1 &
TL=$!
python3 "$WS/test_harness/other_app.py" 24 "$OTHER_TITLE" > /dev/null 2>&1 &
OTHER=$!
sleep 1
ROS_DOMAIN_ID=$DOMAIN_B python3 "$WS/test_harness/pty_teleop_default.py" "$STATE" "$WS/default_focus_terminal_output.txt" > "$WS/default_focus_pty.log" 2>&1 &
PTY=$!
for _ in $(seq 1 80); do grep -q "FOCUS_ON_AUTO\|FOCUS_ON_TIMEOUT" "$STATE" 2>/dev/null && break; sleep 0.25; done
echo "--- B 启动状态：$(tr '\n' ' ' < "$STATE" 2>/dev/null)"
python3 "$WS/test_harness/focus_window.py" "$OTHER_TITLE"
sleep 0.3
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.5 30
sleep 0.5
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" k 0.15 0
for _ in $(seq 1 40); do grep -q "FOCUS_OFF\|FOCUS_OFF_TIMEOUT" "$STATE" 2>/dev/null && break; sleep 0.25; done
sleep 0.4
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.0 30
wait "$PTY"; PTY_RC=$?
wait "$TL"; wait "$OTHER"; OTHER=""
echo "--- B 状态 ---"; cat "$STATE"
echo "pty_exit=$PTY_RC"
echo "--- B 时间线 ---"; cat "$PREV/default_focus_terminal_timeline.txt"
echo "--- B 节点输出关键行 ---"; grep -E "专注模式|无法开启|默认" "$WS/default_focus_terminal_output.txt" | head -5
cleanup
sleep 1

echo "================ C) focus_mode:=false 不自动抓取 ================"
DOMAIN_C=168
ROS_DOMAIN_ID=$DOMAIN_C setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false focus_mode:=false > "$WS/default_gui_off_launch.log" 2>&1 &
LAUNCH=$!
if ! wait_window "$GUI_TITLE" 40; then echo "C GUI 窗口未出现"; exit 1; fi
sleep 2
if grep -q "已进入专注模式" "$WS/default_gui_off_launch.log"; then
  echo "[FAIL] focus_mode:=false 仍然进入专注模式"
else
  echo "[OK] focus_mode:=false 未进入专注模式"
fi
python3 "$WS/test_harness/other_app.py" 8 "$OTHER_TITLE" > /dev/null 2>&1 &
OTHER=$!
sleep 1
python3 "$WS/test_harness/focus_window.py" "$OTHER_TITLE"
ROS_DOMAIN_ID=$DOMAIN_C python3 "$WS/test_harness/wheel_timeline.py" 6 > "$PREV/default_focus_off_timeline.txt" 2>&1
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.2 30
sleep 0.5
wait "$OTHER"; OTHER=""
echo "--- C 时间线（应为全零/无变化）---"
cat "$PREV/default_focus_off_timeline.txt"
cleanup
echo "================ 默认专注模式验收完成 ================"
