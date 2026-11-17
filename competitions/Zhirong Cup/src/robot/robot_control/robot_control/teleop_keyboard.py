"""终端原始键盘遥控节点（节点名 ``teleop_keyboard``）。

在没有图形界面的终端里用键盘遥控麦轮底盘：读取终端原始按键（termios raw
模式 + select 非阻塞读取），把按键归一化为车体速度，再换算成四轮角速度后
按固定频率发布：

* ``/cmd_vel``（``geometry_msgs/Twist``）：``linear.x`` 前向、``linear.y``
  左向、``angular.z`` 逆时针；
* ``/wheel_cmd``（``std_msgs/Float64MultiArray``，顺序 FL FR RL RR，rad/s）。

键位（与 ``mecanum.KEY_ALIASES`` 一致，映射统一走 ``mecanum.key_action``）：

===========  ==========  ==================================
按键          动作        说明
===========  ==========  ==================================
W / ↑        前进        ``+linear.x``
S / ↓        后退        ``-linear.x``
A / ←        左平移      ``+linear.y``
D / →        右平移      ``-linear.y``
Q            左转        ``+angular.z``（逆时针）
E            右转        ``-angular.z``（顺时针）
空格          急停        立即清零
K            专注模式    全局键盘抓取开/关（X11）
Ctrl-C       退出        恢复终端并发布零速
===========  ==========  ==================================

终端没有"按键松开"事件，因此采用 hold 语义：收到按键后保持动作，超过
``stale_timeout``（默认 0.4 s）没有该键的新事件（终端自动重复可以维持）就
自动停车；空格立即清零。

专注模式（K）
-------------
启动后**默认自动进入专注模式**（参数 ``focus_mode_default``，默认 true）：
节点就绪后立即调用 :class:`robot_control.focus_grab.X11KeyboardGrab` 做 X11
主动键盘抓取，无需先聚焦终端即可用 WASD/方向键遥控；想关闭默认开启可加
``--ros-args -p focus_mode_default:=false``（launch 里是 ``focus_mode:=false``）。
自动进入只在启动时尝试一次，按 ``k`` 退出后**不会**自动重新进入，再按 ``k``
可手动重新进入。

进入后无论焦点在哪个窗口（其它应用/桌面/别的终端）都能遥控。全局按键回调
运行在后台线程，本节点只把 ``(name, pressed, ctrl)`` 投递到队列，由主循环
消费后复用同一套 ``key_action`` / ``keys_to_body`` / hold 逻辑，绝不在回调
线程里改运动状态。专注模式中的 Ctrl-C 会优雅退出（恢复 termios、发布零速、
释放键盘）。启动自动进入失败或之后按 ``k`` 遇到无 DISPLAY / 抓取失败时，只
打印中文原因，普通终端遥控继续可用。

运行：``python3 -m robot_control.teleop_keyboard``（优先读 ``/dev/tty``，
回退 stdin；没有 TTY 时报错并以退出码 1 结束）。
"""

from __future__ import annotations

import copy
import os
import queue
import select
import shutil
import sys
import termios
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, MultiArrayDimension

from robot_control.focus_grab import TOGGLE_KEY, is_toggle_key
from robot_control.mecanum import (
    ACTION_KEY_HINTS,
    ACTION_LABELS,
    BodyVelocity,
    MecanumKinematics,
    format_wheels,
    key_action,
    keys_to_body,
)

#: 读取键盘事件的特殊返回值：退出。
EVENT_CTRL_C = "CTRL_C"
EVENT_CTRL_D = "CTRL_D"
_QUIT_EVENTS = frozenset({EVENT_CTRL_C, EVENT_CTRL_D})

#: 全局抓取回调事件的分类结果。
GLOBAL_EVENT_PRESS = "press"
GLOBAL_EVENT_RELEASE = "release"
GLOBAL_EVENT_TOGGLE = "toggle"
GLOBAL_EVENT_QUIT = "quit"
GLOBAL_EVENT_IGNORE = "ignore"

