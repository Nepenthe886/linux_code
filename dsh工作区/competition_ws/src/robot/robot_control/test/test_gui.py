#!/usr/bin/env python3
"""``TeleopPanel`` 的 pytest 测试（无 ROS 依赖，无显示时自动 skip）。

运行方式::

    cd src/robot_control
    DISPLAY=:1 python3 -m pytest test/test_gui.py -q

覆盖范围：

* 按键按下 -> sink 收到正确的 /cmd_vel 与四轮轮速（FL FR RL RR 顺序与符号）；
* 松开 -> 零速（含 X11 自动重复防抖）；
* 空格 / Esc 急停；
* 滑块改变线速度 / 横移速度 / 角速度后指令随之变化；
* 轮速限幅、斜向移动归一化、/odom 状态显示、关闭时发布零速。
"""

from __future__ import annotations

import math
import os
import sys
import time
from types import SimpleNamespace

import pytest

# 保证从源码目录直接运行 pytest 时也能 import robot_control。
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

try:
    import tkinter as tk
except ImportError:  # pragma: no cover - 极简环境
    pytest.skip("未安装 tkinter，跳过 GUI 测试", allow_module_level=True)

from robot_control.gui_teleop import FocusModeController, TeleopPanel  # noqa: E402


def _display_available() -> bool:
    """Linux 下要求 DISPLAY / WAYLAND_DISPLAY 至少有一个。"""
    if sys.platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    return True


if not _display_available():  # pragma: no cover - CI 无显示
    pytest.skip(
        "没有可用的图形显示（DISPLAY 未设置），跳过 Tkinter 界面测试",
        allow_module_level=True,
    )


def _create_root() -> tk.Tk:
    """创建一个隐藏的 Tk 根窗口；失败时 skip 而不是报错。"""
    try:
        root = tk.Tk()
    except tk.TclError as exc:  # pragma: no cover - 显示不可用
        pytest.skip(f"无法创建 Tk 窗口（{exc}），跳过 GUI 测试")
    root.withdraw()
    return root


class FakeSink:
    """记录 ``TeleopPanel`` 发布的假 sink。"""

    def __init__(self) -> None:
        self.calls: list[tuple[object, tuple[float, ...]]] = []

    def publish(self, body_velocity, wheel_speeds) -> None:  # noqa: ANN001
        self.calls.append((body_velocity, tuple(float(v) for v in wheel_speeds)))

    @property
    def last(self):
        assert self.calls, "sink 还没有收到任何发布调用"
        return self.calls[-1]


class FakeGrab:
    """假 X11 抓取对象：记录 start/stop，并保存后台按键回调。"""

    def __init__(self, start_result=(True, "已进入专注模式：键盘被本程序接管，按 K 退出")):
        self.start_result = start_result
        self.on_key = None
        self.start_calls = 0
        self.stop_calls = 0
        self.active = False

    def start(self):
        self.start_calls += 1
        ok, message = self.start_result
        self.active = bool(ok)
        return ok, message

    def stop(self):
        self.stop_calls += 1
        self.active = False


def _press(panel: TeleopPanel, keysym: str) -> None:
    """模拟一次 Tk KeyPress 事件（走面板真实的按键事件入口）。"""
    panel._on_key_press_event(SimpleNamespace(keysym=keysym))  # noqa: SLF001


def _release(panel: TeleopPanel, keysym: str) -> None:
    panel._on_key_release_event(SimpleNamespace(keysym=keysym))  # noqa: SLF001


