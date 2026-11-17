#!/usr/bin/env bash
# 在虚拟 X (Xvfb) 上启动 gzclient 并截图，用于无物理显示器的 Gazebo 场景可视化验证。
# 用法: capture_gui.sh <world文件> <输出png> [等待秒数] [master端口]
set -o pipefail
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
WORLD="${1:?用法: capture_gui.sh <world> <out.png> [wait] [port]}"
OUT="${2:?用法: capture_gui.sh <world> <out.png> [wait] [port]}"
WAIT="${3:-25}"
PORT="${4:-11393}"
DISP=":99"
export GAZEBO_MASTER_URI="http://127.0.0.1:${PORT}"
source "$WS/tools/gazebo_env.sh"
export DISPLAY="$DISP" LIBGL_ALWAYS_SOFTWARE=1
mkdir -p "$(dirname "$OUT")"
TMP="$(dirname "$OUT")"
# 清理可能残留的本用途进程
pkill -f 'gzclient[ ]--capture' 2>/dev/null || true
Xvfb "$DISP" -screen 0 1400x1000x24 +extension GLX +render -noreset > "$TMP/xvfb_gui.log" 2>&1 &
XPID=$!
sleep 2
gzserver "$WORLD" --verbose > "$TMP/gzserver_gui.log" 2>&1 &
SPID=$!
sleep 6
gzclient > "$TMP/gzclient.log" 2>&1 &
CPID=$!
sleep "$WAIT"
xwd -root -display "$DISP" -out "$TMP/_shot.xwd" 2>>"$TMP/gzclient.log"
python3 "$WS/tools/xwd2png.py" "$TMP/_shot.xwd" "$OUT" >>"$TMP/gzclient.log" 2>&1
RC=$?
kill $CPID $SPID $XPID 2>/dev/null
sleep 1
echo "capture rc=$RC out=$OUT"
exit $RC
