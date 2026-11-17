#!/usr/bin/env bash
# 用户态安装 Gazebo Classic 11 + ros-humble-gazebo-ros-pkgs（环境无 sudo，仅解包到前缀）
set -uo pipefail
WS="/home/nepenthe/zmf/linux_code/dsh工作区"
PREFIX="$WS/gazebo_userland"
DEBDIR="$PREFIX/debs"
LOG="$PREFIX/install.log"
mkdir -p "$PREFIX" "$DEBDIR"
: > "$LOG"

log(){ echo "$*" | tee -a "$LOG"; }

log "=== [1/4] 解析依赖包列表 ==="
PKGS=$(apt-get -s install --no-install-recommends \
        ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins ros-humble-gazebo-ros \
        gazebo gazebo-common 2>>"$LOG" \
      | grep -E '^Inst ' | awk '{print $2}' | sed 's/:amd64$//' | sort -u)
if [ -z "$PKGS" ]; then log "错误：无法解析依赖列表"; exit 1; fi
log "待安装包数量: $(echo "$PKGS" | wc -l)"

log "=== [2/4] 下载 deb 包 ==="
cd "$DEBDIR" || exit 1
FAILED=""
for p in $PKGS; do
  if ls "${p}_"*.deb >/dev/null 2>&1; then continue; fi
  ok=0
  for try in 1 2 3; do
    if apt-get download "$p" >>"$LOG" 2>&1; then ok=1; break; fi
    sleep 2
  done
  if [ "$ok" -eq 0 ]; then FAILED="$FAILED $p"; log "下载失败: $p"; fi
done
log "下载完成。失败: ${FAILED:-无}"

log "=== [3/4] 解包到前缀 $PREFIX ==="
cnt=0
for f in "$DEBDIR"/*.deb; do
  dpkg-deb -x "$f" "$PREFIX" || log "解包失败: $f"
  cnt=$((cnt+1))
done
log "解包 deb 数量: $cnt"

log "=== [4/4] 生成环境脚本 ==="
cat > "$WS/tools/gazebo_env.sh" <<'ENV'
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
export LD_LIBRARY_PATH="$PREFIX/usr/lib/x86_64-linux-gnu:$PREFIX/usr/lib:$PREFIX/opt/ros/humble/lib:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$PREFIX/opt/ros/humble/lib/python3.10/site-packages:${PYTHONPATH:-}"
export PKG_CONFIG_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/pkgconfig:$PREFIX/usr/share/pkgconfig:${PKG_CONFIG_PATH:-}"
export CMAKE_PREFIX_PATH="$PREFIX/opt/ros/humble:$PREFIX/usr:${CMAKE_PREFIX_PATH:-}"
export AMENT_PREFIX_PATH="$PREFIX/opt/ros/humble:${AMENT_PREFIX_PATH:-/opt/ros/humble}"
export COLCON_PREFIX_PATH="$PREFIX/opt/ros/humble:${COLCON_PREFIX_PATH:-}"
# Gazebo 资源与插件路径
export GAZEBO_RESOURCE_PATH="$PREFIX/usr/share/gazebo-11:${GAZEBO_RESOURCE_PATH:-}"
export GAZEBO_MODEL_PATH="$PREFIX/usr/share/gazebo-11/models:${GAZEBO_MODEL_PATH:-}"
export GAZEBO_PLUGIN_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:$PREFIX/opt/ros/humble/lib:${GAZEBO_PLUGIN_PATH:-}"
export GAZEBO_SYSTEM_PLUGIN_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:${GAZEBO_SYSTEM_PLUGIN_PATH:-}"
export OGRE_RESOURCE_PATH="$PREFIX/usr/lib/x86_64-linux-gnu/OGRE-1.9.0:${OGRE_RESOURCE_PATH:-}"
export SDF_PATH="$PREFIX/usr/share/sdformat9:${SDF_PATH:-}"
# 沙箱内 HOME 不可写：ROS/Matplotlib/Gazebo 工作目录放到工作区
export ROS_HOME="$WS/ros_home"
export ROS_LOG_DIR="$WS/ros_logs"
export MPLCONFIGDIR="$WS/.mplconfig"
mkdir -p "$ROS_HOME" "$ROS_LOG_DIR" "$MPLCONFIGDIR"
ENV
chmod +x "$WS/tools/gazebo_env.sh"
log "=== 安装脚本结束 ==="