@pytest.fixture()
def focus_panel(panel_factory):
    """返回 ``(panel, sink, controller, holder)``，holder["grab"] 在 enable 后出现。"""
    controllers: list[FocusModeController] = []

    def make(
        start_result=(True, "已进入专注模式：键盘被本程序接管，按 K 退出"),
        **panel_kwargs,
    ):
        panel, sink = panel_factory(**panel_kwargs)
        holder: dict = {}

        def grab_factory(on_key):
            grab = FakeGrab(start_result)
            grab.on_key = on_key
            holder["grab"] = grab
            return grab

        controller = FocusModeController(panel.root, grab_factory=grab_factory)
        controller.bind(panel)
        # 与 main() 一致：关闭窗口时由 controller 释放专注模式抓取。
        panel._on_close_callback = controller.close  # noqa: SLF001
        controllers.append(controller)
        return panel, sink, controller, holder

    yield make
    for controller in controllers:
        try:
            controller.close()
        except Exception:  # pragma: no cover
            pass


@pytest.fixture()
def panel_factory():
    """返回 ``(panel, sink)`` 的工厂，退出时统一关闭窗口。"""
    created: list[tuple[TeleopPanel, tk.Tk]] = []

    def factory(**kwargs):
        root = _create_root()
        sink = FakeSink()
        panel = TeleopPanel(root, sink, **kwargs)
        created.append((panel, root))
        return panel, sink

    yield factory
    for panel, root in created:
        try:
            panel.close()
        except Exception:  # pragma: no cover
            pass
        try:
            root.destroy()
        except Exception:  # pragma: no cover
            pass


def _flush(panel: TeleopPanel) -> None:
    """处理一次 Tk 事件循环，确认绘制/回调不抛异常。"""
    try:
        panel.root.update()
    except tk.TclError:  # pragma: no cover
        pass


def _pump(panel: TeleopPanel, seconds: float = 0.3) -> None:
    """驱动 Tk 事件循环一段时间（等待 root.after 定时任务执行）。"""
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        panel.root.update()
        time.sleep(0.01)


ZERO = dict(abs=1e-9)


def test_forward_w_publishes_cmd_and_wheels(panel_factory):
    """按 W：vx=线速度，四轮同向正转（FL FR RL RR）。"""
    panel, sink = panel_factory()
    panel.on_key_press("w")
    _flush(panel)

    body, wheels = sink.last
    assert body.vx == pytest.approx(panel.linear_speed, rel=1e-6)
    assert body.vy == pytest.approx(0.0, **ZERO)
    assert body.wz == pytest.approx(0.0, **ZERO)
    assert panel.last_body_velocity is body
    assert panel.last_wheel_speeds == wheels
    assert len(wheels) == 4

    expected = panel.linear_speed / panel.kinematics.wheel_radius
    for value in wheels:
        assert value == pytest.approx(expected, rel=1e-6)
    assert panel.pressed_keys == frozenset({"w"})
    assert panel.actions == frozenset({"forward"})


@pytest.mark.parametrize(
    "keysym, vx_sign, vy_sign, wz_sign",
    [
        ("Up", 1, 0, 0),
        ("Down", -1, 0, 0),
        ("Left", 0, 1, 0),
        ("Right", 0, -1, 0),
        ("q", 0, 0, 1),
        ("e", 0, 0, -1),
    ],
)
def test_arrow_and_rotation_keys(panel_factory, keysym, vx_sign, vy_sign, wz_sign):
    """方向键 / Q / E 的符号约定与 mecanum.keys_to_body 一致。"""
    panel, sink = panel_factory()
    panel.on_key_press(keysym)
    body = sink.last[0]

    if vx_sign == 0:
        assert body.vx == pytest.approx(0.0, **ZERO)
    else:
        assert body.vx * vx_sign > 0.0
        assert abs(body.vx) == pytest.approx(panel.linear_speed, rel=1e-6)
    if vy_sign == 0:
        assert body.vy == pytest.approx(0.0, **ZERO)
    else:
        assert body.vy * vy_sign > 0.0
        assert abs(body.vy) == pytest.approx(panel.lateral_speed, rel=1e-6)
    if wz_sign == 0:
        assert body.wz == pytest.approx(0.0, **ZERO)
    else:
        assert body.wz * wz_sign > 0.0
        assert abs(body.wz) == pytest.approx(panel.angular_speed, rel=1e-6)


