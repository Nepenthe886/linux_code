#!/usr/bin/env python3
"""Focus an X11 window by title substring, or the root window: focus_window.py <title|@root>"""
import sys

from x11_util import find_window, focus_window, open_display

x11 = None
root = None


def main() -> int:
    target = sys.argv[1]
    dpy = open_display()
    if target == "@root":
        from x11_util import x11 as x11mod

        display_root = x11mod.XDefaultRootWindow(dpy)
        focus_window(dpy, display_root)
        print("focused root window")
        return 0
    win = find_window(dpy, target)
    if win is None:
        print(f"window {target!r} not found", file=sys.stderr)
        return 1
    focus_window(dpy, win)
    print(f"focused window {hex(win)} ({target!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
