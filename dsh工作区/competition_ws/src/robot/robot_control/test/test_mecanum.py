"""``robot_control.mecanum`` 的单元测试（纯 Python，不依赖 ROS 运行时）。

运行方式（无需 colcon 安装）：

.. code-block:: bash

    cd robot_control_ws/src/robot_control
    python3 -m pytest test -q
"""

from __future__ import annotations

import math
import os
import sys

import pytest

# 允许直接 `python3 -m pytest test -q`（cwd 为包根目录）以及从工作区根目录运行。
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from robot_control import mecanum  # noqa: E402

R = 0.065
BX = 0.170
BY = 0.170
ARM = BX + BY


def kinematics(**kwargs) -> mecanum.MecanumKinematics:
    """默认几何参数的 MecanumKinematics。"""
    params = dict(
        wheel_radius=R,
        wheel_base_x=BX,
        wheel_base_y=BY,
        max_wheel_speed=30.0,
    )
    params.update(kwargs)
    return mecanum.MecanumKinematics(**params)


# --------------------------------------------------------------------------- #
# 常量与 URDF 一致性
# --------------------------------------------------------------------------- #
def test_wheel_names_match_urdf():
    """轮序固定 FL FR RL RR，关节名与 URDF 一致。"""
    assert mecanum.WHEEL_NAMES == (
        "wheel_front_left_joint",
        "wheel_front_right_joint",
        "wheel_rear_left_joint",
        "wheel_rear_right_joint",
    )
    assert mecanum.WHEEL_LABELS == ("FL", "FR", "RL", "RR")
    # 别名保持同步（下游代码可能用 WHEEL_JOINTS 遍历）。
    assert mecanum.WHEEL_JOINTS == mecanum.WHEEL_NAMES


def test_default_geometry_matches_urdf():
    kin = kinematics()
    assert kin.wheel_radius == pytest.approx(0.065)
    assert kin.wheel_base_x == pytest.approx(0.170)
    assert kin.wheel_base_y == pytest.approx(0.170)
    assert kin.lever_arm == pytest.approx(0.340)


# --------------------------------------------------------------------------- #
# 正/逆运动学
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "body",
    [
        (0.0, 0.0, 0.0),
        (0.30, 0.0, 0.0),
        (0.0, 0.30, 0.0),
        (0.0, 0.0, 1.00),
        (0.20, -0.15, 0.50),
        (-0.25, 0.10, -0.80),
        (0.10, 0.25, 2.00),
    ],
)
def test_inverse_then_forward_round_trip(body):
    """body_to_wheels -> wheels_to_body 应还原原车体速度。"""
    kin = kinematics()
    wheels = kin.body_to_wheels(*body)
    recovered = kin.wheels_to_body(wheels)
    assert recovered.vx == pytest.approx(body[0], abs=1e-9)
    assert recovered.vy == pytest.approx(body[1], abs=1e-9)
    assert recovered.wz == pytest.approx(body[2], abs=1e-9)


def test_forward_then_inverse_round_trip():
    """可行轮速 -> body -> 轮速 应还原（wheel_signs 全 +1 时）。

    四个轮速来自一次逆运动学，保证落在秩 3 的可行子空间内；任意 4 个数字
    （如 (3,-1.5,0.75,-4.25)）不一定可行，正运动学后只能得到其投影。
    """
    kin = kinematics()
    wheels = kin.body_to_wheels(0.20, -0.10, 0.60)
    body = kin.wheels_to_body(wheels)
    assert kin.body_to_wheels(body.vx, body.vy, body.wz) == pytest.approx(wheels)


def test_forward_kinematics_matches_documented_formula():
    """前向运动学与 docstring/README 中的 r/4 公式逐项一致。"""
    kin = kinematics()
    w = (1.0, 2.0, 3.0, 4.0)
    body = kin.wheels_to_body(w)
    assert body.vx == pytest.approx(R / 4.0 * (w[0] + w[1] + w[2] + w[3]))
    assert body.vy == pytest.approx(R / 4.0 * (-w[0] + w[1] + w[2] - w[3]))
    assert body.wz == pytest.approx(
        R / (4.0 * ARM) * (-w[0] + w[1] - w[2] + w[3])
    )


# --------------------------------------------------------------------------- #
# 单一自由度的符号（与 README / URDF 约定一致）
# --------------------------------------------------------------------------- #
def test_pure_forward_all_wheels_positive():
    wheels = kinematics().body_to_wheels(0.30, 0.0, 0.0)
    expected = 0.30 / R
    assert wheels == pytest.approx((expected,) * 4)


