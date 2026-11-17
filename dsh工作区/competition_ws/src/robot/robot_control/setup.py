"""Installation script for the ``robot_control`` ament_python package."""

import os
from glob import glob

from setuptools import setup

package_name = "robot_control"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml", "README.md"]),
        (
            os.path.join("share", package_name, "docs"),
            glob("docs/*.png"),
        ),
        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.launch.py"),
        ),
        (
            os.path.join("share", package_name, "rviz"),
            glob("rviz/*.rviz"),
        ),
        # Gazebo 自带测试世界（zhirong_maps 比赛地图缺失时 gazebo.launch.py 回退用）
        (
            os.path.join("share", package_name, "worlds"),
            glob("worlds/*.world"),
        ),
        (
            os.path.join("share", package_name, "worlds", "test"),
            glob("worlds/test/*.world"),
        ),
        # Gazebo 网格模型目录：让 URDF 中的 model://robot_description/meshes/*
        # 能通过 GAZEBO_MODEL_PATH 解析（见 models/robot_description/model.config）
        (
            os.path.join("share", package_name, "models", "robot_description"),
            glob("models/robot_description/*.config") + glob("models/robot_description/*.sdf"),
        ),
        (
            os.path.join("share", package_name, "models", "robot_description", "meshes"),
            glob("models/robot_description/meshes/*"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Zhirong Cup Team",
    maintainer_email="nepenthe@example.com",
    description=(
        "Mecanum-wheel teleoperation (WASD / arrow keys) and Tk GUI test "
        "panel for the Zhirong Cup robot"
    ),
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            # terminal (TTY) keyboard teleoperation
            "teleop_keyboard = robot_control.teleop_keyboard:main",
            # visual keyboard operation panel (Tkinter)
            "gui_teleop = robot_control.gui_teleop:main",
            # simulated mecanum drivetrain: wheel commands -> odom + TF + joint states
            "sim_node = robot_control.sim_node:main",
        ],
    },
)
