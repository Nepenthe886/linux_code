#!/usr/bin/env python3
"""Gazebo Classic 11 仿真 launch：gzserver + 机器人 spawn + TF + 可选遥控/RViz。

与 ``teleop_gui.launch.py`` / ``teleop_keyboard.launch.py`` 的区别
------------------------------------------------------------------
那两个 launch 用的是本包自带的 :mod:`robot_control.sim_node`（纯 Python 运动学
仿真：``/wheel_cmd`` 积分出 ``/joint_states``、``/odom`` 与 TF）；
本 launch 改用 **Gazebo 物理引擎 + URDF 里的 Gazebo 插件**：

* ``libgazebo_ros_planar_move.so``：速度级平面运动，订阅 ``/cmd_vel``，
  发布 ``/odom`` 与 TF ``odom -> base_footprint``；
* ``libgazebo_ros_joint_state_publisher.so``：发布四轮 ``/joint_states``；
* ``/clock``（由 gzserver 的 ``libgazebo_ros_init.so`` 提供），
  所有节点 ``use_sim_time:=true``。

因此 **Gazebo 模式下不要启动 sim_node**（否则两套 ``/odom`` 与 TF 会打架）。

典型用法
--------
::

    # 0) 环境（Gazebo 为用户态安装，必须先 source；headless 时 unset DISPLAY）
    source tools/gazebo_env.sh
    unset DISPLAY

    # 1) 默认：加载 zhirong_maps 比赛地图（找不到时回退自带测试世界并 warning）
    ros2 launch robot_control gazebo.launch.py

    # 2) 指定 world 文件 / 出生点
    ros2 launch robot_control gazebo.launch.py \\
        world:=/path/to/zhirong_arena.world x:=2.9 y:=1.6 z:=0.05 yaw:=3.14159

    # 3) 无显示环境（CI / 服务器）：不开 gzclient、不开 RViz
    ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false

    # 4) 源码目录直接启动（不 colcon install 本包）
    ros2 launch ./launch/gazebo.launch.py

    # 5) 伴随终端键盘遥控（Gazebo 下按键发的是 /cmd_vel）
    ros2 launch robot_control gazebo.launch.py teleop:=keyboard

启动参数（全部 ``DeclareLaunchArgument``，见 :data:`ARG_SPECS`）
--------------------------------------------------------------
``world``
    世界文件绝对路径；留空表示自动解析：优先 ``zhirong_maps`` 包的
    ``worlds/zhirong_arena.world``（已安装 share 或源码目录
    ``src/maps/zhirong_maps/worlds/...``），都找不到时回退到本包自带的
    ``worlds/test/gazebo_test.world`` 并打印 warning。
``x`` / ``y`` / ``z`` / ``yaw``
    spawn 位姿（m / rad）。默认取地图 README 约定的入口外侧出生点
    ``(2.9, 1.6, yaw=π)``。``z`` 是 **模型根 link base_footprint 的高度**（地面投影），
    给 0.05~0.1 让轮子自然落地；``z=0`` 时轮子（半径 0.065）刚好触地。
``use_sim_time``
    是否使用 ``/clock`` 仿真时间，默认 ``true``（Gazebo 模式必须为 true）。
``gui``
    是否启动 ``gzclient``，默认 ``false``（本机 X :1 的 GLX 损坏，headless 优先）。
``rviz``
    是否启动 RViz2（加载 ``rviz/teleop.rviz``），默认 ``false``。
``teleop``
    ``none`` / ``keyboard`` / ``gui``，默认 ``none``（避免无显示环境卡住）。
    注意：``keyboard`` 节点从标准输入读键，经 ``ros2 launch`` 启动时标准输入
    不一定是交互终端，**实际遥控建议另开终端** ``ros2 run robot_control
    teleop_keyboard``。
``verbose``
    ``gzserver --verbose``，默认 ``false``。
``model_name``
    Gazebo 里的模型名，默认 ``zhirong_robot``。
``pause``
    gzserver 是否以暂停状态启动，默认 ``false``（暂停时机器人不会运动）。

gazebo_ros 插件参数对照（已按 gazebo_ros 3.9 源码 / 官方 demo world 核实）
-------------------------------------------------------------------------
planar_move：``update_rate``、``publish_rate``、``publish_odom``、
``publish_odom_tf``、``odometry_frame``、``robot_base_frame``、
``covariance_x`` / ``covariance_y`` / ``covariance_yaw``；话题为 ``cmd_vel``
与 ``odom``（可用 ``<remapping>`` 改名）。
joint_state_publisher：``update_rate`` + 多个 ``joint_name``；话题 ``joint_states``。
``libgazebo_ros_init.so`` / ``libgazebo_ros_factory.so`` 是 SystemPlugin，
只能通过 gzserver 命令行 ``-s`` 加载（本 launch 已处理）。

实现说明
--------
ROS ``launch`` 相关模块在 ``generate_launch_description()`` / ``_launch_setup()``
内部才 import，模块顶层只依赖标准库：这样 ``test/test_gazebo_launch.py`` 可以
在**没装 ROS 的环境**里 import 本文件并单测 ``_resolve_world``、
``_load_robot_description`` 等纯函数。
"""

from __future__ import annotations

import math
import os
import tempfile
import shutil
import socket
import subprocess
from typing import NamedTuple, Optional

# --------------------------------------------------------------------------- #
# 纯 Python 常量（可离线单测）
# --------------------------------------------------------------------------- #

#: robot_description 包内 URDF 的相对路径（与 INTERFACE.md 一致）。
_URDF_RELATIVE_PATH = os.path.join("urdf", "omni_robot.urdf")

