# -*- coding: utf-8 -*-
"""叠加校验图：把图 2 的红线 + 障碍轮廓按 Lead 映射仿射到世界坐标，
与 docs/plan.png 在同一画布、同一比例尺下半透明叠加，用于直观看出剩余偏差。

映射（Lead 提供）：x = (px - 507.5) * 0.0082645，y = (552.5 - py) * 0.0057143
实现方式：由于该映射对 px / py 都是线性的，直接把图 2 的 mask 以 imshow + extent
画到 plan 的 matplotlib 坐标轴上（与 make_plan.draw 共用同一 axes），因此不会出现
“plan.png 像素坐标反推”带来的错位。

输出：
  preview/scene/overlay_diff.png      （半透明叠加图，4200×4200）
  preview/scene/overlay_residuals.txt （各障碍中心 vs 图 2 像素映射的残差表）
用法：cd preview/scene && MPLCONFIGDIR=<ws>/.mplconfig python3 overlay_diff.py
"""

import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage

import make_plan
import scene_layout as L

WS = "/home/nepenthe/zmf/linux_code/dsh工作区"
HERE = os.path.join(WS, "preview/scene")
FIG2 = os.path.join(WS, "preview/docx_media/image2.png")
OUT_IMG = os.path.join(HERE, "overlay_diff.png")
OUT_TXT = os.path.join(HERE, "overlay_residuals.txt")


def figure2_layers():
    """返回 (红色线 RGBA, 障碍轮廓 RGBA, extent, 统计) —— 以世界坐标为 extent。"""
    im = np.array(Image.open(FIG2).convert("RGB")).astype(int)
    h, w, _ = im.shape
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    red = np.all(im == [240, 74, 74], axis=2)
    black = (r < 70) & (g < 70) & (b < 70)
    # 只保留“厚墙”连通域（去掉虚线网格/标注引线等小连通域）
    lab, n = ndimage.label(black, structure=np.ones((3, 3)))
    areas = ndimage.sum(black, lab, range(1, n + 1))
    keep = np.zeros(n + 1, dtype=bool)
    for i, a in enumerate(areas, start=1):
        keep[i] = a >= 250
    wall = keep[lab]

    x_left = (0 - L.PX_CX) * L.PX_SX
    x_right = (w - 1 - L.PX_CX) * L.PX_SX
    y_top = (L.PX_CY - 0) * L.PX_SY
    y_bottom = (L.PX_CY - (h - 1)) * L.PX_SY
    extent = (x_left, x_right, y_bottom, y_top)

    def rgba(mask, color, alpha):
        out = np.zeros((h, w, 4), dtype=np.float32)
        out[..., 0] = color[0] / 255.0
        out[..., 1] = color[1] / 255.0
        out[..., 2] = color[2] / 255.0
        out[..., 3] = mask.astype(np.float32) * alpha
        return out

    return (rgba(wall, (0, 0, 0), 0.45), rgba(red, (255, 20, 20), 0.65),
            extent, int(wall.sum()), int(red.sum()))


def overlay():
    wall_rgba, red_rgba, extent, n_wall, n_red = figure2_layers()

    def _overlay(ax):
        ax.imshow(wall_rgba, extent=extent, origin="upper",
                  interpolation="nearest", zorder=20)
        ax.imshow(red_rgba, extent=extent, origin="upper",
                  interpolation="nearest", zorder=21)
        ax.text(extent[0] + 0.05, extent[3] - 0.05,
                "叠加图层：图2 红线(红) + 障碍轮廓(黑)；半透明覆盖在 v3 布局上",
                fontsize=8, color="#7a0000", ha="left", va="top", zorder=22,
                bbox=dict(boxstyle="round,pad=0.25", fc="#fff6f0",
                          ec="#c98a8a", alpha=0.9))
        ax.text(extent[0] + 0.05, extent[3] - 0.32,
                "图2 px→世界：x=(px-507.5)*0.0082645, y=(552.5-py)*0.0057143；"
                "轮廓 %d px / 红线 %d px" % (n_wall, n_red),
                fontsize=7, color="#555555", ha="left", va="top", zorder=22)

    make_plan.draw(overlay=_overlay, out_path=OUT_IMG)
    print("overlay ->", OUT_IMG, "（4200x4200）")


def residuals():
    """各障碍世界中心 vs 图 2 像素映射中心的残差。"""
    rows = []
    for b in L.BLOCKS:
        if "px" not in b:
            continue
        fx, fy = L.px2world(*b["px"])
        x, y = L.world_xy(b)
        d = math.hypot(x - fx, y - fy)
        rows.append((b["name"], b.get("cell", ""), fx, fy, x, y, d, b.get("note", "")))
    rows.sort(key=lambda t: -t[6])
    lines = ["障碍中心残差（世界坐标 vs 图 2 像素映射；>0.15 m 为需说明项）",
             "%-22s %-7s %18s %18s %9s  %s" %
             ("name", "cell", "图2(px映射)", "当前v3", "残差(m)", "note")]
    for name, cell, fx, fy, x, y, d, note in rows:
        flag = "  <== >0.15" if d > 0.15 else ""
        lines.append("%-22s %-7s (%7.3f,%7.3f) (%7.3f,%7.3f) %8.3f%s  %s"
                     % (name, cell, fx, fy, x, y, d, flag, note))
    over = [r for r in rows if r[6] > 0.15]
    lines += ["", ">0.15 m 的项：%d 个" % len(over)]
    for name, cell, *_r in over:
        lines.append("  - %s (%s) 残差 %.3f m" % (name, cell, _r[-2]))
    lines += ["", "说明：",
              "  * wall_a_frame_041x027：为“避开出生点、防机器人出生碰撞”的安全偏移（任务书要求 y≥2.0）；",
              "  * wall_l_113_049：v3 按 Lead 指定中心 (1.28,1.46) 校正（图 2 像素映射为 1.128,1.397），",
              "    该墙跨 A3/A4 边界，视觉上仍压在图 2 红折线上。"]
    txt = "\n".join(lines)
    with open(OUT_TXT, "w") as fh:
        fh.write(txt + "\n")
    print(txt)
    print("\nresiduals ->", OUT_TXT)


if __name__ == "__main__":
    overlay()
    residuals()
