"""自检查：显示“前进+左平移+旋转”状态的界面，供外部进程截图（非交付文件）。"""
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
panel = TeleopPanel(
    root, sink,
    linear_speed=0.45,
    lateral_speed=0.45,
    angular_speed=1.5,
)
panel.start()
root.update()
root.lift()
root.focus_force()
# 自检专用：不让失焦保护干扰“模拟按住”的展示（真实窗口仍保留失焦停车）。
panel._check_focus_lost = lambda: None
panel.on_key_press('w')
panel.on_key_press('a')
panel.on_key_press('q')
panel.set_odom(0.42, 0.18, 0.35)  # 模拟收到 /odom
root.update()
print('DEMO body=', panel.last_body_velocity, 'wheels=', panel.last_wheel_speeds, flush=True)
end = time.time() + 8.0
while time.time() < end:
    root.update()
    time.sleep(0.02)
panel.close()
print('DEMO_DONE calls=', len(sink.calls))
