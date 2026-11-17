#!/usr/bin/env python3
"""View the robot: robot_state_publisher + joint state source + RViz.

Works both from the source tree (ros2 launch ./launch/view_robot.launch.py)
and from an installed colcon workspace (ros2 launch robot_description
view_robot.launch.py).
"""

import os
import sys
from urllib.parse import quote

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _package_root() -> str:
    """Return the package root for installed and source-tree launches."""
    # source tree: <root>/launch/view_robot.launch.py
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists(os.path.join(here, "urdf", "omni_robot.urdf")):
        return here
    return get_package_share_directory("robot_description")


def generate_launch_description() -> LaunchDescription:
    package_root = _package_root()
    urdf_path = os.path.join(package_root, "urdf", "omni_robot.urdf")
    rviz_path = os.path.join(package_root, "rviz", "omni_robot.rviz")

    with open(urdf_path, "r", encoding="utf-8") as f:
        robot_description = f.read()

    # RViz resolves package:// through the ament index.  When this file is
    # launched from the source tree (without colcon install) that index entry
    # may not exist, so rewrite package:// mesh URLs to percent-encoded file://
    # URLs pointing at the package root.  The URDF on disk stays portable.
    mesh_prefix = "file://" + quote(package_root, safe="/") + "/"
    robot_description = robot_description.replace(
        "package://robot_description/", mesh_prefix
    )

    # joint_state_publisher is the standard choice; fall back to a tiny local
    # node when it is not installed (e.g. minimal ROS 2 installations).
    try:
        get_package_share_directory("joint_state_publisher")
        joint_state_source = Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            name="joint_state_publisher",
            output="screen",
            parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}],
        )
    except Exception:
        joint_state_source = ExecuteProcess(
            cmd=[
                sys.executable,
                os.path.join(package_root, "scripts", "zero_joint_states.py"),
            ],
            name="zero_joint_state_publisher",
            output="screen",
        )

    use_sim_time = LaunchConfiguration("use_sim_time")
    start_rviz = LaunchConfiguration("rviz")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time", default_value="false",
                description="Use the /clock topic as the time source.",
            ),
            DeclareLaunchArgument(
                "rviz", default_value="true",
                description="Start RViz together with the publishers.",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[{
                    "robot_description": robot_description,
                    "use_sim_time": use_sim_time,
                }],
            ),
            joint_state_source,
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", rviz_path],
                condition=IfCondition(start_rviz),
            ),
        ]
    )