def test_left_strafe_wheel_signs(panel_factory):
    """A（左平移，vy>0）时四轮符号为 FL- FR+ RL+ RR-（左轮反转）。"""
    panel, sink = panel_factory()
    panel.on_key_press("a")
    _, wheels = sink.last

    expected = panel.kinematics.body_to_limited_wheels(
        0.0, panel.lateral_speed, 0.0, panel.max_wheel_speed
    )
    assert wheels == pytest.approx(expected, rel=1e-6)
    assert wheels[0] < 0.0 and wheels[1] > 0.0
    assert wheels[2] > 0.0 and wheels[3] < 0.0


def test_release_stops_after_debounce(panel_factory):
    """松开按键：宽限期内保持，宽限期后发布零速。"""
    panel, sink = panel_factory()
    panel.on_key_press("w")
    panel.on_key_release("w")

    # 仍在防抖宽限期内，不应停车
    assert sink.last[0].vx == pytest.approx(panel.linear_speed, rel=1e-6)

    panel.update(now=time.monotonic() + 0.2)
    assert sink.last[0].is_zero()
    assert panel.pressed_keys == frozenset()


def test_auto_repeat_release_press_does_not_stop(panel_factory):
    """模拟 X11 自动重复的 Release+Press 抖动，不应误停车。"""
    panel, sink = panel_factory()
    panel.on_key_press("w")
    panel.on_key_release("w")
    panel.on_key_press("w")  # 自动重复的重新按下
    panel.update(now=time.monotonic() + 0.2)

    assert sink.last[0].vx == pytest.approx(panel.linear_speed, rel=1e-6)
    assert panel.pressed_keys == frozenset({"w"})


def test_space_emergency_stop(panel_factory):
    """空格：立即零速并清除所有按键。"""
    panel, sink = panel_factory()
    panel.on_key_press("w")
    panel.on_key_press("space")
    assert sink.last[0].is_zero()
    assert panel.pressed_keys == frozenset()

    # 松开空格后再按方向键仍能恢复运动
    panel.on_key_release("space")
    panel.on_key_press("s")
    assert sink.last[0].vx < 0.0


def test_escape_stops(panel_factory):
    """Esc：停车。"""
    panel, sink = panel_factory()
    panel.on_key_press("w")
    panel.on_key_press("Escape")
    assert sink.last[0].is_zero()
    assert panel.pressed_keys == frozenset()


def test_slider_linear_speed_changes_command(panel_factory):
    """滑块改变线速度后，按下 W 的指令随之变化。"""
    panel, sink = panel_factory()
    panel.set_linear_speed(0.55)
    assert panel.linear_speed == pytest.approx(0.55)

    panel.on_key_press("w")
    assert sink.last[0].vx == pytest.approx(0.55, rel=1e-6)


def test_slider_lateral_speed_changes_command(panel_factory):
    """滑块改变横移速度后，按下 A 的指令随之变化。"""
    panel, sink = panel_factory()
    panel.set_lateral_speed(0.8)
    panel.on_key_press("a")
    assert sink.last[0].vy == pytest.approx(0.8, rel=1e-6)


def test_slider_angular_speed_changes_command(panel_factory):
    """滑块改变角速度后，按下 Q/E 的指令随之变化。"""
    panel, sink = panel_factory()
    panel.set_angular_speed(2.0)
    panel.on_key_press("q")
    assert sink.last[0].wz == pytest.approx(2.0, rel=1e-6)

    panel.stop_motion()  # 先停车，避免 Q/E 同时按住互相抵消
    panel.on_key_press("e")
    assert sink.last[0].wz == pytest.approx(-2.0, rel=1e-6)


def test_scale_callback_path(panel_factory):
    """直接触发 ttk.Scale 的 command 回调（模拟拖动滑块）。"""
    panel, _sink = panel_factory()
    panel._on_scale_changed("linear", "0.42")  # noqa: SLF001 - 测试内部回调
    assert panel.linear_speed == pytest.approx(0.42)
    panel._on_scale_changed("angular", "1.5")  # noqa: SLF001
    assert panel.angular_speed == pytest.approx(1.5)