#: RViz 配置在 robot_control 包内的相对路径。
_RVIZ_RELATIVE_PATH = os.path.join("rviz", "teleop.rviz")

#: robot_control 自带测试世界的相对路径（zhirong_maps 缺失时回退用）。
_TEST_WORLD_RELATIVE_PATH = os.path.join("worlds", "test", "gazebo_test.world")

#: 比赛地图包名与 world 相对路径（scene-builder / zhirong_maps 约定）。
_MAPS_PACKAGE = "zhirong_maps"
_MAPS_WORLD_RELATIVE_PATH = os.path.join("worlds", "zhirong_arena.world")

#: 出生点默认值：入口外侧（地图包 README 约定，yaw=π 面向场内）。
DEFAULT_SPAWN_X = 2.9
DEFAULT_SPAWN_Y = 1.6
DEFAULT_SPAWN_Z = 0.05
DEFAULT_SPAWN_YAW = math.pi

#: gzserver 必须通过命令行 -s 加载的系统插件（SystemPlugin）。
_GAZEBO_SYSTEM_PLUGINS = ("libgazebo_ros_init.so", "libgazebo_ros_factory.so")

#: 本机 Gazebo 为用户态安装（无 sudo），前缀可用环境变量覆盖。
_USERLAND_GAZEBO_PREFIX = os.environ.get(
    "GAZEBO_USERLAND_PREFIX",
    "/home/nepenthe/zmf/linux_code/dsh工作区/gazebo_userland",
)

#: Gazebo 缺失时给用户的统一安装提示（工作空间自带的系统安装脚本）。
_GAZEBO_ENV_HINT = (
    "统一安装（推荐）：在工作空间根目录执行 sudo bash scripts/install_environment.sh；"
    "无 sudo 的临时方案：source tools/gazebo_env.sh（用户态安装，仅本机）"
)


_OPENGL_CACHE = {}


def _opengl_available() -> bool:
    """用 ctypes 直接探测当前 DISPLAY 能否创建 GLX 上下文（结果缓存）。

    为什么不用 rviz2/gzclient 探测：它们依赖 GLX，坏驱动下会不断重试、不退出，
    无法用超时判断。这里直接调 libX11 + libGL 的
    ``XOpenDisplay`` + ``glXChooseVisual`` + ``glXCreateContext``，
    毫秒级返回，且与 gzclient/rviz2 真正失败的原因一致。

    判定：
      * 没有 DISPLAY / 打开失败 -> 不可用（GUI 无法显示）；
      * glXChooseVisual 或 glXCreateContext 返回空 -> 不可用（典型：GLX BadValue）；
      * 成功建上下文 -> 可用。
    可用 ``ZHIRONG_SKIP_GL_CHECK=1`` 跳过（返回可用）。
    """
    if "ok" in _OPENGL_CACHE:
        return _OPENGL_CACHE["ok"]
    if os.environ.get("ZHIRONG_SKIP_GL_CHECK", "0") == "1":
        _OPENGL_CACHE["ok"] = True
        return True
    if not os.environ.get("DISPLAY", "").strip():
        _OPENGL_CACHE["ok"] = False
        return False
    try:
        import ctypes

        x11 = ctypes.CDLL("libX11.so.6")
        gl = ctypes.CDLL("libGL.so.1")
        x11.XOpenDisplay.restype = ctypes.c_void_p
        x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
        x11.XDefaultScreen.restype = ctypes.c_int
        x11.XDefaultScreen.argtypes = [ctypes.c_void_p]
        x11.XCloseDisplay.argtypes = [ctypes.c_void_p]
        x11.XFree.argtypes = [ctypes.c_void_p]
        gl.glXChooseVisual.restype = ctypes.c_void_p
        gl.glXChooseVisual.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        gl.glXCreateContext.restype = ctypes.c_void_p
        gl.glXCreateContext.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
        gl.glXDestroyContext.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

        # 坏 GLX 下 glXCreateContext 会产生 X Error（默认处理器会直接终止进程），
        # 这里装一个只置标志位的错误处理器，避免探测把 launch 进程带崩。
        x_error = {"hit": False}
        error_handler_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)

        def _on_x_error(_dpy, _event):
            x_error["hit"] = True
            return 0

        handler = error_handler_t(_on_x_error)
        x11.XSetErrorHandler.argtypes = [error_handler_t]
        x11.XSetErrorHandler.restype = ctypes.c_void_p
        x11.XSetErrorHandler(handler)

        display = x11.XOpenDisplay(None)
        if not display:
            _OPENGL_CACHE["ok"] = False
            return False
        ok = False
        visual = None
        ctx = None
        try:
            # GLX_RGBA=4, GLX_DOUBLEBUFFER=5, GLX_RED_SIZE=8(->+1), etc., 以 None(0) 结尾
            attribs = (ctypes.c_int * 9)(4, 5, 8, 8, 9, 8, 10, 8, 0)
            visual = gl.glXChooseVisual(display, x11.XDefaultScreen(display), attribs)
            if visual:
                ctx = gl.glXCreateContext(display, visual, None, 1)
                ok = bool(ctx) and not x_error["hit"]
        finally:
            if ctx:
                gl.glXDestroyContext(display, ctx)
            if visual:
                x11.XFree(visual)
            x11.XCloseDisplay(display)
        _OPENGL_CACHE["ok"] = ok
        return ok
    except Exception:  # noqa: BLE001 - 探测失败时向后兼容：不阻断
        _OPENGL_CACHE["ok"] = True
        return True


