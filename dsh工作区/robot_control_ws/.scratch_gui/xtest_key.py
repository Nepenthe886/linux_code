"""用 XTest 往指定窗口注入按键（自检用，非交付文件）。

用法：
  python3 xtest_key.py focus 0x2c000b0
  python3 xtest_key.py press w
  python3 xtest_key.py release w
"""
import ctypes
import sys

x11 = ctypes.CDLL('libX11.so.6')
xtst = ctypes.CDLL('libXtst.so.6')

x11.XOpenDisplay.restype = ctypes.c_void_p
x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
x11.XFlush.argtypes = [ctypes.c_void_p]
x11.XStringToKeysym.restype = ctypes.c_ulong
x11.XStringToKeysym.argtypes = [ctypes.c_char_p]
x11.XKeysymToKeycode.restype = ctypes.c_ubyte
x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
x11.XRaiseWindow.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
x11.XSetInputFocus.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
xtst.XTestFakeKeyEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]

display = x11.XOpenDisplay(None)
if not display:
    raise SystemExit('无法打开 X display')

command = sys.argv[1]
if command == 'focus':
    window = int(sys.argv[2], 16)
    x11.XRaiseWindow(display, window)
    x11.XSetInputFocus(display, window, 2, 0)  # RevertToParent, CurrentTime
    x11.XFlush(display)
elif command in ('press', 'release'):
    keysym = x11.XStringToKeysym(sys.argv[2].encode('ascii'))
    keycode = x11.XKeysymToKeycode(display, keysym)
    xtst.XTestFakeKeyEvent(display, keycode, 1 if command == 'press' else 0, 0)
    x11.XFlush(display)
else:
    raise SystemExit(f'未知命令 {command}')
print('XTEST_OK', command, sys.argv[2:], flush=True)