#: 方向键转义序列 -> 与 ``mecanum.KEY_ALIASES`` 对应的键符号。
_ESCAPE_SEQUENCES: dict[bytes, str] = {
    b"\x1b[A": "Up",
    b"\x1b[B": "Down",
    b"\x1b[C": "Right",
    b"\x1b[D": "Left",
    # 部分终端（application cursor mode）用 ESC O 前缀。
    b"\x1bOA": "Up",
    b"\x1bOB": "Down",
    b"\x1bOC": "Right",
    b"\x1bOD": "Left",
}

#: 帮助信息里的按键顺序。
_HELP_ACTIONS = (
    "forward",
    "backward",
    "left",
    "right",
    "rotate_left",
    "rotate_right",
    "stop",
)


class TerminalError(RuntimeError):
    """终端不可用（没有 TTY）时抛出。"""


class RawTerminal:
    """把终端切到 raw 模式并读取原始按键字节。

    优先打开 ``/dev/tty``（即使 stdin/stdout 被重定向也能工作）；失败后回退
    ``sys.stdin``；两者都不是终端时抛 :class:`TerminalError`。
    """

    def __init__(self) -> None:
        self._stream = None
        self._fd = -1
        self._old_attrs = None

        stream = None
        try:
            candidate = open("/dev/tty", "rb", buffering=0)
            if os.isatty(candidate.fileno()):
                stream = candidate
            else:
                candidate.close()
        except OSError:
            stream = None

        if stream is None:
            if sys.stdin is None or not sys.stdin.isatty():
                raise TerminalError(
                    "无法打开 /dev/tty，且 stdin 不是终端（当前没有可用的 TTY）。"
                    "请在真实终端中运行 teleop_keyboard，或改用 gui_teleop。"
                )
            stream = sys.stdin

        self._stream = stream
        self._fd = stream.fileno()

    # -- 上下文管理：进入时保存并设置 termios，退出时恢复 --------------
    def __enter__(self) -> "RawTerminal":
        self._old_attrs = termios.tcgetattr(self._fd)
        attrs = copy.deepcopy(self._old_attrs)

        # 输入：关闭特殊字符处理，按键立即可读。
        attrs[0] &= ~(
            termios.BRKINT
            | termios.ICRNL
            | termios.INLCR
            | termios.IGNCR
            | termios.INPCK
            | termios.ISTRIP
            | termios.IXON
            | termios.PARMRK
        )
        # 输出：保持 OPOST（状态行用 \r 刷新，和普通终端输出共存）。
        # 控制：8 位字符，无校验。
        attrs[2] &= ~(termios.CSIZE | termios.PARENB)
        attrs[2] |= termios.CS8
        # 本地：关闭回显、行缓冲、信号键（Ctrl-C 作为字节 0x03 交给程序处理）。
        attrs[3] &= ~(
            termios.ECHO
            | termios.ECHONL
            | termios.ICANON
            | termios.ISIG
            | termios.IEXTEN
        )
        attrs[6][termios.VMIN] = 0
        attrs[6][termios.VTIME] = 0
        termios.tcsetattr(self._fd, termios.TCSANOW, attrs)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.restore()
        if self._stream is not None and self._stream is not sys.stdin:
            try:
                self._stream.close()
            except OSError:
                pass
            self._stream = None

    def restore(self) -> None:
        """恢复进入前的终端属性（幂等）。"""
        if self._old_attrs is not None:
            try:
                termios.tcsetattr(self._fd, termios.TCSANOW, self._old_attrs)
            except (OSError, termios.error):
                pass
            self._old_attrs = None

    # -- 读取 ----------------------------------------------------------
    def read(self, timeout: float) -> bytes:
        """最多等待 ``timeout`` 秒，返回本次可读到的原始字节。"""
        try:
            readable, _, _ = select.select([self._fd], [], [], max(0.0, timeout))
        except (OSError, ValueError):
            return b""
        if not readable:
            return b""
        try:
            return os.read(self._fd, 64)
        except (BlockingIOError, InterruptedError):
            return b""
        except OSError:
            return b""


