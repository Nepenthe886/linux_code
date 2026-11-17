#!/usr/bin/env python3
"""Backward-compatible alias for view_robot.launch.py."""

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    here = os.path.dirname(os.path.abspath(__file__))
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
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(here, "view_robot.launch.py")
                ),
                launch_arguments={
                    "use_sim_time": LaunchConfiguration("use_sim_time"),
                    "rviz": LaunchConfiguration("rviz"),
                }.items(),
            ),
        ]
    )
