"""``gazebo.launch.py`` / URDF Gazebo 标签的**离线**单元测试。

不启动 Gazebo、不依赖 ROS 运行时（``launch`` 相关 import 放在 launch 文件的
函数内部，模块顶层只有标准库），因此可以在任何 Python 3.10 环境跑：

.. code-block:: bash

    cd competition_ws/src/robot/robot_control
    python3 -m pytest test/test_gazebo_launch.py -q

覆盖内容：

* URDF 里两个 ModelPlugin（planar_move / joint_state_publisher）及关键参数；
* 四轮 joint 名与 :data:`robot_control.mecanum.WHEEL_NAMES` 一致；
* 根 link ``base_footprint`` **不带** inertial（KDL 根 link 惯性警告）；
* 轮子摩擦/材质等 Gazebo 标签存在；
* launch 参数规格（默认值 / teleop 取值 / 与机器人 spawn 约定一致）；
* ``_resolve_world``：自动解析地图包、回退测试世界、显式覆盖、错误路径报错；
* ``_load_robot_description`` 把 ``package://`` 重写成 ``file://``；
* 自带测试世界 ``worlds/test/gazebo_test.world`` 是合法 SDF。
"""

from __future__ import annotations

import importlib.util
import os
import sys
import xml.etree.ElementTree as ET

import pytest

# 允许直接 `python3 -m pytest test -q`（cwd 为包根目录）以及从工作区根目录运行。
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from robot_control import mecanum  # noqa: E402

LAUNCH_PATH = os.path.join(PACKAGE_ROOT, "launch", "gazebo.launch.py")

#: robot_description 包在源码树里的位置（competition_ws/src/robot/robot_description）。
ROBOT_DESCRIPTION_ROOT = os.path.normpath(
    os.path.join(PACKAGE_ROOT, "..", "robot_description")
)
URDF_PATH = os.path.join(ROBOT_DESCRIPTION_ROOT, "urdf", "omni_robot.urdf")

PLANAR_PLUGIN = "libgazebo_ros_planar_move.so"
JOINT_STATE_PLUGIN = "libgazebo_ros_joint_state_publisher.so"

#: gazebo.launch.py 里必须通过 gzserver 命令行 -s 加载的 SystemPlugin。
SYSTEM_PLUGINS = ("libgazebo_ros_init.so", "libgazebo_ros_factory.so")


