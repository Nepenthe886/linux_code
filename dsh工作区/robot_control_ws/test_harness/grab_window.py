#!/usr/bin/env python3
"""Grab the screen (optionally cropped to a window title) with PyQt5.

Usage: grab_window.py <out.png> [window-title]
"""
import sys

from PyQt5.QtWidgets import QApplication

from x11_util import find_window, open_display, window_geometry


def main() -> int:
    out = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    app = QApplication(sys.argv)  # noqa: F841  (needed for grabWindow)
    pixmap = QApplication.primaryScreen().grabWindow(0)
    box = None
    if title and pixmap.save("/dev/null", "PNG") is not None:
        import ctypes

        dpy = open_display()
        win = find_window(dpy, title)
        if win is not None:
            x, y, w, h = window_geometry(dpy, win)
            print(f"window {hex(win)} geometry {x},{y} {w}x{h}")
            box = (x, y, w, h)
        else:
            print(f"window {title!r} not found; full-screen grab", file=sys.stderr)
    if box:
        pixmap = pixmap.copy(*box)
    if not pixmap.save(out, "PNG"):
        print("failed to save screenshot", file=sys.stderr)
        return 1
    print(f"screenshot saved: {out} ({pixmap.width()}x{pixmap.height()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
