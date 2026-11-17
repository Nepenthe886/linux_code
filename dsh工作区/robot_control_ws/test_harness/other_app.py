#!/usr/bin/env python3
"""Simple X11 window used as "another application" in focus-mode tests.

Usage: other_app.py <seconds> [title]
"""
import sys
import tkinter as tk

seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
title = sys.argv[2] if len(sys.argv) > 2 else "FocusTest-OtherApp"

root = tk.Tk()
root.title(title)
root.geometry("360x140+900+80")
tk.Label(
    root,
    text="另一个应用窗口\n（专注模式测试：按键不再送给它）",
    font=("Sans", 13),
    justify="center",
).pack(expand=True)
root.after(int(seconds * 1000), root.destroy)
root.mainloop()