class KeyParser:
    """把原始字节流解析成键符号（``w``/``Up``/`` ``/Ctrl-C...）。

    方向键会拆成 ESC 序列；解析器内部保留不完整的转义序列前缀，等后续字节
    到达再处理。
    """

    def __init__(self) -> None:
        self._buffer = b""

    def feed(self, data: bytes) -> list[str]:
        if data:
            self._buffer += data
        events: list[str] = []
        while self._buffer:
            if self._buffer[0] == 0x1B:  # ESC：方向键等转义序列
                matched = None
                for sequence, symbol in _ESCAPE_SEQUENCES.items():
                    if self._buffer.startswith(sequence):
                        matched = (sequence, symbol)
                        break
                if matched is not None:
                    events.append(matched[1])
                    self._buffer = self._buffer[len(matched[0]):]
                    continue
                # 可能是还没收全的转义序列前缀，先等更多字节。
                if any(sequence.startswith(self._buffer) for sequence in _ESCAPE_SEQUENCES):
                    break
                self._buffer = self._buffer[1:]  # 未知转义序列：丢弃 ESC 继续
                continue

            byte = self._buffer[0]
            self._buffer = self._buffer[1:]
            if byte == 0x03:  # Ctrl-C
                events.append(EVENT_CTRL_C)
            elif byte == 0x04:  # Ctrl-D
                events.append(EVENT_CTRL_D)
            elif byte in (0x0A, 0x0D):  # 回车忽略
                continue
            elif byte in (0x7F, 0x08):  # 退格忽略
                continue
            else:
                try:
                    events.append(bytes([byte]).decode("utf-8"))
                except UnicodeDecodeError:
                    continue
        return events


class HoldState:
    """hold 语义的按键状态：记录每个键最近一次事件时间，超时自动失效。

    终端没有 key-up 事件；X11 自动重复是 press/release 成对事件。两种输入
    都把"最近一次事件"写进这里，超过 ``stale_timeout`` 没有新事件就认为
    松开了。纯 Python 实现，方便在无 ROS/X11 的单测里直接验证。
    """

    def __init__(self, stale_timeout: float = 0.4) -> None:
        if stale_timeout < 0.0:
            raise ValueError("stale_timeout 不能为负数（s）")
        self.stale_timeout = float(stale_timeout)
        self._pressed: dict[str, float] = {}

    @property
    def keys(self) -> tuple[str, ...]:
        """当前仍"按住"的键（按字典序，便于状态行稳定显示）。"""
        return tuple(sorted(self._pressed))

    def __bool__(self) -> bool:
        return bool(self._pressed)

    def press(self, key: str, now: float) -> None:
        """刷新按键：按下、自动重复、松开都调用它来续命。"""
        if key:
            self._pressed[key] = float(now)

    def release(self, key: str) -> None:
        """立即移除某个键（空格急停/专注模式切换时使用）。"""
        self._pressed.pop(key, None)

    def clear(self) -> None:
        """清空所有按键。"""
        self._pressed.clear()

    def prune(self, now: float) -> tuple[str, ...]:
        """清理超过 ``stale_timeout`` 未更新的按键，返回剩余按键。"""
        self._pressed = {
            key: stamp
            for key, stamp in self._pressed.items()
            if now - stamp <= self.stale_timeout
        }
        return self.keys


