#!/bin/bash
# 实验：对比 gzclient 在不同世界/环境/并发条件下是否卡在 model database 更新
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
LOG=$WS/verification/logs/gzclient_hang
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=140
unset GAZEBO_MODEL_PATH
MAPS_MODELS="$CWS/install/zhirong_maps/share/zhirong_maps/models"
ARENA="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
EMPTY="/usr/share/gazebo-11/worlds/empty.world"
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3

run_case () { # $1=名称 $2=world $3=master端口 $4=client额外env (字符串 key=val;key2=val2)
  local name=$1 world=$2 port=$3 extra=$4
  export GAZEBO_MASTER_URI="http://127.0.0.1:${port}"
  rm -f "$HOME/.gazebo/client-${port}/default.log"
  GAZEBO_MODEL_PATH="$MAPS_MODELS" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
    gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$world" > "$LOG/${name}_server.log" 2>&1 & SP=$!
  sleep 6
  # 启动客户端（按需注入环境）
  if [ -n "$extra" ]; then
    env $extra GAZEBO_MASTER_URI="$GAZEBO_MASTER_URI" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
      gzclient > "$LOG/${name}_client.log" 2>&1 & CP=$!
  else
    DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient > "$LOG/${name}_client.log" 2>&1 & CP=$!
  fi
  sleep 20
  echo "### $name：客户端存活=$(kill -0 $CP 2>/dev/null && echo YES || echo NO) CPU=$(ps -o pcpu= -p $CP 2>/dev/null | tr -d ' ')%"
  # 客户端 transport 日志关键行
  echo "    --- client default.log 关键行 ---"
  grep -aE "Connected|Waiting for model database|Loaded .ini|Loading world|model database update to complete" "$HOME/.gazebo/client-${port}/default.log" 2>/dev/null | head -6
  echo "    --- client 终端输出 ---"
  tail -3 "$LOG/${name}_client.log" 2>/dev/null
  kill -9 $CP $SP 2>/dev/null; sleep 1
  pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1
  unset GAZEBO_MASTER_URI
}

echo "===== A) 空世界 + 无 GAZEBO_MODEL_PATH ====="
run_case A_empty "$EMPTY" 11501 ""
echo
echo "===== B) 比赛世界 + 客户端无 GAZEBO_MODEL_PATH（≈ launch 现状）====="
run_case B_arena_nomodel "$ARENA" 11502 ""
echo
echo "===== C) 比赛世界 + 客户端有 GAZEBO_MODEL_PATH ====="
run_case C_arena_with_model "$ARENA" 11503 "GAZEBO_MODEL_PATH=$MAPS_MODELS"

kill $XP 2>/dev/null
