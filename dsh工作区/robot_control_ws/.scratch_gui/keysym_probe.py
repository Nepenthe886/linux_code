"""诊断：XTest 注入的按键在 Tk 里实际产生什么 keysym / 是否自动重复。"""
import ctypes
import time

import tkinter as tk

events = []
root = tk.Tk()
root.title('keysym-probe')
tk.Label(root, text='probe', width=40, height=5).pack()
root.geometry('300x120+800+500')
root.update()
root.lift()
root.focus_force()
root.update()


def on_press(event):
    events.append(('press', event.keysym, round(time.monotonic(), 3)))


def on_release(event):
    events.append(('release', event.keysym, round(time.monotonic(), 3)))


root.bind('<KeyPress>', on_press)
root.bind('<KeyRelease>', on_release)

x11 = ctypes.CDLL('libX11.so.6')
xtst = ctypes.CDLL('libXtst.so.6')
x11.XOpenDisplay.restype = ctypes.c_void_p
x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
x11.XFlush.argtypes = [ctypes.c_void_p]
x11.XStringToKeysym.restype = ctypes.c_ulong
x11.XStringToKeysym.argtypes = [ctypes.c_char_p]
x11.XKeysymToKeycode.restype = ctypes.c_ubyte
x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
xtst.XTestFakeKeyEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]

display = x11.XOpenDisplay(None)
print('focus_get=', root.focus_get(), flush=True)
for keysym_name in ('w', 's'):
    keysym = x11.XStringToKeysym(keysym_name.encode())
    keycode = x11.XKeysymToKeycode(display, keysym)
    print('keysym', keysym_name, hex(keysym), '-> keycode', keycode, flush=True)
    xtst.XTestFakeKeyEvent(display, keycode, 1, 0)
    x11.XFlush(display)
    end = time.monotonic() + 1.2
    while time.monotonic() < end:
        root.update()
        time.sleep(0.01)
    xtst.XTestFakeKeyEvent(display, keycode, 0, 0)
    x11.XFlush(display)
    end = time.monotonic() + 0.2
    while time.monotonic() < end:
        root.update()
        time.sleep(0.01)

print('EVENTS:', events)
root.destroy()
