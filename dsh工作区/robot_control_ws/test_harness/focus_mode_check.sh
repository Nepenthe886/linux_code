#!/usr/bin/env bash
# End-to-end focus-mode verification against the workspace install.
#   A) GUI: K enters focus mode, focus moves to another window, global W still
#      drives /wheel_cmd; global K exits; W then does nothing.
#   B) terminal teleop: pty sends K to enter focus mode, global W drives, global
#      K exits, W then does nothing, pty Ctrl-C exits gracefully.
set +u
WS="$(cd "$(dirname "$0")/.." && pwd)"
PREV="$WS/preview"
source /opt/ros/humble/setup.bash
INSTALL_SETUP="${INSTALL_SETUP:-$WS/install/setup.bash}"
source "$INSTALL_SETUP"
set -u
export DISPLAY=:1
export ROS_HOME="$WS/ros_home"
export ROS_LOG_DIR="$WS/ros_logs"
export PYTHONDONTWRITEBYTECODE=1
export ROS_LOCALHOST_ONLY=1
DOMAIN_A="${DOMAIN_A:-96}"
DOMAIN_B="${DOMAIN_B:-97}"

GUI_TITLE="遥控操作台"
OTHER_TITLE="FocusTest-OtherApp"
GUI_LAUNCH=""
SIM_LAUNCH=""
OTHER=""
cleanup() {
  [ -n "$OTHER" ] && kill "$OTHER" 2>/dev/null || true
  for group in "$GUI_LAUNCH" "$SIM_LAUNCH"; do
    [ -n "$group" ] && kill -INT -- -"$group" 2>/dev/null || true
  done
  sleep 2
  for group in "$GUI_LAUNCH" "$SIM_LAUNCH"; do
    [ -n "$group" ] || continue
    kill -TERM -- -"$group" 2>/dev/null || true
    sleep 1
    kill -KILL -- -"$group" 2>/dev/null || true
  done
}
trap cleanup EXIT

wait_window() {  # $1=title substring, $2=attempts
  for _ in $(seq 1 "${2:-30}"); do
    python3 "$WS/test_harness/focus_window.py" "$1" >/dev/null 2>&1 && return 0
    sleep 1
  done
  return 1
}

echo "================ A) GUI 专注模式 ================"
ROS_DOMAIN_ID="$DOMAIN_A" setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false > "$WS/focus_gui_launch.log" 2>&1 &
GUI_LAUNCH=$!
if ! wait_window "$GUI_TITLE" 40; then
  echo "GUI 窗口未出现"; tail -20 "$WS/focus_gui_launch.log"; exit 1
fi
sleep 2
ROS_DOMAIN_ID="$DOMAIN_A" python3 "$WS/test_harness/wheel_timeline.py" 42 > "$PREV/focus_gui_timeline.txt" 2>&1 &
TL=$!
python3 "$WS/test_harness/focus_window.py" "$GUI_TITLE"
echo "-- 按 K 进入专注模式"
python3 "$WS/test_harness/send_key.py" "$GUI_TITLE" k 0.15 0
sleep 1.0
python3 "$WS/test_harness/grab_window.py" "$PREV/focus_mode_badge.png" "$GUI_TITLE"
echo "-- 打开另一个应用并让焦点离开 GUI"
python3 "$WS/test_harness/other_app.py" 20 "$OTHER_TITLE" > "$WS/focus_other_app.log" 2>&1 &
OTHER=$!
sleep 1.2
python3 "$WS/test_harness/focus_window.py" "$OTHER_TITLE"
sleep 0.3
echo "-- 焦点在其它窗口时，全局按住 W 1.5s（期望仍输出前进轮速）"
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.5 30
sleep 0.5
echo "-- 全局按 K 退出专注模式"
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" k 0.15 0
sleep 0.8
echo "-- 未进入专注模式时，其它窗口按 W 1.0s（期望无运动）"
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.0 30
sleep 0.5
wait "$TL"
wait "$OTHER"
OTHER=""
echo "--- GUI /wheel_cmd 时间线 ---"
cat "$PREV/focus_gui_timeline.txt"
echo "--- GUI 专注模式日志 ---"
grep -E "专注模式" "$WS/focus_gui_launch.log" | tail -3
echo "--- GUI launch 错误 ---"
grep -E "\[ERROR\]|Traceback" "$WS/focus_gui_launch.log" | head -5 || true
cleanup
GUI_LAUNCH=""
sleep 1

echo "================ B) 终端遥控专注模式 ================"
STATE="$WS/preview/focus_terminal_state.txt"
rm -f "$STATE"
ROS_DOMAIN_ID="$DOMAIN_B" setsid ros2 launch robot_control teleop_gui.launch.py rviz:=false gui:=false > "$WS/focus_sim_launch.log" 2>&1 &
SIM_LAUNCH=$!
sleep 6
ROS_DOMAIN_ID="$DOMAIN_B" python3 "$WS/test_harness/wheel_timeline.py" 40 > "$PREV/focus_terminal_timeline.txt" 2>&1 &
TL=$!
python3 "$WS/test_harness/other_app.py" 40 "$OTHER_TITLE" > "$WS/focus_other_app2.log" 2>&1 &
OTHER=$!
sleep 1
echo "-- pty 启终端遥控并自动按 k 进入专注模式"
ROS_DOMAIN_ID="$DOMAIN_B" python3 "$WS/test_harness/pty_teleop.py" "$STATE" "$WS/focus_terminal_output.txt" > "$WS/focus_terminal_pty.log" 2>&1 &
PTY=$!
for _ in $(seq 1 120); do grep -q "FOCUS_ON" "$STATE" 2>/dev/null && break; sleep 0.25; done
echo "-- 终端状态: $(tr '\n' ' ' < "$STATE" 2>/dev/null)"
python3 "$WS/test_harness/focus_window.py" "$OTHER_TITLE"
sleep 0.3
echo "-- 焦点在其它窗口时，全局按住 W 1.5s（期望终端节点输出前进轮速）"
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.5 30
sleep 0.5
echo "-- 全局按 K 退出终端专注模式"
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" k 0.15 0
for _ in $(seq 1 40); do grep -q "FOCUS_OFF" "$STATE" 2>/dev/null && break; sleep 0.25; done
sleep 0.4
echo "-- 退出后其它窗口按 W 1.0s（期望无运动）"
python3 "$WS/test_harness/send_key.py" "$OTHER_TITLE" w 1.0 30
wait "$PTY"; PTY_RC=$?
wait "$TL"
wait "$OTHER"
OTHER=""
echo "--- pty 状态/退出 ---"
cat "$STATE"
echo "pty_exit=$PTY_RC"
echo "--- 终端节点输出（关键行）---"
grep -E "专注模式|无法开启|停车|键位|退出" "$WS/focus_terminal_output.txt" | tail -8 || tail -5 "$WS/focus_terminal_output.txt"
echo "--- 终端 /wheel_cmd 时间线 ---"
cat "$PREV/focus_terminal_timeline.txt"
echo "--- 无残留键盘抓取检查（应返回 success）---"
python3 - <<'PY'
from robot_control.focus_grab import X11KeyboardGrab
grab = X11KeyboardGrab(lambda name, pressed, ctrl: None)
ok, message = grab.start()
print("grab probe:", ok, message)
grab.stop()
sys.exit(0 if ok else 1)
PY
cleanup
SIM_LAUNCH=""
echo "================ 专注模式验收完成 ================"
