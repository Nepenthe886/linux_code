#!/usr/bin/env python3
"""麦伦机器人 Tkinter 可视化遥控操作台（ROS 2 节点名 ``mecanum_gui``）。

功能
----
* 中文深色界面：左侧键位说明、中央麦轮底盘俯视图、右侧速度滑块、底部状态栏；
* 按住方向键持续移动（W/↑ 前进、S/↓ 后退、A/← 左平移、D/→ 右平移、
  Q/E 原地转），空格急停、Esc 停车；
* 以 ``publish_rate``（默认 20 Hz）发布 ``/cmd_vel``（``geometry_msgs/Twist``）
  与 ``/wheel_cmd``（``std_msgs/Float64MultiArray``，顺序 FL FR RL RR，rad/s）；
* 轮速统一由 :class:`robot_control.mecanum.MecanumKinematics` 计算并限幅，
  不在这里重复实现运动学公式；
* 订阅 ``/odom`` 在状态栏显示 ``(x, y, θ)``；ROS 回调跑在
  ``MultiThreadedExecutor`` 后台线程，Tk 主线程只做 UI 与定时发布；
* 窗口失焦、关闭窗口、Ctrl-C 时立即发布零速并退出；无 ``DISPLAY`` 时给出
  清晰报错并以退出码 1 结束；
* **专注模式（K）**：按 ``K`` 用 X11 全局键盘抓取接管键盘，之后即使窗口/终端
  失去焦点也能用 WASD/方向键遥控，再按 ``K`` 退出（仅 X11；抓取失败时界面
  徽标显示中文原因）。由 :class:`FocusModeController` 在 Tk 主线程分发全局按键。

与 ROS 解耦的可测试设计
-----------------------
真正的界面类是 :class:`TeleopPanel`，它不导入 ``rclpy``，构造时只接收：

* ``root``：Tk 根窗口；
* ``sink``：任何带 ``publish(body_velocity, wheel_speeds)`` 方法的对象
  （``body_velocity`` 为 :class:`mecanum.BodyVelocity`，``wheel_speeds`` 为
  四元组 rad/s）。生产代码传入 :class:`GuiTeleopNode`，测试传入假 sink。

这样 ``pytest`` 可以用假 sink + 手工调用 ``on_key_press`` / ``on_key_release``
来验证按键 -> 速度 -> 轮速链路，不需要 ROS 或图形显示。

调试运行（本机 DISPLAY=:1）::

    cd src/robot_control
    export ROS_HOME=... ROS_LOG_DIR=... ROS_DOMAIN_ID=68 ROS_LOCALHOST_ONLY=1
    DISPLAY=:1 python3 -m robot_control.gui_teleop
"""

from __future__ import annotations

import math
import queue
import sys
import threading
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from typing import Callable, Optional, Protocol, Sequence

from .focus_grab import TOGGLE_KEY, X11KeyboardGrab, is_toggle_key
from .mecanum import (
    ACTION_KEY_HINTS,
    ACTION_LABELS,
    BodyVelocity,
    MecanumKinematics,
    WHEEL_LABELS,
    key_action,
    keys_to_body,
    keys_to_actions,
)

__all__ = [
    "DEFAULT_KEY_SILENCE_TIMEOUT",
    "DEFAULT_WINDOW_TITLE",
    "FocusModeController",
    "TeleopPanel",
    "GuiTeleopNode",
    "main",
]

#: 默认窗口标题。
DEFAULT_WINDOW_TITLE = "麦伦机器人 · 麦轮遥控操作台"

#: /cmd_vel、/wheel_cmd 默认发布频率 [Hz]。
DEFAULT_PUBLISH_RATE = 20.0

#: 失焦 / 长时间没有按键事件时的自动停车超时 [s]（0 表示关闭该保护）。
DEFAULT_CMD_TIMEOUT = 0.5

#: 按键静默兜底超时 [s]：只要还有按键状态、却超过该时间没有收到任何按键
#: 事件，就清空按键并发布零速（无论窗口是否有焦点）。用于兜住“X 服务器在
#: KeyRelease 之后又送一个迟到的自动重复 KeyPress / 丢失 KeyRelease / 远程
#: 虚拟键盘”等情况下方向指令永久粘滞的健壮性缺口。``<=0`` 表示关闭该保护。
#: 默认 1.2 s 大于本机 X11 自动重复初始延迟（约 500 ms），正常按住不会误停。
DEFAULT_KEY_SILENCE_TIMEOUT = 1.2

#: X11 自动重复（auto-repeat）产生的 Release/Press 抖动宽限时间 [s]。
#: 收到 KeyRelease 后延迟这么久才真正移除按键，期间若又收到 KeyPress
#: （自动重复）则取消移除，保证按住时连续移动、松开后停车。
RELEASE_GRACE_S = 0.06

#: 界面配色（深色主题）。
BG = "#0d1117"
PANEL_BG = "#161b22"
PANEL_BG_ALT = "#21262d"
BORDER = "#30363d"
FG = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#58a6ff"
GREEN = "#3fb950"
RED = "#f85149"
ORANGE = "#d29922"
CANVAS_BG = "#0a0e14"

#: 四个轮子的指示条颜色（FL FR RL RR）。
WHEEL_COLORS = ("#4cc9f0", "#f9c74f", "#90be6d", "#c77dff")

#: 中文字体候选（按优先级）。
_CJK_FONT_CANDIDATES = (
    "Noto Sans CJK SC",
    "Noto Sans CJK JP",
    "Noto Sans Mono CJK SC",
    "Source Han Sans SC",
    "WenQuanYi Zen Hei",
    "WenQuanYi Micro Hei",
    "Microsoft YaHei",
    "PingFang SC",
    "Noto Sans SC",
    "Droid Sans Fallback",
    "AR PL UKai CN",
)

_MONO_FONT_CANDIDATES = (
    "Noto Sans Mono CJK SC",
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Noto Mono",
    "Courier New",
)


class CommandSink(Protocol):
    """``TeleopPanel`` 需要的发布接口（生产环境由 ROS 节点实现）。"""

    def publish(
        self,
        body_velocity: BodyVelocity,
        wheel_speeds: Sequence[float],
    ) -> None:  # pragma: no cover - 仅用于类型标注
        ...


def _clamp(value: float, minimum: float, maximum: float) -> float:
    """把 ``value`` 限制在 ``[minimum, maximum]`` 区间内。"""
    return max(minimum, min(maximum, float(value)))


