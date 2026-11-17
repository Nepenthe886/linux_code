"""X11 全局键盘抓取：给「专注模式」提供跨窗口的按键输入。

背景
----
Tkinter / 终端节点的按键只会在窗口或终端拥有键盘焦点时到达。本模块用 X11
的主动键盘抓取（``XGrabKeyboard``）在专注模式下把整个键盘接管过来：按键事件
会直接送到本进程，与当前焦点在哪个窗口无关。按 ``k`` 可随时退出专注模式。

使用约束
--------
* 仅支持 **X11**（Xorg / XWayland 下的 X11 客户端）；纯 Wayland 桌面、无
  ``DISPLAY`` 的 SSH 会话里 ``availability()`` 会返回不可用及原因。
* 抓取期间键盘被本进程独占，其它程序的键盘输入会被吞掉，这是“专注模式”的
  本意；务必保证 ``k`` 退出键在抓取期间仍被处理（调用方负责）。
* 抓取由后台读线程持有；``on_key`` 回调在**后台线程**里执行，调用方必须自己
  把事件转投到 GUI/节点主线程（GUI 用 ``root.after``／队列，终端节点用队列）。

按键名约定
----------
``on_key`` 的 ``name`` 与 :mod:`robot_control.mecanum` 的键位表兼容：
``w``/``a``/``s``/``d``/``q``/``e``、``" "``（空格）、``Up``/``Down``/
``Left``/``Right``、``Escape`` 等；``pressed`` 为 True 表示按下；``ctrl``
表示同时按住了 Ctrl（供终端节点处理 Ctrl-C 退出）。
"""

from __future__ import annotations

import ctypes
import os
import select
import sys
import threading
import time
from ctypes import POINTER, byref, c_char_p, c_int, c_uint, c_ulong, c_void_p
from typing import Callable, Optional

__all__ = [
    "X11KeyboardGrab",
    "GrabError",
    "TOGGLE_KEY",
    "is_toggle_key",
    "x11_available",
]

#: 专注模式切换键（大小写均可）。
TOGGLE_KEY = "k"

#: X11 修饰键掩码。
_SHIFT_MASK = 0x0001
_CONTROL_MASK = 0x0004

#: 常用非 ASCII keysym -> 名字。
_KEYSYM_NAMES = {
    0xFF08: "BackSpace",
    0xFF09: "Tab",
    0xFF0D: "Return",
    0xFF1B: "Escape",
    0xFF51: "Left",
    0xFF52: "Up",
    0xFF53: "Right",
    0xFF54: "Down",
    0xFF55: "Prior",
    0xFF56: "Next",
    0xFF63: "Insert",
    0xFFFF: "Delete",
    0xFF50: "Home",
    0xFF57: "End",
}

#: XGrabKeyboard 返回值。
_GRAB_SUCCESS = 0
_GRAB_ALREADY_GRABBED = 1
_GRAB_NOT_VIEWABLE = 3
_GRAB_FROZEN = 4

_GRAB_MODE_ASYNC = 1
_CURRENT_TIME = 0


def is_toggle_key(name: str) -> bool:
    """判断按键名是否为专注模式切换键（``k``/``K``）。"""
    return isinstance(name, str) and name.lower() == TOGGLE_KEY


class GrabError(RuntimeError):
    """专注模式无法启动时抛出的异常。"""


# ---------------------------------------------------------------------- #
# ctypes 绑定（只在支持 X11 的系统上可用）
# ---------------------------------------------------------------------- #
_HAS_X11 = False
_x11 = None

