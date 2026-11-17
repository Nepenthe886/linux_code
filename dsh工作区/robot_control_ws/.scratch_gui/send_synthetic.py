"""向 X11 窗口发送一个“合成” KeyPress（XSendEvent，不改变服务器按键状态）。"""
import ctypes
import sys
import time

from ctypes import POINTER, c_int, c_long, c_uint, c_ulong, c_void_p, c_char_p

x11 = ctypes.CDLL("libX11.so.6")
x11.XOpenDisplay.restype = c_void_p
x11.XOpenDisplay.argtypes = [c_char_p]
x11.XDefaultRootWindow.restype = c_ulong
x11.XDefaultRootWindow.argtypes = [c_void_p]
x11.XStringToKeysym.restype = c_ulong
x11.XStringToKeysym.argtypes = [c_char_p]
x11.XKeysymToKeycode.restype = c_uint
x11.XKeysymToKeycode.argtypes = [c_void_p, c_ulong]
x11.XSendEvent.restype = c_int
x11.XSendEvent.argtypes = [c_void_p, c_ulong, c_int, c_long, c_void_p]
x11.XFlush.argtypes = [c_void_p]


class XKeyEvent(ctypes.Structure):
    _fields_ = [
        ("type", c_int),
        ("serial", c_ulong),
        ("send_event", c_int),
        ("display", c_void_p),
        ("window", c_ulong),
        ("root", c_ulong),
        ("subwindow", c_ulong),
        ("time", c_ulong),
        ("x", c_int),
        ("y", c_int),
        ("x_root", c_int),
        ("y_root", c_int),
        ("state", c_uint),
        ("keycode", c_uint),
        ("same_screen", c_int),
    ]


def send_keypress(display, window, keysym: str) -> None:
    root = x11.XDefaultRootWindow(display)
    keysym_value = x11.XStringToKeysym(keysym.encode())
    keycode = x11.XKeysymToKeycode(display, keysym_value)
    buffer = ctypes.create_string_buffer(192)  # sizeof(XEvent)
    event = ctypes.cast(buffer, POINTER(XKeyEvent)).contents
    event.type = 2  # KeyPress
    event.serial = 0
    event.send_event = 1
    event.display = display
    event.window = window
    event.root = root
    event.subwindow = 0
    event.time = 0
    event.x = 0
    event.y = 0
    event.x_root = 0
    event.y_root = 0
    event.state = 0
    event.keycode = keycode
    event.same_screen = 1
    x11.XSendEvent(display, window, 0, 1, ctypes.byref(event))  # KeyPressMask
    x11.XFlush(display)


if __name__ == "__main__":
    if sys.argv[1] == "probe":
        import tkinter as tk

        root = tk.Tk()
        root.title("synthetic-probe")
        root.geometry("300x120+800+400")
        seen = []
        root.bind_all("<KeyPress>", lambda e: seen.append(("press", e.keysym, e.send_event)))
        root.bind_all("<KeyRelease>", lambda e: seen.append(("release", e.keysym)))
        root.update()
        display = x11.XOpenDisplay(None)
        win = root.winfo_id()
        time.sleep(0.2)
        send_keypress(display, win, "Left")
        end = time.monotonic() + 0.5
        while time.monotonic() < end:
            root.update()
            time.sleep(0.01)
        print("SYNTHETIC_EVENTS", seen, flush=True)
        root.destroy()
    else:
        # 用法: send_synthetic.py <window-id-hex> <keysym>
        display = x11.XOpenDisplay(None)
        send_keypress(display, int(sys.argv[1], 16), sys.argv[2])
        print("SYNTHETIC_SENT", sys.argv[2], flush=True)
