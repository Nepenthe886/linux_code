#!/usr/bin/env python3
"""一键启动（演示模式）：在有显示器的机器上直接看到 Gazebo 客户端 + RViz + 图形遥控。

等价于::

    ros2 launch bring_up bring_up.launch.py gui:=true rviz:=true teleop:=gui lidar:=true
（默认同时启动 Mid-360 激光雷达/IMU 模拟，``lidar:=false`` 可关）

用法::

    ros2 launch bring_up demo.launch.py                # 默认全开
    ros2 launch bring_up demo.launch.py gui:=false     # 只开 RViz + 遥控面板

注意：gzclient 需要可用的 OpenGL/显示器；无显示环境请用 ``bring_up.launch.py``。
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def _bring_up_launch() -> str:
    share = get_package_share_directory("bring_up")
    return os.path.join(share, "launch", "bring_up.launch.py")


def generate_launch_description() -> LaunchDescription:
    from launch.actions import DeclareLaunchArgument

    args = [
        DeclareLaunchArgument("gui", default_value="true", description="启动 gzclient（需要显示器）"),
        DeclareLaunchArgument("rviz", default_value="true", description="启动 RViz2"),
        DeclareLaunchArgument("teleop", default_value="gui", description="遥控方式 none/keyboard/gui"),
        DeclareLaunchArgument("world", default_value="", description="世界文件（留空自动解析比赛地图）"),
        DeclareLaunchArgument("x", default_value="2.9", description="spawn x [m]"),
        DeclareLaunchArgument("y", default_value="1.6", description="spawn y [m]"),
        DeclareLaunchArgument("z", default_value="0.05", description="spawn z [m]"),
        DeclareLaunchArgument("yaw", default_value="3.141592653589793", description="spawn yaw [rad]"),
        DeclareLaunchArgument("use_sim_time", default_value="true", description="使用仿真时间"),
        DeclareLaunchArgument("verbose", default_value="false", description="gzserver --verbose"),
        DeclareLaunchArgument("model_name", default_value="zhirong_robot", description="机器人模型名"),
        DeclareLaunchArgument("pause", default_value="false", description="gzserver 暂停启动"),
        DeclareLaunchArgument("lidar", default_value="true", description="启用激光雷达/IMU（false=off）"),
        DeclareLaunchArgument(
            "lidar_sim", default_value="gazebo",
            description="雷达数据源：gazebo=真实场景射线点云+200Hz IMU / python=合成点云 / off",
        ),
    ]
    include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(_bring_up_launch()),
        launch_arguments={
            "gui": LaunchConfiguration("gui"),
            "rviz": LaunchConfiguration("rviz"),
            "teleop": LaunchConfiguration("teleop"),
            "world": LaunchConfiguration("world"),
            "x": LaunchConfiguration("x"),
            "y": LaunchConfiguration("y"),
            "z": LaunchConfiguration("z"),
            "yaw": LaunchConfiguration("yaw"),
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "verbose": LaunchConfiguration("verbose"),
            "model_name": LaunchConfiguration("model_name"),
            "pause": LaunchConfiguration("pause"),
            "lidar": LaunchConfiguration("lidar"),
            "lidar_sim": LaunchConfiguration("lidar_sim"),
        }.items(),
    )
    return LaunchDescription(args + [include])
