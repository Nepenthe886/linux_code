#!/usr/bin/env python3
"""Exit 0 if a window with the given title substring exists (no focus change)."""
import sys

from x11_util import find_window, open_display

dpy = open_display()
win = find_window(dpy, sys.argv[1])
sys.exit(0 if win is not None else 1)