def test_pure_lateral_left_alternating():
    """+vy（向左横移）: FL/RR 反转，FR/RL 正转。"""
    wheels = kinematics().body_to_wheels(0.0, 0.30, 0.0)
    expected = 0.30 / R
    assert wheels == pytest.approx((-expected, expected, expected, -expected))


def test_pure_rotation_ccw_alternating():
    """+wz（逆时针）: 左侧轮反转、右侧轮正转。"""
    wheels = kinematics().body_to_wheels(0.0, 0.0, 1.0)
    expected = ARM / R
    assert wheels == pytest.approx((-expected, expected, -expected, expected))


# --------------------------------------------------------------------------- #
# 键盘组合
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("key", ["w", "W", "Up", "KEY_UP"])
def test_forward_key_aliases(key):
    assert mecanum.key_action(key) == "forward"
    assert mecanum.keys_to_body([key]) == mecanum.BodyVelocity(0.30, 0.0, 0.0)


@pytest.mark.parametrize("key", ["s", "S", "Down", "KEY_DOWN"])
def test_backward_key_aliases(key):
    assert mecanum.key_action(key) == "backward"
    assert mecanum.keys_to_body([key]) == mecanum.BodyVelocity(-0.30, 0.0, 0.0)


@pytest.mark.parametrize("key", ["a", "A", "Left", "KEY_LEFT"])
def test_left_key_aliases(key):
    assert mecanum.key_action(key) == "left"
    assert mecanum.keys_to_body([key]) == mecanum.BodyVelocity(0.0, 0.30, 0.0)


@pytest.mark.parametrize("key", ["d", "D", "Right", "KEY_RIGHT"])
def test_right_key_aliases(key):
    assert mecanum.key_action(key) == "right"
    assert mecanum.keys_to_body([key]) == mecanum.BodyVelocity(0.0, -0.30, 0.0)


@pytest.mark.parametrize("key", ["q", "Q"])
def test_rotate_left_key(key):
    assert mecanum.key_action(key) == "rotate_left"
    assert mecanum.keys_to_body([key]) == mecanum.BodyVelocity(0.0, 0.0, 1.00)


@pytest.mark.parametrize("key", ["e", "E"])
def test_rotate_right_key(key):
    assert mecanum.key_action(key) == "rotate_right"
    assert mecanum.keys_to_body([key]) == mecanum.BodyVelocity(0.0, 0.0, -1.00)


@pytest.mark.parametrize("key", [" ", "space", "KEY_SPACE"])
def test_space_stop_overrides_other_keys(key):
    assert mecanum.key_action(key) == "stop"
    assert mecanum.keys_to_body([key]) == mecanum.BodyVelocity()
    assert mecanum.keys_to_body(["w", "a", key]) == mecanum.BodyVelocity()


def test_unknown_keys_are_ignored():
    assert mecanum.key_action("z") is None
    assert mecanum.key_action("") is None
    assert mecanum.keys_to_body(["z", "x", "F1"]) == mecanum.BodyVelocity()


def test_w_plus_a_diagonal_wheel_speeds():
    """w+a（前进+左平移 45°）: FL/RR 轮速抵消为 0，FR/RL 加倍。"""
    body = mecanum.keys_to_body(["w", "a"])
    assert body.vx > 0.0 and body.vy > 0.0
    assert body.vx == pytest.approx(body.vy)

    wheels = kinematics().body_to_wheels(body.vx, body.vy, body.wz)
    assert wheels[0] == pytest.approx(0.0, abs=1e-9)  # FL
    assert wheels[3] == pytest.approx(0.0, abs=1e-9)  # RR
    expected = 2.0 * body.vx / R
    assert wheels[1] == pytest.approx(expected)  # FR
    assert wheels[2] == pytest.approx(expected)  # RL


def test_w_plus_d_diagonal_wheel_speeds():
    """w+d（前进+右平移 45°）: FR/RL 轮速抵消为 0，FL/RR 加倍。"""
    body = mecanum.keys_to_body(["w", "d"])
    assert body.vx > 0.0 and body.vy < 0.0
    wheels = kinematics().body_to_wheels(body.vx, body.vy, body.wz)
    assert wheels[1] == pytest.approx(0.0, abs=1e-9)  # FR
    assert wheels[2] == pytest.approx(0.0, abs=1e-9)  # RL
    expected = 2.0 * body.vx / R
    assert wheels[0] == pytest.approx(expected)  # FL
    assert wheels[3] == pytest.approx(expected)  # RR


