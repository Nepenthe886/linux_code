#!/usr/bin/env bash
# 创建工作空间 Python 虚拟环境并按 requirements.txt 安装依赖。
#
# 特点：
#   * venv 带 --system-site-packages，因此仍能 import 系统 ROS 2 的 rclpy/launch；
#   * 本机系统 Python 没装 pip 时，自动用 get-pip.py 在 venv 内引导，不污染系统；
#   * 不修改系统 Python（无需 sudo）。
#
# 用法:
#   bash scripts/setup_python_env.sh            # 默认 .venv
#   VENV_DIR=/path/to/venv bash scripts/setup_python_env.sh
# 使用:
#   source .venv/bin/activate        # 之后 python/pytest 均用该环境
set -eo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$HERE/.." && pwd)"
VENV="${VENV_DIR:-$WS/.venv}"
PY="${PYTHON:-python3}"

# pip/matplotlib 缓存放到工作区（避免 HOME 不可写时告警，也便于迁移时清理）
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-$WS/.pip-cache}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$WS/.cache}"
mkdir -p "$PIP_CACHE_DIR" "$XDG_CACHE_HOME"

echo "[1/4] 创建虚拟环境（--system-site-packages，可 import rclpy）: $VENV"
if [ ! -x "$VENV/bin/python" ]; then
  "$PY" -m venv --system-site-packages "$VENV" 2>/dev/null || \
  "$PY" -m venv --system-site-packages --without-pip "$VENV"
fi

echo "[2/4] 检查 pip"
if ! "$VENV/bin/python" -m pip --version >/dev/null 2>&1; then
  echo "       venv 内没有 pip，使用 get-pip.py 引导 ..."
  GETPIP="$VENV/get-pip.py"
  if [ ! -s "$GETPIP" ]; then
    curl -fsSL https://bootstrap.pypa.io/get-pip.py -o "$GETPIP" || \
    wget -qO "$GETPIP" https://bootstrap.pypa.io/get-pip.py
  fi
  "$VENV/bin/python" "$GETPIP"
fi
"$VENV/bin/python" -m pip --version

echo "[3/4] 安装 requirements.txt 依赖"
"$VENV/bin/python" -m pip install --upgrade pip wheel >/dev/null
"$VENV/bin/python" -m pip install -r "$WS/requirements.txt"

echo "[4/4] 校验关键依赖"
"$VENV/bin/python" - <<'PY'
import numpy, cv2, yaml, PIL, matplotlib, pytest
print("  numpy", numpy.__version__)
print("  opencv", cv2.__version__)
print("  PyYAML", yaml.__version__)
print("  Pillow", PIL.__version__)
print("  matplotlib", matplotlib.__version__)
print("  pytest", pytest.__version__)
PY
echo
echo "Python 依赖就绪。启用方式： source $VENV/bin/activate"
echo "（ROS 2 / Gazebo 系统依赖请跑： sudo bash $WS/scripts/install_environment.sh）"