def _require_opengl(what: str) -> None:
    """``what`` 为 gui / rviz 时，检查 OpenGL；不可用则给出明确中文报错。"""
    if _opengl_available():
        return
    raise RuntimeError(
        "gazebo.launch.py: 当前 DISPLAY 无法创建 OpenGL 上下文，{what} 会卡死（无响应）。\n"
        "  原因：显卡驱动/GLX 异常（如 NVIDIA 驱动未加载，nvidia-smi 报错）。\n"
        "  解决办法（任选其一）：\n"
        "    1) 无显示器方案（推荐，本机可用）：ros2 launch bring_up bring_up.launch.py\n"
        "       实时画面：bash scripts/view_sim.sh（用 Gazebo 相机 + rqt_image_view，不依赖本机 OpenGL）\n"
        "    2) 修复显卡驱动后重试（sudo ubuntu-drivers autoinstall 或重装 NVIDIA 驱动，重启 X）\n"
        "    3) 确认可用后跳过本检查：export ZHIRONG_SKIP_GL_CHECK=1".format(what=what)
    )


def _gazebo_master_endpoint():
    """解析 GAZEBO_MASTER_URI，返回 (host, port)。"""
    from urllib.parse import urlsplit

    uri = os.environ.get("GAZEBO_MASTER_URI", "http://localhost:11345")
    try:
        parts = urlsplit(uri)
        return (parts.hostname or "localhost", parts.port or 11345)
    except ValueError:
        return ("localhost", 11345)


def _model_path_env(robot_control_root: str) -> dict:
    """返回要注入 Gazebo 的模型搜索路径（``GAZEBO_MODEL_PATH``）。

    机器人 URDF 的 LiDAR 网格是 ``package://robot_description/meshes/*.stl``，
    spawn 时由 ``spawn_entity.py -package_to_model`` 转成
    ``model://robot_description/meshes/*.stl``。**gzserver 和 gzclient 都必须能
    解析它**：如果 gzclient 解析不到，GUI 会回退到在线模型库
    （models.gazebosim.org / Fuel），启动被 "Waiting for model database update
    to complete..." 阻塞，表现为 Gazebo 窗口出现但一直「未响应」
    （2026-11-17 实测定位）。比赛 world 里的 ``model://`` 模型同理。

    :returns: 形如 ``{"GAZEBO_MODEL_PATH": "<robot models>:<maps models>:<原值>"}``
    """
    current = [p for p in os.environ.get("GAZEBO_MODEL_PATH", "").split(os.pathsep) if p]
    # 机器人网格模型
    robot_models = _robot_models_dir(robot_control_root)
    # 地图模型：把 **所有存在的候选目录**（已安装 share + 源码树）都加入，
    # 避免“地图包正在 colcon build 的瞬间 install/models 不可用”导致
    # Gazebo 回退在线模型库而卡住（2026-11-17 联调实测过这个瞬时窗口）。
    maps_dirs = []
    try:
        for root in _maps_root_candidates(robot_control_root):
            models_dir = os.path.join(root, "models")
            if os.path.isdir(models_dir) and models_dir not in maps_dirs:
                maps_dirs.append(models_dir)
    except Exception:  # noqa: BLE001 - 候选解析失败时退回单目录逻辑
        single = _maps_models_dir(robot_control_root)
        if single:
            maps_dirs.append(single)
    for directory in [robot_models] + maps_dirs:
        if directory and directory not in current:
            current.insert(0, directory)
    return {"GAZEBO_MODEL_PATH": os.pathsep.join(current)} if current else {}


def _check_master_port_free():
    """启动前检查 Gazebo master 端口：被占用时说明已有 Gazebo 在跑。

    典型症状：本函数未检查时，新 gzserver 因 ``Address already in use``
    直接以退出码 255 死掉，launch 只显示 ``process has died``，很难排查。
    """
    host, port = _gazebo_master_endpoint()
    try:
        with socket.create_connection((host, port), timeout=0.5):
            pass
    except OSError:
        return  # 端口空闲，正常
    raise RuntimeError(
        "gazebo.launch.py: Gazebo master 端口 {host}:{port} 已被占用，"
        "通常是有上一次的 gzserver 没有退出（会导致新 gzserver 以 255 退出）。\n"
        "  解决办法（任选其一）：\n"
        "    1) 结束残留进程： pkill -x gzserver ; pkill -x gzclient\n"
        "    2) 使用工作空间封装脚本（会自动清理残留）： bash scripts/run_sim.sh\n"
        "    3) 换一个 master 端口： export GAZEBO_MASTER_URI=http://127.0.0.1:11346".format(
            host=host, port=port
        )
    )


