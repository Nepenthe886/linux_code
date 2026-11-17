"""``robot_control.teleop_keyboard`` 可分离逻辑的单元测试。

纯 Python：不启动 rclpy、不打开 X11、不创建真实节点；专注模式用假 grab
注入，按 ``X11KeyboardGrab`` 的 ``(on_key, start, stop, active)`` 接口模拟。

覆盖（对应 task-5 验收）：
* ``k`` 切换专注模式（tty 按键 / 全局按键都测）；
* 全局按键事件经队列进入 motion 状态（复用 hold 逻辑）；
* 专注模式中 Ctrl-C 置退出标志；
* hold/stale 语义不回归；
* 无 DISPLAY / 抓取失败时打印中文原因且不崩溃；
* 状态行包含 ``[专注模式 开/关]``、帮助包含 K 键。

运行：``cd robot_control_ws/src/robot_control && python3 -m pytest test -q``。
"""

from __future__ import annotations

import os
import sys
import threading
import time
import types

import pytest

# 允许直接从包根目录运行 pytest（与 test_mecanum.py 一致）。
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

try:  # 纯 Python 环境没有 rclpy 时整体 skip（模块 import 依赖 rclpy）
    from robot_control import teleop_keyboard as tk
except Exception as exc:  # pragma: no cover - 仅纯 Python 环境触发
    pytest.skip(
        f"robot_control.teleop_keyboard 导入失败（可能缺 rclpy）：{exc}",
        allow_module_level=True,
    )

from robot_control import mecanum  # noqa: E402


# --------------------------------------------------------------------------- #
# 测试替身
# --------------------------------------------------------------------------- #
class FakeGrab:
    """假的 X11KeyboardGrab：记录 start/stop，保存回调供测试触发。"""

    def __init__(self, on_key, result=(True, "已进入专注模式：按 K 退出")):
        self.on_key = on_key
        self.result = result
        self.start_calls = 0
        self.stop_calls = 0
        self._active = False

    @property
    def active(self) -> bool:
        return self._active

    def start(self):
        self.start_calls += 1
        ok, message = self.result
        self._active = bool(ok)
        return ok, message

    def stop(self):
        self.stop_calls += 1
        self._active = False


class FakeFocus:
    """假 FocusModeController，供节点逻辑（dummy）测试使用。"""

    def __init__(self, active=False, toggle_result=(True, "已进入专注模式")):
        self.active = active
        self.toggle_result = toggle_result
        self.toggle_calls = 0
        self.stop_calls = 0

    @staticmethod
    def availability():
        return False, "没有 DISPLAY（测试环境）"

    def toggle(self):
        self.toggle_calls += 1
        if self.active:
            self.active = False
            return False, "键盘已释放"
        ok, message = self.toggle_result
        self.active = bool(ok)
        return self.active, message

    def stop(self):
        self.stop_calls += 1
        self.active = False


def make_controller(result=(True, "已进入专注模式：按 K 退出")):
    """返回 (controller, grabs 列表)。"""
    grabs: list[FakeGrab] = []

    def factory(on_key):
        grab = FakeGrab(on_key, result=result)
        grabs.append(grab)
        return grab

    return tk.FocusModeController(factory), grabs


def make_dummy(focus=None):
    """构造只带节点方法所需属性的 dummy 对象，避免 rclpy.init()。

    通过 ``MethodType`` 把 ``TeleopKeyboard`` 的真实方法绑到 dummy 上，这样
    测的是节点里那份逻辑，而不是复制品。
    """
    dummy = types.SimpleNamespace()
    dummy._running = True
    dummy._hold = tk.HoldState(0.4)
    dummy._focus = focus if focus is not None else FakeFocus()
    dummy.focus_mode_default = True
    dummy._focus_auto_done = False
    dummy._publish_calls = []
    dummy._status_calls = []
    dummy._lines = []

    def publish_body(body):
        dummy._publish_calls.append(body)
        return (0.0, 0.0, 0.0, 0.0)

    dummy._publish_body = publish_body
    dummy._print_status = lambda body, wheels: dummy._status_calls.append((body, wheels))
    dummy._print_line = dummy._lines.append
    # _print_help 需要的参数
    dummy.linear_speed = 0.30
    dummy.lateral_speed = 0.30
    dummy.angular_speed = 1.00
    dummy.max_wheel_speed = 30.0
    dummy.publish_rate = 20.0
    dummy.stale_timeout = 0.4
    dummy._status_width = 0

    for name in (
        "_handle_event",
        "_handle_global_event",
        "_toggle_focus_mode",
        "_auto_enable_focus_mode",
        "_print_status",
        "_print_help",
    ):
        setattr(dummy, name, types.MethodType(getattr(tk.TeleopKeyboard, name), dummy))
    return dummy


