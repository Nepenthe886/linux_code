#!/usr/bin/env python3
"""Exercise robot_control.focus_grab against the real X display :1."""
import ctypes
import sys
import time
from ctypes import c_char_p, c_int, c_uint, c_ulong, c_void_p

from robot_control.focus_grab import X11KeyboardGrab, is_toggle_key, x11_available

x11 = ctypes.CDLL("libX11.so.6")
xtst = ctypes.CDLL("libXtst.so.6")
x11.XOpenDisplay.restype = c_void_p
x11.XOpenDisplay.argtypes = [c_char_p]
x11.XKeysymToKeycode.argtypes = [c_void_p, c_ulong]
x11.XKeysymToKeycode.restype = c_uint
x11.XStringToKeysym.restype = c_ulong
x11.XStringToKeysym.argtypes = [c_char_p]
xtst.XTestFakeKeyEvent.argtypes = [c_void_p, c_uint, c_int, c_ulong]
x11.XFlush.argtypes = [c_void_p]
x11.XCloseDisplay.argtypes = [c_void_p]

events = []

def on_key(name, pressed, ctrl):
    events.append((name, pressed, ctrl))

print("availability:", x11_available())
print("is_toggle_key('K') =", is_toggle_key("K"))

grab = X11KeyboardGrab(on_key, logger=print)
ok, msg = grab.start()
print("start:", ok, msg, "active=", grab.active)
time.sleep(0.2)

# 另一个 X 连接扮演“别的应用”，把焦点放到 root（完全不是我们的窗口）
sender = x11.XOpenDisplay(None)
for keysym_name in (b"k", b"w", b"a", b"Up", b" "):
    sym = x11.XStringToKeysym(keysym_name)
    code = x11.XKeysymToKeycode(sender, sym)
    xtst.XTestFakeKeyEvent(sender, code, 1, 0)
    x11.XFlush(sender)
    time.sleep(0.05)
    xtst.XTestFakeKeyEvent(sender, code, 0, 0)
    x11.XFlush(sender)
    time.sleep(0.05)
x11.XCloseDisplay(sender)
time.sleep(0.3)
print("events captured globally:", events)
grab.stop()
print("after stop active=", grab.active)

ok2, msg2 = grab.start()
print("restart:", ok2, msg2)
grab.stop()
print("OK" if events and not grab.active else "FAIL")