# --------------------------------------------------------------------------- #
# 速度上限
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "keys",
    [["w"], ["s"], ["a"], ["d"], ["q"], ["e"], ["w", "a"], ["w", "d"],
     ["s", "a"], ["s", "d"], ["w", "a", "q"], ["w", "d", "e"]],
)
def test_diagonal_body_speed_respects_cap(keys):
    body = mecanum.keys_to_body(keys)
    assert body.speed() <= max(0.30, 0.30) + 1e-12
    assert abs(body.wz) <= 1.00 + 1e-12


def test_custom_speeds_and_diagonal_scaling():
    body = mecanum.keys_to_body(
        ["w", "a"], max_linear=0.5, max_lateral=0.5, max_angular=2.0
    )
    assert body.speed() == pytest.approx(0.5)
    assert body.vx == pytest.approx(math.sqrt(0.5**2 / 2.0))
    assert body.vy == pytest.approx(body.vx)

    body = mecanum.keys_to_body(
        ["w", "q"], max_linear=0.3, max_lateral=0.3, max_angular=1.0
    )
    assert body.vx == pytest.approx(0.3)
    assert body.wz == pytest.approx(1.0)


def test_wheel_limit_preserves_ratio_and_peak():
    """超限时四轮按同一比例缩放，方向不变。"""
    kin = kinematics(max_wheel_speed=10.0)
    raw = kin.body_to_wheels(1.0, 0.2, 0.5)
    limited = kin.body_to_limited_wheels(1.0, 0.2, 0.5)
    peak = max(abs(value) for value in raw)
    assert peak > 10.0  # 越界了才谈限幅
    scale = 10.0 / peak
    for got, reference in zip(limited, raw):
        assert got == pytest.approx(reference * scale)
    assert max(abs(value) for value in limited) == pytest.approx(10.0)


def test_wheel_limit_keeps_direction_of_travel():
    """限幅后的车体速度与指令方向一致（纯 Python 侧核对）。"""
    kin = kinematics(max_wheel_speed=5.0)
    feasible, limited = kin.body_to_limited_velocity(1.0, 0.5, 2.0)
    assert max(abs(value) for value in limited) == pytest.approx(5.0)
    assert feasible.vx / 1.0 == pytest.approx(feasible.vy / 0.5)
    assert feasible.wz / 2.0 == pytest.approx(feasible.vx / 1.0)


def test_no_limit_when_within_range():
    kin = kinematics(max_wheel_speed=30.0)
    assert kin.body_to_wheels(0.3, 0.3, 1.0) == pytest.approx(
        kin.clamp_wheels(kin.body_to_wheels(0.3, 0.3, 1.0))
    )


# --------------------------------------------------------------------------- #
# 非法参数 / 非法输入
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "kwargs",
    [
        {"wheel_radius": 0.0},
        {"wheel_radius": -0.065},
        {"wheel_base_x": 0.0},
        {"wheel_base_x": -0.17},
        {"wheel_base_y": 0.0},
        {"wheel_base_y": -0.17},
        {"wheel_signs": (1.0, 1.0, 1.0)},
        {"wheel_signs": (1.0, 1.0, 1.0, 1.0, 1.0)},
    ],
)
def test_invalid_kinematics_parameters_raise(kwargs):
    with pytest.raises(ValueError):
        mecanum.MecanumKinematics(**kwargs)


def test_invalid_wheel_vectors_raise():
    kin = kinematics()
    with pytest.raises(ValueError):
        kin.wheels_to_body((1.0, 2.0, 3.0))
    with pytest.raises(ValueError):
        kin.clamp_wheels((1.0, 2.0, 3.0))
    with pytest.raises(ValueError):
        kin.clamp_wheels((1.0, 2.0, 3.0, 4.0, 5.0))


# --------------------------------------------------------------------------- #
# 辅助函数
# --------------------------------------------------------------------------- #
def test_format_wheels_and_wheel_rps():
    text = mecanum.format_wheels((1.0, -2.5, 0.0, 3.25))
    assert "FL=+1.00" in text
    assert "FR=-2.50" in text
    assert "RL=+0.00" in text
    assert "RR=+3.25" in text
    assert mecanum.wheel_rps(2.0 * math.pi) == pytest.approx(1.0)