def _ensure_gazebo_env():
    """确保 ``gazebo_ros`` / ``gzserver`` 在当前环境可用。

    * 系统 apt 安装或已 ``source tools/gazebo_env.sh``：直接返回 ``None``；
    * 检测到本机用户态 Gazebo 前缀（``GAZEBO_USERLAND_PREFIX``，默认
      ``dsh工作区/gazebo_userland``）：**自动注入** PATH/LD_LIBRARY_PATH/
      PYTHONPATH/AMENT_PREFIX_PATH/GAZEBO_* 到当前进程环境，使未 source
      环境脚本的普通终端也能直接 ``ros2 launch``；返回提示文本；
    * 都找不到：抛 ``RuntimeError``，给出明确的 source 命令提示
      （比 launch 的 ``package 'gazebo_ros' not found`` 更清晰）。
    """
    try:
        from ament_index_python.packages import get_package_prefix

        get_package_prefix("gazebo_ros")
        return None  # 系统安装 / 已 source
    except Exception:  # noqa: BLE001 - PackageNotFoundError 等
        pass

    prefix = _USERLAND_GAZEBO_PREFIX
    ros_prefix = os.path.join(prefix, "opt", "ros", "humble")
    if not os.path.isdir(os.path.join(ros_prefix, "share", "gazebo_ros")):
        raise RuntimeError(
            "gazebo.launch.py: 找不到 ROS 包 gazebo_ros（gazebo_ros_pkgs）。\n"
            "  本机 Gazebo 为用户态安装，请先 source 环境脚本后重试：\n"
            "    {hint}\n"
            "  （系统级安装后无需任何环境脚本，脚本见工作空间 scripts/install_environment.sh）".format(
                hint=_GAZEBO_ENV_HINT
            )
        )

    # ---- 注入用户态 Gazebo 环境 ----
    lib_dir = os.path.join(prefix, "usr", "lib", "x86_64-linux-gnu")
    gz_plugins = os.path.join(lib_dir, "gazebo-11", "plugins")
    usr_lib = os.path.join(prefix, "usr", "lib")
    usr_bin = os.path.join(prefix, "usr", "bin")
    ros_lib = os.path.join(ros_prefix, "lib")
    ros_bin = os.path.join(ros_prefix, "bin")

    def _inject(name, value):
        if not value:
            return
        current = [p for p in os.environ.get(name, "").split(os.pathsep) if p]
        if value not in current:
            os.environ[name] = os.pathsep.join([value] + current)

    for d in (usr_bin, ros_bin):
        _inject("PATH", d)
    for d in (lib_dir, gz_plugins, usr_lib, ros_lib):
        _inject("LD_LIBRARY_PATH", d)
    for d in (
        os.path.join(ros_prefix, "lib", "python3.10", "site-packages"),
        os.path.join(ros_prefix, "local", "lib", "python3.10", "dist-packages"),
    ):
        _inject("PYTHONPATH", d)
    _inject("AMENT_PREFIX_PATH", ros_prefix)
    _inject("CMAKE_PREFIX_PATH", ros_prefix)
    _inject("CMAKE_PREFIX_PATH", os.path.join(prefix, "usr"))
    _inject("PKG_CONFIG_PATH", os.path.join(lib_dir, "pkgconfig"))
    _inject("GAZEBO_RESOURCE_PATH", os.path.join(prefix, "usr", "share", "gazebo-11"))
    _inject("GAZEBO_MODEL_PATH", os.path.join(prefix, "usr", "share", "gazebo-11", "models"))
    _inject("GAZEBO_PLUGIN_PATH", gz_plugins)
    _inject("GAZEBO_PLUGIN_PATH", ros_lib)
    _inject("GAZEBO_SYSTEM_PLUGIN_PATH", gz_plugins)
    _inject("SDF_PATH", os.path.join(prefix, "usr", "share", "sdformat9"))
    return (
        "[gazebo.launch.py] 系统里没有 gazebo_ros，已自动注入本机用户态 Gazebo 前缀：{}\n"
        "  这是无 sudo 机器的临时方案；正式部署请执行 sudo bash scripts/install_environment.sh"
        "（系统安装后不再需要任何环境脚本）".format(prefix)
    )


#: URDF 里由 Gazebo 插件发布的话题 / TF（文档与单测共用）。
GAZEBO_TOPICS = {
    "/cmd_vel": "geometry_msgs/msg/Twist：planar_move 订阅（teleop/导航发出）",
    "/odom": "nav_msgs/msg/Odometry：planar_move 发布，frame_id=odom, child=base_footprint",
    "/joint_states": "sensor_msgs/msg/JointState：四轮关节状态（joint_state_publisher 插件）",
    "/clock": "rosgraph_msgs/msg/Clock：gzserver 仿真时钟（libgazebo_ros_init.so）",
    "TF odom->base_footprint": "planar_move 发布；base_footprint->base_link 等由 robot_state_publisher 发布",
}


class LaunchArgSpec(NamedTuple):
    """一个 launch 参数的声明规格（generate_launch_description 与单测共用）。"""

    name: str
    default_value: str
    description: str
    choices: Optional[tuple] = None


#: 全部 launch 参数（顺序即 ``ros2 launch ... --show-args`` 的顺序）。
ARG_SPECS = (
    LaunchArgSpec(
        "world",
        "",
        "世界文件绝对路径；留空自动解析 zhirong_maps 的 zhirong_arena.world，"
        "找不到时回退本包 worlds/test/gazebo_test.world",
    ),
    LaunchArgSpec(
        "x",
        str(DEFAULT_SPAWN_X),
        "spawn 的 x 坐标 [m]（默认地图入口外侧出生点）",
    ),
    LaunchArgSpec(
        "y",
        str(DEFAULT_SPAWN_Y),
        "spawn 的 y 坐标 [m]",
    ),
    LaunchArgSpec(
        "z",
        str(DEFAULT_SPAWN_Z),
        "spawn 的 z 坐标 [m]：模型根 link base_footprint 离地高度，"
        "给 0.05~0.1 让轮子自然落地",
    ),
    LaunchArgSpec(
        "yaw",
        str(DEFAULT_SPAWN_YAW),
        "spawn 的偏航角 yaw [rad]（默认 π，面向场内）",
    ),
    LaunchArgSpec(
        "use_sim_time",
        "true",
        "是否使用 /clock 仿真时间（Gazebo 模式必须 true）",
    ),
    LaunchArgSpec(
        "gui",
        "false",
        "是否启动 gzclient（无显示环境保持 false）",
    ),
    LaunchArgSpec(
        "rviz",
        "false",
        "是否启动 RViz2（加载 rviz/teleop.rviz）",
    ),
    LaunchArgSpec(
        "teleop",
        "none",
        "遥控节点：none / keyboard / gui（默认 none，避免无显示环境卡住）",
        choices=("none", "keyboard", "gui"),
    ),
    LaunchArgSpec(
        "verbose",
        "false",
        "是否给 gzserver 加 --verbose",
    ),
    LaunchArgSpec(
        "model_name",
        "zhirong_robot",
        "Gazebo 中的模型名（spawn 后可用 gz model -m <name> -i 查位姿）",
    ),
    LaunchArgSpec(
        "pause",
        "false",
        "gzserver 是否以暂停状态启动（暂停时机器人不运动）",
    ),
)


