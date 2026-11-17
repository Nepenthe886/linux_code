"""真实 X11 专注模式集成自检（不依赖窗口焦点）：程序化 enable -> XTest W -> 面板收到前进 -> 退出。"""
import sys
import time

sys.path.insert(0, '/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws/src/robot_control')
sys.path.insert(0, '/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws/test_harness')

import tkinter as tk

from robot_control.gui_teleop import FocusModeController, TeleopPanel
from x11_util import fake_key, key_code, open_display


class Sink:
    def __init__(self):
        self.calls = []

    def publish(self, body, wheels):
        self.calls.append((time.monotonic(), body, tuple(wheels)))

    @property
    def last(self):
        return self.calls[-1]


root = tk.Tk()
root.title("focus-grab-real-check")
root.geometry("300x100+900+300")
sink = Sink()
controller = FocusModeController(root)
panel = TeleopPanel(root, sink, on_toggle_focus=controller.toggle, on_close=controller.close)
controller.bind(panel)
panel.start()  # 启动 20 Hz 发布/刷新循环（松开防抖依赖它）
root.update()

display = open_display()
w = key_code(display, "w")
k = key_code(display, "k")


def pump(seconds):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        root.update()
        time.sleep(0.01)


events = []
_original_enqueue = controller.enqueue_global_key


def _recording_enqueue(name, pressed, ctrl=False):
    events.append((time.monotonic(), name, pressed))
    _original_enqueue(name, pressed, ctrl)


controller.enqueue_global_key = _recording_enqueue

assert controller.enable() is True, "专注模式 enable 失败（可能有其它程序占用键盘）"
pump(0.3)
print("ENABLE_OK active=", controller.active, flush=True)

fake_key(display, w, True)
for _ in range(10):
    fake_key(display, w, True)
    time.sleep(0.03)
pump(0.3)
forward = sink.last[1]
print("XTest W -> last body =", forward, flush=True)
assert forward.vx > 0, f"专注模式下 W 未驱动面板: {forward}"

release_at = time.monotonic()
fake_key(display, w, False)
pump(0.4)
print("release W -> last body =", sink.last[1], "pressed=", panel.pressed_keys, flush=True)
late_events = [ev for ev in events if ev[0] > release_at and ev[1] == "w" and ev[2]]
print("release 之后的 w KeyPress 事件数 =", len(late_events), late_events[:8], flush=True)
print("events tail:", [(round(ev[0]-release_at, 3), ev[1], ev[2]) for ev in events[-12:]], flush=True)
print("pending_release:", getattr(panel, "_pending_release", None), flush=True)
assert sink.last[1].is_zero(), f"松开后未回零: {sink.last[1]}"

fake_key(display, k, True)
fake_key(display, k, False)
pump(0.5)
print("XTest K -> active =", controller.active, "focus_mode =", panel.focus_mode, flush=True)
assert controller.active is False, "全局 K 未退出专注模式"

# 退出后（键盘抓取已释放）再注入 W 不应再驱动本面板
fake_key(display, w, True)
time.sleep(0.05)
fake_key(display, w, False)
pump(0.4)
print("focus off, XTest W -> last body =", sink.last[1], flush=True)
assert sink.last[1].is_zero(), "退出专注模式后仍收到全局按键"

controller.close()
root.destroy()
print("FOCUS_GRAB_REAL_CHECK_OK", flush=True)
