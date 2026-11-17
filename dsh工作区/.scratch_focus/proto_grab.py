#!/usr/bin/env python3
"""Prototype: XGrabKeyboard via ctypes; verify keys are captured globally."""
import ctypes
import select
import sys
import time
from ctypes import POINTER, byref, c_char_p, c_int, c_uint, c_ulong, c_void_p

x11 = ctypes.CDLL("libX11.so.6")
xtst = ctypes.CDLL("libXtst.so.6")

x11.XOpenDisplay.restype = c_void_p
x11.XOpenDisplay.argtypes = [c_char_p]
x11.XDefaultRootWindow.restype = c_ulong
x11.XDefaultRootWindow.argtypes = [c_void_p]
x11.XGrabKeyboard.argtypes = [c_void_p, c_ulong, c_int, c_int, c_int, c_ulong]
x11.XGrabKeyboard.restype = c_int
x11.XUngrabKeyboard.argtypes = [c_void_p, c_ulong]
x11.XUngrabKeyboard.restype = c_int
x11.XNextEvent.argtypes = [c_void_p, c_void_p]
x11.XNextEvent.restype = c_int
x11.XPending.argtypes = [c_void_p]
x11.XPending.restype = c_int
x11.XConnectionNumber.argtypes = [c_void_p]
x11.XConnectionNumber.restype = c_int
x11.XSync.argtypes = [c_void_p, c_int]
x11.XkbKeycodeToKeysym.restype = c_ulong
x11.XkbKeycodeToKeysym.argtypes = [c_void_p, c_uint, c_int, c_int]
x11.XKeysymToString.restype = c_char_p
x11.XKeysymToString.argtypes = [c_ulong]
x11.XSetInputFocus.argtypes = [c_void_p, c_ulong, c_int, c_ulong]
x11.XFlush.argtypes = [c_void_p]
xtst.XTestFakeKeyEvent.argtypes = [c_void_p, c_uint, c_int, c_ulong]
x11.XKeysymToKeycode.argtypes = [c_void_p, c_ulong]
x11.XKeysymToKeycode.restype = c_uint

GrabModeAsync = 1
CurrentTime = 0


class XKeyEvent(ctypes.Structure):
    _fields_ = [
        ("type", c_int), ("serial", c_ulong), ("send_event", c_int),
        ("display", c_void_p), ("window", c_ulong), ("root", c_ulong),
        ("subwindow", c_ulong), ("time", c_ulong),
        ("x", c_int), ("y", c_int), ("x_root", c_int), ("y_root", c_int),
        ("state", c_uint), ("keycode", c_uint), ("same_screen", c_int),
    ]


def main():
    dpy = x11.XOpenDisplay(None)
    if not dpy:
        print("no display")
        return 1
    root = x11.XDefaultRootWindow(dpy)
    status = x11.XGrabKeyboard(dpy, root, 0, GrabModeAsync, GrabModeAsync, CurrentTime)
    print("XGrabKeyboard status =", status, "(0=Success,1=AlreadyGrabbed,2=InvalidTime,3=NotViewable,4=Frozen)")
    if status != 0:
        return 1
    x11.XSync(dpy, 0)

    # second connection acts as "some other application"
    sender = x11.XOpenDisplay(None)
    keysym = x11.XStringToKeysym(b"w")
    code = x11.XKeysymToKeycode(sender, keysym)
    print("sending w (keycode", code, ") while focused window is NOT ours")
    # move focus to root: our window isn't focused at all
    x11.XSetInputFocus(sender, root, 2, CurrentTime)
    x11.XFlush(sender)
    time.sleep(0.2)
    xtst.XTestFakeKeyEvent(sender, code, 1, 0)
    x11.XFlush(sender)
    time.sleep(0.2)
    xtst.XTestFakeKeyEvent(sender, code, 0, 0)
    x11.XFlush(sender)

    fd = x11.XConnectionNumber(dpy)
    deadline = time.time() + 3.0
    got = []
    buf = ctypes.create_string_buffer(192)
    while time.time() < deadline and len(got) < 2:
        r, _, _ = select.select([fd], [], [], 0.1)
        while x11.XPending(dpy):
            x11.XNextEvent(dpy, buf)
            ev = ctypes.cast(buf, POINTER(XKeyEvent)).contents
            if ev.type in (2, 3):
                sym = x11.XkbKeycodeToKeysym(dpy, ev.keycode, 0, 0)
                name = x11.XKeysymToString(sym)
                print("event type", ev.type, "keycode", ev.keycode, "keysym", hex(sym), name)
                got.append(ev.type)
    x11.XUngrabKeyboard(dpy, CurrentTime)
    x11.XSync(dpy, 0)
    x11.XCloseDisplay(sender)
    x11.XCloseDisplay(dpy)
    print("captured press+release:", got == [2, 3] or sorted(got) == [2, 3])
    return 0 if len(got) >= 2 else 1


if __name__ == "__main__":
    sys.exit(main())