# --------------------------------------------------------------------------- #
# 路径定位（源码目录 与 colcon 安装后 都可用）
# --------------------------------------------------------------------------- #
def _package_root(package_name: str, marker_relative_path: str) -> str:
    """返回包的根目录：源码目录优先，其次 colcon 安装后的 share 目录。"""
    from ament_index_python.packages import get_package_share_directory

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists(os.path.join(here, marker_relative_path)):
        return here
    return get_package_share_directory(package_name)


def _robot_control_root() -> str:
    """robot_control 包根目录（定位 rviz 配置 / 自带测试世界）。"""
    return _package_root("robot_control", _RVIZ_RELATIVE_PATH)


def _robot_description_root() -> str:
    """定位 robot_description 包根目录，找不到时给出清晰报错。"""
    from ament_index_python.packages import get_package_share_directory

    candidates = []

    env_root = os.environ.get("ROBOT_DESCRIPTION_ROOT")
    if env_root:
        candidates.append(os.path.abspath(os.path.expanduser(env_root)))

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 部署形态：<ws>/src/robot/robot_control -> <ws>/src/robot/robot_description
    candidates.append(os.path.normpath(os.path.join(here, "..", "robot_description")))

    try:
        candidates.append(get_package_share_directory("robot_description"))
    except Exception:  # ament 索引里没有该包（未安装）时继续尝试其它候选
        pass

    for candidate in candidates:
        if os.path.isfile(os.path.join(candidate, _URDF_RELATIVE_PATH)):
            return candidate

    raise RuntimeError(
        "找不到 robot_description 包（需要其中的 {}）。\n"
        "  已尝试目录：{}\n"
        "  解决办法：\n"
        "    1) 先 colcon build robot_description 并 source install/setup.bash；或\n"
        "    2) 从 Zhirong Cup / competition_ws/src/robot 工作区直接启动；或\n"
        "    3) export ROBOT_DESCRIPTION_ROOT=/path/to/robot_description".format(
            _URDF_RELATIVE_PATH,
            "、".join(candidates) if candidates else "（无）",
        )
    )


def _load_robot_description(package_root: str) -> str:
    """读取 URDF 原文（保留 ``package://`` 网格 URI，不做绝对路径重写）。

    网格解析策略：URDF 里 ``package://robot_description/meshes/*.stl`` 由
    ``spawn_entity.py -package_to_model``（本 launch 已固定加上）转成
    ``model://robot_description/meshes/*.stl``，再由 Gazebo 通过
    ``GAZEBO_MODEL_PATH`` 解析到 ``<robot_control>/models/robot_description``。

    为什么不在 Python 里重写成 ``file://`` 绝对路径（早期做法，已废弃）：
    urdf->sdf 转换会把含中文/空格的绝对路径破坏掉，Gazebo 报 ``[Err] No mesh specified``；
    而 ``model://`` 是纯 ASCII URI，与工作区路径无关，最稳。
    RViz 需要的 ``package://`` 由 ament 索引解析（colcon 安装后可用）。
    """
    urdf_path = os.path.join(package_root, _URDF_RELATIVE_PATH)
    with open(urdf_path, "r", encoding="utf-8") as handle:
        return handle.read()


def _robot_description_for_rviz(urdf: str, robot_description_root: str):
    """把 ``package://robot_description/`` 改写成「无空格绝对路径」的 ``file://``。

    RViz2 的 resource_retriever 会把 ``package://`` 解析成未做百分号编码的
    ``file://`` 路径；当工作区路径含空格（本仓库 ``.../Zhirong Cup/...``）时
    网格读取失败，表现为 RViz 里机器人缺少 LiDAR 等网格部件（``Error
    retrieving file [file:///.../Zhirong Cup/...]``，2026-11-17 实测）。

    这里把网格目录软链到 ``/tmp/zhirong_robot_rviz_*``（纯 ASCII、无空格），
    再改写 URDF 里的 package URI，RViz 即可正常加载网格。Gazebo 仍然使用
    原始 URDF（``package://`` -> ``-package_to_model`` -> ``model://``），
    两条链路互不影响。

    :returns: ``(rviz 用 URDF 文本, assets 临时目录)``
    """
    assets_dir = tempfile.mkdtemp(prefix="zhirong_robot_rviz_")
    meshes_src = os.path.join(robot_description_root, "meshes")
    meshes_dst = os.path.join(assets_dir, "meshes")
    try:
        os.symlink(meshes_src, meshes_dst)
    except OSError:  # 软链不可用时退化为拷贝
        shutil.copytree(meshes_src, meshes_dst)
    # 目录本身由 tempfile 生成（/tmp 下，无空格），子路径只有 meshes/<文件名>
    prefix = "file://" + assets_dir + os.sep
    return urdf.replace("package://robot_description/", prefix), assets_dir