def test_diagonal_speed_is_normalized(panel_factory):
    """W+A 斜向移动：合成平面速度不超过 max(linear, lateral)。"""
    panel, sink = panel_factory(linear_speed=0.4, lateral_speed=0.3)
    panel.on_key_press("w")
    panel.on_key_press("a")
    body = sink.last[0]

    assert body.vx > 0.0 and body.vy > 0.0
    assert math.hypot(body.vx, body.vy) <= max(
        panel.linear_speed, panel.lateral_speed
    ) + 1e-9


def test_wheel_speed_limit_is_applied(panel_factory):
    """max_wheel_speed 限幅后，四轮不超过上限且 /cmd_vel 自洽。"""
    panel, sink = panel_factory(linear_speed=1.0, max_wheel_speed=5.0)
    panel.on_key_press("w")
    body, wheels = sink.last

    assert max(abs(value) for value in wheels) == pytest.approx(5.0, rel=1e-6)
    assert body.vx == pytest.approx(5.0 * panel.kinematics.wheel_radius, rel=1e-6)
    assert body.vx < 1.0


def test_odom_status_is_updated(panel_factory):
    """/odom 位姿写入后显示在状态栏。"""
    panel, _sink = panel_factory()
    panel.set_odom(1.25, -0.5, math.pi / 2.0)
    panel.update()

    text = panel._odom_text.get()  # noqa: SLF001 - 检查状态栏文本
    assert "x=+1.250" in text
    assert "y=-0.500" in text
    assert "θ=+90.0°" in text


def test_canvas_draws_wheels_and_body(panel_factory):
    """俯视图画布至少画出车体、四轮与文字。"""
    panel, _sink = panel_factory()
    panel.on_key_press("w")
    _flush(panel)
    items = panel.canvas.find_all()
    assert len(items) >= 10


def test_update_publishes_periodically(panel_factory):
    """update() 按发布周期发布，同一周期内不重复发布。"""
    panel, sink = panel_factory(publish_rate=20.0)
    panel.on_key_press("w")
    count = len(sink.calls)
    now = time.monotonic()

    panel.update(now=now)  # 刚发布过，同一周期内不重复
    assert len(sink.calls) == count

    panel.update(now=now + 0.2)  # 已过周期，发布下一帧
    assert len(sink.calls) == count + 1
    panel.update(now=now + 0.201)  # 又回到同一周期
    assert len(sink.calls) == count + 1


def test_cmd_timeout_stops_motion(panel_factory):
    """cmd_timeout 内没有新的按键事件时自动停车。"""
    panel, sink = panel_factory(cmd_timeout=0.2)
    panel.on_key_press("w")
    panel.update(now=time.monotonic() + 0.05)
    assert sink.last[0].vx > 0.0

    panel.update(now=time.monotonic() + 0.5)
    assert sink.last[0].is_zero()
    assert panel.pressed_keys == frozenset()


def test_default_key_silence_timeout(panel_factory):
    """默认 key_silence_timeout = 1.2 s，且有按键时才生效。"""
    panel, _sink = panel_factory()
    assert panel.key_silence_timeout == pytest.approx(1.2)


def test_key_silence_timeout_keeps_motion_before_threshold(panel_factory):
    """只有 press 没有 release：静默未超过 1.2 s 时仍保持该方向。"""
    panel, sink = panel_factory(key_silence_timeout=1.2, cmd_timeout=0.0)
    panel.on_key_press("w")
    press_time = time.monotonic()

    panel.update(now=press_time + 0.5)
    assert sink.last[0].vx == pytest.approx(panel.linear_speed, rel=1e-6)
    assert panel.pressed_keys == frozenset({"w"})


