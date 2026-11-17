"""专注模式真实 X11 自检：K 进入 -> 焦点切到另一个 Tk 窗口 -> W 仍生效 -> K 退出 -> W 不再生效。"""
import ctypes
import sys
import time
import tkinter as tk
from ctypes import POINTER, c_int, c_ulong

WS = '/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws'
sys.path.insert(0, WS + '/test_harness')

from x11_util import fake_key, find_window, focus_window, key_code, open_display, x11  # noqa: E402

# 忽略脚本里 XSetInputFocus 的异步 BadMatch（自检脚本不因窗口属性失败而退出）
_ERROR_HANDLER = ctypes.CFUNCTYPE(c_int, ctypes.c_void_p, ctypes.c_void_p)


def _ignore_error(_display, _event):
    return 0


_error_handler = _ERROR_HANDLER(_ignore_error)
x11.XSetErrorHandler.restype = ctypes.c_void_p
x11.XSetErrorHandler.argtypes = [ctypes.c_void_p]
x11.XSetErrorHandler(_error_handler)

x11.XGetInputFocus.restype = None
x11.XGetInputFocus.argtypes = [ctypes.c_void_p, POINTER(c_ulong), POINTER(c_int)]

display = open_display()
gui = find_window(display, "麦伦机器人")
if gui is None:
    raise SystemExit("GUI 窗口未找到")
focus_window(display, gui)
time.sleep(0.4)

k = key_code(display, "k")
fake_key(display, k, True)
fake_key(display, k, False)
print("sent k -> enter focus mode", flush=True)
time.sleep(1.0)

# 另一个 Tk 窗口：用来把键盘焦点从 GUI 抢走
other = tk.Tk()
other.title("focus-steal-probe")
tk.Label(other, text="focus steal probe", width=30, height=4).pack()
other.geometry("260x120+40+520")
other.update()
other.lift()
other.focus_force()
other.update()
focus_window(display, other.winfo_id())
time.sleep(0.4)
focus_now = c_ulong()
revert = c_int()
x11.XGetInputFocus(display, ctypes.byref(focus_now), ctypes.byref(revert))
print(
    f"focused other window: gui={hex(gui)} other={hex(other.winfo_id())} "
    f"current_focus={hex(focus_now.value)}",
    flush=True,
)
time.sleep(0.3)

w = key_code(display, "w")


def hold_w(seconds: float) -> None:
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        fake_key(display, w, True)
        time.sleep(0.033)
    fake_key(display, w, False)


hold_w(0.7)
print("held w 0.7s (GUI 无焦点, 专注模式开 -> 应输出前进)", flush=True)
time.sleep(0.6)

fake_key(display, k, True)
fake_key(display, k, False)
print("sent k -> exit focus mode", flush=True)
time.sleep(0.9)

hold_w(0.7)
print("held w 0.7s (GUI 无焦点, 专注模式关 -> 应被忽略)", flush=True)
time.sleep(0.8)
other.destroy()
print("DEMO_DONE", flush=True)
