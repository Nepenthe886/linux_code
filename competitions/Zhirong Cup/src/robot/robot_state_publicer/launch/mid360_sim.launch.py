#!/usr/bin/env python3
"""Start the simulated Livox Mid-360 LiDAR + IMU publisher."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _package_root() -> str:
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists(os.path.join(here, "config", "mid360_sim.yaml")):
        return here
    return get_package_share_directory("robot_state_publicer")


def generate_launch_description() -> LaunchDescription:
    root = _package_root()
    params = os.path.join(root, "config", "mid360_sim.yaml")
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time", default_value="false",
                description="使用 /clock 仿真时间（在 Gazebo 中建议 true）",
            ),
            DeclareLaunchArgument(
                "frame_id", default_value="livox_frame",
                description="点云/IMU 的 frame_id；与 URDF 统一时可设为 livox_mid360_link",
            ),
            DeclareLaunchArgument(
                "publish_tf", default_value="true",
                description="是否发布 base_link->frame_id 静态 TF；由 robot_state_publisher 提供时设 false",
            ),
            DeclareLaunchArgument(
                "stamp_from_sim_clock", default_value="true",
                description=(
                    "消息时间戳用 /clock 插值（仿真时间），定时器仍按真实时间运行；"
                    "Gazebo 中建议 true（/clock 仅约 10 Hz，use_sim_time=true 会把 IMU 限到 ~20 Hz）"
                ),
            ),
            Node(
                package="robot_state_publicer",
                executable="mid360_sim",
                name="mid360_sim",
                output="screen",
                parameters=[
                    params,
                    {
                        "use_sim_time": LaunchConfiguration("use_sim_time"),
                        "frame_id": LaunchConfiguration("frame_id"),
                        "publish_tf": LaunchConfiguration("publish_tf"),
                        "stamp_from_sim_clock": LaunchConfiguration("stamp_from_sim_clock"),
                    },
                ],
            ),
        ]
    )
