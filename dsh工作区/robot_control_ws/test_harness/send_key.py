#!/usr/bin/env python3
"""Focus a window by title and hold a key: send_key.py <title> <keysym> <seconds> [repeat_hz]"""
import sys
import time

from x11_util import (fake_key, find_window, focus_window, key_code, open_display)


def main() -> int:
    title, keysym = sys.argv[1], sys.argv[2]
    hold = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    repeat_hz = float(sys.argv[4]) if len(sys.argv) > 4 else 30.0
    dpy = open_display()
    win = find_window(dpy, title)
    if win is None:
        print(f"window containing {title!r} not found", file=sys.stderr)
        return 1
    focus_window(dpy, win)
    code = key_code(dpy, keysym)
    print(f"holding {keysym!r} (keycode {code}) on window {hex(win)} for {hold}s")
    fake_key(dpy, code, True)
    end = time.time() + hold
    period = 1.0 / repeat_hz if repeat_hz > 0 else 0.0
    while time.time() < end:
        if period:
            fake_key(dpy, code, True)  # emulate auto-repeat so "hold" works
            time.sleep(period)
        else:
            time.sleep(end - time.time())
    fake_key(dpy, code, False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
