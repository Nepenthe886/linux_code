# -*- coding: utf-8 -*-
"""启动 zhirong_maps 的 Gazebo Classic 11 反恐搜救比赛场地。

用法（源码目录或 colcon 安装后均可）::

    # 无显示环境（headless，仅物理/话题，默认）
    ros2 launch zhirong_maps zhirong_arena.launch.py
    # 带 gzclient（需要可用的 OpenGL/X；本仓库验证环境可用 Xvfb + 软件渲染）
    ros2 launch zhirong_maps zhirong_arena.launch.py gui:=true
    # 覆盖 world / 指定 gazebo master（多实例隔离）
    ros2 launch zhirong_maps zhirong_arena.launch.py \
        world:=/abs/path/zhirong_arena.world gazebo_master_uri:=http://127.0.0.1:11391

说明：
  * world 路径默认取本包（源码或 install/share）下的 worlds/zhirong_arena.world；
  * 本包 models/ 目录会追加进 GAZEBO_MODEL_PATH / GAZEBO_RESOURCE_PATH，
    世界文件通过 model:// 引用模型，因此无需安装到 ~/.gazebo/models；
  * 本 world 只含纯 Gazebo 内容，不含 ROS 系统插件（system plugin 必须由
    ``gzserver -s libgazebo_ros_init.so`` 命令行加载，不能写进 world）；
  * spawn_x / spawn_y / spawn_z / spawn_yaw 是本场景约定的机器人出生点
    （入口外侧，朝向场地内），供上层机器人 launch 组合使用。
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (AppendEnvironmentVariable, DeclareLaunchArgument,
                            IncludeLaunchDescription, LogInfo, OpaqueFunction,
                            SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

# 包根目录：源码目录结构 <pkg>/{launch,worlds,models} 与安装后
# <install>/share/zhirong_maps/{launch,worlds,models} 相同，故用 __file__ 推导，
# 这样即使尚未 colcon build（源码目录直接 launch）也能正确找到资源。
_LAUNCH_DIR = os.path.dirname(os.path.abspath(__file__))
_PKG_ROOT = os.path.dirname(_LAUNCH_DIR)

# 出生点（入口外侧，东边界外 0.4 m，朝向场地内即 -x 方向）
SPAWN_DEFAULTS = dict(x="2.90", y="1.60", z="0.05", yaw="3.1416")


def _gazebo_share():
    try:
        return get_package_share_directory("gazebo_ros")
    except Exception:  # pragma: no cover - 环境未 source 时给出可读错误
        return ""


def _set_master_uri(context):
    """仅当显式给出 gazebo_master_uri 时才覆盖 GAZEBO_MASTER_URI。"""
    uri = LaunchConfiguration("gazebo_master_uri").perform(context)
    if uri:
        return [SetEnvironmentVariable("GAZEBO_MASTER_URI", uri)]
    return []


def generate_launch_description():
    pkg_root = LaunchConfiguration("pkg_root")
    world = LaunchConfiguration("world")
    gui = LaunchConfiguration("gui")
    verbose = LaunchConfiguration("verbose")

    gazebo_share = _gazebo_share()
    gzserver_launch = os.path.join(gazebo_share, "launch", "gzserver.launch.py")
    gzclient_launch = os.path.join(gazebo_share, "launch", "gzclient.launch.py")

    actions = [
        DeclareLaunchArgument(
            "gui", default_value="false",
            description="是否启动 gzclient 图形界面（默认 false，headless）"),
        DeclareLaunchArgument(
            "world", default_value=os.path.join(_PKG_ROOT, "worlds",
                                                "zhirong_arena.world"),
            description="world 文件路径，可覆盖"),
        DeclareLaunchArgument(
            "verbose", default_value="false",
            description="gzserver 详细日志"),
        DeclareLaunchArgument(
            "gazebo_master_uri", default_value="",
            description="覆盖 GAZEBO_MASTER_URI（多实例隔离时使用，如 "
                        "http://127.0.0.1:11391）；留空则沿用环境变量默认值"),
        DeclareLaunchArgument(
            "spawn_x", default_value=SPAWN_DEFAULTS["x"],
            description="机器人出生点 x（入口外侧，m）"),
        DeclareLaunchArgument(
            "spawn_y", default_value=SPAWN_DEFAULTS["y"],
            description="机器人出生点 y（入口外侧，m）"),
        DeclareLaunchArgument(
            "spawn_z", default_value=SPAWN_DEFAULTS["z"],
            description="机器人出生高度（m，spawn_entity 的 z）"),
        DeclareLaunchArgument(
            "spawn_yaw", default_value=SPAWN_DEFAULTS["yaw"],
            description="机器人出生朝向（rad，pi 表示朝 -x 即场地内）"),

        # 让 gzserver/gzclient 能通过 model:// 找到本包 models
        AppendEnvironmentVariable("GAZEBO_MODEL_PATH",
                                  os.path.join(_PKG_ROOT, "models")),
        AppendEnvironmentVariable("GAZEBO_RESOURCE_PATH",
                                  os.path.join(_PKG_ROOT, "models")),
        OpaqueFunction(function=_set_master_uri),

        LogInfo(msg=["[zhirong_maps] world = ", world]),
        LogInfo(msg=["[zhirong_maps] 机器人出生点 spawn(入口外侧): x=",
                     LaunchConfiguration("spawn_x"), " y=",
                     LaunchConfiguration("spawn_y"), " z=",
                     LaunchConfiguration("spawn_z"), " yaw=",
                     LaunchConfiguration("spawn_yaw")]),
        LogInfo(msg="[zhirong_maps] 场地 5 m x 5 m，16 单元格；入口=东侧偏北，出口=西侧中部"),
    ]

    if not gazebo_share:
        actions.append(LogInfo(
            msg="[zhirong_maps][ERROR] 未找到 gazebo_ros，请先 source ROS 2 与 Gazebo 环境"))
    else:
        actions += [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(gzserver_launch),
                launch_arguments={
                    "world": world,
                    "verbose": verbose,
                    "pause": "false",
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(gzclient_launch),
                condition=IfCondition(gui),
            ),
        ]

    return LaunchDescription(actions)
