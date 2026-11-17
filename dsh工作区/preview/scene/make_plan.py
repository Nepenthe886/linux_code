# -*- coding: utf-8 -*-
"""绘制 zhirong_arena v2 俯视平面图（docs/plan.png，300 dpi），用于与规则图 2 逐块比对。

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
    ground="#dedbd5", floor="#8d8983", grid="#333333",
    yellow="#f7d117", orange="#f79217", red_zone="#b8261f",
    camo="#4d5a45", red_panel="#b02020", ramp="#e9a54a",
    boundary="#d21b1b", plate="#ffffff", spawn="#0f8f3f", ring="#15417a",
    gate="#c22", dim="#1f4f8f",
)

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "Noto Sans CJK SC",
                                   "DejaVu Sans", "Droid Sans Fallback"]
plt.rcParams["axes.unicode_minus"] = False


def rot_rect(cx, cy, sx, sy, yaw=0.0):
    c, s = math.cos(yaw), math.sin(yaw)
    return [(cx + u * c - v * s, cy + u * s + v * c)
            for u, v in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2),
                         (sx / 2, sy / 2), (-sx / 2, sy / 2))]


def add_rect(ax, cx, cy, sx, sy, yaw=0.0, **kw):
    ax.add_patch(Polygon(rot_rect(cx, cy, sx, sy, yaw), closed=True, **kw))


KIND = {
    "l_wall": "L 型墙", "wall_z": "Z 型墙", "t_wall": "T 型墙",
    "thin_wall": "薄墙", "horiz_wall": "背景墙", "a_frame": "A 字架",
    "i_obstacle": "工型障碍", "red_barrier": "红区围挡",
    "ramp_single": "斜坡1", "ramp_double": "斜坡2",
}


def kind_of(model):
    for k, v in KIND.items():
        if model.startswith(k):
            return v
    return model


def draw(overlay=None, out_path=None):
    """绘制 plan；overlay(ax) 可在保存前追加半透明图层（供 overlay_diff.py 使用）。"""
    fig = plt.figure(figsize=(14.0, 14.0), dpi=300)
    ax = fig.add_axes([0.045, 0.055, 0.91, 0.865])
    ax.set_xlim(-4.75, 4.75)
    ax.set_ylim(-4.85, 4.75)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("#ffffff")

    # ---------------- 地面 / 场地铺装 ----------------
    add_rect(ax, 0, 0, L.GROUND_SIZE, L.GROUND_SIZE, fc=C["ground"],
             ec="#9a958d", lw=1.2, zorder=0.5)
    ax.text(3.95, -3.95, "8 m × 8 m 承载地面（水泥）", fontsize=9,
            color="#6b665f", ha="right", va="bottom", zorder=1)
    add_rect(ax, L.FLOOR_CENTER[0], L.FLOOR_CENTER[1], L.FLOOR_SIZE,
             L.FLOOR_SIZE, fc=C["floor"], ec="#55524d", lw=1.2, zorder=1)

    # ---------------- 分区 ----------------
    for i, (x0, y0, x1, y1) in enumerate(L.YELLOW_ZONES):
        add_rect(ax, (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0,
                 fc=C["yellow"], ec="none", alpha=0.95, zorder=2)
    for b in L.BLOCKS:
        if b["model"] == "ramp_single_120":
            x, y = L.world_xy(b)
            ax.add_patch(Circle((x, y), L.ZONE_ORANGE_SPEC["ramp1_r"],
                                fc=C["orange"], ec="none", alpha=0.85, zorder=2))
        if b["model"] == "ramp_double_120":
            x, y = L.world_xy(b)
            ax.add_patch(Circle((x, y), L.ZONE_ORANGE_SPEC["ramp2_r"],
                                fc=C["orange"], ec="none", alpha=0.85, zorder=2))
    rz = L.RED_ZONE
    add_rect(ax, rz["center"][0], rz["center"][1], rz["size"][0], rz["size"][1],
             fc=C["red_zone"], ec="none", alpha=0.75, zorder=2)
    ax.text(-1.62, 1.15, "黄区", fontsize=16, color="#6d5a00", ha="center",
            va="center", fontweight="bold", zorder=3)
    ax.text(0.938, 0.254, "桔区\n斜坡1", fontsize=10.5, color="#7a4300",
            ha="center", va="center", fontweight="bold", zorder=3)
    ax.text(-0.53, -1.20, "桔区\n斜坡2", fontsize=10.5, color="#7a4300",
            ha="center", va="center", fontweight="bold", zorder=3)
    ax.text(rz["center"][0], -2.44, "红区", fontsize=12, color="#fff0ee",
            ha="center", va="center", fontweight="bold", zorder=3)

    # ---------------- 16 单元格网格 + 编号 ----------------
    for c in (-L.CELL, 0.0, L.CELL):
        ax.add_line(Line2D([c, c], [-L.FIELD_HALF, L.FIELD_HALF],
                           color=C["grid"], lw=0.9, ls=(0, (7, 4)), zorder=3.2))
        ax.add_line(Line2D([-L.FIELD_HALF, L.FIELD_HALF], [c, c],
                           color=C["grid"], lw=0.9, ls=(0, (7, 4)), zorder=3.2))
    for name, (x, y) in L.CELLS.items():
        ax.text(x, y, name, fontsize=14, color="#4a463f", ha="center",
                va="center", alpha=0.75, zorder=3.4, fontfamily="DejaVu Sans")
    for tx, ty, s in ((-2.5, 2.5, "(-2.5, +2.5)"), (2.5, 2.5, "(+2.5, +2.5)"),
                      (-2.5, -2.5, "(-2.5, -2.5)"), (2.5, -2.5, "(+2.5, -2.5)")):
        ax.text(tx, ty + (0.12 if ty > 0 else -0.12), s, fontsize=7.5,
                color="#6b665f", ha="center",
                va="bottom" if ty > 0 else "top", zorder=9)

    # ---------------- 红色比赛边界（图 2 不规则折线） ----------------
    for chain in L.boundary_world_chains():
        xs = [p[0] for p in chain]
        ys = [p[1] for p in chain]
        ax.add_line(Line2D(xs, ys, color=C["boundary"], lw=3.2,
                           solid_joinstyle="miter", zorder=4.5))
    spur = L.boundary_world_spur()
    ax.add_line(Line2D([p[0] for p in spur], [p[1] for p in spur],
                       color=C["boundary"], lw=2.2, ls=(0, (4, 2)), zorder=4.4))

    # ---------------- 斜坡 ----------------
    for b in L.BLOCKS:
        if b["model"] == "ramp_single_120":
            sp = L.RAMP_SINGLE_SPEC
            x, y = L.world_xy(b)
            add_rect(ax, x, y, sp["length"], sp["width"], fc=C["ramp"],
                     ec="#8a5a1c", lw=1.2, zorder=5)
            ax.add_patch(FancyArrow(x - 0.40, y, 0.80, 0, width=0.025,
                                    head_width=0.11, head_length=0.15,
                                    color="#6b3f10", zorder=5.2))
            ax.text(x - 0.02, y + 0.68, "斜坡1 单面 1.1×1.0 坡向+x",
                    fontsize=7.6, color="#5b3a10", ha="center", va="bottom",
                    zorder=6)
        if b["model"] == "ramp_double_120":
            sp = L.RAMP_DOUBLE_SPEC
            x, y = L.world_xy(b)
            add_rect(ax, x, y, sp["length"], sp["width"], fc=C["ramp"],
                     ec="#8a5a1c", lw=1.2, zorder=5)
            ax.add_line(Line2D([x, x], [y - 0.6, y + 0.6], color="#6b3f10",
                               lw=2.2, zorder=5.2))
            ax.text(-1.30, -0.72, "斜坡2 双面 Λ\n(1.0×1.0, 脊高0.18)",
                    fontsize=7.6, color="#5b3a10", ha="center", va="center",
                    zorder=6,
                    bbox=dict(boxstyle="round,pad=0.2", fc="#fde9c8",
                              ec="#c98a2a", alpha=0.9))

    # ---------------- 墙体 / 障碍 ----------------
    for inst in L.instances():
        spec = L.WALL_MODELS.get(inst["model"])
        if spec is None:
            continue
        fc = C["red_panel"] if spec["material"] == "red" else C["camo"]
        for panel in spec["panels"]:
            r = L.panel_world_rect(inst, panel)
            add_rect(ax, r["center"][0], r["center"][1], r["size"][0],
                     r["size"][1], r["yaw"], fc=fc, ec="#15180f", lw=0.9,
                     zorder=6)

    # 障碍标注（名称 + 标注尺寸），贴 bbox 中心
    for inst in L.instances():
        spec = L.WALL_MODELS.get(inst["model"])
        if spec is None:
            continue
        b = L.instance_bbox(inst)
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        a, bb = spec["dims"]
        kind = kind_of(inst["model"])
        if inst["model"] == "red_barrier":
            continue
        if inst["model"].startswith("i_obstacle"):
            label = "%s\n%.2f×%.2fm" % (kind, a, bb)
        else:
            label = "%s %.2f×%.2f" % (kind, a, bb)
        ax.text(cx, cy, label, fontsize=6.2, color="#ffffff", ha="center",
                va="center", zorder=7,
                bbox=dict(boxstyle="round,pad=0.16", fc="#2c3526", ec="none",
                          alpha=0.75))

    # ---------------- 目标板（自动贴墙） ----------------
    for t in L.TARGETS:
        x, y, z, yaw = L.attach_pose(t["wall"], t["panel"], t["face"],
                                     t["along"], t["z"], L.TARGET_PLATE["offset"])
        p = L.TARGET_PLATE
        add_rect(ax, x, y, p["w"], p["h"], yaw, fc=C["plate"], ec="#333333",
                 lw=0.8, zorder=7.5)
        ch = {"target_hostage": "身", "target_chest": "胸", "target_qr": "码"}[t["model"]]
        ax.text(x, y, ch, fontsize=7, color="#111111", ha="center", va="center",
                fontweight="bold", zorder=8)

    # ---------------- 圆环触碰点（自动贴墙） ----------------
    for i, r in enumerate(L.TOUCH_RINGS, 1):
        x, y, z, yaw = L.attach_pose(r["wall"], r["panel"], r["face"],
                                     r["along"], r["z"], L.RING_SPEC["offset"])
        ax.add_patch(Circle((x, y), L.RING_SPEC["outer_r"], fc="none",
                            ec=C["ring"], lw=1.6, zorder=8))
        ax.add_patch(Circle((x, y), L.RING_SPEC["center_r"], fc="#000000",
                            ec="none", zorder=8.1))
        ax.text(x, y + 0.20, "R%d" % i, fontsize=7.5, color=C["ring"],
                ha="center", va="bottom", fontweight="bold", zorder=8.2)

    # ---------------- 入口 / 出口 / 门柱 / 出生点 ----------------
    e1, e2, x1, x2 = L.boundary_gap_points()
    for g in L.GATE_POSTS:
        ax.add_patch(Rectangle((g["pos"][0] - 0.035, g["pos"][1] - 0.035),
                               0.07, 0.07, fc=C["gate"], ec="none", zorder=9))
    # 入口：门洞在 (e1,e2) 之间，箭头从场地外指向门洞
    ex, ey = (e1[0] + e2[0]) / 2, (e1[1] + e2[1]) / 2
    ax.add_patch(FancyArrow(1.55, 2.80, -0.98, -0.55, width=0.03,
                            head_width=0.15, head_length=0.17,
                            color=C["spawn"], zorder=9))
    ax.text(1.55, 2.86, "入口（东北角门洞）缺口 0.80 m", fontsize=9.5,
            color=C["spawn"], ha="center", va="bottom", fontweight="bold", zorder=9)
    # 出口
    xx, xy = (x1[0] + x2[0]) / 2, (x1[1] + x2[1]) / 2
    ax.add_patch(FancyArrow(xx - 0.62, xy, 0.42, 0, width=0.03,
                            head_width=0.15, head_length=0.17,
                            color=C["boundary"], zorder=9))
    ax.text(xx - 0.72, xy, "出口（西侧中部）\n缺口 0.80 m", fontsize=9.5,
            color=C["boundary"], ha="right", va="center", fontweight="bold",
            zorder=9)
    # 标牌（位置点 + 文字）
    for sgn, col, txt, tx, ty in (
            (L.SIGNS[0], "#0a5c26", "入口牌 IN", 1.55, 2.10),
            (L.SIGNS[1], "#8a1410", "出口牌 OUT", -3.15, 0.30)):
        sx_, sy_ = sgn["pos"]
        ax.add_patch(Circle((sx_, sy_), 0.045, fc=col, ec="none", zorder=9))
        ax.add_line(Line2D([sx_, tx], [sy_, ty], color=col, lw=0.9, zorder=9))
        ax.text(tx, ty, txt, fontsize=8, color=col,
                ha="left" if tx > sx_ else "center", va="center",
                fontweight="bold", zorder=9)
    # 出生点
    sx, sy = L.SPAWN["x"], L.SPAWN["y"]
    ax.add_patch(Circle((sx, sy), 0.36, fc="none", ec=C["spawn"], lw=2.0,
                        zorder=9))
    ax.add_patch(Circle((sx, sy), 0.05, fc=C["spawn"], ec="none", zorder=9.2))
    ax.add_patch(FancyArrow(sx + 0.30, sy, -0.55, 0, width=0.03,
                            head_width=0.13, head_length=0.14,
                            color=C["spawn"], zorder=9.1))
    ax.text(sx + 0.05, sy - 0.50, "出生点 spawn\n(%.2f, %.2f) yaw=π"
            % (sx, sy), fontsize=9, color=C["spawn"], ha="center", va="top",
            fontweight="bold", zorder=9.3)

    # ---------------- 坐标系 / 比例尺 ----------------
    ax.add_patch(FancyArrow(0, 0, 1.0, 0, width=0.02, head_width=0.10,
                            head_length=0.14, color="#111111", zorder=10))
    ax.add_patch(FancyArrow(0, 0, 0, 1.0, width=0.02, head_width=0.10,
                            head_length=0.14, color="#111111", zorder=10))
    ax.text(1.02, -0.16, "+x 东（m）", fontsize=10, color="#111111", zorder=10)
    ax.text(0.12, 1.03, "+y 北（m）", fontsize=10, color="#111111", zorder=10)
    ax.text(-0.10, -0.16, "O", fontsize=11, color="#111111", ha="right",
            zorder=10)
    ax.add_line(Line2D([-4.35, -3.35], [-4.55, -4.55], color="#111111", lw=3))
    ax.text(-3.85, -4.45, "1 m", fontsize=9, ha="center", va="bottom")
    ax.text(3.95, 3.95, "图 2 方向：+x 东（右）/ +y 北（上）", fontsize=8,
            color="#6b665f", ha="right", va="top", zorder=9)

    # ---------------- 图例 ----------------
    handles = [
        Rectangle((0, 0), 1, 1, fc=C["yellow"], ec="none", label="黄区（图 2 黄色填充）"),
        Rectangle((0, 0), 1, 1, fc=C["orange"], ec="none", label="桔区（斜坡处橙椭圆）"),
        Rectangle((0, 0), 1, 1, fc=C["red_panel"], ec="none", label="红区（工型障碍+红块）"),
        Rectangle((0, 0), 1, 1, fc=C["camo"], ec="#15180f", label="军绿迷彩围挡 h=0.55 m"),
        Line2D([0], [0], color=C["boundary"], lw=3.2, label="红色比赛边界（图 2 折线）"),
        Line2D([0], [0], color=C["grid"], lw=0.9, ls=(0, (7, 4)), label="16 单元格网格（1.25 m）"),
        Circle((0, 0), 1, fc="none", ec=C["ring"], lw=1.6, label="圆环触碰点 ×5"),
        Rectangle((0, 0), 1, 1, fc=C["plate"], ec="#333", label="目标板（身/胸/码）×6"),
        Line2D([0], [0], marker="o", color=C["spawn"], lw=0, label="出生点 / 入口方向"),
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=8.3, framealpha=0.93,
              ncol=1, title="图例", title_fontsize=9.5,
              bbox_to_anchor=(0.005, 0.995))

    # ---------------- 标题 / 说明 ----------------
    fig.text(0.5, 0.968,
             "“戎智杯”反恐搜救赛项 —— 5 m × 5 m 比赛场地方案（v3 微调）",
             fontsize=17, ha="center", va="center", fontweight="bold")
    fig.text(0.5, 0.941,
             "4×4 单元格（A1..D4，行 A 北→D 南、列 1 西→4 东）逐块摆放；墙体尺寸取自图 2 标注，"
             "v3：斜坡/橙区按图 2 橙色椭圆缩小，黄区十字与红区范围修正；红边界按红色线像素折点重建",
             fontsize=9.5, ha="center", va="center", color="#444444")
    note = (
        "坐标：原点=场地中心，x 东 / y 北 / z 上；每格 1.25 m。障碍尺寸用图 2 文字标注"
        "（≈0.95×0.61 / 1.30×0.52 / 1.13×0.49 / 1.12×0.60 / 0.73×0.58 ×2 / 1.14×0.48 / "
        "1.43×0.57 / 薄墙 0.85×0.08 / 工型 0.89×0.49 m），墙高 0.55 m、厚 0.06 m。\n"
        "形状按图 2 放大裁剪图判读：A1=A1 L 墙（顶横+左竖）、A2 L 墙（顶横+右竖）、A3 L 墙（底横+左竖）、"
        "C2 Z 形墙（左上竖+中横+右下竖）、B1/C1 T 墙（竖臂通高+横臂居中东向）、C4 L 墙（顶横+右竖）、"
        "东南 T 墙（竖臂+横臂东向）。红线外还有薄墙 / A 字架 / 背景横墙 / 东南 T 墙，与图 2 一致。\n"
        "斜坡（图4 整板规格按图2 橙色椭圆缩放）：单面 1.1×1.0 m、rise 0.18（坡向 +x、坡角≈9.3°）；"
        "双面 1.0×1.0 m 对拼成 Λ（每侧坡 0.5 m、脊高 0.18 m，两侧落地），脊下 3 个支撑木块。\n"
        "目标板/圆环按“墙体面板 + 面朝向”自动贴墙，随墙体移动。"
    )
    fig.text(0.5, 0.021, note, fontsize=7.3, ha="center", va="bottom",
             color="#333333", linespacing=1.55,
             bbox=dict(boxstyle="round,pad=0.5", fc="#f4f2ee", ec="#c8c3ba"))

    if overlay is not None:
        overlay(ax)
    os.makedirs(os.path.dirname(out_path or OUT), exist_ok=True)
    fig.savefig(out_path or OUT, dpi=300, facecolor="white")
    plt.close(fig)
    print("plan ->", out_path or OUT)


if __name__ == "__main__":
    draw()