# --------------------------------------------------------------------------- #
# 辅助
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def launch_module():
    """以「普通 Python 模块」导入 launch 文件（顶层只 import 标准库，无需 ROS）。"""
    spec = importlib.util.spec_from_file_location("gazebo_launch_under_test", LAUNCH_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def urdf_root():
    """解析 URDF，返回根元素。"""
    return ET.parse(URDF_PATH).getroot()


@pytest.fixture(scope="module")
def gazebo_plugins(urdf_root):
    """返回 {插件名: 插件元素}。"""
    plugins = {}
    for plugin in urdf_root.findall("gazebo/plugin"):
        plugins[plugin.get("name")] = plugin
    return plugins


# --------------------------------------------------------------------------- #
# URDF：插件
# --------------------------------------------------------------------------- #
def test_urdf_exists_and_parses(urdf_root):
    """URDF 仍是合法 XML，robot 名称与 link 数量不变（不破坏 RViz 结构）。"""
    assert urdf_root.tag == "robot"
    assert urdf_root.get("name") == "zhirong_omni_robot"
    link_names = {link.get("name") for link in urdf_root.findall("link")}
    assert {
        "base_footprint",
        "base_link",
        "wheel_front_left_link",
        "wheel_front_right_link",
        "wheel_rear_left_link",
        "wheel_rear_right_link",
        "livox_mid360_link",
        "camera_link",
        "camera_optical_frame",
    } <= link_names


def test_urdf_has_both_gazebo_plugins(gazebo_plugins):
    """URDF 里有且仅有 planar_move + joint_state_publisher 两个 ModelPlugin。"""
    assert PLANAR_PLUGIN in [p.get("filename") for p in gazebo_plugins.values()]
    assert JOINT_STATE_PLUGIN in [p.get("filename") for p in gazebo_plugins.values()]
    # SystemPlugin 不能写进 URDF，必须 gzserver -s 加载。
    for filename in gazebo_plugins.values():
        assert "libgazebo_ros_init" not in filename.get("filename", "")
        assert "libgazebo_ros_factory" not in filename.get("filename", "")


def test_planar_move_parameters(gazebo_plugins):
    """planar_move 的话题/坐标系/频率参数（按 gazebo_ros 3.9 插件源码核实）。"""
    plugin = next(p for p in gazebo_plugins.values() if p.get("filename") == PLANAR_PLUGIN)

    def text(tag):
        element = plugin.find(tag)
        assert element is not None, "planar_move 缺少 <{}>".format(tag)
        return (element.text or "").strip()

    assert text("publish_odom").lower() == "true"
    assert text("publish_odom_tf").lower() == "true"
    assert text("odometry_frame") == "odom"
    assert text("robot_base_frame") == "base_footprint"
    assert float(text("update_rate")) > 0
    assert float(text("publish_rate")) > 0
    # 协方差参数存在（demo world 里的写法）
    assert plugin.find("covariance_x") is not None
    assert plugin.find("covariance_y") is not None
    assert plugin.find("covariance_yaw") is not None
    # 不自定义 namespace/remapping：保持 /cmd_vel、/odom 默认话题
    remapping = plugin.findall("ros/remapping")
    assert remapping == []


def test_joint_state_publisher_joints_match_mecanum(gazebo_plugins):
    """joint_state_publisher 发布的 4 个关节与 mecanum.WHEEL_NAMES 完全一致。"""
    plugin = next(
        p for p in gazebo_plugins.values() if p.get("filename") == JOINT_STATE_PLUGIN
    )
    joints = [element.text.strip() for element in plugin.findall("joint_name")]
    assert tuple(joints) == mecanum.WHEEL_NAMES
    assert float((plugin.find("update_rate").text or "").strip()) > 0


def test_base_footprint_has_no_inertial(urdf_root):
    """根 link 不能有 inertial：KDL 会警告，Gazebo 侧靠 fixed-joint lumping 处理。"""
    base_footprint = urdf_root.find("link[@name='base_footprint']")
    assert base_footprint is not None
    assert base_footprint.find("inertial") is None


def test_wheel_gazebo_tags_low_friction(urdf_root):
    """四轮有 Gazebo 材质 + 低摩擦系数（避免与 planar_move 速度约束打架）。"""
    for link in (
        "wheel_front_left_link",
        "wheel_front_right_link",
        "wheel_rear_left_link",
        "wheel_rear_right_link",
    ):
        element = urdf_root.find("gazebo[@reference='{}']".format(link))
        assert element is not None, "缺少 <gazebo reference={}>".format(link)
        assert element.find("material") is not None
        assert float(element.find("mu1").text) <= 0.2
        assert float(element.find("mu2").text) <= 0.2
        assert (element.find("self_collide").text or "").strip().lower() == "false"


def test_chassis_and_sensor_materials_present(urdf_root):
    """底盘/雷达/相机也有 Gazebo 材质（Gazebo 不读 URDF 顶层 material 名）。"""
    for link in ("base_link", "livox_mid360_link", "camera_link"):
        element = urdf_root.find("gazebo[@reference='{}']".format(link))
        assert element is not None, "缺少 <gazebo reference={}>".format(link)
        assert element.find("material") is not None


# --------------------------------------------------------------------------- #
# launch：参数规格与纯函数
# --------------------------------------------------------------------------- #
def test_launch_argument_specs(launch_module):
    """所有 launch 参数都声明了且有合理默认值。"""
    specs = {spec.name: spec for spec in launch_module.ARG_SPECS}
    assert set(specs) >= {
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
    }
    assert specs["world"].default_value == ""
    assert float(specs["x"].default_value) == pytest.approx(2.9)
    assert float(specs["y"].default_value) == pytest.approx(1.6)
    assert 0.0 <= float(specs["z"].default_value) <= 0.1  # 轮子自然落地
    assert float(specs["yaw"].default_value) == pytest.approx(3.14159265, abs=1e-6)
    assert specs["use_sim_time"].default_value == "true"
    assert specs["gui"].default_value == "false"
    assert specs["rviz"].default_value == "false"
    assert specs["teleop"].default_value == "none"
    assert tuple(specs["teleop"].choices) == ("none", "keyboard", "gui")
    # 每个参数都要有中文说明，便于 --show-args
    for spec in specs.values():
        assert spec.description


def test_launch_declares_args_and_opaque_function(tmp_path, monkeypatch):
    """ROS launch 可用时，真实生成 LaunchDescription 校验参数声明。"""
    pytest.importorskip("launch")
    from launch.actions import DeclareLaunchArgument, OpaqueFunction

    # launch 模块会给 DeclareLaunchArgument 建日志文件；CI/沙箱里 HOME 可能只读，
    # 显式指到 pytest 的临时目录（与生产环境无关）。
    monkeypatch.setenv("ROS_LOG_DIR", str(tmp_path / "ros_logs"))

    spec = importlib.util.spec_from_file_location("gazebo_launch_declared", LAUNCH_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    description = module.generate_launch_description()

    declared = {
        entity.name
        for entity in description.entities
        if isinstance(entity, DeclareLaunchArgument)
    }
    assert declared == {arg.name for arg in module.ARG_SPECS}
    assert any(isinstance(entity, OpaqueFunction) for entity in description.entities)


def test_launch_uses_system_plugins_on_command_line(urdf_root, launch_module):
    """SystemPlugin 必须由 gzserver 命令行 -s 加载，不能写成 URDF 插件。"""
    assert tuple(launch_module._GAZEBO_SYSTEM_PLUGINS) == SYSTEM_PLUGINS
    source = open(LAUNCH_PATH, encoding="utf-8").read()
    # 命令行里以 -s 方式加载（gzserver -s <system plugin>）
    assert '"-s"' in source
    # URDF 里只能有 ModelPlugin（两个），不能把 init/factory 当成模型插件
    plugin_filenames = {p.get("filename") for p in urdf_root.findall("gazebo/plugin")}
    assert plugin_filenames == {PLANAR_PLUGIN, JOINT_STATE_PLUGIN}
    for plugin in SYSTEM_PLUGINS:
        assert plugin not in plugin_filenames


def test_resolve_world_explicit(tmp_path):
    """world:=<path> 显式覆盖优先。"""
    explicit = tmp_path / "custom.world"
    explicit.write_text("<sdf version='1.6'><world name='x'/></sdf>", encoding="utf-8")
    spec = importlib.util.spec_from_file_location("gazebo_launch_world_explicit", LAUNCH_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    resolved = module._resolve_world(str(explicit), PACKAGE_ROOT)
    assert resolved["source"] == "user"
    assert resolved["path"] == str(explicit)


def test_resolve_world_explicit_missing_raises(tmp_path):
    """world:= 指向不存在的文件时报错要包含路径与提示。"""
    spec = importlib.util.spec_from_file_location("gazebo_launch_world_missing", LAUNCH_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    missing = str(tmp_path / "nope.world")
    with pytest.raises(RuntimeError) as excinfo:
        module._resolve_world(missing, PACKAGE_ROOT)
    assert missing in str(excinfo.value)
    assert "world" in str(excinfo.value)


def test_resolve_world_auto_prefers_maps_package(tmp_path, monkeypatch):
    """ZHIRONG_MAPS_ROOT 指向地图包根目录时自动选中 zhirong_arena.world。"""
    spec = importlib.util.spec_from_file_location("gazebo_launch_world_maps", LAUNCH_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    maps_root = tmp_path / "zhirong_maps"
    world = maps_root / "worlds" / "zhirong_arena.world"
    world.parent.mkdir(parents=True)
    world.write_text("<sdf version='1.6'><world name='arena'/></sdf>", encoding="utf-8")
    monkeypatch.setenv("ZHIRONG_MAPS_ROOT", str(maps_root))

    resolved = module._resolve_world("", PACKAGE_ROOT)
    assert resolved["source"] == "zhirong_maps"
    assert resolved["path"] == str(world)


def test_resolve_world_falls_back_to_bundled_test_world(monkeypatch, launch_module):
    """找不到地图包时回退到包内 worlds/test/gazebo_test.world。"""
    monkeypatch.delenv("ZHIRONG_MAPS_ROOT", raising=False)
    # 屏蔽真实 zhirong_maps（scene-builder 可能已经在源码树里建好），
    # 只验证「地图包不存在 -> 回退自带测试世界」这条分支。
    monkeypatch.setattr(launch_module, "_maps_world_candidates", lambda root: [])
    resolved = launch_module._resolve_world("", PACKAGE_ROOT)
    assert resolved["source"] == "fallback"
    assert resolved["path"] == os.path.join(
        PACKAGE_ROOT, "worlds", "test", "gazebo_test.world"
    )
    assert os.path.isfile(resolved["path"])


def test_maps_models_dir_from_env(tmp_path, monkeypatch, launch_module):
    """地图包的 models 目录会被自动加到 GAZEBO_MODEL_PATH。"""
    maps_root = tmp_path / "zhirong_maps"
    models = maps_root / "models"
    models.mkdir(parents=True)
    monkeypatch.setenv("ZHIRONG_MAPS_ROOT", str(maps_root))
    assert launch_module._maps_models_dir(PACKAGE_ROOT) == str(models)


def test_load_robot_description_keeps_package_urls(launch_module):
    """URDF 原文保留 package://（由 spawn_entity -package_to_model 转 model://）。

    不重写成 file:// 绝对路径：含中文/空格的工作区路径在 urdf->sdf 转换中
    会被破坏，Gazebo 报 ``[Err] No mesh specified``（2026-11 实测）。
    """
    description = launch_module._load_robot_description(ROBOT_DESCRIPTION_ROOT)
    assert "package://robot_description/meshes/" in description
    assert "file://" not in description
    root = ET.fromstring(description)
    assert root.get("name") == "zhirong_omni_robot"


def test_robot_models_dir_has_mid360_meshes(launch_module):
    """robot_control/models/robot_description 提供 model:// 网格解析目录。"""
    models = launch_module._robot_models_dir(PACKAGE_ROOT)
    assert models == os.path.join(PACKAGE_ROOT, "models")
    mesh_dir = os.path.join(models, "robot_description", "meshes")
    for name in ("mid360_base.stl", "mid360_top.stl", "mid360_dome.stl"):
        assert os.path.isfile(os.path.join(mesh_dir, name)), name
    assert os.path.isfile(os.path.join(models, "robot_description", "model.config"))


def test_lidar_sensors_snippet_is_valid(launch_module):
    """Mid-360 Gazebo 传感器片段：合法 XML、挂在 livox_mid360_link、含 ray+imu 插件。"""
    path = launch_module._lidar_sensors_path()
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    root = ET.fromstring("<wrap>" + text + "</wrap>")
    gazebo = root.find("gazebo")
    assert gazebo is not None
    assert gazebo.get("reference") == "livox_mid360_link"
    sensors = {sensor.get("name"): sensor.get("type") for sensor in gazebo.findall("sensor")}
    assert sensors == {
        "livox_mid360_imu": "imu",
        "livox_mid360_ray": "ray",
    }, sensors
    plugins = [p.get("filename") for p in gazebo.iter("plugin")]
    assert "libgazebo_ros_imu_sensor.so" in plugins
    assert "libgazebo_ros_ray_sensor.so" in plugins
    # 点云输出类型必须是 PointCloud2（供 /livox/lidar 消费）
    assert "sensor_msgs/PointCloud2" in text


def test_load_robot_description_can_append_lidar_sensors(launch_module):
    """lidar_sensors:=true 时 URDF 末尾追加 Gazebo 传感器块，且仍是合法 XML。"""
    plain = launch_module._load_robot_description(ROBOT_DESCRIPTION_ROOT)
    with_sensors = launch_module._load_robot_description(ROBOT_DESCRIPTION_ROOT, sensors=True)
    assert "livox_mid360_ray" not in plain
    assert "livox_mid360_ray" in with_sensors
    assert "livox_mid360_imu" in with_sensors
    assert "package://robot_description/meshes/" in with_sensors
    assert "file://" not in with_sensors
    # 追加后仍是一个合法的 URDF（robot 根、link 数量不变）
    root_plain = ET.fromstring(plain)
    root_sensors = ET.fromstring(with_sensors)
    assert root_sensors.tag == "robot"
    assert len(root_plain.findall("link")) == len(root_sensors.findall("link"))


def test_model_path_env_includes_robot_and_maps_models(launch_module, monkeypatch, tmp_path):
    """gzclient 与 gzserver 都必须拿到 robot + maps 的 GAZEBO_MODEL_PATH。

    回归：此前只给 gzserver 注入 GAZEBO_MODEL_PATH，gzclient 解析不到
    ``model://robot_description/meshes/*`` 会去请求在线模型库，GUI 卡在
    ``Waiting for model database update to complete...``（Gazebo 未响应）。
    """
    maps_root = tmp_path / "zhirong_maps"
    (maps_root / "models").mkdir(parents=True)
    monkeypatch.setenv("ZHIRONG_MAPS_ROOT", str(maps_root))
    monkeypatch.delenv("GAZEBO_MODEL_PATH", raising=False)

    env = launch_module._model_path_env(PACKAGE_ROOT)
    assert "GAZEBO_MODEL_PATH" in env
    paths = env["GAZEBO_MODEL_PATH"].split(os.pathsep)
    assert os.path.join(PACKAGE_ROOT, "models") in paths          # 机器人网格模型
    assert str(maps_root / "models") in paths                     # 比赛地图模型


def test_model_path_env_includes_all_maps_candidates(launch_module, monkeypatch, tmp_path):
    """地图包多个候选目录（已安装 share + 源码树）都要进 GAZEBO_MODEL_PATH。

    回归：地图包 colcon build 的瞬间 install/models 可能不可用，若只给一个
    候选目录，gzserver/gzclient 会回退在线模型库而卡住；多候选可兜底。
    """
    installed = tmp_path / "install_zhirong_maps"
    source = tmp_path / "src_zhirong_maps"
    for root in (installed, source):
        (root / "models").mkdir(parents=True)
    monkeypatch.setattr(
        launch_module, "_maps_root_candidates", lambda _root: [str(installed), str(source)]
    )
    monkeypatch.delenv("GAZEBO_MODEL_PATH", raising=False)
    env = launch_module._model_path_env(PACKAGE_ROOT)
    paths = env["GAZEBO_MODEL_PATH"].split(os.pathsep)
    assert str(installed / "models") in paths
    assert str(source / "models") in paths


def test_gzclient_action_gets_model_path_env(launch_module):
    """回归：gazebo.launch.py 里 gzclient 的 ExecuteProcess 必须带模型路径环境。"""
    source = open(
        os.path.join(PACKAGE_ROOT, "launch", "gazebo.launch.py"), encoding="utf-8"
    ).read()
    gzclient_block = source[source.index('cmd=["gzclient"]'):]
    assert "_model_path_env(robot_control_root)" in gzclient_block[:400], (
        "gzclient 启动必须注入 GAZEBO_MODEL_PATH（见 _model_path_env）"
    )


def test_bundled_test_world_is_valid_sdf(launch_module):
    """回退世界是合法 SDF，含太阳光与地面。"""
    world_path = os.path.join(PACKAGE_ROOT, "worlds", "test", "gazebo_test.world")
    assert os.path.isfile(world_path)
    root = ET.parse(world_path).getroot()
    assert root.tag == "sdf"
    includes = [include.find("uri").text for include in root.findall("world/include")]
    assert "model://sun" in includes
    assert "model://ground_plane" in includes
    assert root.find("world/physics") is not None
