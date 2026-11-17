#!/usr/bin/env bash
# 用户态 Gazebo Classic 11 环境（无 sudo 安装）。用法： source tools/gazebo_env.sh
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
PREFIX="$WS/gazebo_userland"
# ROS 基础环境（系统已装 Humble）
if [ -f /opt/ros/humble/setup.bash ]; then
  . /opt/ros/humble/setup.bash
fi
export PREFIX
# 优先使用前缀里的库/程序
export PATH="$PREFIX/usr/bin:$PREFIX/opt/ros/humble/bin:$PATH"
export LD_LIBRARY_PATH="$PREFIX/usr/lib/x86_64-linux-gnu:$PREFIX/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:$PREFIX/usr/lib:$PREFIX/opt/ros/humble/lib:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$PREFIX/opt/ros/humble/lib/python3.10/site-packages:$PREFIX/opt/ros/humble/local/lib/python3.10/dist-packages:${PYTHONPATH:-}"
export PKG_CONFIG_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/pkgconfig:$PREFIX/usr/share/pkgconfig:${PKG_CONFIG_PATH:-}"
export CMAKE_PREFIX_PATH="$PREFIX/opt/ros/humble:$PREFIX/usr:${CMAKE_PREFIX_PATH:-}"
export AMENT_PREFIX_PATH="$PREFIX/opt/ros/humble:${AMENT_PREFIX_PATH:-/opt/ros/humble}"
# Gazebo 资源与插件路径
export GAZEBO_RESOURCE_PATH="$PREFIX/usr/share/gazebo-11:${GAZEBO_RESOURCE_PATH:-}"
export GAZEBO_MODEL_PATH="$PREFIX/usr/share/gazebo-11/models:${GAZEBO_MODEL_PATH:-}"
export GAZEBO_PLUGIN_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:$PREFIX/opt/ros/humble/lib:${GAZEBO_PLUGIN_PATH:-}"
export GAZEBO_SYSTEM_PLUGIN_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:${GAZEBO_SYSTEM_PLUGIN_PATH:-}"
export OGRE_RESOURCE_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/OGRE-1.9.0:${OGRE_RESOURCE_PATH:-}"
export SDF_PATH="$PREFIX/usr/share/sdformat9:${SDF_PATH:-}"
# 沙箱内 HOME 不可写（Gazebo 需要 ~/.gazebo 可写）：把 HOME 指到工作区
export GAZEBO_HOME="$WS/gazebo_home"
mkdir -p "$GAZEBO_HOME"
export HOME="$GAZEBO_HOME"
export ROS_HOME="$WS/ros_home"
export ROS_LOG_DIR="$WS/ros_logs"
export MPLCONFIGDIR="$WS/.mplconfig"
mkdir -p "$ROS_HOME" "$ROS_LOG_DIR" "$MPLCONFIGDIR"