def body_of(dummy):
    """按 dummy 当前 hold 状态计算车体速度（与节点 _publish_hold 一致）。"""
    return mecanum.keys_to_body(
        dummy._hold.keys,
        max_linear=dummy.linear_speed,
        max_lateral=dummy.lateral_speed,
        max_angular=dummy.angular_speed,
    )


# --------------------------------------------------------------------------- #
# 全局事件分类
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "name,pressed,ctrl,expected",
    [
        ("w", True, False, "press"),
        ("s", False, False, "release"),
        ("Up", True, False, "press"),
        (" ", True, False, "press"),
        ("k", True, False, "toggle"),
        ("K", True, False, "toggle"),
        ("k", False, False, "release"),  # 松开 k 不切换
        ("c", True, True, "quit"),  # 专注模式 Ctrl-C 退出
        ("C", True, True, "quit"),
        ("c", False, True, "ignore"),
        ("w", True, True, "ignore"),  # Ctrl+其它键不参与运动
    ],
)
def test_classify_global_event(name, pressed, ctrl, expected):
    assert tk.classify_global_event(name, pressed, ctrl) == expected


# --------------------------------------------------------------------------- #
# FocusModeController
# --------------------------------------------------------------------------- #
def test_toggle_enables_then_disables_grab():
    controller, grabs = make_controller()
    assert controller.active is False

    ok, message = controller.toggle()
    assert ok is True
    assert controller.active is True
    assert len(grabs) == 1
    assert grabs[0].start_calls == 1
    assert "专注模式" in message

    ok, message = controller.toggle()
    assert ok is False
    assert controller.active is False
    assert grabs[0].stop_calls == 1
    assert message  # 退出也有中文说明


def test_global_events_are_queued_thread_safely():
    controller, grabs = make_controller()
    controller.enable()
    grab = grabs[0]
    assert controller.poll() == []

    sent = [("w", True, False), ("w", False, False), ("a", True, False), ("k", True, False)]

    def producer():
        for event in sent:
            grab.on_key(*event)

    thread = threading.Thread(target=producer)
    thread.start()
    thread.join()

    assert controller.poll() == sent  # 回调线程只入队，主线程消费
    assert controller.poll() == []


def test_enable_failure_no_display_keeps_disabled():
    reason = "没有 DISPLAY（SSH/无图形会话无法使用专注模式）"
    controller, grabs = make_controller(result=(False, reason))

    ok, message = controller.enable()
    assert ok is False
    assert controller.active is False
    assert message == reason
    assert controller.last_message == reason

    # 不崩溃、可重试，且仍然拿不到键盘
    ok2, message2 = controller.enable()
    assert ok2 is False
    assert message2 == reason
    assert grabs[0].start_calls == 2
    assert controller.active is False


def test_disable_discards_pending_global_events():
    controller, grabs = make_controller()
    controller.enable()
    grabs[0].on_key("w", True, False)
    grabs[0].on_key("a", True, False)
    controller.disable()
    assert controller.active is False
    assert controller.poll() == []  # 退出后不残留旧按键


def test_stop_is_safe_and_releases_grab():
    controller, grabs = make_controller()
    controller.enable()
    controller.stop()
    controller.stop()  # 幂等，不抛异常
    assert controller.active is False
    assert grabs[0].stop_calls >= 1


# --------------------------------------------------------------------------- #
# HoldState（hold / stale 不回归）
# --------------------------------------------------------------------------- #
def test_hold_state_press_and_stale_expiry():
    hold = tk.HoldState(stale_timeout=0.4)
    hold.press("w", 100.0)
    assert hold.keys == ("w",)
    assert bool(hold) is True

    assert hold.prune(100.3) == ("w",)  # 仍在 hold 窗口内
    assert hold.prune(100.41) == ()  # 超过 0.4 s 自动松开
    assert bool(hold) is False
    assert hold.prune(200.0) == ()


def test_hold_state_release_and_clear():
    hold = tk.HoldState(0.4)
    hold.press("w", 1.0)
    hold.press("a", 1.0)
    assert hold.keys == ("a", "w")  # 稳定排序
    hold.release("w")
    assert hold.keys == ("a",)
    hold.release("not-pressed")  # 不抛异常
    hold.clear()
    assert hold.keys == ()


