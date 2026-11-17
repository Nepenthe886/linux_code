#!/bin/bash
# 对比实验：不同世界/客户端环境下的 gzclient 画面与状态（Xvfb 软件 GL）
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
LOG=$WS/verification/logs/gzclient_shot
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=141
unset GAZEBO_MODEL_PATH
MAPS_MODELS="$CWS/install/zhirong_maps/share/zhirong_maps/models"
ARENA="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
EMPTY="/usr/share/gazebo-11/worlds/empty.world"
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3

run_case () { # $1名称 $2 world $3 port $4 client_has_model_path(yes/no)
  local name=$1 world=$2 port=$3 hasmodel=$4
  export GAZEBO_MASTER_URI="http://127.0.0.1:${port}"
  rm -rf "$HOME/.gazebo/client-${port}"
  GAZEBO_MODEL_PATH="$MAPS_MODELS" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
    gzserver "$world" > "$LOG/${name}_server.log" 2>&1 & SP=$!
  sleep 6
  if [ "$hasmodel" = "yes" ]; then
    env "GAZEBO_MODEL_PATH=$MAPS_MODELS" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
      gzclient > "$LOG/${name}_client.log" 2>&1 & CP=$!
  else
    DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient > "$LOG/${name}_client.log" 2>&1 & CP=$!
  fi
  sleep 18
  local cpu=$(ps -o pcpu= -p $CP 2>/dev/null | tr -d ' ')
  xwd -root -display :99 -out "$LOG/${name}.xwd" >/dev/null 2>&1
  python3 "$WS/tools/xwd2png.py" "$LOG/${name}.xwd" "$LOG/${name}.png" >/dev/null 2>&1
  echo "### $name: alive=$(kill -0 $CP 2>/dev/null && echo YES || echo NO) cpu=${cpu}%"
  echo "    client log: $(grep -ac 'model database' "$HOME/.gazebo/client-${port}/default.log" 2>/dev/null) 条 model-database 消息; $(wc -l < "$HOME/.gazebo/client-${port}/default.log" 2>/dev/null) 行"
  kill -9 $CP $SP 2>/dev/null; sleep 1
  pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1
  unset GAZEBO_MASTER_URI
}
echo "=== A) 空世界 ==="; run_case A_empty "$EMPTY" 11511 no
echo "=== B) 比赛世界, 客户端无 GAZEBO_MODEL_PATH ==="; run_case B_arena_nomodel "$ARENA" 11512 no
echo "=== C) 比赛世界, 客户端有 GAZEBO_MODEL_PATH ==="; run_case C_arena_with_model "$ARENA" 11513 yes
kill $XP 2>/dev/null
ls -la "$LOG"/*.png