def test_key_silence_timeout_clears_stale_key(panel_factory):
    """静默超过 key_silence_timeout 后自动清空按键并回零。"""
    panel, sink = panel_factory(key_silence_timeout=1.2, cmd_timeout=0.0)
    panel.on_key_press("w")
    press_time = time.monotonic()

    panel.update(now=press_time + 0.5)
    assert sink.last[0].vx > 0.0

    panel.update(now=press_time + 1.3)
    assert sink.last[0].is_zero()
    assert panel.pressed_keys == frozenset()


def test_key_silence_timeout_zero_disables(panel_factory):
    """key_silence_timeout=0 时关闭静默兜底（保持按住语义）。"""
    panel, sink = panel_factory(key_silence_timeout=0.0, cmd_timeout=0.0)
    assert panel.key_silence_timeout == pytest.approx(0.0)
    panel.on_key_press("w")
    press_time = time.monotonic()

    panel.update(now=press_time + 5.0)
    assert sink.last[0].vx == pytest.approx(panel.linear_speed, rel=1e-6)
    assert panel.pressed_keys == frozenset({"w"})


def test_late_repeat_press_is_cleared_by_silence_timeout(panel_factory):
    """复现粘滞场景：release 之后还剩一个迟到的自动重复 KeyPress -> 兜底回零。"""
    panel, sink = panel_factory(key_silence_timeout=1.2, cmd_timeout=0.0)
    panel.on_key_press("w")
    panel.on_key_release("w")
    time.sleep(0.07)  # 越过 60 ms 防抖宽限（release 本应已生效）
    panel.on_key_press("w")  # 模拟 X 服务器在 release 后补送的重复 KeyPress
    late_press = time.monotonic()

    panel.update(now=late_press + 0.5)
    assert sink.last[0].vx > 0.0  # 1.2 s 内仍按按住处理

    panel.update(now=late_press + 1.3)
    assert sink.last[0].is_zero()
    assert panel.pressed_keys == frozenset()


def test_repeat_key_events_keep_motion_alive(panel_factory):
    """正常按住：周期性的自动重复 KeyPress 持续刷新活动时间，不会误停。"""
    panel, sink = panel_factory(key_silence_timeout=0.15, cmd_timeout=0.0)
    panel.on_key_press("w")
    end = time.monotonic() + 0.6

    while time.monotonic() < end:
        panel.on_key_press("w")  # 模拟 X11 自动重复
        panel.update()
        time.sleep(0.02)

    assert sink.last[0].vx == pytest.approx(panel.linear_speed, rel=1e-6)
    assert panel.pressed_keys == frozenset({"w"})


def test_focus_loss_stops_motion(panel_factory):
    """窗口失焦（<FocusOut>）后自动停车。"""
    panel, sink = panel_factory()
    panel.on_key_press("w")
    assert sink.last[0].vx > 0.0

    panel._on_focus_out()  # noqa: SLF001 - 模拟 Tk 的 <FocusOut> 事件
    end = time.monotonic() + 0.25
    while time.monotonic() < end:
        panel.root.update()
        time.sleep(0.01)

    assert sink.last[0].is_zero()
    assert panel.pressed_keys == frozenset()


def test_close_publishes_zero_and_is_idempotent(panel_factory):
    """关闭窗口：发布零速，重复 close 不报错。"""
    panel, sink = panel_factory()
    panel.on_key_press("w")
    panel.close()

    assert sink.last[0].is_zero()
    assert panel.closed is True
    panel.close()  # 二次调用应无副作用


def test_focus_badge_initial_off(panel_factory):
    """初始徽标为「专注模式：关（按 K 开启）」。"""
    panel, _sink = panel_factory()
    assert panel.focus_mode is False
    text = panel._focus_label.cget("text")  # noqa: SLF001
    assert "专注模式：关" in text
    assert "按 K 开启" in text