def test_hold_state_rejects_negative_timeout():
    with pytest.raises(ValueError):
        tk.HoldState(-0.1)


def test_hold_auto_repeat_extends_motion():
    """模拟全局按键（含 X11 自动重复的 press/release 对）与 stale 停车。"""
    dummy = make_dummy()
    # 按下 w
    dummy._handle_global_event("w", True, False)
    assert dummy._hold.keys == ("w",)
    # X11 自动重复：press/release 都刷新 hold
    dummy._handle_global_event("w", False, False)
    dummy._handle_global_event("w", True, False)
    assert dummy._hold.keys == ("w",)
    body = body_of(dummy)
    assert body.vx == pytest.approx(0.30)
    assert body.vy == pytest.approx(0.0)

    # 物理松开后不再有事件 -> 超过 stale_timeout 自动停车
    future = time.monotonic() + 10.0
    assert dummy._hold.prune(future) == ()
    assert body_of(dummy).is_zero()


# --------------------------------------------------------------------------- #
# 节点逻辑（真实方法 + dummy 属性，无需 rclpy.init）
# --------------------------------------------------------------------------- #
def test_terminal_ctrl_c_sets_exit_flag():
    dummy = make_dummy()
    dummy._handle_event(tk.EVENT_CTRL_C)
    assert dummy._running is False


def test_terminal_k_toggles_focus_mode():
    dummy = make_dummy()
    dummy._handle_event("k")
    assert dummy._focus.toggle_calls == 1
    assert dummy._focus.active is True
    assert any("专注模式" in line and "已开启" in line for line in dummy._lines)


def test_global_k_toggles_focus_mode():
    dummy = make_dummy()
    dummy._handle_global_event("k", True, False)
    assert dummy._focus.toggle_calls == 1
    assert dummy._focus.active is True


def test_global_ctrl_c_sets_exit_flag():
    dummy = make_dummy(FakeFocus(active=True))
    dummy._handle_global_event("c", True, True)
    assert dummy._running is False


def test_global_ctrl_other_key_is_ignored():
    dummy = make_dummy(FakeFocus(active=True))
    dummy._handle_global_event("w", True, True)  # Ctrl+W 不驱动运动
    assert dummy._hold.keys == ()
    assert dummy._publish_calls == []


def test_global_space_immediate_stop():
    dummy = make_dummy(FakeFocus(active=True))
    dummy._handle_global_event("w", True, False)
    assert dummy._hold.keys == ("w",)

    dummy._handle_global_event(" ", True, False)
    assert dummy._hold.keys == ()
    assert dummy._publish_calls, "空格急停应立刻发布零速"
    assert dummy._publish_calls[-1].is_zero()
    # 松开空格不应重新激活动作
    dummy._handle_global_event(" ", False, False)
    assert dummy._hold.keys == ()


def test_toggle_failure_prints_reason_and_keeps_running():
    focus = FakeFocus(toggle_result=(False, "没有 DISPLAY（SSH/无图形会话无法使用专注模式）"))
    dummy = make_dummy(focus)
    dummy._hold.press("w", time.monotonic())

    dummy._handle_event("k")  # 按 K 但环境不可用

    assert dummy._running is True  # 不崩溃、继续遥控
    assert dummy._focus.active is False
    assert any("无法开启" in line and "DISPLAY" in line for line in dummy._lines)
    assert dummy._hold.keys == ()  # 切换时先清空旧按键
    assert dummy._publish_calls and dummy._publish_calls[-1].is_zero()


def test_status_line_contains_focus_flag(capsys):
    dummy = make_dummy()
    dummy._print_status(mecanum.BodyVelocity(), (0.0, 0.0, 0.0, 0.0))
    out_off = capsys.readouterr().out
    assert "[专注模式 关]" in out_off
    assert "车体 vx=" in out_off

    dummy._focus.active = True
    dummy._print_status(mecanum.BodyVelocity(), (0.0, 0.0, 0.0, 0.0))
    out_on = capsys.readouterr().out
    assert "[专注模式 开]" in out_on


def test_help_mentions_toggle_key_and_availability():
    dummy = make_dummy()  # FakeFocus.availability -> (False, 没有 DISPLAY...)
    dummy._print_help()
    text = "\n".join(dummy._lines)  # make_dummy 把 _print_line 收集到 _lines
    assert "K" in text
    assert "专注模式" in text
    assert "不可用" in text  # 无 DISPLAY 时帮助里给出原因提示


