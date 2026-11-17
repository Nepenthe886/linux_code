#!/usr/bin/env python3
"""Raise an X11 window by title substring (does not change focus)."""
import sys

from x11_util import find_window, open_display

from x11_util import x11 as x11mod


def main() -> int:
    dpy = open_display()
    win = find_window(dpy, sys.argv[1])
    if win is None:
        print(f"window {sys.argv[1]!r} not found", file=sys.stderr)
        return 1
    x11mod.XRaiseWindow(dpy, win)
    x11mod.XFlush(dpy)
    print(f"raised {hex(win)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