def classify_global_event(name: str, pressed: bool, ctrl: bool) -> str:
    """把 X11 全局抓取回调 ``(name, pressed, ctrl)`` 分类成主循环事件。

    * ``ctrl=True`` + ``c`` 按下 -> :data:`GLOBAL_EVENT_QUIT`（专注模式中 Ctrl-C 退出）；
    * ``ctrl=True`` 的其它键 -> :data:`GLOBAL_EVENT_IGNORE`（避免 Ctrl 组合误触发运动）；
    * ``k`` 按下 -> :data:`GLOBAL_EVENT_TOGGLE`（切换专注模式）；
    * 其余按下/松开 -> press/release（由节点复用 hold 逻辑处理）。
    """
    if ctrl:
        if pressed and isinstance(name, str) and name.lower() == "c":
            return GLOBAL_EVENT_QUIT
        return GLOBAL_EVENT_IGNORE
    if pressed and is_toggle_key(name):
        return GLOBAL_EVENT_TOGGLE
    return GLOBAL_EVENT_PRESS if pressed else GLOBAL_EVENT_RELEASE


class FocusModeController:
    """专注模式控制器：管理 X11 键盘抓取生命周期 + 线程安全事件队列。

    不直接依赖 ROS / X11：``grab_factory(on_key)`` 由测试注入假 grab，节点里
    注入 :class:`robot_control.focus_grab.X11KeyboardGrab`。全局按键回调只在
    后台线程执行，统一 ``put`` 进队列，主线程用 :meth:`poll` 消费。
    """

    def __init__(self, grab_factory, logger=None) -> None:
        self._grab_factory = grab_factory
        self._logger = logger or (lambda message: None)
        self._events: queue.Queue = queue.Queue()
        self._grab = None
        self._active = False
        self._last_message = ""

    # -- 状态 ----------------------------------------------------------
    @property
    def active(self) -> bool:
        """是否处于专注模式。"""
        return self._active

    @property
    def last_message(self) -> str:
        """最近一次开启/失败的中文说明。"""
        return self._last_message

    def pressed_keys(self):
        """查询当前物理按住的按键集合；不可用/假 grab 时返回 ``None``。

        专注模式下不依赖 X11 自动重复事件：主循环每个 tick 用物理键盘位图
        同步 hold 状态，物理按住就一直动，物理松开立即停。
        """
        if not self._active or self._grab is None:
            return None
        getter = getattr(self._grab, "pressed_keys", None)
        if getter is None:
            return None
        try:
            return getter()
        except Exception:
            return None

    @staticmethod
    def availability() -> tuple[bool, str]:
        """检查当前环境是否支持 X11 全局抓取（转调 focus_grab）。"""
        from robot_control.focus_grab import X11KeyboardGrab

        return X11KeyboardGrab.availability()

    # -- 抓取生命周期 --------------------------------------------------
    def _on_key(self, name: str, pressed: bool, ctrl: bool) -> None:
        """后台抓取线程回调：只投递，不碰任何运动状态。"""
        self._events.put((name, bool(pressed), bool(ctrl)))

    def _ensure_grab(self):
        if self._grab is None:
            self._grab = self._grab_factory(self._on_key)
        return self._grab

    def enable(self) -> tuple[bool, str]:
        """进入专注模式；返回 ``(是否成功, 中文说明)``，失败不抛异常。"""
        if self._active:
            return True, self._last_message or "已处于专注模式"
        try:
            grab = self._ensure_grab()
        except Exception as exc:  # 创建 grab 本身失败也要能继续普通遥控
            self._last_message = f"创建键盘抓取失败：{exc}"
            self._active = False
            return False, self._last_message
        ok, message = grab.start()
        self._last_message = str(message)
        self._active = bool(ok)
        if not self._active:
            self._discard_events()  # 启动失败时丢弃残留事件
        return self._active, self._last_message

    def disable(self) -> None:
        """退出专注模式并释放键盘（可重复调用，不抛异常）。"""
        grab = self._grab
        if grab is not None:
            try:
                grab.stop()
            except Exception as exc:
                self._logger(f"释放键盘时出错：{exc}")
        self._active = False
        self._last_message = "键盘已释放"
        self._discard_events()

    def toggle(self) -> tuple[bool, str]:
        """开/关专注模式；返回切换后的状态与消息。"""
        if self._active:
            self.disable()
            return False, self._last_message
        return self.enable()

    # -- 事件队列 ------------------------------------------------------
    def poll(self) -> list[tuple[str, bool, bool]]:
        """取出主循环待处理的全部全局按键事件（线程安全）。"""
        events: list[tuple[str, bool, bool]] = []
        while True:
            try:
                events.append(self._events.get_nowait())
            except queue.Empty:
                return events

    def _discard_events(self) -> None:
        self.poll()

    def stop(self) -> None:
        """退出路径统一调用：释放键盘并清空事件。"""
        if self._active or self._grab is not None:
            self.disable()


