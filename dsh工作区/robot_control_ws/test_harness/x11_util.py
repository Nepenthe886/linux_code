"""Minimal X11 helpers via ctypes: find a window by title, focus it, fake keys."""
from __future__ import annotations

import ctypes
from ctypes import POINTER, byref, c_char_p, c_int, c_uint, c_ulong, c_void_p

x11 = ctypes.CDLL("libX11.so.6")
xtst = ctypes.CDLL("libXtst.so.6")

x11.XOpenDisplay.restype = c_void_p
x11.XOpenDisplay.argtypes = [c_char_p]
x11.XDefaultRootWindow.restype = c_ulong
x11.XDefaultRootWindow.argtypes = [c_void_p]
x11.XQueryTree.argtypes = [
    c_void_p, c_ulong, POINTER(c_ulong), POINTER(c_ulong),
    POINTER(POINTER(c_ulong)), POINTER(c_uint),
]
x11.XFetchName.argtypes = [c_void_p, c_ulong, POINTER(c_char_p)]
x11.XFree.argtypes = [c_void_p]
x11.XSetInputFocus.argtypes = [c_void_p, c_ulong, c_int, c_ulong]
x11.XRaiseWindow.argtypes = [c_void_p, c_ulong]
x11.XFlush.argtypes = [c_void_p]
x11.XStringToKeysym.restype = c_ulong
x11.XStringToKeysym.argtypes = [c_char_p]
x11.XKeysymToKeycode.restype = c_uint
x11.XKeysymToKeycode.argtypes = [c_void_p, c_ulong]
x11.XGetGeometry.argtypes = [
    c_void_p, c_ulong, POINTER(c_ulong), POINTER(c_int), POINTER(c_int),
    POINTER(c_uint), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint),
]
x11.XTranslateCoordinates.argtypes = [
    c_void_p, c_ulong, c_ulong, c_int, c_int,
    POINTER(c_int), POINTER(c_int), POINTER(c_ulong),
]
xtst.XTestFakeKeyEvent.argtypes = [c_void_p, c_uint, c_int, c_ulong]

RevertToParent = 2
CurrentTime = 0


def open_display():
    dpy = x11.XOpenDisplay(None)
    if not dpy:
        raise RuntimeError("cannot open DISPLAY")
    return dpy


def _window_name(dpy, win) -> str:
    name = c_char_p()
    if x11.XFetchName(dpy, win, byref(name)) and name.value:
        try:
            return name.value.decode("utf-8", "replace")
        finally:
            x11.XFree(name)
    return ""


def find_window(dpy, needle: str):
    """Breadth-first search for a mapped window whose title contains *needle*."""
    root = x11.XDefaultRootWindow(dpy)
    queue = [root]
    while queue:
        win = queue.pop(0)
        title = _window_name(dpy, win)
        if needle in title and win != root:
            return win
        r, p = c_ulong(), c_ulong()
        children = POINTER(c_ulong)()
        n = c_uint()
        if x11.XQueryTree(dpy, win, byref(r), byref(p), byref(children), byref(n)):
            for i in range(n.value):
                queue.append(children[i])
            if children:
                x11.XFree(children)
    return None


def focus_window(dpy, win) -> None:
    x11.XRaiseWindow(dpy, win)
    x11.XSetInputFocus(dpy, win, RevertToParent, CurrentTime)
    x11.XFlush(dpy)


def key_code(dpy, keysym: str) -> c_uint:
    sym = x11.XStringToKeysym(keysym.encode())
    code = x11.XKeysymToKeycode(dpy, sym)
    if code == 0:
        raise RuntimeError(f"no keycode for keysym {keysym!r}")
    return code


def fake_key(dpy, code: c_uint, pressed: bool) -> None:
    xtst.XTestFakeKeyEvent(dpy, code, 1 if pressed else 0, 0)
    x11.XFlush(dpy)


def window_geometry(dpy, win):
    root = x11.XDefaultRootWindow(dpy)
    g_root, x, y, w, h, bw, depth = (
        c_ulong(), c_int(), c_int(), c_uint(), c_uint(), c_uint(), c_uint(),
    )
    x11.XGetGeometry(dpy, win, byref(g_root), byref(x), byref(y), byref(w), byref(h),
                     byref(bw), byref(depth))
    rx, ry, child = c_int(), c_int(), c_ulong()
    x11.XTranslateCoordinates(dpy, win, root, 0, 0, byref(rx), byref(ry), byref(child))
    return rx.value, ry.value, w.value, h.value
