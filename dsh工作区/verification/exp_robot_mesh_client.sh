#!/bin/bash
# 确认实验：世界里有机器人（model://robot_description/meshes）时，
# gzclient 若没有 GAZEBO_MODEL_PATH 会不会卡在 model database 更新
WS=/home/nepenthe/zmf/linux_code/dsh工作区
CWS="/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
LOG=$WS/verification/logs/robot_mesh_client
mkdir -p "$LOG" /tmp/.X11-unix
source /opt/ros/humble/setup.bash
source "$CWS/install/setup.bash" 2>/dev/null
export HOME="$WS/gazebo_home" ROS_LOG_DIR="$LOG/ros_logs" ROS_DOMAIN_ID=142
unset GAZEBO_MODEL_PATH
MAPS_MODELS="$CWS/install/zhirong_maps/share/zhirong_maps/models"
ROBOT_MODELS="$CWS/install/robot_control/share/robot_control/models"
ARENA="$CWS/install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world"
RD="$CWS/install/robot_description/share/robot_description"
python3 - "$RD/urdf/omni_robot.urdf" "$LOG/robot_gazebo.urdf" <<'PY'
import sys
s=open(sys.argv[1],encoding='utf-8').read().replace("package://robot_description/","model://robot_description/")
open(sys.argv[2],'w',encoding='utf-8').write(s)
PY
"$WS/gazebo_userland/usr/bin/Xvfb" :99 -screen 0 1600x1000x24 +extension GLX +render -noreset > "$LOG/xvfb.log" 2>&1 & XP=$!
sleep 3

case_run () { # $1=name $2=port $3=client_model_path(yes/no)
  local name=$1 port=$2 has=$3
  export GAZEBO_MASTER_URI="http://127.0.0.1:${port}"
  rm -rf "$HOME/.gazebo/client-${port}" "$HOME/.gazebo/server-${port}"
  GAZEBO_MODEL_PATH="$ROBOT_MODELS:$MAPS_MODELS" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 \
    gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so "$ARENA" > "$LOG/${name}_server.log" 2>&1 & SP=$!
  sleep 6
  ros2 run gazebo_ros spawn_entity.py -file "$LOG/robot_gazebo.urdf" -entity zhirong_robot -x 2.9 -y 1.6 -z 0.05 -Y 3.14159 > "$LOG/${name}_spawn.log" 2>&1
  sleep 2
  if [ "$has" = "yes" ]; then
    env "GAZEBO_MODEL_PATH=$ROBOT_MODELS:$MAPS_MODELS" DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient > "$LOG/${name}_client.log" 2>&1 & CP=$!
  else
    DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient > "$LOG/${name}_client.log" 2>&1 & CP=$!
  fi
  sleep 22
  echo "### $name (client_model_path=$has): alive=$(kill -0 $CP 2>/dev/null && echo YES || echo NO) cpu=$(ps -o pcpu= -p $CP 2>/dev/null | tr -d ' ')%"
  echo "   client log 关键行:"
  grep -aE "Waiting for model database|model database update to complete|URI not supported by Fuel|No mesh specified|Connected" "$HOME/.gazebo/client-${port}/default.log" 2>/dev/null | head -8 | sed 's/^/     /'
  xwd -root -display :99 -out "$LOG/${name}.xwd" >/dev/null 2>&1
  python3 "$WS/tools/xwd2png.py" "$LOG/${name}.xwd" "$LOG/${name}.png" >/dev/null 2>&1
  kill -9 $CP $SP 2>/dev/null; sleep 1
  pkill -x gzserver 2>/dev/null; pkill -x gzclient 2>/dev/null; sleep 1
  unset GAZEBO_MASTER_URI
}
case_run NO_MODEL_PATH 11521 no
case_run WITH_MODEL_PATH 11522 yes
kill $XP 2>/dev/null
ls -la "$LOG"/*.png