class TeleopKeyboard(Node):
    """终端键盘 -> /cmd_vel + /wheel_cmd（支持 K 键专注模式）。"""

    def __init__(self) -> None:
        super().__init__("teleop_keyboard")

        # ---------------- 参数（默认值见 INTERFACE.md） ----------------
        self.cmd_vel_topic = str(
            self.declare_parameter("cmd_vel_topic", "/cmd_vel").value
        )
        self.wheel_cmd_topic = str(
            self.declare_parameter("wheel_cmd_topic", "/wheel_cmd").value
        )
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
            self.declare_parameter("publish_rate", 20.0).value
        )
        self.stale_timeout = float(
            self.declare_parameter("stale_timeout", 0.4).value
        )
        # 启动后是否默认进入专注模式（终端 launch 参数 focus_mode 映射到这里）。
        self.focus_mode_default = bool(
            self.declare_parameter("focus_mode_default", True).value
        )

        # ---------------- 参数校验 ----------------
        if self.publish_rate <= 0.0:
            raise ValueError("publish_rate 必须为正数（Hz）")
        if self.stale_timeout < 0.0:
            raise ValueError("stale_timeout 不能为负数（s）")
        if self.linear_speed < 0.0 or self.lateral_speed < 0.0:
            raise ValueError("linear_speed / lateral_speed 不能为负数（m/s）")
        if self.angular_speed < 0.0:
            raise ValueError("angular_speed 不能为负数（rad/s）")
        if self.max_wheel_speed <= 0.0:
            raise ValueError("max_wheel_speed 必须为正数（rad/s）")

        # 轮子几何与 URDF 一致；遥控只关心"车体速度 -> 轮速"换算。
        self.kinematics = MecanumKinematics(max_wheel_speed=self.max_wheel_speed)

        # ---------------- ROS 接口 ----------------
        self._cmd_vel_pub = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self._wheel_cmd_pub = self.create_publisher(
            Float64MultiArray, self.wheel_cmd_topic, 10
        )

        # ---------------- 运行时状态 ----------------
        self._parser = KeyParser()
        self._hold = HoldState(self.stale_timeout)
        self._focus = FocusModeController(
            grab_factory=self._make_focus_grab,
            logger=self._log_focus_message,
        )
        self._running = True
        self._status_width = 0
        # 启动自动进入专注模式只尝试一次（按 K 退出后不得自动重进）。
        self._focus_auto_done = False

    # ------------------------------------------------------------------ #
    # 专注模式
    # ------------------------------------------------------------------ #
    def _make_focus_grab(self, on_key):
        """延迟创建 X11 抓取对象（导入 focus_grab 不影响普通遥控）。"""
        from robot_control.focus_grab import X11KeyboardGrab

        return X11KeyboardGrab(on_key, logger=self._log_focus_message)

    @staticmethod
    def _log_focus_message(message: str) -> None:
        # 抓取线程也可能调用，直接写 stderr，避免和 \r 状态行抢 stdout。
        print(f"[专注模式] {message}", file=sys.stderr, flush=True)

    def _toggle_focus_mode(self) -> None:
        """K 键切换专注模式；任何失败都只打印原因，不中断遥控。"""
        was_active = self._focus.active
        # 切换瞬间先清空旧按键并立即发零速，避免残留 motion。
        self._hold.clear()
        self._publish_body(BodyVelocity())
        ok, message = self._focus.toggle()
        self._print_line("")
        if ok:
            self._print_line(f"[专注模式] 已开启：{message}")
        elif was_active:
            self._print_line(f"[专注模式] 已退出：{message}")
        else:
            self._print_line(f"[专注模式] 无法开启：{message}")
        # 立即刷新一次状态行，让 [专注模式 开/关] 马上可见。
        self._print_status(BodyVelocity(), (0.0, 0.0, 0.0, 0.0))

    def _auto_enable_focus_mode(self) -> None:
        """节点就绪后按 ``focus_mode_default`` 自动进入专注模式（仅一次）。

        失败（无 DISPLAY / 键盘被占用）只打印中文原因，继续普通终端遥控，
        不抛异常；``_focus_auto_done`` 保证按 K 退出后不会被自动重进。
        """
        if self._focus_auto_done or not self.focus_mode_default:
            return
        self._focus_auto_done = True
        ok, message = self._focus.enable()
        self._print_line("")
        if ok:
            self._print_line(f"[专注模式] 已启动自动进入专注模式：{message}")
        else:
            self._print_line(
                f"[专注模式] 启动自动进入专注模式失败：{message}"
                "（继续普通终端遥控；可按 K 重试）"
            )
        # 让状态行立刻显示 [专注模式 开/关]。
        self._print_status(BodyVelocity(), (0.0, 0.0, 0.0, 0.0))

    # ------------------------------------------------------------------ #
    # 主循环
    # ------------------------------------------------------------------ #
    def run(self) -> int:
        """运行遥控循环，返回进程退出码（0 正常，1 终端不可用）。"""
        exit_code = 0
        self._print_help()
        try:
            with RawTerminal() as terminal:
                # 终端就绪后按 focus_mode_default 尝试默认进入专注模式（仅一次）。
                self._auto_enable_focus_mode()
                self._loop(terminal)
        except TerminalError as exc:
            self.get_logger().error(str(exc))
            exit_code = 1
        except (KeyboardInterrupt, ExternalShutdownException):
            exit_code = 0
        finally:
            # 退出路径统一释放专注模式键盘；再发布零速、恢复终端（with 已恢复）。
            try:
                self._focus.stop()
            except Exception as exc:  # 退出流程不再抛异常
                self.get_logger().warn(f"退出时释放键盘失败：{exc}")
            self._hold.clear()
            try:
                self._publish_body(BodyVelocity())
            except Exception:  # 外部已 shutdown context 时不再二次抛异常
                pass
            self._print_line("")
            self._print_line("已发布停车指令，teleop_keyboard 退出。")
        return exit_code

    def _loop(self, terminal: RawTerminal) -> None:
        period = 1.0 / self.publish_rate
        next_tick = time.monotonic()
        while self._running:
            now = time.monotonic()
            # 20ms 上限：保证专注模式的全局按键（含 K 切换）足够跟手。
            wait = min(period, 0.02, max(0.0, next_tick - now))
            events = self._parser.feed(terminal.read(wait))
            for event in events:
                self._handle_event(event)
                if not self._running:
                    break
            if not self._running:
                break

            # 消费后台抓取线程投递的全局按键（线程安全队列）。
            for name, pressed, ctrl in self._focus.poll():
                self._handle_global_event(name, pressed, ctrl)
                if not self._running:
                    break
            if not self._running:
                break
            # 专注模式：用 XQueryKeymap 物理状态精确同步长按（不依赖自动重复）。
            if self._focus.active:
                self._sync_global_hold()

            now = time.monotonic()
            if now >= next_tick:
                self._publish_hold(now)
                next_tick += period
                if next_tick < now:  # 落后太多时不补发，避免突发
                    next_tick = now + period
            # 该节点没有订阅，spin 只为保持 rclpy 执行器状态一致。
            rclpy.spin_once(self, timeout_sec=0.0)

    # ------------------------------------------------------------------ #
    # 按键处理
    # ------------------------------------------------------------------ #
    def _handle_event(self, event: str) -> None:
        """处理终端按键（也复用于全局按键的 press）。"""
        now = time.monotonic()
        if event in _QUIT_EVENTS:
            self._running = False
            return

        if is_toggle_key(event):
            self._toggle_focus_mode()
            return

        action = key_action(event)
        if action is None:
            return  # 未映射按键直接忽略

        if action == "stop":
            # 空格急停：立即清零并马上发布一次零速。
            self._hold.clear()
            body = BodyVelocity()
            wheels = self._publish_body(body)
            self._print_status(body, wheels)
            return

        # hold 语义：记录该键最近一次事件时间，过期由 _publish_hold 清理。
        self._hold.press(event, now)

    def _handle_global_event(self, name: str, pressed: bool, ctrl: bool) -> None:
        """处理来自专注模式全局抓取的按键事件（在主循环线程执行）。"""
        kind = classify_global_event(name, pressed, ctrl)
        if kind == GLOBAL_EVENT_QUIT:
            # 专注模式中的 Ctrl-C：优雅退出（恢复终端/零速/grab.stop 由 run 统一做）。
            self._handle_event(EVENT_CTRL_C)
            return
        if kind == GLOBAL_EVENT_TOGGLE:
            self._toggle_focus_mode()
            return
        if kind == GLOBAL_EVENT_IGNORE:
            return

        action = key_action(name)
        if action is None:
            return
        if action == "stop":
            # 空格只在按下时急停；松开事件不重新激活。
            if kind == GLOBAL_EVENT_PRESS:
                self._handle_event(name)
            return

        # X11 自动重复是 press/release 成对事件：按下与松开都刷新 hold，
        # 物理松开后 stale_timeout 内没有新事件才自动停车（与终端一致）。
        self._hold.press(name, time.monotonic())

    def _sync_global_hold(self) -> None:
        """专注模式下按物理键盘位图同步 hold 状态。

        终端/X11 自动重复可能不稳定，只靠事件续命会导致长按被 stale_timeout
        误停。这里以 X 服务器键盘位图为准：物理按住就一直动，物理松开立即停；
        空格仍然立即急停，K 由事件切换不参与同步。
        """
        pressed = self._focus.pressed_keys()
        if pressed is None:
            return
        now = time.monotonic()
        active: set[str] = set()
        for name in pressed:
            if not isinstance(name, str):
                continue
            if is_toggle_key(name):
                continue
            action = key_action(name)
            if action is None:
                continue
            if action == "stop":
                # 空格在物理按下期间始终急停（急停优先于其它方向键）。
                self._hold.clear()
                return
            active.add(name)
        for key in self._hold.keys:
            if key not in active:
                self._hold.release(key)
        for key in active:
            self._hold.press(key, now)

    def _publish_hold(self, now: float) -> None:
        """清理过期按键，按当前仍"按住"的键计算并发布速度。"""
        keys = self._hold.prune(now)
        body = keys_to_body(
            keys,
            max_linear=self.linear_speed,
            max_lateral=self.lateral_speed,
            max_angular=self.angular_speed,
        )
        wheels = self._publish_body(body)
        self._print_status(body, wheels)

    def _publish_body(self, body: BodyVelocity) -> tuple[float, float, float, float]:
        """发布车体速度与四轮速度（轮速按上限整体缩放）。"""
        # 按契约统一用 body_to_limited_wheels 计算四轮指令。
        wheels = self.kinematics.body_to_limited_wheels(
            body.vx,
            body.vy,
            body.wz,
            max_wheel_speed=self.max_wheel_speed,
        )
        # 再由限幅后的轮速反算"实际可行"的车体速度，保证两个话题一致。
        feasible = self.kinematics.wheels_to_body(wheels)

        twist = Twist()
        twist.linear.x = feasible.vx
        twist.linear.y = feasible.vy
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = feasible.wz
        self._cmd_vel_pub.publish(twist)

        wheel_msg = Float64MultiArray()
        wheel_msg.layout.dim = [
            MultiArrayDimension(
                label="wheel_fl, wheel_fr, wheel_rl, wheel_rr",
                size=4,
                stride=4,
            )
        ]
        wheel_msg.data = [float(value) for value in wheels]
        self._wheel_cmd_pub.publish(wheel_msg)
        return wheels

    # ------------------------------------------------------------------ #
    # 终端输出
    # ------------------------------------------------------------------ #
    def _print_help(self) -> None:
        self._print_line("=== Zhirong Cup 麦轮底盘 · 终端键盘遥控 ===")
        for action in _HELP_ACTIONS:
            hint = ACTION_KEY_HINTS.get(action, "")
            self._print_line(f"  {hint:<8s} -> {ACTION_LABELS.get(action, action)}")
        self._print_line(
            f"  {TOGGLE_KEY.upper():<8s} -> 专注模式（全局键盘，再按 {TOGGLE_KEY.upper()} 退出）"
        )
        self._print_line("  Ctrl-C / Ctrl-D -> 退出并停车")
        available, reason = self._focus.availability()
        if available:
            self._print_line(
                "  专注模式可用（X11）：进入后键盘被本程序独占，焦点在其它窗口也能遥控。"
            )
        else:
            self._print_line(
                f"  专注模式不可用：{reason}（按 {TOGGLE_KEY.upper()} 会提示原因，普通遥控不受影响）"
            )
        if self.focus_mode_default:
            self._print_line(
                "  默认: 启动后自动进入专注模式（关闭用 -p focus_mode_default:=false）。"
            )
        else:
            self._print_line(
                "  默认: 不自动进入专注模式，按 K 手动进入。"
            )
        self._print_line(
            f"参数: 线速度 {self.linear_speed:.2f} m/s, 横移 {self.lateral_speed:.2f} m/s, "
            f"角速度 {self.angular_speed:.2f} rad/s, 轮速上限 {self.max_wheel_speed:.1f} rad/s, "
            f"发布 {self.publish_rate:.1f} Hz"
        )
        self._print_line(
            f"hold 语义: 松开按键 {self.stale_timeout:.2f} s 后自动停车（空格立即停）。"
        )

    def _print_status(self, body: BodyVelocity, wheels) -> None:
        """用 ``\\r`` 单行刷新状态：专注模式 + 车体速度 + 四轮 rad/s + 按键。"""
        focus = "[专注模式 开]" if self._focus.active else "[专注模式 关]"
        keys = " ".join(self._hold.keys) or "无"
        line = (
            f"{focus} 车体 vx={body.vx:+.2f} vy={body.vy:+.2f} wz={body.wz:+.2f} m/s | "
            f"轮速 {format_wheels(wheels)} rad/s | 按键: {keys}"
        )
        # 某些 pty（如 openpty 未设置窗口大小）会返回 0 列，退化为 120 列。
        columns = shutil.get_terminal_size((120, 20)).columns
        if columns <= 1:
            columns = 120
        width = max(1, columns - 1)
        text = line[:width].ljust(min(self._status_width, width))
        print("\r" + text, end="", flush=True)
        self._status_width = max(self._status_width, len(line))

    @staticmethod
    def _print_line(text: str) -> None:
        print(text, flush=True)


def main(args=None) -> None:
    rclpy.init(args=args)
    node: TeleopKeyboard | None = None
    exit_code = 0
    try:
        node = TeleopKeyboard()
        exit_code = node.run()
    except KeyboardInterrupt:
        exit_code = 0
    except ValueError as exc:
        print(f"参数错误: {exc}", file=sys.stderr, flush=True)
        exit_code = 1
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    if exit_code != 0:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