try:  # pragma: no cover - 依赖运行平台
    _x11 = ctypes.CDLL("libX11.so.6")
    _x11.XOpenDisplay.restype = c_void_p
    _x11.XOpenDisplay.argtypes = [c_char_p]
    _x11.XCloseDisplay.argtypes = [c_void_p]
    _x11.XCloseDisplay.restype = c_int
    _x11.XDefaultRootWindow.restype = c_ulong
    _x11.XDefaultRootWindow.argtypes = [c_void_p]
    _x11.XGrabKeyboard.argtypes = [
        c_void_p, c_ulong, c_int, c_int, c_int, c_ulong
    ]
    _x11.XGrabKeyboard.restype = c_int
    _x11.XUngrabKeyboard.argtypes = [c_void_p, c_ulong]
    _x11.XUngrabKeyboard.restype = c_int
    _x11.XSync.argtypes = [c_void_p, c_int]
    _x11.XSync.restype = c_int
    _x11.XPending.argtypes = [c_void_p]
    _x11.XPending.restype = c_int
    _x11.XNextEvent.argtypes = [c_void_p, c_void_p]
    _x11.XNextEvent.restype = c_int
    _x11.XConnectionNumber.argtypes = [c_void_p]
    _x11.XConnectionNumber.restype = c_int
    _x11.XkbKeycodeToKeysym.restype = c_ulong
    _x11.XkbKeycodeToKeysym.argtypes = [c_void_p, c_uint, c_int, c_int]
    _x11.XStringToKeysym.restype = c_ulong
    _x11.XStringToKeysym.argtypes = [c_char_p]
    _x11.XKeysymToKeycode.restype = c_uint
    _x11.XKeysymToKeycode.argtypes = [c_void_p, c_ulong]
    _HAS_X11 = True
except (OSError, AttributeError):  # 非 X11 平台：模块仍可导入，但不可用
    _x11 = None


class _XKeyEvent(ctypes.Structure):
    """XKeyEvent（XEvent 联合体里键盘事件部分）的 ctypes 映射。

    实际事件缓冲区按 XEvent 的 192 字节读取，这里只声明需要解析的前缀字段。
    """

    _fields_ = [
        ("type", c_int),
        ("serial", c_ulong),
        ("send_event", c_int),
        ("display", c_void_p),
        ("window", c_ulong),
        ("root", c_ulong),
        ("subwindow", c_ulong),
        ("time", c_ulong),
        ("x", c_int),
        ("y", c_int),
        ("x_root", c_int),
        ("y_root", c_int),
        ("state", c_uint),
        ("keycode", c_uint),
        ("same_screen", c_int),
    ]


def x11_available() -> tuple[bool, str]:
    """检查当前环境是否可以用 X11 全局键盘抓取。"""
    if not _HAS_X11:
        return False, "未找到 libX11（专注模式仅支持 X11 桌面环境）"
    if not os.environ.get("DISPLAY"):
        return False, "没有 DISPLAY（SSH/无图形会话无法使用专注模式）"
    try:
        display = _x11.XOpenDisplay(None)
    except Exception as exc:  # pragma: no cover - 极端环境
        return False, f"打开 X 显示失败：{exc}"
    if not display:
        return False, f"无法连接 X 显示 DISPLAY={os.environ.get('DISPLAY')}"
    _x11.XCloseDisplay(display)
    return True, "X11 可用"


