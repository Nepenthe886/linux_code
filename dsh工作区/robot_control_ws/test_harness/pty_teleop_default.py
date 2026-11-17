#!/usr/bin/env python3
"""Verify terminal teleop auto-enters focus mode at startup (K exits externally).

Usage: pty_teleop_default.py <state_file> <output_file>
"""
import os
import pty
import select
import subprocess
import sys
import time

state_file = sys.argv[1]
output_file = sys.argv[2]
master, slave = pty.openpty()
proc = subprocess.Popen(
    ["ros2", "run", "robot_control", "teleop_keyboard"],
    stdin=slave, stdout=slave, stderr=slave, close_fds=True, env=dict(os.environ),
)
os.close(slave)
buffer = bytearray()
start = time.time()


def write_state(tag: str) -> None:
    with open(state_file, "a", encoding="utf-8") as handle:
        handle.write(tag + "\n")


def pump() -> str:
    readable, _, _ = select.select([master], [], [], 0.05)
    if readable:
        try:
            chunk = os.read(master, 8192)
        except OSError:
            return ""
        if chunk:
            buffer.extend(chunk)
    return buffer.decode("utf-8", "replace")


phase = "wait_on"
sent_ctrl_c = False
while True:
    elapsed = time.time() - start
    text = pump()
    tail = text[-6000:]
    if phase == "wait_on":
        if "[专注模式 开]" in tail or "默认已进入专注模式" in tail:
            write_state("FOCUS_ON_AUTO")
            phase = "wait_off"
            off_started = time.time()
        elif elapsed > 12.0:
            write_state("FOCUS_ON_TIMEOUT")
            phase = "wait_exit"
            exit_started = time.time()
    elif phase == "wait_off":
        if "[专注模式 关]" in tail:
            write_state("FOCUS_OFF")
            phase = "wait_exit"
            exit_started = time.time()
        elif time.time() - off_started > 10.0:
            write_state("FOCUS_OFF_TIMEOUT")
            phase = "wait_exit"
            exit_started = time.time()
    elif phase == "wait_exit":
        if not sent_ctrl_c and time.time() - exit_started > 2.0:
            try:
                os.write(master, b"\x03")
            except OSError:
                pass
            sent_ctrl_c = True
            write_state("CTRL_C_SENT")
        if proc.poll() is not None:
            break
        if elapsed > 30.0:
            proc.terminate()
            break
    if proc.poll() is not None:
        break

try:
    code = proc.wait(timeout=5)
except subprocess.TimeoutExpired:
    proc.kill()
    code = proc.wait()
try:
    os.close(master)
except OSError:
    pass
text = buffer.decode("utf-8", "replace")
with open(output_file, "w", encoding="utf-8") as handle:
    handle.write(text)
write_state(f"EXIT {code}")
print(f"=== exit_code={code} ===")
sys.exit(0 if code == 0 else 1)