def _robot_models_dir(robot_control_root: str) -> str:
    """返回 robot_control 包内的 Gazebo 模型目录（``models``）。

    该目录下有 ``robot_description/meshes/*.stl``，配合 ``-package_to_model``
    让 URDF 的 ``package://robot_description/meshes/*`` 解析为
    ``model://robot_description/meshes/*``。安装后与源码目录两种布局都支持。
    """
    # _robot_control_root() 在源码树与 colcon 安装后都返回包根目录，
    # 因此 models/ 一律位于 <root>/models。
    candidate = os.path.join(robot_control_root, "models")
    if os.path.isdir(os.path.join(candidate, "robot_description", "meshes")):
        return candidate
    return ""


def _maps_root_candidates(robot_control_root: str) -> list:
    """返回 zhirong_maps 地图包根目录的候选（按优先级）。"""
    candidates = []

    env_maps_root = os.environ.get("ZHIRONG_MAPS_ROOT")
    if env_maps_root:
        candidates.append(os.path.abspath(os.path.expanduser(env_maps_root)))

    # colcon 安装后：ament 索引里的 zhirong_maps share 目录
    try:
        from ament_index_python.packages import get_package_share_directory

        candidates.append(get_package_share_directory(_MAPS_PACKAGE))
    except Exception:
        pass

    # 源码目录（robot_control 包根 -> <ws>/src/robot/robot_control）：
    #   <ws>/src/robot/robot_control/../../maps/zhirong_maps = <ws>/src/maps/zhirong_maps
    candidates.append(
        os.path.normpath(
            os.path.join(robot_control_root, "..", "..", "maps", _MAPS_PACKAGE)
        )
    )
    # colcon 安装后从 install share 反推源码树：
    #   <ws>/install/robot_control/share/robot_control/../../../../src/maps/...
    candidates.append(
        os.path.normpath(
            os.path.join(
                robot_control_root,
                "..",
                "..",
                "..",
                "..",
                "src",
                "maps",
                _MAPS_PACKAGE,
            )
        )
    )
    return candidates


def _maps_world_candidates(robot_control_root: str) -> list:
    """返回 zhirong_maps 比赛 world 的候选绝对路径（按优先级）。"""
    return [
        os.path.join(root, _MAPS_WORLD_RELATIVE_PATH)
        for root in _maps_root_candidates(robot_control_root)
    ]


def _maps_models_dir(robot_control_root: str) -> str:
    """返回 zhirong_maps 的 models 目录（world 里 model:// 资源需要它）。

    比赛 world 用 ``model://xxx`` 引用自己的模型；Gazebo 通过
    ``GAZEBO_MODEL_PATH`` 解析，启动时必须把这个目录加进去。
    """
    for root in _maps_root_candidates(robot_control_root):
        models_dir = os.path.join(root, "models")
        if os.path.isdir(models_dir):
            return models_dir
    return ""


def _resolve_world(explicit_world: str, robot_control_root: str) -> dict:
    """解析要加载的 world 文件。

    :param explicit_world: 用户 ``world:=`` 传入的路径；空字符串表示自动解析。
    :param robot_control_root: robot_control 包根目录。
    :returns: ``{"path": 绝对路径, "source": "user"|"zhirong_maps"|"fallback"}``
    :raises RuntimeError: 用户显式指定的路径不存在，或回退世界也找不到。
    """
    if explicit_world and explicit_world.strip():
        path = os.path.abspath(os.path.expanduser(explicit_world.strip()))
        if not os.path.isfile(path):
            raise RuntimeError(
                "gazebo.launch.py: world 参数指定的文件不存在：{}\n"
                "  请传绝对路径，例如 world:=/path/to/zhirong_arena.world".format(path)
            )
        return {"path": path, "source": "user"}

    maps_candidates = _maps_world_candidates(robot_control_root)
    for candidate in maps_candidates:
        if os.path.isfile(candidate):
            return {"path": candidate, "source": "zhirong_maps"}

    fallback = os.path.join(robot_control_root, _TEST_WORLD_RELATIVE_PATH)
    if os.path.isfile(fallback):
        return {
            "path": fallback,
            "source": "fallback",
            "maps_candidates": maps_candidates,
        }

    raise RuntimeError(
        "gazebo.launch.py: 找不到任何可用的 world 文件。\n"
        "  zhirong_maps 候选：{}\n"
        "  自带测试世界：{}\n"
        "  解决办法：等地图包构建完成后 colcon build + source install/setup.bash，"
        "或用 world:=<绝对路径> 指定。".format(
            "、".join(maps_candidates) if maps_candidates else "（无）",
            fallback,
        )
    )


def _gazebo_ros_lib_dir() -> str:
    """返回 gazebo_ros 插件所在 lib 目录（找不到时返回空串）。"""
    try:
        from ament_index_python.packages import get_package_share_directory

        prefix = os.path.dirname(
            os.path.dirname(get_package_share_directory("gazebo_ros"))
        )
        lib_dir = os.path.join(prefix, "lib")
        if os.path.isdir(lib_dir):
            return lib_dir
    except Exception:
        pass
    return ""


