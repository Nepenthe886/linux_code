"""用 Tk event_generate 验证真实按键绑定链路（非 pytest 的 delivrable）。"""
import sys
import time

sys.path.insert(0, '/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws/src/robot_control')
import tkinter as tk

from robot_control.gui_teleop import TeleopPanel


class Sink:
    def __init__(self):
        self.calls = []

    def publish(self, body, wheels):
        self.calls.append((body, tuple(wheels)))

    @property
    def last(self):
        return self.calls[-1]


root = tk.Tk()
sink = Sink()
panel = TeleopPanel(root, sink)
panel.start()  # 启动 20Hz tick 循环
root.update()
root.focus_force()
root.update()
time.sleep(0.1)
root.update()

# 1) 真实 KeyPress 事件 -> 前进
root.event_generate('<KeyPress>', keysym='w')
root.update()
body = sink.last[0]
assert abs(body.vx - panel.linear_speed) < 1e-6, ('press w', body)
print('PRESS_W_OK', body)

# 2) 自动重复抖动（Release + Press）不应误停车
root.event_generate('<KeyRelease>', keysym='w')
root.update()
root.event_generate('<KeyPress>', keysym='w')
end = time.time() + 0.15
while time.time() < end:
    root.update()
    time.sleep(0.01)
body = sink.last[0]
assert body.vx > 0, ('auto repeat', body)
print('AUTO_REPEAT_OK', body)

# 3) 真正松开 -> 防抖宽限后零速
root.event_generate('<KeyRelease>', keysym='w')
end = time.time() + 0.3
while time.time() < end:
    root.update()
    time.sleep(0.01)
body = sink.last[0]
assert body.is_zero(), ('release', body)
print('RELEASE_OK', body)

# 4) 空格急停
root.event_generate('<KeyPress>', keysym='w')
root.update()
assert not sink.last[0].is_zero()
root.event_generate('<KeyPress>', keysym='space')
root.update()
assert sink.last[0].is_zero(), ('space', sink.last[0])
print('SPACE_STOP_OK', sink.last[0])

panel.close()
print('BINDING_CHECK_OK calls=', len(sink.calls))
