#!/usr/bin/env python3
"""戎智杯反恐搜救赛项 —— 一键启动（bringup）。

一条命令拉起完整仿真链路：

    ros2 launch bring_up bring_up.launch.py

包含：
1. Gazebo Classic 11（gzserver）加载比赛场景 ``zhirong_maps/worlds/zhirong_arena.world``；
2. 机器人 ``robot_description``（URDF + Gazebo 插件）spawn 到入口外侧出生点；
3. ``robot_state_publisher`` 发布 URDF→TF 树；
4. Gazebo 插件发布 ``/clock``、``/joint_states``、``/odom``、TF ``odom->base_footprint``；
5. 可选：``teleop:=keyboard|gui`` 遥控、``rviz:=true``、``gui:=true``（gzclient）。

本 launch 是对 ``robot_control`` 包内 ``gazebo.launch.py`` 的**统一入口封装**：
默认参数/话题/插件行为与它保持一致，参数名一一透传，便于比赛现场只用一条命令。

常用示例
--------
::

    # 1) 无显示器（服务器 / SSH）：默认即为 headless
    ros2 launch bring_up bring_up.launch.py

    # 2) 有显示器：Gazebo 客户端 + RViz + 图形遥控面板
    ros2 launch bring_up demo.launch.py

    # 3) 指定世界文件或出生点
    ros2 launch bring_up bring_up.launch.py world:=/abs/path/zhirong_arena.world x:=0 y:=0 yaw:=0

    # 4) 终端键盘遥控（建议另开一个终端）
    ros2 launch bring_up bring_up.launch.py teleop:=keyboard

启动前提：已 ``colcon build`` 并 ``source install/setup.bash``；Gazebo 用系统安装
（``sudo bash scripts/install_environment.sh``）。若上一次仿真没退干净导致
master 端口被占，先执行 ``bash scripts/kill_sim.sh`` 或直接用
``bash scripts/run_sim.sh``（会自动清理）。
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


#: 与 robot_control/gazebo.launch.py 完全一致的一键启动参数（名字/默认值/说明）
ARG_SPECS = [
    ("world", "", "世界文件绝对路径；留空自动解析 zhirong_maps 的 worlds/zhirong_arena.world"),
    ("x", "2.9", "机器人 spawn x 坐标 [m]（默认比赛入口外侧）"),
    ("y", "1.6", "机器人 spawn y 坐标 [m]"),
    ("z", "0.05", "机器人 spawn 高度 [m]（base_footprint；0.05~0.1 让轮子自然落地）"),
    ("yaw", "3.141592653589793", "机器人 spawn 偏航角 [rad]（π = 面向场内）"),
    ("use_sim_time", "true", "使用 /clock 仿真时间（Gazebo 模式必须 true）"),
    ("gui", "false", "是否启动 gzclient（需要可用显示器/OpenGL；本机 GLX 损坏时保持 false）"),
    ("rviz", "false", "是否启动 RViz2（Fixed Frame=odom）"),
    ("teleop", "none", "遥控方式：none / keyboard / gui"),
    ("verbose", "false", "gzserver 是否 --verbose"),
    ("model_name", "zhirong_robot", "Gazebo 中机器人模型名"),
    ("pause", "false", "gzserver 是否以暂停状态启动"),
]

#: 需要透传给 robot_control/gazebo.launch.py 的参数
_FORWARD_ARGS = (
    "world",
    "x",
    "y",
    "z",
    "yaw",
    "use_sim_time",
    "gui",
    "rviz",
    "teleop",
    "verbose",
    "model_name",
    "pause",
)


def _robot_control_launch() -> str:
    """定位 robot_control 包内 gazebo.launch.py（安装后 share 目录）。"""
    share = get_package_share_directory("robot_control")
    path = os.path.join(share, "launch", "gazebo.launch.py")
    if not os.path.isfile(path):
        raise RuntimeError(
            "bring_up: 找不到 robot_control 的 gazebo.launch.py：{}\n"
            "  请先在工作空间根目录 colcon build 并 source install/setup.bash".format(path)
        )
    return path


def _launch_setup(context):
    """组装：提示横幅 + 透传 include robot_control/gazebo.launch.py。"""
    cfg = context.launch_configurations
    actions = [
        LogInfo(
            msg=(
                "[bring_up] 一键启动：Gazebo 比赛场景 + 机器人 + TF + 插件"
                "（gui={gui}, rviz={rviz}, teleop={teleop}）"
            ).format(
                gui=cfg.get("gui", "false"),
                rviz=cfg.get("rviz", "false"),
                teleop=cfg.get("teleop", "none"),
            )
        )
    ]
    actions.append(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(_robot_control_launch()),
            launch_arguments={name: LaunchConfiguration(name) for name in _FORWARD_ARGS}.items(),
        )
    )
    return actions


def generate_launch_description() -> LaunchDescription:
    declared = [
        DeclareLaunchArgument(
            name,
            default_value=default,
            description=desc,
        )
        for name, default, desc in ARG_SPECS
    ]
    return LaunchDescription(declared + [OpaqueFunction(function=_launch_setup)])