def _spawn_python_env() -> dict:
    """给 ``spawn_entity.py`` 补 PYTHONPATH。

    gazebo_ros / gazebo_msgs 的 Python 模块可能装在 ROS 前缀的
    ``local/lib/python3.10/dist-packages``（用户态安装常见），而环境脚本只加了
    ``lib/python3.10/site-packages``；这里把它补进去，避免
    ``ModuleNotFoundError: No module named 'gazebo_msgs'``。
    """
    extra_dirs = []
    try:
        from ament_index_python.packages import get_package_share_directory

        prefix = os.path.dirname(
            os.path.dirname(get_package_share_directory("gazebo_msgs"))
        )
    except Exception:
        return {}

    for relative in (
        os.path.join("local", "lib", "python3.10", "dist-packages"),
        os.path.join("lib", "python3.10", "site-packages"),
    ):
        candidate = os.path.join(prefix, relative)
        if os.path.isdir(candidate):
            extra_dirs.append(candidate)

    if not extra_dirs:
        return {}

    current = os.environ.get("PYTHONPATH", "")
    current_dirs = [directory for directory in current.split(os.pathsep) if directory]
    missing = [directory for directory in extra_dirs if directory not in current_dirs]
    if not missing:
        return {}
    return {"PYTHONPATH": os.pathsep.join(missing + current_dirs)}


