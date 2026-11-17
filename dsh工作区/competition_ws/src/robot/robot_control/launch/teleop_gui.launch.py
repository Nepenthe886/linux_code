#!/usr/bin/env python3
"""可视化遥控 launch：robot_state_publisher + 模拟底盘 + Tkinter 操作台 + RViz2。

用法（安装后）::

    ros2 launch robot_control teleop_gui.launch.py
    ros2 launch robot_control teleop_gui.launch.py rviz:=false          # 不开 RViz
    ros2 launch robot_control teleop_gui.launch.py focus_mode:=false    # 不默认进入专注模式
    ros2 launch robot_control teleop_gui.launch.py gui:=false rviz:=false  # 无显示环境

用法（源码目录直接启动，不 colcon install 本包也可解析 URDF/RViz 路径）::

    ros2 launch ./launch/teleop_gui.launch.py

启动参数
--------
``rviz``（默认 true）
    是否启动 RViz2（加载 ``rviz/teleop.rviz``）。
``gui``（默认 true）
    是否启动 Tkinter 可视化操作台（无 DISPLAY 时请设 false）。
``focus_mode``（默认 true）
    GUI 启动后是否默认进入「专注模式」（X11 全局键盘抓取，无需先点窗口；
    按 K 退出/重新进入）。设为 false 则需先聚焦窗口再按 K 开启。
``use_sim_time``（默认 false）
    是否使用 ``/clock`` 仿真时间（playback / Gazebo 时设 true）。

URDF 来源
---------
优先取 ``robot_description`` 包的 ``urdf/omni_robot.urdf``；源码目录启动且
ament 索引里找不到该包时，回退到本包同级的 ``../robot_description``
（即部署后的 ``src/robot/robot_description``）；也可用环境变量
``ROBOT_DESCRIPTION_ROOT`` 直接指定包目录。URDF 里的 ``package://`` 网格
路径会被重写成 ``file://`` 百分号编码 URL，保证源码目录下 RViz 也能加载
mesh。
"""

import os
from urllib.parse import quote

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

#: robot_description 包内的 URDF 相对路径（与 INTERFACE.md 一致）。
_URDF_RELATIVE_PATH = os.path.join("urdf", "omni_robot.urdf")

#: RViz 配置在 robot_control 包内的相对路径。
_RVIZ_RELATIVE_PATH = os.path.join("rviz", "teleop.rviz")


def _package_root(package_name: str, marker_relative_path: str) -> str:
    """返回包的根目录：源码目录优先，其次 colcon 安装后的 share 目录。"""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists(os.path.join(here, marker_relative_path)):
        return here
    return get_package_share_directory(package_name)


def _robot_control_root() -> str:
    """robot_control 包根目录（用于定位 rviz/teleop.rviz）。"""
    return _package_root("robot_control", _RVIZ_RELATIVE_PATH)


def _robot_description_root() -> str:
    """定位 robot_description 包根目录，找不到时给出清晰报错。"""
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
        "    2) 从 Zhirong Cup 工作区直接启动；或\n"
        "    3) export ROBOT_DESCRIPTION_ROOT=/path/to/robot_description".format(
            _URDF_RELATIVE_PATH,
            "、".join(candidates) if candidates else "（无）",
        )
    )


def _load_robot_description(package_root: str) -> str:
    """读取 URDF，并把 package://robot_description/ 重写为 file:// URL。"""
    urdf_path = os.path.join(package_root, _URDF_RELATIVE_PATH)
    with open(urdf_path, "r", encoding="utf-8") as handle:
        robot_description = handle.read()
    # 源码目录启动时 ament 索引里可能没有 robot_description，RViz 无法解析
    # package:// 网格路径；重写为本机 file:// URL 后两种启动方式都能显示。
    mesh_prefix = "file://" + quote(package_root, safe="/") + "/"
    return robot_description.replace("package://robot_description/", mesh_prefix)


def generate_launch_description() -> LaunchDescription:
    """组装 teleop_gui.launch.py 的 LaunchDescription。"""
    robot_control_root = _robot_control_root()
    robot_description = _load_robot_description(_robot_description_root())
    rviz_config_path = os.path.join(robot_control_root, _RVIZ_RELATIVE_PATH)

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_parameter = ParameterValue(use_sim_time, value_type=bool)
    start_gui = LaunchConfiguration("gui")
    start_rviz = LaunchConfiguration("rviz")
    focus_mode = LaunchConfiguration("focus_mode")
    focus_mode_default_parameter = ParameterValue(focus_mode, value_type=bool)

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "rviz",
                default_value="true",
                description="是否启动 RViz2（加载 rviz/teleop.rviz）",
            ),
            DeclareLaunchArgument(
                "gui",
                default_value="true",
                description="是否启动 Tkinter 可视化操作台（无 DISPLAY 时设 false）",
            ),
            DeclareLaunchArgument(
                "focus_mode",
                default_value="true",
                description=(
                    "GUI 启动后是否默认进入专注模式（X11 全局键盘抓取；"
                    "K 退出/重新进入；false 则需先聚焦窗口再按 K 开启）"
                ),
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="是否使用 /clock 仿真时间",
            ),
            # 机器人的 URDF -> TF 树（base_footprint -> base_link -> 轮子 ...）
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "robot_description": robot_description,
                        "use_sim_time": use_sim_time_parameter,
                    }
                ],
            ),
            # 模拟底盘：/wheel_cmd -> /joint_states + /odom + TF(odom->base_footprint)
            Node(
                package="robot_control",
                executable="sim_node",
                name="mecanum_sim",
                output="screen",
                parameters=[{"use_sim_time": use_sim_time_parameter}],
            ),
            # Tkinter 可视化操作台：/cmd_vel + /wheel_cmd 发布，/odom 状态显示
            Node(
                package="robot_control",
                executable="gui_teleop",
                output="screen",
                parameters=[
                    {
                        "use_sim_time": use_sim_time_parameter,
                        "focus_mode_default": focus_mode_default_parameter,
                    }
                ],
                condition=IfCondition(start_gui),
            ),
            # RViz2：Fixed Frame=odom，RobotModel + TF + Grid + Odometry
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", rviz_config_path],
                parameters=[{"use_sim_time": use_sim_time_parameter}],
                condition=IfCondition(start_rviz),
            ),
        ]
    )