def test_set_focus_mode_updates_badge(panel_factory):
    """set_focus_mode() 更新只读状态与徽标文案。"""
    panel, _sink = panel_factory()
    panel.set_focus_mode(True)
    assert panel.focus_mode is True
    assert "开" in panel._focus_label.cget("text")  # noqa: SLF001

    panel.set_focus_mode(False, "抓取失败原因")
    assert panel.focus_mode is False
    assert "抓取失败原因" in panel._focus_label.cget("text")  # noqa: SLF001


def test_focus_k_toggles_enable_and_disable(focus_panel):
    """K 键：进入专注模式（enable + 徽标开），再按 K 退出（disable + 零速）。"""
    panel, sink, controller, holder = focus_panel()

    _press(panel, "k")
    grab = holder["grab"]
    assert grab.start_calls == 1
    assert controller.active is True
    assert panel.focus_mode is True
    text = panel._focus_label.cget("text")  # noqa: SLF001
    assert "开" in text and "全局键盘" in text and "按 K 退出" in text

    _press(panel, "k")
    assert grab.stop_calls == 1
    assert controller.active is False
    assert panel.focus_mode is False
    assert sink.last[0].is_zero()
    text = panel._focus_label.cget("text")  # noqa: SLF001
    assert "关" in text


def test_focus_k_is_not_motion_key(panel_factory):
    """没有专注模式回调时，K 不参与运动映射、不发布指令。"""
    panel, sink = panel_factory()
    _press(panel, "k")
    _release(panel, "k")
    assert sink.calls == []
    assert panel.pressed_keys == frozenset()
    assert panel.focus_mode is False


def test_focus_global_events_drive_sink(focus_panel):
    """全局回调经队列 + 主线程 dispatch 后能驱动 /cmd_vel 与零速。"""
    panel, sink, controller, holder = focus_panel()
    _press(panel, "k")
    grab = holder["grab"]

    grab.on_key("w", True, False)  # 后台线程回调 -> 入队
    assert controller.poll_once() == 1
    assert sink.last[0].vx == pytest.approx(panel.linear_speed, rel=1e-6)

    grab.on_key("w", False, False)
    controller.poll_once()
    panel.update(now=time.monotonic() + 0.2)  # 结算 60 ms 松开防抖
    assert sink.last[0].is_zero()


def test_focus_global_k_toggles_instead_of_moving(focus_panel):
    """全局抓取时的 K 用于切换专注模式，而不是当成运动键。"""
    panel, sink, controller, holder = focus_panel()
    _press(panel, "k")
    grab = holder["grab"]
    # 模拟“已经过了一段时间”（避开进入/退出瞬间的 K 自动重复防抖窗口）
    controller._last_toggle_time = 0.0  # noqa: SLF001

    grab.on_key("k", True, False)
    controller.poll_once()
    assert controller.active is False
    assert panel.focus_mode is False
    assert sink.last[0].is_zero()
    assert grab.stop_calls == 1


def test_focus_global_k_ignored_right_after_enable(focus_panel):
    """刚进入专注模式时同一物理 K 键的自动重复不应立刻把它退出。"""
    panel, _sink, controller, holder = focus_panel()
    _press(panel, "k")
    assert controller.active is True

    holder["grab"].on_key("k", True, False)  # 抓取线程立刻收到重复 K
    controller.poll_once()
    assert controller.active is True
    assert panel.focus_mode is True


def test_focus_enable_failure_shows_reason(focus_panel):
    """enable 失败（如无 DISPLAY）：保持关闭并在徽标显示中文原因。"""
    reason = "没有 DISPLAY（SSH/无图形会话无法使用专注模式）"
    panel, _sink, controller, holder = focus_panel(start_result=(False, reason))

    _press(panel, "k")
    assert holder["grab"].start_calls == 1
    assert controller.active is False
    assert panel.focus_mode is False
    text = panel._focus_label.cget("text")  # noqa: SLF001
    assert "DISPLAY" in text


