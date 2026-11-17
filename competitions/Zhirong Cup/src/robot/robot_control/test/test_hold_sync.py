#!/usr/bin/env python3
"""专注模式长按保持的回归测试（不依赖真实键盘抓取，无 X11 grab）。

背景：X11 自动重复事件在部分桌面/远程/虚拟键盘环境下不可靠，如果只靠
自动重复续命，长按前进几秒后会被静默超时清掉。修复方案是专注模式下用
``XQueryKeymap`` 的物理键盘位图精确同步按键状态，本测试用假 grab 验证：

* 物理按住 W 的 10 秒内（期间没有任何自动重复事件），速度始终保持；
* 物理松开后一次同步内立即回零；
* 退出专注模式后恢复普通超时逻辑。
"""

from __future__ import annotations

import os
import sys
import time

import pytest

PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

try:
    import tkinter as tk
except ImportError:  # pragma: no cover
    pytest.skip("未安装 tkinter，跳过长按保持测试", allow_module_level=True)

from robot_control.focus_grab import keymap_bits_to_keycodes  # noqa: E402
from robot_control.gui_teleop import FocusModeController, TeleopPanel  # noqa: E402

if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
    pytest.skip("没有 DISPLAY，跳过 Tkinter 长按保持测试", allow_module_level=True)


class FakeSink:
    def __init__(self) -> None:
        self.calls = []

    def publish(self, body_velocity, wheel_speeds) -> None:
        self.calls.append((body_velocity, tuple(wheel_speeds)))

    @property
    def last(self):
        return self.calls[-1]


class PhysGrab:
    """假抓取：支持 pressed_keys() 物理键盘位图接口。"""

    def __init__(self, pressed=()):
        self.pressed = set(pressed)
        self.on_key = None
        self.active = False
        self.start_calls = 0
        self.stop_calls = 0

    def start(self):
        self.active = True
        self.start_calls += 1
        return True, "已进入专注模式"

    def stop(self):
        self.active = False
        self.stop_calls += 1

    def pressed_keys(self):
        return frozenset(self.pressed)


class NoPhysGrab:
    """不支持物理位图的假抓取（老接口）：控制器应跳过同步。"""

    def __init__(self):
        self.on_key = None
        self.active = False
        self.start_calls = 0

    def start(self):
        self.active = True
        self.start_calls += 1
        return True, "已进入专注模式"

    def stop(self):
        self.active = False


def test_keymap_bit_decoding():
    bits = bytes([0b00000101, 0b10000000] + [0] * 30)
    codes = keymap_bits_to_keycodes(bits)
    assert codes == frozenset({0, 2, 15})


def _make_panel():
    root = tk.Tk()
    root.withdraw()
    sink = FakeSink()
    panel = TeleopPanel(
        root,
        sink,
        cmd_timeout=0.5,
        key_silence_timeout=1.2,
    )
    return root, panel, sink


def test_hold_survives_without_autorepeat_10s():
    root, panel, sink = _make_panel()
    grab = PhysGrab()
    controller = FocusModeController(root, grab=grab)
    controller.bind(panel)
    try:
        assert controller.enable() is True
        assert panel.global_capture is True
        grab.pressed = {"w"}
        base = time.monotonic()
        for step in range(100):  # 模拟 10 s，期间没有任何按键/重复事件
            controller.poll_once()
            panel.update(now=base + step * 0.1)
            body, _wheels = sink.last
            assert body.vx > 0.0, f"第 {step} 步前进指令被意外清零"
        # 物理松开：下一次同步后立即回零
        grab.pressed = set()
        controller.poll_once()
        panel.update(now=base + 10.1)
        body, _wheels = sink.last
        assert body.vx == 0.0 and body.vy == 0.0
    finally:
        controller.close()
        try:
            panel.close()
        except Exception:
            pass


def test_disable_restores_normal_timeouts():
    root, panel, sink = _make_panel()
    grab = PhysGrab({"w"})
    controller = FocusModeController(root, grab=grab)
    controller.bind(panel)
    try:
        assert controller.enable() is True
        controller.poll_once()
        panel.update()
        assert panel.global_capture is True
        controller.disable()
        assert panel.global_capture is False
        assert grab.stop_calls >= 1
        panel.update()
        body, _wheels = sink.last
        assert body.vx == 0.0
    finally:
        controller.close()
        try:
            panel.close()
        except Exception:
            pass


def test_controller_skips_sync_when_grab_has_no_physical_state():
    root, panel, _sink = _make_panel()
    grab = NoPhysGrab()
    controller = FocusModeController(root, grab=grab)
    controller.bind(panel)
    try:
        assert controller.enable() is True
        # 老抓取没有 pressed_keys：不应把已有按键状态错误清空
        panel.on_key_press("w")
        controller.poll_once()
        assert panel.pressed_keys == {"w"}
    finally:
        controller.close()
        try:
            panel.close()
        except Exception:
            pass