def _as_bool(value: object, default: bool = False) -> bool:
    """把 ROS 参数覆盖值稳健地转成 bool（兼容 ``"false"`` 字符串）。"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "t"}
    if value is None:
        return default
    return bool(value)


def _pick_font(root: tk.Misc) -> str:
    """挑选一个可用的中文字体族名。"""
    try:
        families = set(tkfont.families(root))
    except tk.TclError:  # pragma: no cover - 无 Tk 环境的兜底
        return "TkDefaultFont"
    for name in _CJK_FONT_CANDIDATES:
        if name in families:
            return name
    for name in sorted(families):
        if "CJK" in name or "Han" in name or "WenQuanYi" in name or "Hei" in name:
            return name
    return "TkDefaultFont"


def _pick_mono_font(root: tk.Misc) -> str:
    """挑选一个可用的等宽字体族名（用于状态栏数值对齐）。"""
    try:
        families = set(tkfont.families(root))
    except tk.TclError:  # pragma: no cover
        return "TkFixedFont"
    for name in _MONO_FONT_CANDIDATES:
        if name in families:
            return name
    return "TkFixedFont"


class TeleopPanel:
    """Tkinter 遥控面板：与 ROS 解耦，通过注入的 ``sink`` 发布速度指令。

    Parameters
    ----------
    root:
        Tk 根窗口（测试中可以先 ``withdraw()``）。
    sink:
        带 ``publish(body_velocity, wheel_speeds)`` 方法的对象。
    linear_speed, lateral_speed, angular_speed:
        默认线速度 / 横移速度（m/s）与角速度（rad/s），也会显示在滑块上。
    max_wheel_speed:
        轮速限幅上限 [rad/s]，传给 ``MecanumKinematics.body_to_limited_wheels``。
    publish_rate:
        指令发布频率 [Hz]（默认 20）。
    window_title:
        窗口标题（中文）。
    cmd_timeout:
        失焦 / 无按键事件多久后自动停车 [s]（窗口仍持有键盘焦点时不会误停），
        0 表示关闭该保护。
    key_silence_timeout:
        按键静默兜底超时 [s]（默认 1.2）。有按键状态但超过该时间完全没有
        收到任何按键事件时，清空按键并发布零速（无论窗口是否有焦点），
        用于防止迟到的自动重复 KeyPress / 丢失 KeyRelease 造成指令粘滞；
        ``<=0`` 表示关闭该保护。
    release_grace_s:
        松开按键的防抖宽限时间 [s]（默认 60 ms，处理 X11 自动重复）。
    kinematics:
        可选的自定义运动学对象（默认按几何参数新建）。
    on_toggle_focus:
        ``K`` 键专注模式切换回调（由 :class:`FocusModeController` 提供）；
        为 ``None`` 时 ``K`` 被忽略、不作为运动键。
    on_close:
        窗口关闭时的可选回调（主程序用它通知退出）。
    """

    def __init__(
        self,
        root: tk.Tk,
        sink: CommandSink,
        *,
        linear_speed: float = 0.30,
        lateral_speed: float = 0.30,
        angular_speed: float = 1.00,
        max_wheel_speed: float = 30.0,
        publish_rate: float = DEFAULT_PUBLISH_RATE,
        window_title: str = DEFAULT_WINDOW_TITLE,
        cmd_timeout: float = DEFAULT_CMD_TIMEOUT,
        key_silence_timeout: float = DEFAULT_KEY_SILENCE_TIMEOUT,
        release_grace_s: float = RELEASE_GRACE_S,
        kinematics: Optional[MecanumKinematics] = None,
        on_toggle_focus: Optional[Callable[[], None]] = None,
        on_close: Optional[Callable[[], None]] = None,
    ) -> None:
        self.root = root
        self.sink = sink
        self.window_title = str(window_title)
        self.linear_speed = _clamp(linear_speed, 0.05, 1.0)
        self.lateral_speed = _clamp(lateral_speed, 0.05, 1.0)
        self.angular_speed = _clamp(angular_speed, 0.1, 3.0)
        self.max_wheel_speed = float(max_wheel_speed)
        self.publish_rate = max(1.0, float(publish_rate))
        self.cmd_timeout = max(0.0, float(cmd_timeout))
        self.key_silence_timeout = max(0.0, float(key_silence_timeout))
        self.release_grace_s = max(0.0, float(release_grace_s))
        self.kinematics = (
            kinematics
            if kinematics is not None
            else MecanumKinematics(max_wheel_speed=self.max_wheel_speed)
        )
        self._on_close_callback = on_close
        #: ``K`` 键专注模式切换回调（FocusModeController.toggle）。
        self.on_toggle_focus = on_toggle_focus

        # ---------------- 运行时状态 ----------------
        self._keys: set[str] = set()
        self._pending_release: dict[str, float] = {}
        self._last_key_activity = time.monotonic()
        self._publish_period = 1.0 / self.publish_rate
        self._next_publish = 0.0
        self._publish_count = 0
        self._publish_error: Optional[str] = None
        self._last_body_velocity = BodyVelocity()
        self._last_wheel_speeds: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
        self._last_publish_time: Optional[float] = None
        self._odom_lock = threading.Lock()
        self._odom: Optional[tuple[float, float, float]] = None
        self._closed = False
        self._focus_mode = False
        self._focus_mode_message = ""
        self._after_id: Optional[str] = None
        self._legend_key_labels: dict[str, tk.Label] = {}
        self._canvas_size = (460, 400)
        self.font_family = "TkDefaultFont"
        self.mono_family = "TkFixedFont"

        self._build_ui()
        self._update_focus_badge()

    # ------------------------------------------------------------------ #
    # 对外属性（测试与主程序使用）
    # ------------------------------------------------------------------ #
    @property
    def pressed_keys(self) -> frozenset[str]:
        """当前按住（已去掉抖动）的按键 keysym 集合。"""
        return frozenset(self._keys)

    @property
    def actions(self) -> frozenset[str]:
        """当前生效的动作集合（``forward`` / ``left`` / ...）。"""
        return frozenset(keys_to_actions(self._keys))

    @property
    def last_body_velocity(self) -> BodyVelocity:
        """最近一次发布的 ``/cmd_vel``。"""
        return self._last_body_velocity

    @property
    def last_wheel_speeds(self) -> tuple[float, float, float, float]:
        """最近一次发布的 ``/wheel_cmd``（FL FR RL RR，rad/s）。"""
        return self._last_wheel_speeds

    @property
    def closed(self) -> bool:
        """面板是否已经关闭。"""
        return self._closed

    @property
    def focus_mode(self) -> bool:
        """是否处于专注模式（X11 全局键盘抓取生效中）。"""
        return self._focus_mode

    def set_focus_mode(self, enabled: bool, message: str = "") -> None:
        """更新专注模式状态徽标。

        Parameters
        ----------
        enabled:
            是否处于专注模式。
        message:
            ``enabled=False`` 时展示的原因（例如抓取失败的中文说明）；
            ``enabled=True`` 时可为空。
        """
        if self._closed:
            return
        self._focus_mode = bool(enabled)
        self._focus_mode_message = str(message or "")
        self._update_focus_badge()

    def _update_focus_badge(self) -> None:
        """刷新顶部「专注模式」徽标文案与配色。"""
        if self._closed:
            return
        try:
            if self._focus_mode:
                self._focus_label.configure(
                    text="专注模式：开（全局键盘，按 K 退出）",
                    bg="#1f6feb",
                    fg="#ffffff",
                )
            else:
                if self._focus_mode_message:
                    text = f"专注模式：关（{self._focus_mode_message}）"
                else:
                    text = "专注模式：关（按 K 开启）"
                self._focus_label.configure(
                    text=text,
                    bg=PANEL_BG_ALT,
                    fg=MUTED,
                )
        except tk.TclError:  # pragma: no cover - 窗口已销毁
            pass

    # ------------------------------------------------------------------ #
    # 键盘输入（也是 pytest 直接调用的入口）
    # ------------------------------------------------------------------ #
    def on_key_press(self, keysym: str) -> None:
        """处理一次按键按下（``keysym`` 直接取自 Tk 事件或测试字符串）。"""
        if self._closed:
            return
        action = key_action(keysym)
        if action is None:
            # ESC 不在运动键位表中，但要求能随时停车。
            if keysym in ("Escape", "Esc"):
                self.stop_motion()
            return
        self._last_key_activity = time.monotonic()
        # 自动重复的 "Release + Press" 抖动：重新按下即取消待移除状态。
        self._pending_release.pop(keysym, None)
        if action == "stop":
            self.stop_motion()
            return
        if keysym not in self._keys:
            self._keys.add(keysym)
            self.publish_now()
            self._redraw()

    def on_key_release(self, keysym: str) -> None:
        """处理一次按键松开（延迟 ``release_grace_s`` 后真正移除）。"""
        if self._closed or keysym not in self._keys:
            return
        self._pending_release[keysym] = time.monotonic() + self.release_grace_s

    def stop_motion(self) -> None:
        """立即清除所有按键并发布零速（急停 / 失焦 / 关窗使用）。"""
        if self._closed:
            return
        self._keys.clear()
        self._pending_release.clear()
        self._last_key_activity = time.monotonic()
        self.publish_now()
        self._redraw()

    def flush_pending_releases(self) -> bool:
        """立刻结算所有待移除按键（忽略防抖宽限），返回是否有变化。"""
        if self._closed or not self._pending_release:
            return False
        self._pending_release.clear()
        self._keys.clear()
        self.publish_now()
        self._redraw()
        return True

    # ------------------------------------------------------------------ #
    # 速度滑块
    # ------------------------------------------------------------------ #
    def set_linear_speed(self, value: float) -> None:
        """设置前进/后退线速度（0.05~1.0 m/s）。"""
        self.linear_speed = _clamp(value, 0.05, 1.0)
        self._linear_var.set(self.linear_speed)
        self._linear_value_text.set(f"{self.linear_speed:.2f} m/s")
        self._after_speed_changed()

    def set_lateral_speed(self, value: float) -> None:
        """设置横移速度（0.05~1.0 m/s）。"""
        self.lateral_speed = _clamp(value, 0.05, 1.0)
        self._lateral_var.set(self.lateral_speed)
        self._lateral_value_text.set(f"{self.lateral_speed:.2f} m/s")
        self._after_speed_changed()

    def set_angular_speed(self, value: float) -> None:
        """设置原地旋转角速度（0.1~3.0 rad/s）。"""
        self.angular_speed = _clamp(value, 0.1, 3.0)
        self._angular_var.set(self.angular_speed)
        self._angular_value_text.set(f"{self.angular_speed:.2f} rad/s")
        self._after_speed_changed()

    def _after_speed_changed(self) -> None:
        """滑块改变后，若正在移动则立即用新速度重新发布。"""
        if self._keys:
            self.publish_now()
            self._redraw()

    # ------------------------------------------------------------------ #
    # /odom 状态（ROS 后台线程安全写入）
    # ------------------------------------------------------------------ #
    def set_odom(self, x: float, y: float, theta: float) -> None:
        """记录最新里程计位姿（可从任意线程调用，加锁）。"""
        with self._odom_lock:
            self._odom = (float(x), float(y), float(theta))

    def _read_odom(self) -> Optional[tuple[float, float, float]]:
        with self._odom_lock:
            return self._odom

    # ------------------------------------------------------------------ #
    # 定时更新 / 发布
    # ------------------------------------------------------------------ #
    def start(self) -> None:
        """启动界面：先发布一次零速，再开始 20 Hz 的刷新/发布循环。"""
        if self._closed:
            return
        self.publish_now()
        self._redraw()
        self._grab_keyboard_focus()
        self._schedule_tick()

    def _grab_keyboard_focus(self) -> None:
        """把键盘焦点拉到主窗口，保证打开即可用 WASD。"""
        try:
            self.root.focus_force()
        except tk.TclError:  # pragma: no cover
            pass

    def _schedule_tick(self) -> None:
        if self._closed:
            return
        interval_ms = max(10, int(round(1000.0 / self.publish_rate)))
        try:
            self._after_id = self.root.after(interval_ms, self._tick)
        except tk.TclError:  # pragma: no cover - 窗口已销毁
            self._after_id = None

    def _tick(self) -> None:
        if self._closed:
            return
        self.update()
        self._schedule_tick()

    def update(self, now: Optional[float] = None) -> None:
        """执行一次刷新：结算松开防抖、发布指令、重画界面。

        ``now`` 可显式传入（测试用），默认取 ``time.monotonic()``。
        """
        if self._closed:
            return
        current = time.monotonic() if now is None else float(now)
        changed = self._apply_due_releases(current)
        if (
            self._keys
            and self.key_silence_timeout > 0.0
            and (current - self._last_key_activity) > self.key_silence_timeout
        ):
            # 按键静默兜底：X 服务器可能在 KeyRelease 之后又排入一个迟到的
            # 自动重复 KeyPress（XTest/远程/虚拟键盘、丢失 release 时都可能
            # 出现），60 ms 防抖会把它当成“仍在按住”。只要超过
            # key_silence_timeout 再没有任何按键事件，就一律清空并回零，
            # 无论窗口是否有焦点，避免方向指令永久粘滞。
            self._keys.clear()
            self._pending_release.clear()
            self._last_key_activity = current
            changed = True
        if (
            self._keys
            and self.cmd_timeout > 0.0
            and (current - self._last_key_activity) > self.cmd_timeout
            and not self._window_has_focus()
        ):
            # 安全保护：窗口已经失去键盘焦点、却仍残留按键状态时直接回零
            # （正常按住时 X11 自动重复会持续刷新按键事件，不会误停）。
            self._keys.clear()
            self._pending_release.clear()
            self._last_key_activity = current
            changed = True
        if changed:
            self._publish(current)
        elif current >= self._next_publish:
            self._publish(current)
        self._redraw()

    def _apply_due_releases(self, now: float) -> bool:
        if not self._pending_release:
            return False
        changed = False
        for keysym, deadline in list(self._pending_release.items()):
            if deadline <= now:
                self._pending_release.pop(keysym, None)
                self._keys.discard(keysym)
                changed = True
        return changed

    def publish_now(self) -> tuple[BodyVelocity, tuple[float, float, float, float]]:
        """立即按当前按键状态发布一次指令。"""
        return self._publish(time.monotonic())

    def _compute_command(self) -> tuple[BodyVelocity, tuple[float, float, float, float]]:
        """按键 -> 车体速度 -> 四轮限幅轮速（只调用公共运动学 API）。"""
        requested = keys_to_body(
            self._keys,
            self.linear_speed,
            self.lateral_speed,
            self.angular_speed,
        )
        wheels = self.kinematics.body_to_limited_wheels(
            requested.vx,
            requested.vy,
            requested.wz,
            self.max_wheel_speed,
        )
        # 发布限幅后实际可达的车体速度，保证 /cmd_vel 与 /wheel_cmd 自洽。
        applied = self.kinematics.wheels_to_body(wheels)
        return applied, wheels

    def _publish(
        self, now: float
    ) -> tuple[BodyVelocity, tuple[float, float, float, float]]:
        body, wheels = self._compute_command()
        self._last_body_velocity = body
        self._last_wheel_speeds = wheels
        self._last_publish_time = now
        self._next_publish = now + self._publish_period
        self._publish_count += 1
        try:
            self.sink.publish(body, wheels)
            self._publish_error = None
        except Exception as exc:  # 发布异常不能打挂界面（例如 ROS 已关闭）
            self._publish_error = f"{type(exc).__name__}: {exc}"
        return body, wheels

    # ------------------------------------------------------------------ #
    # 关闭
    # ------------------------------------------------------------------ #
    def close(self) -> None:
        """发布零速、取消定时器并销毁窗口（可重复调用）。"""
        if self._closed:
            return
        try:
            self.stop_motion()
        except Exception:  # pragma: no cover - 退出路径尽量不抛异常
            pass
        self._closed = True
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except tk.TclError:  # pragma: no cover
                pass
            self._after_id = None
        callback = self._on_close_callback
        if callback is not None:
            try:
                callback()
            except Exception:  # pragma: no cover
                pass
        try:
            self.root.destroy()
        except tk.TclError:  # pragma: no cover
            pass

    # ------------------------------------------------------------------ #
    # Tk 事件绑定
    # ------------------------------------------------------------------ #
    def _on_key_press_event(self, event: tk.Event) -> None:
        keysym = getattr(event, "keysym", "")
        if isinstance(keysym, str) and keysym.lower() == TOGGLE_KEY:
            # K 只用于切换专注模式：不参与运动映射，也不刷新按键活动时间/
            # 触发静默兜底逻辑。
            self._request_focus_toggle()
            return
        self.on_key_press(keysym)

    def _on_key_release_event(self, event: tk.Event) -> None:
        keysym = getattr(event, "keysym", "")
        if isinstance(keysym, str) and keysym.lower() == TOGGLE_KEY:
            return
        self.on_key_release(keysym)

    def _request_focus_toggle(self) -> None:
        """请求切换专注模式（回调由 FocusModeController 注入）。"""
        callback = self.on_toggle_focus
        if callback is None:
            return
        try:
            callback()
        except Exception as exc:  # 回调异常不能打挂界面
            self.set_focus_mode(False, f"切换专注模式失败：{exc}")

    def _on_focus_out(self, _event: Optional[tk.Event] = None) -> None:
        # 失焦时稍等一下再判断：点击滑块等子控件也会产生 FocusOut，
        # 只有当整个窗口都没有焦点（切换到别的程序）时才停车。
        try:
            self.root.after(60, self._check_focus_lost)
        except tk.TclError:  # pragma: no cover
            pass

    def _on_focus_in(self, _event: Optional[tk.Event] = None) -> None:
        self._last_key_activity = time.monotonic()

    def _window_has_focus(self) -> bool:
        """当前 Tk 窗口是否持有键盘焦点。"""
        try:
            focused = self.root.focus_get()
        except (KeyError, tk.TclError):  # pragma: no cover
            return False
        return focused is not None and self._is_inside(focused)

    def _check_focus_lost(self) -> None:
        if self._closed:
            return
        if not self._window_has_focus():
            self.stop_motion()

    def _is_inside(self, widget: tk.Misc) -> bool:
        current: Optional[tk.Misc] = widget
        while current is not None:
            if current is self.root:
                return True
            current = getattr(current, "master", None)
        return False

    # ------------------------------------------------------------------ #
    # 界面搭建
    # ------------------------------------------------------------------ #
    def _build_ui(self) -> None:
        self.root.title(self.window_title)
        self.root.configure(bg=BG)
        self.font_family = _pick_font(self.root)
        self.mono_family = _pick_mono_font(self.root)
        self._init_styles()
        try:
            self.root.minsize(900, 580)
        except tk.TclError:  # pragma: no cover
            pass
        self._center_window(1000, 640)

        outer = tk.Frame(self.root, bg=BG, padx=14, pady=10)
        outer.pack(fill="both", expand=True)
        outer.rowconfigure(1, weight=1)
        outer.columnconfigure(0, weight=0)
        outer.columnconfigure(1, weight=1)
        outer.columnconfigure(2, weight=0)

        self._build_header(outer).grid(
            row=0, column=0, columnspan=3, sticky="ew", pady=(0, 8)
        )
        self._build_legend(outer).grid(row=1, column=0, sticky="nsw", padx=(0, 10))
        self._build_canvas(outer).grid(row=1, column=1, sticky="nsew")
        self._build_sliders(outer).grid(row=1, column=2, sticky="nse", padx=(10, 0))
        self._build_status(outer).grid(
            row=2, column=0, columnspan=3, sticky="ew", pady=(8, 0)
        )

        # bind_all 保证点击滑块后仍能用 WASD/方向键（键盘焦点在子控件上）。
        self.root.bind_all("<KeyPress>", self._on_key_press_event, add="+")
        self.root.bind_all("<KeyRelease>", self._on_key_release_event, add="+")
        self.root.bind("<FocusOut>", self._on_focus_out, add="+")
        self.root.bind("<FocusIn>", self._on_focus_in, add="+")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self._redraw()

    def _init_styles(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:  # pragma: no cover - 某些 Tk 构建没有 clam
            pass
        style.configure(
            "Teleop.Horizontal.TScale",
            background=PANEL_BG,
            troughcolor=CANVAS_BG,
            bordercolor=BORDER,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
            sliderlength=26,
        )
        style.map(
            "Teleop.Horizontal.TScale",
            background=[("active", PANEL_BG)],
        )

    def _center_window(self, width: int, height: int) -> None:
        try:
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
        except tk.TclError:  # pragma: no cover
            screen_w, screen_h = 1920, 1080
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 3)
        try:
            self.root.geometry(f"{width}x{height}+{x}+{y}")
        except tk.TclError:  # pragma: no cover
            pass

    def _build_header(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent, bg=BG)
        frame.columnconfigure(0, weight=1)
        tk.Label(
            frame,
            text="麦伦机器人 · 可视化遥控台",
            bg=BG,
            fg=FG,
            font=(self.font_family, 16, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            frame,
            text="按住方向键持续移动 · 松开自动停车 · 空格急停 · Esc 停车",
            bg=BG,
            fg=MUTED,
            font=(self.font_family, 10),
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        self._focus_label = tk.Label(
            frame,
            text="专注模式：关（按 K 开启）",
            bg=PANEL_BG_ALT,
            fg=MUTED,
            font=(self.font_family, 9, "bold"),
            anchor="e",
            justify="right",
            padx=8,
            pady=2,
            wraplength=380,
        )
        self._focus_label.grid(row=0, column=1, sticky="e", padx=(12, 0))
        self._action_text = tk.StringVar(master=self.root, value="当前动作：待命")
        self._action_label = tk.Label(
            frame,
            textvariable=self._action_text,
            bg=BG,
            fg=ACCENT,
            font=(self.font_family, 11, "bold"),
            anchor="e",
        )
        self._action_label.grid(row=1, column=1, sticky="e", padx=(12, 0), pady=(2, 0))
        return frame

    def _build_legend(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(
            parent,
            bg=PANEL_BG,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=12,
            pady=12,
        )
        tk.Label(
            frame,
            text="键位说明",
            bg=PANEL_BG,
            fg=FG,
            font=(self.font_family, 12, "bold"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        row = 1
        for action in (
            "forward",
            "backward",
            "left",
            "right",
            "rotate_left",
            "rotate_right",
            "stop",
        ):
            tk.Label(
                frame,
                text=ACTION_LABELS[action],
                bg=PANEL_BG,
                fg=MUTED,
                font=(self.font_family, 10),
                anchor="w",
            ).grid(row=row, column=0, sticky="w", pady=2)
            key_label = tk.Label(
                frame,
                text=ACTION_KEY_HINTS[action],
                bg=PANEL_BG_ALT,
                fg=FG,
                font=(self.font_family, 10, "bold"),
                padx=6,
                pady=1,
                anchor="e",
            )
            key_label.grid(row=row, column=1, sticky="e", pady=2, padx=(10, 0))
            self._legend_key_labels[action] = key_label
            row += 1

        # 专注模式切换键 K（不属于运动动作，不参与高亮）。
        tk.Label(
            frame,
            text="专注模式",
            bg=PANEL_BG,
            fg=MUTED,
            font=(self.font_family, 10),
            anchor="w",
        ).grid(row=row, column=0, sticky="w", pady=2)
        tk.Label(
            frame,
            text="K",
            bg=PANEL_BG_ALT,
            fg=FG,
            font=(self.font_family, 10, "bold"),
            padx=6,
            pady=1,
            anchor="e",
        ).grid(row=row, column=1, sticky="e", pady=2, padx=(10, 0))
        row += 1

        tk.Frame(frame, bg=BORDER, height=1).grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=(8, 8)
        )
        row += 1
        for text in (
            "按住持续移动，松开立即停车",
            "空格：急停并清除按键",
            "Esc：停车",
            "窗口失焦 / 关闭：自动停车",
            "K：专注模式（仅 X11，键盘被接管）",
            "20 Hz 持续发布 /cmd_vel 与 /wheel_cmd",
        ):
            tk.Label(
                frame,
                text=text,
                bg=PANEL_BG,
                fg=MUTED,
                font=(self.font_family, 9),
                anchor="w",
                justify="left",
                wraplength=210,
            ).grid(row=row, column=0, columnspan=2, sticky="w")
            row += 1
        return frame

    def _build_canvas(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(
            parent,
            bg=PANEL_BG,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self.canvas = tk.Canvas(
            frame,
            bg=CANVAS_BG,
            highlightthickness=0,
            width=self._canvas_size[0],
            height=self._canvas_size[1],
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)
        return frame

    def _build_sliders(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(
            parent,
            bg=PANEL_BG,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=14,
            pady=12,
        )
        tk.Label(
            frame,
            text="速度设定",
            bg=PANEL_BG,
            fg=FG,
            font=(self.font_family, 12, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        self._linear_value_text = tk.StringVar(
            master=self.root, value=f"{self.linear_speed:.2f} m/s"
        )
        self._linear_var, self.linear_scale = self._add_speed_block(
            frame,
            "线速度（前进/后退）",
            self._linear_value_text,
            0.05,
            1.0,
            self.linear_speed,
            "linear",
            "m/s",
        )

        self._lateral_value_text = tk.StringVar(
            master=self.root, value=f"{self.lateral_speed:.2f} m/s"
        )
        self._lateral_var, self.lateral_scale = self._add_speed_block(
            frame,
            "横移速度（左右平移）",
            self._lateral_value_text,
            0.05,
            1.0,
            self.lateral_speed,
            "lateral",
            "m/s",
        )

        self._angular_value_text = tk.StringVar(
            master=self.root, value=f"{self.angular_speed:.2f} rad/s"
        )
        self._angular_var, self.angular_scale = self._add_speed_block(
            frame,
            "角速度（原地旋转）",
            self._angular_value_text,
            0.1,
            3.0,
            self.angular_speed,
            "angular",
            "rad/s",
        )

        self._build_stop_button(frame)
        return frame

    def _add_speed_block(
        self,
        parent: tk.Misc,
        title: str,
        value_text: tk.StringVar,
        minimum: float,
        maximum: float,
        initial: float,
        kind: str,
        unit: str,
    ) -> tuple[tk.DoubleVar, ttk.Scale]:
        block = tk.Frame(parent, bg=PANEL_BG)
        block.pack(fill="x", pady=(0, 10))
        header = tk.Frame(block, bg=PANEL_BG)
        header.pack(fill="x")
        tk.Label(
            header,
            text=title,
            bg=PANEL_BG,
            fg=MUTED,
            font=(self.font_family, 10),
            anchor="w",
        ).pack(side="left")
        tk.Label(
            header,
            textvariable=value_text,
            bg=PANEL_BG,
            fg=ACCENT,
            font=(self.font_family, 10, "bold"),
            anchor="e",
        ).pack(side="right")
        variable = tk.DoubleVar(master=self.root, value=initial)
        scale = ttk.Scale(
            block,
            from_=minimum,
            to=maximum,
            orient="horizontal",
            variable=variable,
            command=lambda value, kind=kind: self._on_scale_changed(kind, value),
            style="Teleop.Horizontal.TScale",
            takefocus=False,
        )
        scale.pack(fill="x", pady=(2, 0))
        if unit == "m/s":
            range_text = f"范围 {minimum:.2f} ~ {maximum:.2f} m/s"
        else:
            range_text = f"范围 {minimum:.1f} ~ {maximum:.1f} rad/s"
        tk.Label(
            block,
            text=range_text,
            bg=PANEL_BG,
            fg=MUTED,
            font=(self.font_family, 8),
            anchor="w",
        ).pack(fill="x")
        return variable, scale

    def _build_stop_button(self, parent: tk.Misc) -> None:
        button = tk.Button(
            parent,
            text="急 停（空格）",
            command=self.stop_motion,
            bg="#3d1517",
            fg="#ff7b72",
            activebackground="#5c1f22",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=10,
            pady=9,
            cursor="hand2",
            takefocus=False,
            font=(self.font_family, 11, "bold"),
        )
        button.pack(fill="x", pady=(4, 0))
        tk.Label(
            parent,
            text="提示：拖动滑块后键盘仍然可用",
            bg=PANEL_BG,
            fg=MUTED,
            font=(self.font_family, 9),
            anchor="w",
            wraplength=215,
        ).pack(fill="x", pady=(6, 0))

    def _build_status(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(
            parent,
            bg=PANEL_BG,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=12,
            pady=8,
        )
        frame.columnconfigure(0, weight=1)
        self._cmd_text = tk.StringVar(master=self.root, value="")
        self._wheel_text = tk.StringVar(master=self.root, value="")
        self._odom_text = tk.StringVar(master=self.root, value="")
        self._publish_text = tk.StringVar(master=self.root, value="")

        for row, (variable, color) in enumerate(
            (
                (self._cmd_text, FG),
                (self._wheel_text, FG),
                (self._odom_text, MUTED),
            )
        ):
            tk.Label(
                frame,
                textvariable=variable,
                bg=PANEL_BG,
                fg=color,
                font=(self.mono_family, 10),
                anchor="w",
            ).grid(row=row, column=0, sticky="w")
        self._publish_label = tk.Label(
            frame,
            textvariable=self._publish_text,
            bg=PANEL_BG,
            fg=MUTED,
            font=(self.font_family, 9),
            anchor="e",
            justify="right",
        )
        self._publish_label.grid(
            row=0, column=1, rowspan=3, sticky="ne", padx=(12, 0)
        )
        return frame

    # ------------------------------------------------------------------ #
    # 滑块回调
    # ------------------------------------------------------------------ #
    def _on_scale_changed(self, kind: str, value: object) -> None:
        try:
            numeric = float(value)
        except (TypeError, ValueError):  # pragma: no cover
            return
        if kind == "linear":
            self.set_linear_speed(numeric)
        elif kind == "lateral":
            self.set_lateral_speed(numeric)
        elif kind == "angular":
            self.set_angular_speed(numeric)

    # ------------------------------------------------------------------ #
    # 绘制
    # ------------------------------------------------------------------ #
    def _redraw(self) -> None:
        """重画俯视图并刷新状态栏（20 Hz 调用，开销很小）。"""
        if self._closed:
            return
        self._draw_canvas()
        self._update_status_text()

    def _draw_canvas(self) -> None:
        canvas = self.canvas
        try:
            width = canvas.winfo_width()
            height = canvas.winfo_height()
        except tk.TclError:  # pragma: no cover
            return
        if width <= 1 or height <= 1:
            width, height = self._canvas_size
        canvas.delete("all")

        cx, cy = width / 2.0, height / 2.0
        body_radius_px = min(width, height) * 0.30
        # 车体半径 0.25 m（与 URDF 一致）换算成像素比例。
        scale = body_radius_px / 0.25

        # 十字参考线
        canvas.create_line(cx, 10, cx, height - 10, fill="#141b23")
        canvas.create_line(10, cy, width - 10, cy, fill="#141b23")

        # 车体圆形轮廓
        canvas.create_oval(
            cx - body_radius_px,
            cy - body_radius_px,
            cx + body_radius_px,
            cy + body_radius_px,
            outline=BORDER,
            width=2,
            fill="#11161d",
        )
        canvas.create_oval(
            cx - body_radius_px * 0.55,
            cy - body_radius_px * 0.55,
            cx + body_radius_px * 0.55,
            cy + body_radius_px * 0.55,
            outline="#1b232d",
            width=1,
        )

        # 车头方向箭头（+X）
        nose = body_radius_px * 0.98
        canvas.create_polygon(
            cx + nose,
            cy,
            cx + nose * 0.78,
            cy - body_radius_px * 0.16,
            cx + nose * 0.78,
            cy + body_radius_px * 0.16,
            fill=ACCENT,
            outline="",
        )
        canvas.create_text(
            width - 12,
            cy - 14,
            text="车头 +X",
            anchor="e",
            fill=ACCENT,
            font=(self.font_family, 9),
        )
        canvas.create_text(
            12,
            10,
            text="俯视图 · 车体坐标系（↑ +Y）",
            anchor="nw",
            fill=MUTED,
            font=(self.font_family, 9),
        )

        # 车体速度矢量
        body = self._last_body_velocity
        speed = body.speed()
        max_planar = max(self.linear_speed, self.lateral_speed, 0.1)
        if speed > 1e-3:
            ratio = min(1.0, speed / max_planar)
            vector_length = body_radius_px * (0.25 + 0.55 * ratio)
            direction = math.atan2(-body.vy, body.vx)  # 画布 y 轴向下
            end_x = cx + math.cos(direction) * vector_length
            end_y = cy + math.sin(direction) * vector_length
            canvas.create_line(
                cx,
                cy,
                end_x,
                end_y,
                arrow=tk.LAST,
                width=3,
                fill=GREEN,
                arrowshape=(9, 11, 4),
            )

        # 四轮：位置、彩色指示条、方向箭头、rad/s 数值
        bx = self.kinematics.wheel_base_x
        by = self.kinematics.wheel_base_y
        offsets = ((-bx, by), (bx, by), (-bx, -by), (bx, -by))
        reference = max(self.max_wheel_speed * 0.5, 1e-6)
        for index, (label, color, (wheel_x, wheel_y)) in enumerate(
            zip(WHEEL_LABELS, WHEEL_COLORS, offsets)
        ):
            wheel_speed = float(self._last_wheel_speeds[index])
            px = cx + wheel_x * scale
            py = cy - wheel_y * scale
            bar_length = 0.11 * scale
            bar_thickness = max(6.0, 0.05 * scale)
            active = abs(wheel_speed) > 0.05
            fill_color = color if active else "#2b3340"
            canvas.create_rectangle(
                px - bar_length / 2.0,
                py - bar_thickness / 2.0,
                px + bar_length / 2.0,
                py + bar_thickness / 2.0,
                fill=fill_color,
                outline=color,
                width=1,
            )
            # 箭头方向 = 转向；长度 = 转速相对大小
            direction = 1.0 if wheel_speed >= 0.0 else -1.0
            magnitude = min(1.0, abs(wheel_speed) / reference)
            start_x = px - direction * bar_length * 0.5
            end_x = px + direction * (bar_length * 0.5 + 0.55 * bar_length * magnitude)
            arrow_color = (
                GREEN if wheel_speed > 0.05 else RED if wheel_speed < -0.05 else "#39424e"
            )
            canvas.create_line(
                start_x,
                py,
                end_x,
                py,
                arrow=tk.LAST,
                width=3,
                fill=arrow_color,
                arrowshape=(8, 10, 3),
            )
            canvas.create_text(
                cx + wheel_x * scale * 1.32,
                cy - wheel_y * scale * 1.32,
                text=f"{label}\n{wheel_speed:+.2f} rad/s",
                fill=color if active else MUTED,
                font=(self.font_family, 9, "bold"),
                justify="center",
            )

        # 底部实时数值（与状态栏呼应）
        canvas.create_text(
            cx,
            height - 38,
            text=f"vx={body.vx:+.2f} m/s    vy={body.vy:+.2f} m/s",
            fill=FG,
            font=(self.font_family, 10, "bold"),
        )
        canvas.create_text(
            cx,
            height - 20,
            text=f"wz={body.wz:+.2f} rad/s",
            fill=ACCENT,
            font=(self.font_family, 10, "bold"),
        )

    def _update_status_text(self) -> None:
        body = self._last_body_velocity
        speed = body.speed()
        self._cmd_text.set(
            f"/cmd_vel    vx={body.vx:+.2f} m/s   vy={body.vy:+.2f} m/s   "
            f"wz={body.wz:+.2f} rad/s   |v|={speed:.2f} m/s"
        )
        wheel_text = "   ".join(
            f"{label}={value:+.2f}"
            for label, value in zip(WHEEL_LABELS, self._last_wheel_speeds)
        )
        self._wheel_text.set(f"/wheel_cmd  {wheel_text} rad/s  (FL FR RL RR)")

        odom = self._read_odom()
        if odom is None:
            self._odom_text.set("/odom       等待数据 ...（启动 sim_node 后显示位姿）")
        else:
            x, y, theta = odom
            self._odom_text.set(
                f"/odom       x={x:+.3f} m   y={y:+.3f} m   "
                f"θ={math.degrees(theta):+.1f}°  ({theta:+.2f} rad)"
            )

        if self._publish_error:
            self._publish_text.set(f"发布异常：{self._publish_error}")
            self._publish_label.configure(fg=RED)
        else:
            self._publish_text.set(
                f"{self.publish_rate:.1f} Hz · 已发布 {self._publish_count} 帧"
            )
            self._publish_label.configure(fg=MUTED)

        active = self.actions
        if not active:
            self._action_text.set("当前动作：待命")
            self._action_label.configure(fg=MUTED)
        else:
            labels = [
                ACTION_LABELS[action]
                for action in (
                    "forward",
                    "backward",
                    "left",
                    "right",
                    "rotate_left",
                    "rotate_right",
                )
                if action in active
            ]
            self._action_text.set("当前动作：" + " + ".join(labels))
            self._action_label.configure(fg=GREEN)
        for action, label_widget in self._legend_key_labels.items():
            if action in active:
                label_widget.configure(bg=ACCENT, fg="#0d1117")
            else:
                label_widget.configure(bg=PANEL_BG_ALT, fg=FG)


# ---------------------------------------------------------------------- #
# 专注模式（K）：全局键盘抓取 + Tk 主线程事件分发
# ---------------------------------------------------------------------- #
class FocusModeController:
    """专注模式控制器：X11 全局键盘抓取 <-> Tk 主线程按键分发。

    :class:`~robot_control.focus_grab.X11KeyboardGrab` 的按键回调发生在后台
    读线程，不能直接操作 Tk 控件；这里先把事件放进线程安全队列，再用
    ``root.after(30)`` 在 Tk 主线程轮询并依次调用 :class:`TeleopPanel` 的
    ``on_key_press`` / ``on_key_release``。按下 ``k``（``TOGGLE_KEY``）时切换
    专注模式本身，不作为运动键。

    Parameters
    ----------
    root:
        Tk 根窗口（用于 ``after`` 轮询）。
    grab:
        可选、直接注入的抓取对象（测试用；需提供 ``start()`` / ``stop()`` /
        ``active``）。为 ``None`` 时用 ``grab_factory`` 或
        :class:`X11KeyboardGrab` 惰性创建。
    grab_factory:
        可选的抓取对象工厂 ``factory(on_key) -> grab``（测试注入假 grab）。
    poll_interval_ms:
        队列轮询间隔（默认 30 ms）。
    logger:
        日志函数（默认打印到 stderr）；失败原因同时显示在界面徽标上。
    """

    def __init__(
        self,
        root: tk.Tk,
        *,
        grab: object = None,
        grab_factory: Optional[Callable[[Callable[[str, bool, bool], None]], object]] = None,
        poll_interval_ms: int = 30,
        logger: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.root = root
        self._grab = grab
        self._grab_factory = grab_factory
        self._poll_interval_ms = max(1, int(poll_interval_ms))
        self._logger = logger or (lambda message: print(message, file=sys.stderr))
        self._queue: "queue.Queue[tuple[str, bool, bool]]" = queue.Queue()
        self._panel: Optional[TeleopPanel] = None
        self._active = False
        self._closed = False
        self._after_id: Optional[str] = None
        # 进入/退出瞬间，物理 K 键的自动重复事件可能被全局抓取线程收到；
        # 用一个小时间窗忽略这些抖动，避免刚进入专注模式就被退出。
        self._last_toggle_time = 0.0
        self.toggle_guard_s = 0.8
        # 启动时自动进入专注模式只尝试一次；用户按 K 退出后不再自动重进。
        self._auto_enable_done = False

    # ------------------------------------------------------------------ #
    # 绑定面板 / 状态
    # ------------------------------------------------------------------ #
    def bind(self, panel: TeleopPanel) -> None:
        """绑定面板，并把面板的 ``K`` 切换回调接到本控制器。"""
        self._panel = panel
        panel.on_toggle_focus = self.toggle

    @property
    def panel(self) -> Optional[TeleopPanel]:
        """已绑定的面板。"""
        return self._panel

    @property
    def active(self) -> bool:
        """是否处于专注模式。"""
        return self._active

    @property
    def grab(self):
        """当前使用的抓取对象（未创建时为 ``None``）。"""
        return self._grab

    # ------------------------------------------------------------------ #
    # 后台线程回调（只入队，禁止碰 Tk）
    # ------------------------------------------------------------------ #
    def enqueue_global_key(
        self, name: str, pressed: bool, ctrl: bool = False
    ) -> None:
        """``X11KeyboardGrab`` 的后台线程按键回调：仅入队。"""
        if self._closed:
            return
        self._queue.put((name, bool(pressed), bool(ctrl)))

    # ------------------------------------------------------------------ #
    # 主线程队列轮询
    # ------------------------------------------------------------------ #
    def start_polling(self) -> None:
        """开始 ``root.after`` 队列轮询（重复调用安全）。"""
        if self._closed or self._after_id is not None:
            return
        try:
            self._after_id = self.root.after(self._poll_interval_ms, self._poll)
        except tk.TclError:  # pragma: no cover - 窗口已销毁
            self._after_id = None

    def _stop_polling(self) -> None:
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except tk.TclError:  # pragma: no cover
                pass
            self._after_id = None

    def _poll(self) -> None:
        self._after_id = None
        if self._closed:
            return
        self.poll_once()
        if self._active and not self._closed:
            self.start_polling()

    def poll_once(self) -> int:
        """分发队列中全部待处理事件，返回处理条数（测试可直接调用）。"""
        processed = 0
        while True:
            try:
                name, pressed, ctrl = self._queue.get_nowait()
            except queue.Empty:
                break
            self._dispatch(name, pressed, ctrl)
            processed += 1
        return processed

    def _dispatch(self, name: str, pressed: bool, ctrl: bool) -> None:
        """在 Tk 主线程把全局按键分发给面板（``k`` 用于切换专注模式）。"""
        panel = self._panel
        if panel is None or panel.closed:
            return
        if pressed and is_toggle_key(name):
            # 忽略进入/退出瞬间同一物理按键的自动重复抖动（见 __init__）。
            if time.monotonic() - self._last_toggle_time < self.toggle_guard_s:
                return
            self.toggle()
            return
        if pressed:
            panel.on_key_press(name)
        else:
            panel.on_key_release(name)

    # ------------------------------------------------------------------ #
    # 切换 / 启停
    # ------------------------------------------------------------------ #
    def _ensure_grab(self):
        if self._grab is not None:
            return self._grab
        try:
            if self._grab_factory is not None:
                self._grab = self._grab_factory(self.enqueue_global_key)
            else:
                self._grab = X11KeyboardGrab(
                    self.enqueue_global_key, logger=self._logger
                )
        except Exception as exc:  # pragma: no cover - 极端环境
            self._log(f"专注模式初始化失败：{exc}")
            return None
        return self._grab

    def auto_enable(self) -> bool:
        """启动后自动进入专注模式（只触发一次，失败只写徽标/日志）。

        返回是否处于专注模式。用户按 ``K`` 退出后再次调用本方法不会重新进入
        （一次性语义，由 ``_auto_enable_done`` 保证）。
        """
        if self._closed or self._auto_enable_done:
            return self._active
        self._auto_enable_done = True
        if self._active:
            return True
        try:
            return self.enable()
        except Exception as exc:  # pragma: no cover - enable 内部已兜底
            self._log(f"专注模式自动开启失败：{exc}")
            self._set_panel_focus_mode(False, f"专注模式自动开启失败：{exc}")
            return False

    def schedule_auto_enable(self, enabled: bool = True, delay_ms: int = 250) -> None:
        """``panel.start()`` 之后调用：延迟 ``delay_ms`` 自动进入专注模式。

        ``enabled=False``（对应 ROS 参数 ``focus_mode_default:=false``）时
        不自动进入；无论开关，自动开启都只会在启动阶段尝试一次。
        """
        if self._closed:
            return
        if not enabled:
            self._auto_enable_done = True
            return
        self._auto_enable_done = False
        try:
            self.root.after(max(0, int(delay_ms)), self.auto_enable)
        except tk.TclError:  # pragma: no cover - 窗口已销毁
            self._auto_enable_done = True

    def toggle(self) -> bool:
        """切换专注模式，返回切换后是否处于专注模式。"""
        if self._closed:
            return False
        if self._active or (
            self._grab is not None and bool(getattr(self._grab, "active", False))
        ):
            self.disable()
            return False
        return self.enable()

    def enable(self) -> bool:
        """进入专注模式；失败时在徽标显示中文原因并保持关闭。"""
        if self._closed:
            return False
        if self._active:
            return True
        if self._panel is None:
            self._log("专注模式无法启动：界面尚未初始化")
            return False
        grab = self._ensure_grab()
        if grab is None:
            self._set_panel_focus_mode(False, "专注模式无法启动：X11 抓取不可用")
            return False
        try:
            ok, message = grab.start()
        except Exception as exc:
            ok, message = False, f"专注模式启动失败：{exc}"
        if not ok:
            self._active = False
            reason = message or "专注模式启动失败"
            self._log(reason)
            self._set_panel_focus_mode(False, reason)
            return False
        self._active = True
        self._last_toggle_time = time.monotonic()
        self._log(message or "已进入专注模式")
        self._set_panel_focus_mode(True, message)
        self.start_polling()
        return True

    def disable(self, message: str = "已退出专注模式") -> None:
        """退出专注模式：停止轮询、释放键盘并发布零速。"""
        was_active = self._active
        self._active = False
        self._last_toggle_time = time.monotonic()
        self._stop_polling()
        grab = self._grab
        if grab is not None:
            try:
                grab.stop()
            except Exception as exc:  # pragma: no cover - 极端 X11 错误
                self._log(f"退出专注模式时释放键盘失败：{exc}")
        self._drain_queue()
        if was_active:
            self._log(message)
        if was_active or self._panel is not None:
            self._set_panel_focus_mode(False, message)
        panel = self._panel
        if panel is not None:
            try:
                panel.stop_motion()
            except Exception:  # pragma: no cover
                pass

    def close(self) -> None:
        """GUI 退出时调用：确保释放键盘并停止轮询（可重复调用）。"""
        if self._closed:
            return
        if self._active:
            self.disable("专注模式已关闭")
        else:
            self._stop_polling()
            grab = self._grab
            if grab is not None:
                try:
                    grab.stop()
                except Exception:  # pragma: no cover
                    pass
        self._closed = True
        self._stop_polling()
        self._drain_queue()

    # ------------------------------------------------------------------ #
    # 内部工具
    # ------------------------------------------------------------------ #
    def _set_panel_focus_mode(self, enabled: bool, message: str = "") -> None:
        panel = self._panel
        if panel is None:
            return
        try:
            panel.set_focus_mode(enabled, message)
        except tk.TclError:  # pragma: no cover
            pass

    def _drain_queue(self) -> None:
        while True:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    def _log(self, message: str) -> None:
        try:
            self._logger(message)
        except Exception:  # pragma: no cover
            pass


# ---------------------------------------------------------------------- #
# ROS 2 部分（只在运行时导入 rclpy，保证纯 UI / pytest 不依赖 ROS）
# ---------------------------------------------------------------------- #
def _build_ros_node():
    """创建 ``mecanum_gui`` 节点；节点同时实现 ``TeleopPanel`` 的 sink 接口。"""
    import rclpy  # noqa: F401  （确保调用前已 source ROS 环境）
    from geometry_msgs.msg import Twist
    from nav_msgs.msg import Odometry
    from rclpy.node import Node
    from std_msgs.msg import Float64MultiArray, MultiArrayDimension

    class GuiTeleopNode(Node):
        """ROS 2 节点：发布 /cmd_vel、/wheel_cmd，订阅 /odom。"""

        def __init__(self) -> None:
            super().__init__("mecanum_gui")
            self.cmd_vel_topic = str(
                self.declare_parameter("cmd_vel_topic", "/cmd_vel").value
            )
            self.wheel_cmd_topic = str(
                self.declare_parameter("wheel_cmd_topic", "/wheel_cmd").value
            )
            self.odom_topic = str(self.declare_parameter("odom_topic", "/odom").value)
            self.linear_speed = float(
                self.declare_parameter("linear_speed", 0.30).value
            )
            self.lateral_speed = float(
                self.declare_parameter("lateral_speed", 0.30).value
            )
            self.angular_speed = float(
                self.declare_parameter("angular_speed", 1.00).value
            )
            self.max_wheel_speed = float(
                self.declare_parameter("max_wheel_speed", 30.0).value
            )
            self.publish_rate = float(
                self.declare_parameter("publish_rate", DEFAULT_PUBLISH_RATE).value
            )
            self.window_title = str(
                self.declare_parameter("window_title", DEFAULT_WINDOW_TITLE).value
            )
            self.cmd_timeout = float(
                self.declare_parameter("cmd_timeout", DEFAULT_CMD_TIMEOUT).value
            )
            self.key_silence_timeout = float(
                self.declare_parameter(
                    "key_silence_timeout", DEFAULT_KEY_SILENCE_TIMEOUT
                ).value
            )
            self.focus_mode_default = _as_bool(
                self.declare_parameter("focus_mode_default", True).value,
                default=True,
            )

            self.get_logger().info(
                f"参数：linear_speed={self.linear_speed:.2f} m/s, "
                f"lateral_speed={self.lateral_speed:.2f} m/s, "
                f"angular_speed={self.angular_speed:.2f} rad/s, "
                f"max_wheel_speed={self.max_wheel_speed:.1f} rad/s, "
                f"publish_rate={self.publish_rate:.1f} Hz, "
                f"cmd_timeout={self.cmd_timeout:.2f} s, "
                f"key_silence_timeout={self.key_silence_timeout:.2f} s, "
                f"focus_mode_default={self.focus_mode_default}"
            )

            self._cmd_publisher = self.create_publisher(
                Twist, self.cmd_vel_topic, 10
            )
            self._wheel_publisher = self.create_publisher(
                Float64MultiArray, self.wheel_cmd_topic, 10
            )
            self._odom_callback: Optional[Callable[[float, float, float], None]] = None
            self._odom_subscription = self.create_subscription(
                Odometry, self.odom_topic, self._on_odom, 10
            )

        def set_odom_callback(
            self, callback: Optional[Callable[[float, float, float], None]]
        ) -> None:
            """注册 /odom 回调（在主线程里注册，回调在 executor 线程执行）。"""
            self._odom_callback = callback

        def _on_odom(self, message: Odometry) -> None:
            callback = self._odom_callback
            if callback is None:
                return
            position = message.pose.pose.position
            orientation = message.pose.pose.orientation
            yaw = math.atan2(
                2.0 * (orientation.w * orientation.z + orientation.x * orientation.y),
                1.0 - 2.0 * (orientation.y * orientation.y + orientation.z * orientation.z),
            )
            try:
                callback(float(position.x), float(position.y), float(yaw))
            except Exception:  # pragma: no cover - GUI 关闭时忽略
                pass

        def publish(
            self,
            body_velocity: BodyVelocity,
            wheel_speeds: Sequence[float],
        ) -> None:
            """实现 ``TeleopPanel`` 的 sink 接口：发布 /cmd_vel 与 /wheel_cmd。"""
            twist = Twist()
            twist.linear.x = float(body_velocity.vx)
            twist.linear.y = float(body_velocity.vy)
            twist.linear.z = 0.0
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = float(body_velocity.wz)
            self._cmd_publisher.publish(twist)

            message = Float64MultiArray()
            message.layout.dim = [
                MultiArrayDimension(
                    label="wheel_fl, wheel_fr, wheel_rl, wheel_rr",
                    size=4,
                    stride=4,
                )
            ]
            message.layout.data_offset = 0
            message.data = [float(value) for value in wheel_speeds]
            self._wheel_publisher.publish(message)

    return GuiTeleopNode()


def _install_callback_exception_handler(root: tk.Tk, panel: TeleopPanel) -> None:
    """接管 Tk 回调异常：Ctrl-C 时安静地关窗，其它异常打印中文错误。

    在 Tcl 事件循环里收到 SIGINT 时，Python 可能在 Tk 的回调包装层抛出
    ``KeyboardInterrupt``（traceback 会打印 "Exception in Tkinter callback"）。
    这里统一处理，保证退出时只发布零速、关闭窗口，不输出难看的堆栈。
    """

    def handler(exc_type, exc_value, exc_traceback) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            try:
                root.after_idle(panel.close)
            except tk.TclError:  # pragma: no cover
                panel.close()
            return
        import traceback

        print(
            f"错误：Tk 界面回调异常：{exc_type.__name__}: {exc_value}",
            file=sys.stderr,
        )
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    try:
        root.report_callback_exception = handler
    except tk.TclError:  # pragma: no cover
        pass


def _install_shutdown_watchdog(root: tk.Tk, panel: TeleopPanel, rclpy_module) -> None:
    """定期检查 ROS 上下文；Ctrl-C / ros2 launch SIGINT 后自动关窗口。"""

    def check() -> None:
        if panel.closed:
            return
        try:
            ok = bool(rclpy_module.ok())
        except Exception:  # pragma: no cover
            ok = False
        if not ok:
            panel.close()
            return
        try:
            root.after(200, check)
        except tk.TclError:  # pragma: no cover
            pass

    try:
        root.after(200, check)
    except tk.TclError:  # pragma: no cover
        pass


def main(argv: Optional[Sequence[str]] = None) -> int:
    """``mecanum_gui`` 节点入口（``gui_teleop = robot_control.gui_teleop:main``）。"""
    arguments = list(sys.argv[1:]) if argv is None else list(argv)

    try:
        import rclpy
        from rclpy.executors import MultiThreadedExecutor
    except ImportError as exc:
        print(
            "错误：无法导入 rclpy（{}）。\n"
            "      请先执行 source /opt/ros/humble/setup.bash 并确认 ROS 2 环境已安装。".format(
                exc
            ),
            file=sys.stderr,
        )
        return 1

    try:
        rclpy.init(args=arguments)
    except Exception as exc:  # pragma: no cover
        print(f"错误：rclpy 初始化失败：{exc}", file=sys.stderr)
        return 1

    node = None
    executor = None
    spin_thread: Optional[threading.Thread] = None
    panel: Optional[TeleopPanel] = None
    controller: Optional[FocusModeController] = None
    exit_code = 0
    try:
        node = _build_ros_node()
        panel = None
        key_help = "；".join(
            f"{ACTION_LABELS[action]} {ACTION_KEY_HINTS[action]}"
            for action in (
                "forward",
                "backward",
                "left",
                "right",
                "rotate_left",
                "rotate_right",
                "stop",
            )
        )
        key_help += "；专注模式 K（仅 X11，全局键盘）"
        node.get_logger().info(f"键位：{key_help}")
        node.get_logger().info(
            f"发布 {node.cmd_vel_topic} 与 {node.wheel_cmd_topic} "
            f"({node.publish_rate:.0f} Hz)，订阅 {node.odom_topic}"
        )

        try:
            root = tk.Tk()
        except tk.TclError as exc:
            print(
                "错误：无法创建 Tk 窗口（没有可用的图形显示）。\n"
                "      请在有图形界面的环境运行，并确认 DISPLAY 已设置\n"
                "      （例如本机可尝试 export DISPLAY=:1）。\n"
                f"      Tk 报错：{exc}",
                file=sys.stderr,
            )
            return 1

        # 专注模式：X11 全局键盘抓取，K 切换；抓取失败时徽标显示中文原因。
        controller = FocusModeController(root, logger=node.get_logger().warn)
        panel = TeleopPanel(
            root,
            node,
            linear_speed=node.linear_speed,
            lateral_speed=node.lateral_speed,
            angular_speed=node.angular_speed,
            max_wheel_speed=node.max_wheel_speed,
            publish_rate=node.publish_rate,
            window_title=node.window_title,
            cmd_timeout=node.cmd_timeout,
            key_silence_timeout=node.key_silence_timeout,
            on_toggle_focus=controller.toggle,
            on_close=controller.close,
        )
        controller.bind(panel)
        node.set_odom_callback(panel.set_odom)

        executor = MultiThreadedExecutor(num_threads=2)
        executor.add_node(node)
        spin_thread = threading.Thread(
            target=executor.spin,
            name="mecanum_gui_ros",
            daemon=True,
        )
        spin_thread.start()

        panel.start()

        # 专注模式默认开启：等待窗口映射完成后（250 ms）自动抓取全局键盘。
        # 用户按 K 退出后不会自动重新进入（只触发一次）。
        if node.focus_mode_default:
            node.get_logger().info(
                "默认进入专注模式（focus_mode_default=true）：启动后自动接管全局键盘，"
                "按 K 退出/重新进入；可用 launch 参数 focus_mode:=false 或 "
                "ros2 run robot_control gui_teleop --ros-args -p focus_mode_default:=false 关闭"
            )
        controller.schedule_auto_enable(node.focus_mode_default, delay_ms=250)

        _install_callback_exception_handler(root, panel)
        _install_shutdown_watchdog(root, panel, rclpy)
        try:
            root.mainloop()
        except KeyboardInterrupt:  # pragma: no cover - 终端 Ctrl-C
            node.get_logger().info("收到 Ctrl-C，正在发布零速并退出 ...")
    except Exception as exc:  # pragma: no cover - 顶层异常兜底
        import traceback

        print(
            f"错误：mecanum_gui 异常退出：{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        traceback.print_exc()
        exit_code = 1
    finally:
        if panel is not None:
            try:
                panel.close()  # 内部会通过 on_close 回调 controller.close()
            except Exception:  # pragma: no cover
                pass
        if controller is not None:
            try:
                controller.close()  # 幂等；确保退出时释放 X11 键盘抓取
            except Exception:  # pragma: no cover
                pass
        if executor is not None:
            try:
                executor.shutdown()
            except Exception:  # pragma: no cover
                pass
        if spin_thread is not None and spin_thread.is_alive():
            spin_thread.join(timeout=2.0)
        if node is not None:
            try:
                node.destroy_node()
            except Exception:  # pragma: no cover
                pass
        try:
            rclpy.try_shutdown()
        except Exception:  # pragma: no cover
            pass
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