def _launch_setup(context):
    """OpaqueFunction：按 launch 参数解析 world / 环境后组装实际动作。"""
    from launch.actions import ExecuteProcess, LogInfo, Shutdown
    from launch.conditions import IfCondition
    from launch.substitutions import LaunchConfiguration, PythonExpression
    from launch_ros.actions import Node
    from launch_ros.parameter_descriptions import ParameterValue

    gazebo_env_note = _ensure_gazebo_env()

    cfg = context.launch_configurations
    _check_master_port_free()
    robot_control_root = _robot_control_root()
    robot_description_root = _robot_description_root()
    # Gazebo 链路：保留 package://，由 spawn_entity -package_to_model 转 model://。
    robot_description = _load_robot_description(robot_description_root)
    # RViz 链路：改写成 /tmp 无空格路径的 file://，避免工作区路径含空格导致
    # RViz 读取 LiDAR 网格失败（robot_state_publisher -> RViz2 使用这份）。
    robot_description_rviz, rviz_assets_dir = _robot_description_for_rviz(
        robot_description, robot_description_root
    )
    rviz_config_path = os.path.join(robot_control_root, _RVIZ_RELATIVE_PATH)

    resolved_world = _resolve_world(cfg.get("world", ""), robot_control_root)
    world_path = resolved_world["path"]

    if shutil.which("gzserver") is None:
        raise RuntimeError(
            "gazebo.launch.py: PATH 里找不到 gzserver。\n"
            "  本机 Gazebo 为用户态安装，请先执行：\n"
            "    {hint}\n"
            "  （系统级安装后无需任何环境脚本，脚本见工作空间 scripts/install_environment.sh）".format(
                hint=_GAZEBO_ENV_HINT
            )
        )

    use_sim_time = ParameterValue(
        LaunchConfiguration("use_sim_time"), value_type=bool
    )

    # GUI / RViz 依赖 OpenGL：驱动异常时会「无响应」，这里提前给出清晰报错
    if str(cfg.get("gui", "false")).lower() in ("1", "true", "yes"):
        _require_opengl("gzclient（gui:=true）")
    if str(cfg.get("rviz", "false")).lower() in ("1", "true", "yes"):
        _require_opengl("RViz2（rviz:=true）")

    actions = []

    if gazebo_env_note:
        actions.append(LogInfo(msg=gazebo_env_note))

    # ---- world 来源提示（回退时给 warning，不刷屏） ----
    if resolved_world["source"] == "fallback":
        actions.append(
            LogInfo(
                msg=(
                    "[gazebo.launch.py][警告] 没找到 zhirong_maps 比赛地图"
                    "（{}），已回退到自带测试世界：{}。"
                    "地图包构建完成后重新 colcon build 即可自动使用。".format(
                        "、".join(resolved_world.get("maps_candidates") or ["（无候选）"]),
                        world_path,
                    )
                )
            )
        )
    else:
        actions.append(
            LogInfo(
                msg="[gazebo.launch.py] world = {}（来源：{}）".format(
                    world_path, resolved_world["source"]
                )
            )
        )

    # ---- gzserver ----
    # 用 bash -c 包一层：先校验 world 文件（用户 world:= 传错时给清晰报错），
    # 再 unset DISPLAY。本机 X :1 的 GLX 损坏，gzserver 保留 DISPLAY 会因
    # GLX CreateContext 失败直接崩溃；gzserver 本身不渲染，去掉 DISPLAY 只会在
    # 日志里留一条「Can't open display / rendering disabled」，物理与插件不受影响。
    gzserver_args = []
    if str(cfg.get("verbose", "false")).lower() in ("1", "true", "yes"):
        gzserver_args.append("--verbose")
    if str(cfg.get("pause", "false")).lower() in ("1", "true", "yes"):
        gzserver_args.append("--pause")

    gzserver_script = (
        'world="$1"; shift; '
        'if [ ! -f "$world" ]; then '
        '  echo "[gazebo.launch.py][错误] world 文件不存在: $world" >&2; exit 2; '
        "fi; "
        # ZHIRONG_KEEP_DISPLAY=1 时保留 DISPLAY：用于在 Xvfb(软件 OpenGL) 上
        # 渲染 Gazebo 相机，再经 ROS 图像在无 GL 的桌面上查看（scripts/view_sim.sh）
        'if [ "${ZHIRONG_KEEP_DISPLAY:-0}" = "1" ]; then :; else unset DISPLAY; fi; '
        'exec gzserver "$@" "$world"'
    )
    gzserver_cmd = (
        # bash -c 之后：$0="gazebo.launch.py"，$1=world，$2..=gzserver 选项/插件
        ["bash", "-c", gzserver_script, "gazebo.launch.py", world_path]
        + gzserver_args
        + ["-s", _GAZEBO_SYSTEM_PLUGINS[0], "-s", _GAZEBO_SYSTEM_PLUGINS[1]]
    )

    gzserver_env = {}

    def _prepend_env(name: str, directory: str) -> None:
        """把目录前插到环境变量（已包含则不重复）。"""
        if not directory:
            return
        current = os.environ.get(name, "")
        current_dirs = [item for item in current.split(os.pathsep) if item]
        if directory in current_dirs:
            return
        gzserver_env[name] = os.pathsep.join([directory] + current_dirs)

    # gazebo_ros 的插件库（本机用户态安装时不一定已在 GAZEBO_PLUGIN_PATH 里）
    _prepend_env("GAZEBO_PLUGIN_PATH", _gazebo_ros_lib_dir())
    # 机器人网格 + 比赛地图模型（world / URDF 里的 model:// 资源）
    gzserver_env.update(_model_path_env(robot_control_root))

    actions.append(
        LogInfo(msg="[gazebo.launch.py] gzserver 启动中（headless 模式，渲染关闭）……")
    )
    actions.append(
        ExecuteProcess(
            cmd=gzserver_cmd,
            output="screen",
            additional_env=gzserver_env or None,
            on_exit=Shutdown(),
        )
    )

    # ---- spawn 机器人（直接从原始 URDF 文件读取，保留 package://） ----
    # 不用机器人 /robot_description 话题：话题里的 URDF 已为 RViz 重写成
    # file:// 路径，Gazebo 的 -package_to_model 只认 package://。
    urdf_file = tempfile.NamedTemporaryFile(
        prefix="zhirong_robot_", suffix=".urdf", delete=False, mode="w", encoding="utf-8"
    )
    urdf_file.write(robot_description)
    urdf_file.close()
    spawn_arguments = [
        "-file",
        urdf_file.name,
        "-entity",
        str(cfg.get("model_name", "zhirong_robot")),
        "-x",
        str(cfg.get("x", DEFAULT_SPAWN_X)),
        "-y",
        str(cfg.get("y", DEFAULT_SPAWN_Y)),
        "-z",
        str(cfg.get("z", DEFAULT_SPAWN_Z)),
        "-Y",
        str(cfg.get("yaw", DEFAULT_SPAWN_YAW)),
        "-timeout",
        "120",
        # URDF 的 package://robot_description/meshes/* -> model://...
        # 由 Gazebo 通过 GAZEBO_MODEL_PATH(=robot_control/models) 解析
        "-package_to_model",
    ]
    actions.append(
        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            name="spawn_robot",
            output="screen",
            arguments=spawn_arguments,
            additional_env=_spawn_python_env() or None,
        )
    )

    # ---- 机器人 URDF -> TF 树 ----
    actions.append(
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[
                {
                    "robot_description": robot_description_rviz,
                    "use_sim_time": use_sim_time,
                }
            ],
        )
    )

    # ---- 可选遥控（默认 none：无显示 / 无人值守也能一把起） ----
    teleop_mode = LaunchConfiguration("teleop")
    teleop_keyboard_condition = IfCondition(
        PythonExpression(["'", teleop_mode, "' == 'keyboard'"])
    )
    teleop_gui_condition = IfCondition(
        PythonExpression(["'", teleop_mode, "' == 'gui'"])
    )
    actions.append(
        Node(
            package="robot_control",
            executable="teleop_keyboard",
            name="teleop_keyboard",
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
            condition=teleop_keyboard_condition,
        )
    )
    actions.append(
        Node(
            package="robot_control",
            executable="gui_teleop",
            name="gui_teleop",
            output="screen",
            parameters=[
                {"use_sim_time": use_sim_time, "focus_mode_default": False}
            ],
            condition=teleop_gui_condition,
        )
    )

    # ---- 可选 gzclient（需要可用显示）----
    # 关键：必须把 GAZEBO_MODEL_PATH 也注入给 gzclient（与 gzserver 相同）。
    # 否则客户端解析不到 model://robot_description/meshes/*，会去请求在线模型库，
    # GUI 卡在 "Waiting for model database update to complete..."（窗口未响应）。
    actions.append(
        ExecuteProcess(
            cmd=["gzclient"],
            name="gzclient",
            output="screen",
            additional_env=_model_path_env(robot_control_root) or None,
            condition=IfCondition(LaunchConfiguration("gui")),
        )
    )

    # ---- 可选 RViz2（Fixed Frame=odom） ----
    actions.append(
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config_path],
            parameters=[{"use_sim_time": use_sim_time}],
            condition=IfCondition(LaunchConfiguration("rviz")),
        )
    )

    return actions


# --------------------------------------------------------------------------- #
# 入口
# --------------------------------------------------------------------------- #
def generate_launch_description():
    """组装 gazebo.launch.py 的 LaunchDescription。"""
    from launch import LaunchDescription
    from launch.actions import DeclareLaunchArgument, OpaqueFunction

    declared_arguments = [
        DeclareLaunchArgument(
            spec.name,
            default_value=spec.default_value,
            description=spec.description,
            **({"choices": list(spec.choices)} if spec.choices else {}),
        )
        for spec in ARG_SPECS
    ]
    return LaunchDescription(declared_arguments + [OpaqueFunction(function=_launch_setup)])