# --------------------------------------------------------------------------- #
# 专注模式默认开启（focus_mode_default，task-7）
# --------------------------------------------------------------------------- #
class FakeTerminal:
    """假 RawTerminal 上下文，供 run() 启动接线测试使用。"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def test_auto_focus_default_true_starts_grab():
    controller, grabs = make_controller()
    dummy = make_dummy(controller)

    dummy._auto_enable_focus_mode()

    assert controller.active is True
    assert len(grabs) == 1
    assert grabs[0].start_calls == 1
    assert any("自动进入专注模式" in line for line in dummy._lines)


def test_auto_focus_default_false_does_not_start():
    controller, grabs = make_controller()
    dummy = make_dummy(controller)
    dummy.focus_mode_default = False

    dummy._auto_enable_focus_mode()

    assert controller.active is False
    assert grabs == []  # 连 grab 对象都不创建
    assert dummy._lines == []
    assert dummy._status_calls == []


def test_auto_focus_failure_keeps_running_without_grab():
    reason = "没有 DISPLAY（SSH/无图形会话无法使用专注模式）"
    controller, grabs = make_controller(result=(False, reason))
    dummy = make_dummy(controller)

    dummy._auto_enable_focus_mode()  # 失败只打印原因，不抛异常

    assert controller.active is False
    text = "\n".join(dummy._lines)
    assert "失败" in text and "DISPLAY" in text
    # 普通终端遥控仍然可用
    dummy._handle_event("w")
    assert dummy._hold.keys == ("w",)
    assert dummy._running is True


def test_auto_focus_does_not_reenter_after_k_exit():
    controller, grabs = make_controller()
    dummy = make_dummy(controller)

    dummy._auto_enable_focus_mode()
    assert controller.active is True
    assert grabs[0].start_calls == 1

    dummy._toggle_focus_mode()  # 用户按 K 退出
    assert controller.active is False
    assert grabs[0].stop_calls == 1
    assert any("已退出" in line for line in dummy._lines)

    dummy._auto_enable_focus_mode()  # 不得自动重新进入
    assert controller.active is False
    assert grabs[0].start_calls == 1

    dummy._toggle_focus_mode()  # 用户再次按 K 可手动重新进入
    assert controller.active is True
    assert grabs[0].start_calls == 2


def test_run_auto_enables_focus_on_startup(monkeypatch):
    """run() 启动接线：focus_mode_default=true 时终端就绪后自动 grab.start。"""
    controller, grabs = make_controller()
    dummy = make_dummy(controller)
    dummy._loop = lambda terminal: None  # 跳过真实主循环
    monkeypatch.setattr(tk, "RawTerminal", FakeTerminal)

    exit_code = tk.TeleopKeyboard.run(dummy)

    assert exit_code == 0
    assert len(grabs) == 1
    assert grabs[0].start_calls == 1
    assert any("自动进入专注模式" in line for line in dummy._lines)
    # run() 退出时统一释放键盘
    assert grabs[0].stop_calls >= 1


def test_run_does_not_auto_enable_when_disabled(monkeypatch):
    controller, grabs = make_controller()
    dummy = make_dummy(controller)
    dummy.focus_mode_default = False
    dummy._loop = lambda terminal: None
    monkeypatch.setattr(tk, "RawTerminal", FakeTerminal)

    exit_code = tk.TeleopKeyboard.run(dummy)

    assert exit_code == 0
    assert grabs == []
    assert controller.active is False


# --------------------------------------------------------------------------- #
# 与 mecanum 键位表的一致性（集成防回归）
# --------------------------------------------------------------------------- #
def test_global_wasd_use_existing_key_mapping():
    """全局 WASD/方向键复用 mecanum 映射，产生与终端一致的车体速度。"""
    for name, expected in (
        ("w", mecanum.BodyVelocity(0.30, 0.0, 0.0)),
        ("s", mecanum.BodyVelocity(-0.30, 0.0, 0.0)),
        ("a", mecanum.BodyVelocity(0.0, 0.30, 0.0)),
        ("d", mecanum.BodyVelocity(0.0, -0.30, 0.0)),
        ("Up", mecanum.BodyVelocity(0.30, 0.0, 0.0)),
        ("Left", mecanum.BodyVelocity(0.0, 0.30, 0.0)),
    ):
        dummy = make_dummy(FakeFocus(active=True))
        dummy._handle_global_event(name, True, False)
        assert body_of(dummy) == expected
