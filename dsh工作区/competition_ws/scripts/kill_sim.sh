#!/usr/bin/env bash
# 清理残留的 Gazebo / RViz / 仿真相关进程（避免 master 端口被占导致 gzserver 退出码 255）
# 用法: bash scripts/kill_sim.sh
set -o pipefail

echo "[kill_sim] 当前残留进程："
pgrep -ax gzserver 2>/dev/null | sed 's/^/  gzserver  /' || true
pgrep -ax gzclient 2>/dev/null | sed 's/^/  gzclient  /' || true

pkill -TERM -x gzclient 2>/dev/null || true
pkill -TERM -x gzserver 2>/dev/null || true
sleep 1
pkill -KILL -x gzclient 2>/dev/null || true
pkill -KILL -x gzserver 2>/dev/null || true
sleep 0.5

REMAIN=0
pgrep -x gzserver >/dev/null 2>&1 && REMAIN=$((REMAIN+1))
pgrep -x gzclient >/dev/null 2>&1 && REMAIN=$((REMAIN+1))
if [ "$REMAIN" -eq 0 ]; then
  echo "[kill_sim] 已清理干净。"
else
  echo "[kill_sim][警告] 仍有进程残留（可能不属于当前用户）："
  pgrep -ax gzserver 2>/dev/null | head -3
  pgrep -ax gzclient 2>/dev/null | head -3
fi