class X11KeyboardGrab:
    """专注模式的 X11 全局键盘抓取（后台读线程 + 主动键盘抓取）。

    参数
    ----
    on_key:
        按键回调 ``on_key(name, pressed, ctrl)``，在**后台线程**中执行，
        调用方负责线程间投递（队列 / ``after``）。
    logger:
        可选日志函数，接收一行中文消息（默认打印到 stderr）。
    """

    def __init__(
        self,
        on_key: Callable[[str, bool, bool], None],
        logger: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._on_key = on_key
        self._logger = logger or (lambda message: print(message, file=sys.stderr))
        self._display: Optional[int] = None
        self._root: int = 0
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._active = False
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # 状态
    # ------------------------------------------------------------------ #
    @property
    def active(self) -> bool:
        """是否正在抓取键盘（专注模式是否生效）。"""
        return self._active

    @staticmethod
    def availability() -> tuple[bool, str]:
        """静态检查当前环境是否支持专注模式。"""
        return x11_available()

    # ------------------------------------------------------------------ #
    # 启动 / 停止
    # ------------------------------------------------------------------ #
    def start(self) -> tuple[bool, str]:
        """尝试进入专注模式；返回 ``(是否成功, 中文说明)``。"""
        with self._lock:
            if self._active and self._thread is not None and self._thread.is_alive():
                return True, "已处于专注模式"
            ok, reason = x11_available()
            if not ok:
                return False, reason

            try:
                display = _x11.XOpenDisplay(None)
            except Exception as exc:  # pragma: no cover - 极端环境
                return False, f"打开 X 显示失败：{exc}"
            if not display:
                return False, f"无法连接 X 显示 DISPLAY={os.environ.get('DISPLAY')}"

            root = _x11.XDefaultRootWindow(display)
            status = _GRAB_FROZEN
            # 刚退出过专注模式时 grab 可能短暂 AlreadyGrabbed，重试一小会儿。
            for _ in range(25):
                status = _x11.XGrabKeyboard(
                    display,
                    root,
                    0,  # owner_events=False：所有按键都送给我们
                    _GRAB_MODE_ASYNC,
                    _GRAB_MODE_ASYNC,
                    _CURRENT_TIME,
                )
                if status == _GRAB_SUCCESS:
                    break
                time.sleep(0.02)
            if status != _GRAB_SUCCESS:
                _x11.XCloseDisplay(display)
                if status == _GRAB_ALREADY_GRABBED:
                    return False, "键盘已被其它程序独占（专注模式启动失败）"
                if status == _GRAB_NOT_VIEWABLE:
                    return False, "抓取窗口不可见（专注模式启动失败）"
                return False, f"XGrabKeyboard 失败（状态 {status}）"

            _x11.XSync(display, 0)
            self._display = display
            self._root = root
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._run,
                name="x11_focus_grab",
                daemon=True,
            )
            self._active = True
            self._thread.start()
            return True, "已进入专注模式：键盘被本程序接管，按 K 退出"

    def stop(self) -> None:
        """退出专注模式并释放键盘（可重复调用）。"""
        with self._lock:
            thread = self._thread
            self._thread = None
            if thread is None:
                self._active = False
                return
            self._stop_event.set()
        # 不持锁 join：读线程退出时会调用 _on_loop_exit，不要再抢同一把锁。
        thread.join(timeout=2.0)
        if thread.is_alive():  # pragma: no cover - 只有 X 连接卡死时才可能
            self._logger("警告：专注模式读线程未在 2s 内退出")
        self._active = False

    # ------------------------------------------------------------------ #
    # 后台读线程
    # ------------------------------------------------------------------ #
    def _run(self) -> None:  # pragma: no cover - 需要真实 X11 才能跑
        display = self._display
        if display is None:  # pragma: no cover
            return
        fd = _x11.XConnectionNumber(display)
        buffer = ctypes.create_string_buffer(192)  # sizeof(XEvent)
        try:
            while not self._stop_event.is_set():
                try:
                    readable, _, _ = select.select([fd], [], [], 0.05)
                except (OSError, ValueError):
                    break
                if not readable:
                    continue
                while _x11.XPending(display):
                    _x11.XNextEvent(display, ctypes.cast(buffer, c_void_p))
                    self._dispatch_event(buffer, display)
        finally:
            try:
                _x11.XUngrabKeyboard(display, _CURRENT_TIME)
                _x11.XSync(display, 0)
            except Exception:
                pass
            try:
                _x11.XCloseDisplay(display)
            except Exception:
                pass
            self._display = None
            self._active = False

    def _dispatch_event(self, buffer, display) -> None:  # pragma: no cover
        event = ctypes.cast(buffer, POINTER(_XKeyEvent)).contents
        if event.type not in (2, 3):  # KeyPress / KeyRelease
            return
        shifted = bool(event.state & _SHIFT_MASK)
        level = 1 if shifted else 0
        try:
            keysym = _x11.XkbKeycodeToKeysym(display, event.keycode, 0, level)
        except Exception:
            return
        name = _keysym_to_name(keysym)
        if name is None:
            return
        ctrl = bool(event.state & _CONTROL_MASK)
        try:
            self._on_key(name, event.type == 2, ctrl)
        except Exception:  # 回调异常不能打死抓取线程
            import traceback

            self._logger("警告：专注模式按键回调异常：")
            traceback.print_exc()


def _keysym_to_name(keysym: int) -> Optional[str]:
    """X11 keysym -> 与 ``mecanum.KEY_ALIASES`` 兼容的按键名。"""
    if keysym in _KEYSYM_NAMES:
        return _KEYSYM_NAMES[keysym]
    if keysym == 0x20:
        return " "
    if 0x21 <= keysym <= 0x7E:
        return chr(keysym)
    return None
