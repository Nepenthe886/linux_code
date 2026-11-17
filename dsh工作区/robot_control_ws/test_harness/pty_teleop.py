#!/usr/bin/env python3
"""Drive `ros2 run robot_control teleop_keyboard` inside a pty and exercise focus mode.

Usage: pty_teleop.py <state_file> <output_file>

The script waits until the node is ready, presses 'k' to enter focus mode,
publishes FOCUS_ON in the state file, then waits for the node to leave focus
mode (external 'k' injected over X11), publishes FOCUS_OFF, and finally sends
Ctrl-C so the node exits gracefully (expected exit code 0).
"""
import os
import pty
import select
import subprocess
import sys
import time

state_file = sys.argv[1]
output_file = sys.argv[2]
total = 32.0

master, slave = pty.openpty()
env = dict(os.environ)
proc = subprocess.Popen(
    ["ros2", "run", "robot_control", "teleop_keyboard"],
    stdin=slave,
    stdout=slave,
    stderr=slave,
    close_fds=True,
    env=env,
)
os.close(slave)

buffer = bytearray()
start = time.time()

def write_state(tag: str) -> None:
    with open(state_file, "a", encoding="utf-8") as handle:
        handle.write(tag + "\n")

def send(data: bytes) -> None:
    try:
        os.write(master, data)
    except OSError:
        pass

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

phase = "wait_ready"
entered_at = None
sent_ctrl_c = False
exit_code = None

while True:
    elapsed = time.time() - start
    text = pump()
    tail = text[-4000:]

    if phase == "wait_ready" and ("键位" in tail or "专注模式" in tail or elapsed > 6.0):
        send(b"k")
        write_state("K_SENT")
        phase = "wait_on"
        phase_started = time.time()
    elif phase == "wait_on":
        if "专注模式 开" in tail:
            entered_at = time.time()
            write_state("FOCUS_ON")
            phase = "wait_off"
            phase_started = time.time()
        elif time.time() - phase_started > 4.0:
            write_state("FOCUS_ON_TIMEOUT")
            phase = "wait_exit"
    elif phase == "wait_off":
        if "[专注模式 关]" in tail:
            write_state("FOCUS_OFF")
            phase = "wait_exit"
            phase_started = time.time()
        elif time.time() - phase_started > 6.0:
            write_state("FOCUS_OFF_TIMEOUT")
            phase = "wait_exit"
            phase_started = time.time()
    elif phase == "wait_exit":
        if not sent_ctrl_c and (elapsed > 16.0 or (entered_at and time.time() - entered_at > 10.0)):
            send(b"\x03")
            sent_ctrl_c = True
            write_state("CTRL_C_SENT")
        if proc.poll() is not None:
            exit_code = proc.returncode
            break
        if elapsed > total:
            proc.terminate()
            break
    if proc.poll() is not None:
        exit_code = proc.returncode
        break

try:
    exit_code = proc.wait(timeout=5)
except subprocess.TimeoutExpired:
    proc.kill()
    exit_code = proc.wait()
try:
    os.close(master)
except OSError:
    pass

text = buffer.decode("utf-8", "replace")
with open(output_file, "w", encoding="utf-8") as handle:
    handle.write(text)
write_state(f"EXIT {exit_code}")
print(f"=== teleop_keyboard exit_code={exit_code} (output: {output_file}) ===")
print("\n".join(text.splitlines()[-8:]))
sys.exit(0 if exit_code == 0 else 1)