def test_focus_close_releases_grab(focus_panel):
    """关闭窗口/close() 时必须释放 X11 键盘抓取。"""
    panel, _sink, controller, holder = focus_panel()
    _press(panel, "k")
    grab = holder["grab"]
    assert grab.start_calls == 1

    panel.close()
    assert panel.closed is True
    assert grab.stop_calls >= 1
    assert controller.active is False


def test_focus_after_polling_dispatches_events(focus_panel):
    """root.after 轮询路径：入队事件无需手工 poll_once 也能被主线程处理。"""
    panel, sink, controller, holder = focus_panel()
    _press(panel, "k")  # enable 后自动 start_polling

    holder["grab"].on_key("w", True, False)
    end = time.monotonic() + 0.3
    while time.monotonic() < end:
        panel.root.update()
        time.sleep(0.01)

    assert sink.last[0].vx == pytest.approx(panel.linear_speed, rel=1e-6)


def test_focus_auto_enable_default_on(focus_panel):
    """默认自动开启：schedule_auto_enable 后 grab.start 被调用、徽标=开。"""
    panel, _sink, controller, holder = focus_panel()
    controller.schedule_auto_enable(True, delay_ms=10)
    _pump(panel, 0.3)

    grab = holder.get("grab")
    assert grab is not None
    assert grab.start_calls == 1
    assert controller.active is True
    assert panel.focus_mode is True
    assert "开" in panel._focus_label.cget("text")  # noqa: SLF001


def test_focus_auto_enable_failure_shows_reason(focus_panel):
    """自动开启失败（如无 DISPLAY/已被占用）：程序不崩、徽标=关且含原因。"""
    reason = "没有 DISPLAY（SSH/无图形会话无法使用专注模式）"
    panel, _sink, controller, holder = focus_panel(start_result=(False, reason))
    controller.schedule_auto_enable(True, delay_ms=10)
    _pump(panel, 0.3)

    assert holder["grab"].start_calls == 1
    assert controller.active is False
    assert panel.focus_mode is False
    text = panel._focus_label.cget("text")  # noqa: SLF001
    assert "DISPLAY" in text


def test_focus_auto_enable_disabled(focus_panel):
    """focus_mode_default=false 等价：schedule_auto_enable(False) 不创建/启动 grab。"""
    panel, _sink, controller, holder = focus_panel()
    controller.schedule_auto_enable(False, delay_ms=10)
    _pump(panel, 0.2)

    assert "grab" not in holder
    assert controller.active is False
    assert panel.focus_mode is False
    text = panel._focus_label.cget("text")  # noqa: SLF001
    assert "按 K 开启" in text


def test_focus_auto_enable_does_not_reenter_after_k_exit(focus_panel):
    """自动开启后用户按 K 退出：后续 auto_enable 不能再自动重进（仅启动一次）。"""
    panel, _sink, controller, holder = focus_panel()
    controller.schedule_auto_enable(True, delay_ms=10)
    _pump(panel, 0.3)
    grab = holder["grab"]
    assert controller.active is True
    assert grab.start_calls == 1

    _press(panel, "k")  # 用户按 K 退出
    assert controller.active is False
    assert grab.stop_calls == 1

    assert controller.auto_enable() is False  # 一次性语义
    _pump(panel, 0.2)
    assert controller.active is False
    assert grab.start_calls == 1
    assert panel.focus_mode is False


def test_focus_auto_enable_idempotent(focus_panel):
    """auto_enable 重复调用幂等：已开启时直接返回 True、不重复 grab.start。"""
    panel, _sink, controller, holder = focus_panel()
    controller.schedule_auto_enable(True, delay_ms=10)
    _pump(panel, 0.3)

    assert controller.auto_enable() is True
    assert controller.auto_enable() is True
    assert holder["grab"].start_calls == 1
    assert controller.active is True


def test_panel_does_not_require_ros():
    """gui_teleop 的 UI 层可以在没有 ROS 回调的情况下正常创建（已由本文件证明）。"""
    assert TeleopPanel is not None
