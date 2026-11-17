"""真实 X11 粘滞复现：release 后补一个迟到的合成 KeyPress，观察是否自动回零。

用法: python3 demo_sticky.py <window-id-hex>
"""
import sys
import time

sys.path.insert(0, '/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws/test_harness')
sys.path.insert(0, '/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws/.scratch_gui')

from send_synthetic import send_keypress  # noqa: E402
from x11_util import fake_key, focus_window, key_code, open_display  # noqa: E402

window = int(sys.argv[1], 16)
display = open_display()
focus_window(display, window)
time.sleep(0.2)

# 1) 正常按住 Left 0.5 s，然后松开（60 ms 防抖后应回零）
left = key_code(display, "Left")
fake_key(display, left, True)
end = time.monotonic() + 0.5
while time.monotonic() < end:
    fake_key(display, left, True)   # 模拟自动重复
    time.sleep(0.033)
fake_key(display, left, False)
print("released Left", flush=True)
time.sleep(0.25)

# 2) 模拟 X 服务器在 release 之后补送的迟到自动重复 KeyPress（不改变按键状态）
send_keypress(display, window, "Left")
print("sent late synthetic KeyPress Left", flush=True)
time.sleep(2.2)   # 观察是否 <=1.2 s 内自动回零

# 3) 恢复检查：再按 W 0.5 s 应能正常前进，松开回零
w = key_code(display, "w")
fake_key(display, w, True)
end = time.monotonic() + 0.5
while time.monotonic() < end:
    fake_key(display, w, True)
    time.sleep(0.033)
fake_key(display, w, False)
print("released W", flush=True)
time.sleep(1.0)
