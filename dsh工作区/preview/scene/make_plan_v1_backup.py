# -*- coding: utf-8 -*-
"""绘制 zhirong_arena 俯视 2D 平面图（docs/plan.png，300 dpi），用于与规则图 2 校对。

用法：cd preview/scene && MPLCONFIGDIR=<ws>/.mplconfig python3 make_plan.py
"""

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrow, Polygon, Rectangle

import scene_layout as L

WS = "/home/nepenthe/zmf/linux_code/dsh工作区"
OUT = os.path.join(WS, "competition_ws/src/maps/zhirong_maps/docs/plan.png")

C = dict(
    ground="#dedbd5", asphalt="#8d8983", grid="#333333",
    yellow="#f7d117", orange="#f79217", red_zone="#b8261f",
    camo="#4d5a45", red_panel="#b02020", ramp="#e9a54a",
    boundary="#d21b1b", plate="#ffffff", text="#222222",
    spawn="#0f8f3f", ring="#15417a", dim="#1f4f8f",
)

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "Noto Sans CJK SC",
                                   "DejaVu Sans", "Droid Sans Fallback"]
plt.rcParams["axes.unicode_minus"] = False


def rot_rect(cx, cy, sx, sy, yaw=0.0):
    """返回旋转矩形的 4 个角点。"""
    c, s = math.cos(yaw), math.sin(yaw)
    pts = []
    for u, v in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2),
                 (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        pts.append((cx + u * c - v * s, cy + u * s + v * c))
    return pts


def add_rect(ax, cx, cy, sx, sy, yaw=0.0, **kw):
    ax.add_patch(Polygon(rot_rect(cx, cy, sx, sy, yaw), closed=True, **kw))


def draw():
    fig = plt.figure(figsize=(13.5, 13.5), dpi=300)
    ax = fig.add_axes([0.05, 0.06, 0.90, 0.86])
    ax.set_xlim(-4.75, 4.75)
    ax.set_ylim(-4.85, 4.75)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("#ffffff")

    # ---------------- 地面 / 场地 ----------------
    add_rect(ax, 0, 0, L.GROUND_SIZE, L.GROUND_SIZE, fc=C["ground"],
             ec="#9a958d", lw=1.2, zorder=0.5)
    ax.text(3.95, -3.95, "8 m × 8 m 承载地面（水泥）", fontsize=9, color="#6b665f",
            ha="right", va="bottom", zorder=1)
    add_rect(ax, 0, 0, L.FIELD_HALF * 2, L.FIELD_HALF * 2, fc=C["asphalt"],
             ec="#55524d", lw=1.4, zorder=1)

    # ---------------- 分区 ----------------
    for i, (cx, cy, sx, sy, z) in enumerate(L.YELLOW_BARS):
        add_rect(ax, L.YELLOW_CENTER[0] + cx, L.YELLOW_CENTER[1] + cy, sx, sy,
                 fc=C["yellow"], ec="none", alpha=0.95, zorder=2)
    for z_ in L.ORANGE_ZONES:
        ax.add_patch(Circle(z_["center"], z_["r"], fc=C["orange"], ec="none",
                            alpha=0.85, zorder=2))
    add_rect(ax, L.RED_ZONE["center"][0], L.RED_ZONE["center"][1],
             L.RED_ZONE["size"][0], L.RED_ZONE["size"][1],
             fc=C["red_zone"], ec="none", alpha=0.75, zorder=2)
    ax.text(L.YELLOW_CENTER[0], L.YELLOW_CENTER[1] + 0.05, "黄区",
            fontsize=17, color="#6d5a00", ha="center", va="center",
            fontweight="bold", zorder=3)
    ax.text(0.95, 0.35, "桔区\n斜坡1", fontsize=11, color="#7a4300",
            ha="center", va="center", fontweight="bold", zorder=3)
    ax.text(-0.35, -1.05, "桔区\n斜坡2", fontsize=11, color="#7a4300",
            ha="center", va="center", fontweight="bold", zorder=3)
    ax.text(L.RED_ZONE["center"][0], -2.40, "红区", fontsize=13, color="#fff0ee",
            ha="center", va="center", fontweight="bold", zorder=3)

    # ---------------- 单元格网格 + 编号 ----------------
    for g in L.GRID_LINES:
        (cx, cy), (sx, sy) = g["center"], g["size"]
        if sy < sx:     # 水平网格线
            ax.add_line(Line2D([cx - sx / 2, cx + sx / 2], [cy, cy],
                               color=C["grid"], lw=0.8, ls=(0, (6, 5)), zorder=3.2))
        else:           # 垂直网格线
            ax.add_line(Line2D([cx, cx], [cy - sy / 2, cy + sy / 2],
                               color=C["grid"], lw=0.8, ls=(0, (6, 5)), zorder=3.2))
    for row in range(4):
        for col in range(1, 5):
            x, y = L.cell_center(col, row)
            ax.text(x, y, L.cell_name(col, row), fontsize=13, color="#5a564f",
                    ha="center", va="center", alpha=0.85, zorder=3.4,
                    fontfamily="DejaVu Sans")

    # ---------------- 红色比赛边界（含入口/出口缺口） ----------------
    for seg in L.BOUNDARY_SEGMENTS:
        (cx, cy), (sx, sy) = seg["center"], seg["size"]
        add_rect(ax, cx, cy, sx, sy, fc=C["boundary"], ec="none", zorder=4.5)

    # ---------------- 斜坡 ----------------
    for r in L.RAMPS:
        if r["model"] == "ramp_single_120":
            sp = L.RAMP_SINGLE_SPEC
            add_rect(ax, r["x"], r["y"], sp["length"], sp["width"],
                     fc=C["ramp"], ec="#8a5a1c", lw=1.2, zorder=5)
            # 坡向箭头（+x 为高边）
            ax.add_patch(FancyArrow(r["x"] - 0.35, r["y"], 0.7, 0, width=0.02,
                                    head_width=0.10, head_length=0.14,
                                    color="#6b3f10", zorder=5.2))
            ax.text(r["x"], r["y"] + 0.72, "斜坡1 单面 1.2×1.2\n坡度≈9.5° 高边0.20m",
                    fontsize=8.5, color="#5b3a10", ha="center", va="bottom", zorder=6)
        else:
            sp = L.RAMP_DOUBLE_SPEC
            add_rect(ax, r["x"], r["y"], sp["length"], sp["width"],
                     fc=C["ramp"], ec="#8a5a1c", lw=1.2, zorder=5)
            ax.add_line(Line2D([r["x"], r["x"]], [r["y"] - 0.6, r["y"] + 0.6],
                               color="#6b3f10", lw=2.0, zorder=5.2))
            ax.text(r["x"], r["y"] - 0.72, "斜坡2 双面 2×(0.6×1.2)\nA 字 脊高0.20m",
                    fontsize=8.5, color="#5b3a10", ha="center", va="top", zorder=6)

    # ---------------- 围挡 / 障碍 ----------------
    for r in L.iter_wall_rects():
        fc = C["red_panel"] if r["material"] == "red" else C["camo"]
        add_rect(ax, r["center"][0], r["center"][1], r["size"][0], r["size"][1],
                 r["yaw"], fc=fc, ec="#15180f", lw=0.9, zorder=6)
    # 障碍标注（尺寸 + 名称）
    for w in L.WORLD_WALLS:
        spec = L.WALL_MODELS[w["model"]]
        cx = (L.wall_world_bbox(w["model"], w["x"], w["y"], w["yaw"])[0] +
              L.wall_world_bbox(w["model"], w["x"], w["y"], w["yaw"])[2]) / 2
        cy = (L.wall_world_bbox(w["model"], w["x"], w["y"], w["yaw"])[1] +
              L.wall_world_bbox(w["model"], w["x"], w["y"], w["yaw"])[3]) / 2
        a, b = spec["dims"]
        kind = "工型" if w["model"].startswith("i_") else (
            "红区围挡" if w["model"] == "red_barrier" else
            "薄墙" if w["model"].startswith("thin") else
            "A 字架" if w["model"].startswith("a_frame") else
            "L 型墙" if w["model"].startswith("l_wall") else "T 型墙")
        if w["model"] == "red_barrier":
            continue
        ax.text(cx, cy, "%s\n%.2f×%.2fm" % (kind, a, b), fontsize=6.8,
                color="#ffffff", ha="center", va="center", zorder=7,
                bbox=dict(boxstyle="round,pad=0.16", fc="#2c3526", ec="none",
                          alpha=0.72))

    # ---------------- 目标板 ----------------
    for t in L.TARGETS:
        p = L.TARGET_PLATE
        add_rect(ax, t["x"], t["y"], p["w"], p["h"], t["yaw"],
                 fc=C["plate"], ec="#333333", lw=0.8, zorder=7.5)
        kind = {"target_hostage": "身", "target_chest": "胸",
                "target_qr": "码"}[t["model"]]
        ax.text(t["x"], t["y"], kind, fontsize=7, color="#111111",
                ha="center", va="center", fontweight="bold", zorder=8)

    # ---------------- 圆环触碰点 ----------------
    for i, r in enumerate(L.TOUCH_RINGS, 1):
        ax.add_patch(Circle((r["x"], r["y"]), 0.118, fc="none", ec=C["ring"],
                            lw=1.6, zorder=8))
        ax.add_patch(Circle((r["x"], r["y"]), 0.042, fc="#000000", ec="none",
                            zorder=8.1))
        ax.text(r["x"], r["y"] + 0.20, "R%d" % i, fontsize=7.5, color=C["ring"],
                ha="center", va="bottom", fontweight="bold", zorder=8.2)

    # ---------------- 入口 / 出口 / 门柱 / 出生点 ----------------
    for g in L.GATE_POSTS:
        ax.add_patch(Rectangle((g["x"] - 0.035, g["y"] - 0.035), 0.07, 0.07,
                               fc="#c22", ec="none", zorder=9))
    # 入口箭头（东侧，指向场地内 -x）
    ax.add_patch(FancyArrow(3.55, 1.50, -0.55, 0, width=0.035, head_width=0.16,
                            head_length=0.16, color=C["spawn"], zorder=9))
    ax.text(3.62, 1.86, "入口（东侧偏北）\n缺口宽 0.80 m", fontsize=10.5,
            color=C["spawn"], ha="left", va="bottom", fontweight="bold", zorder=9)
    # 出口箭头（西侧，指向场地外 +x 反向）
    ax.add_patch(FancyArrow(-3.55, 0.0, 0.55, 0, width=0.035, head_width=0.16,
                            head_length=0.16, color="#c22", zorder=9))
    ax.text(-3.62, 0.34, "出口（西侧中部）\n缺口宽 0.80 m", fontsize=10.5,
            color="#c22", ha="right", va="bottom", fontweight="bold", zorder=9)
    # 标牌
    ax.text(2.86, 2.52, "IN\n入口牌", fontsize=8, color="#0a5c26", ha="center",
            va="bottom", fontweight="bold", zorder=9)
    ax.text(-2.86, 0.20, "OUT\n出口牌", fontsize=8, color="#8a1410", ha="center",
            va="bottom", fontweight="bold", zorder=9)
    # 出生点
    sx, sy = L.SPAWN["x"], L.SPAWN["y"]
    ax.add_patch(Circle((sx, sy), 0.36, fc="none", ec=C["spawn"], lw=2.0, zorder=9))
    ax.add_patch(Circle((sx, sy), 0.05, fc=C["spawn"], ec="none", zorder=9.2))
    ax.add_patch(FancyArrow(sx + 0.30, sy, -0.55, 0, width=0.03,
                            head_width=0.13, head_length=0.14,
                            color=C["spawn"], zorder=9.1))
    ax.text(sx + 0.10, sy - 0.52, "出生点 spawn\n(%.2f, %.2f) yaw=π\n朝向场地内(-x)"
            % (sx, sy), fontsize=9, color=C["spawn"], ha="center", va="top",
            fontweight="bold", zorder=9.3)

    # ---------------- 坐标系 / 尺寸标注 ----------------
    ax.add_patch(FancyArrow(0, 0, 1.0, 0, width=0.02, head_width=0.10,
                            head_length=0.14, color="#111111", zorder=10))
    ax.add_patch(FancyArrow(0, 0, 0, 1.0, width=0.02, head_width=0.10,
                            head_length=0.14, color="#111111", zorder=10))
    ax.text(1.02, -0.16, "+x 东（m）", fontsize=10, color="#111111", zorder=10)
    ax.text(0.12, 1.03, "+y 北（m）", fontsize=10, color="#111111", zorder=10)
    ax.text(-0.10, -0.16, "O", fontsize=11, color="#111111", ha="right", zorder=10)
    # 场地四角坐标
    for tx, ty, s in ((-2.5, 2.5, "(-2.5, +2.5)"), (2.5, 2.5, "(+2.5, +2.5)"),
                      (-2.5, -2.5, "(-2.5, -2.5)"), (2.5, -2.5, "(+2.5, -2.5)")):
        ax.text(tx, ty + (0.12 if ty > 0 else -0.12), s, fontsize=8,
                color="#6b665f", ha="center",
                va="bottom" if ty > 0 else "top", zorder=9)

    # 比例尺
    ax.add_line(Line2D([-4.35, -3.35], [-4.55, -4.55], color="#111111", lw=3))
    ax.text(-3.85, -4.45, "1 m", fontsize=9, ha="center", va="bottom")

    # ---------------- 图例 ----------------
    handles = [
        Rectangle((0, 0), 1, 1, fc=C["yellow"], ec="none", label="黄区（基础障碍/普通通道）"),
        Rectangle((0, 0), 1, 1, fc=C["orange"], ec="none", label="桔区（斜坡等轻度障碍）"),
        Rectangle((0, 0), 1, 1, fc=C["red_panel"], ec="none", label="红区（工型障碍）"),
        Rectangle((0, 0), 1, 1, fc=C["camo"], ec="#15180f", label="军绿迷彩围挡 h=0.55 m"),
        Rectangle((0, 0), 1, 1, fc=C["boundary"], ec="none", label="红色比赛边界线"),
        Line2D([0], [0], color=C["grid"], lw=0.8, ls=(0, (6, 5)), label="16 单元格网格线"),
        Circle((0, 0), 1, fc="none", ec=C["ring"], lw=1.6, label="圆环触碰点 ×5"),
        Rectangle((0, 0), 1, 1, fc=C["plate"], ec="#333", label="目标板（身/胸/码）×6"),
        Line2D([0], [0], marker="o", color=C["spawn"], lw=0, label="出生点/入口方向"),
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=8.5, framealpha=0.92,
              ncol=1, title="图例", title_fontsize=9.5,
              bbox_to_anchor=(0.005, 0.995))

    # ---------------- 标题 / 说明 ----------------
    fig.text(0.5, 0.965, "“戎智杯”反恐搜救赛项 —— 5 m × 5 m 比赛场地俯视布置图",
             fontsize=17, ha="center", va="center", fontweight="bold")
    fig.text(0.5, 0.935,
             "依据《3.反恐搜救赛项规则》图 2 复现（16 单元格 / 黄桔红三区 / 工 L T 型障碍 / "
             "斜坡1 斜坡2 / 入口 出口 / 出生点）",
             fontsize=9.5, ha="center", va="center", color="#444444")
    note = (
        "坐标约定：原点 = 场地中心，x 向东，y 向北，z 向上；单元格 4×4，每格 1.25 m，"
        "行 A(北)→D(南)、列 1(西)→4(东)。\n"
        "障碍尺寸取自图 2 标注（≈0.95×0.61 / 0.73×0.58 / 1.30×0.52 / 1.13×0.49 / "
        "1.12×0.60 / 1.14×0.48 / 1.43×0.57 / 薄墙 0.85×0.08 / 工型 0.89×0.49 m），"
        "墙高 0.55 m、厚 0.06 m；\n"
        "斜坡规格取自图 4（单面 1200×1200×19 / 双面 2×600×1200×19，三个支撑木块，"
        "坡度 ≈9.5°、高边/脊高 0.20 m）；目标物/圆环样式取自图 5、6、7、8。\n"
        "位置按图 2 红边界像素比例近似换算（±0.2 m）；图 2 为手绘示意图，障碍画得比实物大，"
        "实物尺寸以标注为准。"
    )
    fig.text(0.5, 0.022, note, fontsize=7.6, ha="center", va="bottom",
             color="#333333", linespacing=1.5,
             bbox=dict(boxstyle="round,pad=0.5", fc="#f4f2ee", ec="#c8c3ba"))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, dpi=300, facecolor="white")
    plt.close(fig)
    print("plan ->", OUT)


if __name__ == "__main__":
    draw()
