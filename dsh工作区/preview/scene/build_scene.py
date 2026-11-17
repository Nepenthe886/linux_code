# -*- coding: utf-8 -*-
"""由 scene_layout.py 生成 zhirong_maps 包的全部场景资源（v2：分块布局）。

生成内容
--------
competition_ws/src/maps/zhirong_maps/
├── models/<model>/model.config, model.sdf   # 纯 primitive 模型（离线可加载）
├── worlds/zhirong_arena.world               # SDF 1.6 世界（Gazebo Classic 11）
└── maps/zhirong_arena.pgm, zhirong_arena.yaml  # 0.05 m/px 2D 占据栅格

全部使用 box / cylinder 等基础几何拼装，不依赖任何外部 mesh、纹理或 fuel URI。
墙体/障碍的世界位姿**只**来自 scene_layout.BLOCKS（cell + 局部偏移），
目标板/圆环由 attach_pose() 从墙体面板自动贴墙，墙体移动后自动跟随。

用法：
    cd preview/scene && MPLCONFIGDIR=../../.mplconfig python3 build_scene.py
"""

import math
import os
import random
import zlib

import scene_layout as L

WS = "/home/nepenthe/zmf/linux_code/dsh工作区"
PKG = os.path.join(WS, "competition_ws/src/maps/zhirong_maps")

FLOOR_Z = 0.0010
GRID_Z = 0.0072


# ------------------------------------------------------------------ 文本工具
def f(v):
    s = "%.4f" % float(v)
    s = s.rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def rgb(name_or_tuple):
    c = L.MATERIALS[name_or_tuple] if isinstance(name_or_tuple, str) else name_or_tuple
    return "%s %s %s 1" % (f(c[0]), f(c[1]), f(c[2]))


def pose6(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0):
    return "%s %s %s %s %s %s" % (f(x), f(y), f(z), f(roll), f(pitch), f(yaw))


def mat_xml(color, spec=0.05):
    c = rgb(color)
    return ("<material><ambient>%s</ambient><diffuse>%s</diffuse>"
            "<specular>%s %s %s 1</specular><emissive>0 0 0 1</emissive></material>"
            % (c, c, f(spec), f(spec), f(spec)))


def geom_box(size):
    return "<box><size>%s %s %s</size></box>" % tuple(f(v) for v in size)


def geom_cyl(radius, length):
    return "<cylinder><radius>%s</radius><length>%s</length></cylinder>" % (
        f(radius), f(length))


def visual(name, pose, geometry, color, spec=0.05):
    return ('<visual name="%s"><pose>%s</pose><geometry>%s</geometry>%s</visual>'
            % (name, pose, geometry, mat_xml(color, spec)))


def collision(name, pose, geometry, mu=0.9):
    return ('<collision name="%s"><pose>%s</pose><geometry>%s</geometry>'
            '<surface><friction><ode><mu>%s</mu><mu2>%s</mu2></ode></friction>'
            '</surface></collision>' % (name, pose, geometry, f(mu), f(mu)))


def model_sdf(name, visuals, collisions):
    lines = ['<?xml version="1.0"?>', '<sdf version="1.6">',
             '  <model name="%s">' % name,
             '    <static>true</static>', '    <link name="link">']
    lines += ["      " + v for v in visuals]
    lines += ["      " + c for c in collisions]
    lines += ['    </link>', '  </model>', '</sdf>', '']
    return "\n".join(lines)


def model_config(name, desc):
    return "\n".join([
        '<?xml version="1.0"?>', '<model>',
        '  <name>%s</name>' % name,
        '  <version>1.0</version>',
        '  <sdf version="1.6">model.sdf</sdf>',
        '  <author><name>scene-builder</name>'
        '<email>scene-builder@zhirong.local</email></author>',
        '  <description>%s</description>' % desc,
        '</model>', ''])


# ------------------------------------------------------------------ 墙体
def camo_panels(model_name, panels, palette, body_color, patch_t=0.004):
    """把面板列表转成带迷彩补丁的 visual + collision 列表。"""
    visuals, collisions = [], []
    for idx, panel in enumerate(panels):
        cx, cy, sx, sy = panel[0], panel[1], panel[2], panel[3]
        pyaw = panel[4] if len(panel) > 4 else 0.0
        visuals.append(visual("%s_body_%d" % (model_name, idx),
                              pose6(cx, cy, L.WALL_H / 2, 0, 0, pyaw),
                              geom_box((sx, sy, L.WALL_H)), body_color))
        collisions.append(collision("%s_col_%d" % (model_name, idx),
                                    pose6(cx, cy, L.WALL_H / 2, 0, 0, pyaw),
                                    geom_box((sx, sy, L.WALL_H))))
        # 迷彩补丁：沿面板长边两面各贴 1~3 块
        rng = random.Random(zlib.crc32(("%s:%d" % (model_name, idx)).encode()))
        long_x = sx >= sy
        length = sx if long_x else sy
        thick = sy if long_x else sx
        n = max(1, min(3, int(round(length / 0.45))))
        c, s = math.cos(pyaw), math.sin(pyaw)
        for face in (1.0, -1.0):
            for k in range(n):
                pl = round(rng.uniform(0.14, min(0.30, max(0.16, length * 0.62))), 3)
                ph = round(rng.uniform(0.10, 0.20), 3)
                u = rng.uniform(-length / 2 + pl / 2 + 0.015,
                                length / 2 - pl / 2 - 0.015)
                zc = rng.uniform(0.07 + ph / 2, L.WALL_H - 0.04 - ph / 2)
                color = palette[rng.randrange(len(palette))]
                off = face * (thick / 2 + patch_t / 2 - 0.0005)
                if long_x:
                    lu, lv = u, off
                    size = (pl, patch_t, ph)
                else:
                    lu, lv = off, u
                    size = (patch_t, pl, ph)
                visuals.append(visual(
                    "%s_camo_%d_%d_%d" % (model_name, idx, 0 if face > 0 else 1, k),
                    pose6(cx + lu * c - lv * s, cy + lu * s + lv * c, zc,
                          0, 0, pyaw), geom_box(size), color))
    return visuals, collisions


def build_wall_model(key, spec):
    palette = L.CAMO_PATCH_COLORS if spec["material"] == "camo" else L.RED_PATCH_COLORS
    body = "camo_body" if spec["material"] == "camo" else "red_panel"
    visuals, collisions = camo_panels(key, spec["panels"], palette, body)
    return model_sdf(key, visuals, collisions)


# ------------------------------------------------------------------ 地面 / 分区 / 网格
def build_ground():
    g = L.GROUND_SIZE
    visuals = [visual("concrete", pose6(0, 0, -0.025),
                      geom_box((g, g, 0.05)), "concrete", 0.01)]
    collisions = [collision("concrete_col", pose6(0, 0, -0.025),
                            geom_box((g, g, 0.05)), 1.0)]
    return model_sdf("ground_8x8", visuals, collisions)


def build_arena_floor():
    s = L.FLOOR_SIZE
    cx, cy = L.FLOOR_CENTER
    visuals = [visual("asphalt", pose6(cx, cy, FLOOR_Z),
                      geom_box((s, s, 0.002)), "asphalt", 0.01)]
    return model_sdf("arena_floor", visuals, [])


def build_zone_yellow():
    visuals = []
    for i, (x0, y0, x1, y1) in enumerate(L.YELLOW_ZONES):
        visuals.append(visual("yellow_%d" % i,
                              pose6((x0 + x1) / 2, (y0 + y1) / 2,
                                    0.0030 + 0.0008 * i),
                              geom_box((x1 - x0, y1 - y0, 0.002)),
                              "zone_yellow", 0.02))
    return model_sdf("zone_yellow", visuals, [])


def build_zone_orange(key, radius):
    """桔区圆盘（半径按图 2 橙色椭圆缩放，见 ZONE_ORANGE_SPEC）。"""
    visuals = [visual("orange_disc", pose6(0, 0, L.ZONE_ORANGE_SPEC["z"]),
                      geom_cyl(radius, 0.002), "zone_orange", 0.02)]
    return model_sdf(key, visuals, [])


def build_zone_red():
    rz = L.RED_ZONE
    visuals = [visual("red_patch", pose6(0, 0, rz["z"]),
                      geom_box((rz["size"][0], rz["size"][1], 0.002)),
                      "zone_red", 0.02)]
    return model_sdf("zone_red", visuals, [])


def build_cell_grid():
    visuals = []
    for i, g in enumerate(L.GRID_LINES):
        c, s = g["center"], g["size"]
        visuals.append(visual("grid_%d" % i, pose6(c[0], c[1], g["z"]),
                              geom_box((s[0], s[1], 0.002)), "grid", 0.02))
    return model_sdf("cell_grid", visuals, [])


# ------------------------------------------------------------------ 红色比赛边界
def _seg_boxes(points):
    """折线 -> 轴对齐红线条段列表 (cx, cy, sx, sy)。"""
    out = []
    t = L.WALL_T
    for (x1, y1), (x2, y2) in zip(points[:-1], points[1:]):
        if abs(y2 - y1) < 1e-9:      # 水平段
            out.append(((x1 + x2) / 2, y1, abs(x2 - x1) + t, t))
        elif abs(x2 - x1) < 1e-9:    # 垂直段
            out.append((x1, (y1 + y2) / 2, t, abs(y2 - y1) + t))
        else:                        # 斜段（本世界无，保留兜底）
            ln = math.hypot(x2 - x1, y2 - y1)
            ang = math.atan2(y2 - y1, x2 - x1)
            out.append(((x1 + x2) / 2, (y1 + y2) / 2, ln, t, ang))
    return out


def build_boundary():
    visuals = []
    idx = 0
    for chain in L.boundary_world_chains():
        for seg in _seg_boxes(chain):
            if len(seg) == 5:
                cx, cy, sx, sy, ang = seg
                pose = pose6(cx, cy, GRID_Z, 0, 0, ang)
            else:
                cx, cy, sx, sy = seg
                pose = pose6(cx, cy, GRID_Z)
            visuals.append(visual("boundary_%d" % idx, pose,
                                  geom_box((sx, sy, 0.002)),
                                  "boundary_red", 0.02))
            idx += 1
    # 图 2 出口内侧的短折线（贴地红线，无碰撞）
    for seg in _seg_boxes(L.boundary_world_spur()):
        if len(seg) == 5:
            cx, cy, sx, sy, ang = seg
            pose = pose6(cx, cy, GRID_Z, 0, 0, ang)
        else:
            cx, cy, sx, sy = seg
            pose = pose6(cx, cy, GRID_Z)
        visuals.append(visual("boundary_spur_%d" % idx, pose,
                              geom_box((sx, sy, 0.002)), "boundary_red", 0.02))
        idx += 1
    return model_sdf("boundary_red", visuals, [])


# ------------------------------------------------------------------ 斜坡
def build_ramp_single():
    sp = L.RAMP_SINGLE_SPEC
    run, rise, bt = sp["length"], sp["rise"], sp["board_t"]
    alpha = L.RAMP_SINGLE_PITCH
    board_len = math.hypot(run, rise)
    zc = rise / 2 + (bt / 2) * math.cos(alpha)
    # 坡向 +x：+x 端抬高 -> 绕 y 轴负向旋转
    visuals = [visual("ramp_board", pose6(0, 0, zc, 0, -alpha, 0),
                      geom_box((board_len, sp["width"], bt)), "wood", 0.02)]
    collisions = [collision("ramp_board_col", pose6(0, 0, zc, 0, -alpha, 0),
                            geom_box((board_len, sp["width"], bt)), 0.7)]
    for i, y in enumerate((-0.42, 0.0, 0.42)):
        visuals.append(visual("support_%d" % i,
                              pose6(run / 2 - 0.055, y, (rise - 0.02) / 2),
                              geom_box((0.06, 0.08, rise - 0.02)), "wood_dark", 0.02))
        collisions.append(collision("support_%d_col" % i,
                                    pose6(run / 2 - 0.055, y, (rise - 0.02) / 2),
                                    geom_box((0.06, 0.08, rise - 0.02)), 0.7))
    return model_sdf("ramp_single_120", visuals, collisions)


def build_ramp_double():
    """双面斜坡：两块板对拼成 **Λ**（v3 footprint 1.0×1.0、脊高 0.18 m，两侧落地）。

    修正说明（v2）：v1 把两块板的 pitch 符号写反，板在中间凹成 V。
    正确：模型局部 x 为坡向，西板 pitch = -alpha、东板 pitch = +alpha，
    使两块板的 +x / -x 端在 x=0 处抬高到脊高。
    """
    sp = L.RAMP_DOUBLE_SPEC
    run, rise, bt = sp["half_run"], sp["rise"], sp["board_t"]
    alpha = L.RAMP_PITCH
    board_len = math.hypot(run, rise)
    zc = rise / 2 + (bt / 2) * math.cos(alpha)
    visuals, collisions = [], []
    for side, cx, pitch in (("w", -run / 2, -alpha), ("e", run / 2, alpha)):
        visuals.append(visual("ramp_board_%s" % side,
                              pose6(cx, 0, zc, 0, pitch, 0),
                              geom_box((board_len, sp["width"], bt)), "wood", 0.02))
        collisions.append(collision("ramp_board_%s_col" % side,
                                   pose6(cx, 0, zc, 0, pitch, 0),
                                   geom_box((board_len, sp["width"], bt)), 0.7))
    # 脊下三个支撑木块（位置保持）
    for i, y in enumerate((-0.42, 0.0, 0.42)):
        visuals.append(visual("ridge_support_%d" % i,
                              pose6(0, y, (rise - 0.02) / 2),
                              geom_box((0.08, 0.08, rise - 0.02)), "wood_dark", 0.02))
        collisions.append(collision("ridge_support_%d_col" % i,
                                    pose6(0, y, (rise - 0.02) / 2),
                                    geom_box((0.08, 0.08, rise - 0.02)), 0.7))
    return model_sdf("ramp_double_120", visuals, collisions)


# ------------------------------------------------------------------ 目标物
def _plate_visuals():
    p = L.TARGET_PLATE
    return [visual("plate", pose6(0, 0, 0),
                   geom_box((p["w"], p["t"], p["h"])), "plate_white", 0.10)]


def build_target_hostage(key="target_hostage"):
    """身靶：白底板 + 人形轮廓 + 胸口同心圆。板面法线 +y。"""
    visuals = _plate_visuals()
    y0 = L.TARGET_PLATE["t"] / 2 + 0.0015
    visuals.append(visual("head", pose6(0, y0, 0.062, math.pi / 2, 0, 0),
                          geom_cyl(0.030, 0.004), "target_dark", 0.02))
    visuals.append(visual("shoulder", pose6(0, y0, 0.036),
                          geom_box((0.150, 0.004, 0.024)), "target_dark", 0.02))
    visuals.append(visual("torso", pose6(0, y0 + 0.0002, 0.000),
                          geom_box((0.092, 0.004, 0.075)), "target_dark", 0.02))
    for side in (-1, 1):
        visuals.append(visual("arm_%d" % side, pose6(side * 0.064, y0, 0.006),
                              geom_box((0.020, 0.004, 0.070)), "target_dark", 0.02))
        visuals.append(visual("leg_%d" % side, pose6(side * 0.024, y0, -0.072),
                              geom_box((0.026, 0.004, 0.070)), "target_dark", 0.02))
    for i, (r, col) in enumerate(((0.036, "target_red"), (0.026, "plate_white"),
                                  (0.017, "target_dark"), (0.007, "plate_white"))):
        visuals.append(visual("chest_%d" % i,
                              pose6(0, y0 + 0.0012 * (i + 1), 0.0, math.pi / 2, 0, 0),
                              geom_cyl(r, 0.002), col, 0.02))
    return model_sdf(key, visuals, [])


def build_target_chest(key="target_chest"):
    """胸靶：白底板 + 同心圆（黑/红/白交替）。板面法线 +y。"""
    visuals = _plate_visuals()
    y0 = L.TARGET_PLATE["t"] / 2 + 0.0015
    rings = ((0.088, "target_dark"), (0.070, "plate_white"),
             (0.052, "target_red"), (0.036, "plate_white"),
             (0.020, "target_dark"), (0.008, "ring_black"))
    for i, (r, col) in enumerate(rings):
        visuals.append(visual("ring_%d" % i,
                              pose6(0, y0 + 0.0012 * (i + 1), 0.0, math.pi / 2, 0, 0),
                              geom_cyl(r, 0.002), col, 0.02))
    return model_sdf(key, visuals, [])


def build_target_qr(key="target_qr"):
    """二维码危险品：白底板 + 橙色标题条 + 9×9 黑白方块模拟二维码。"""
    visuals = _plate_visuals()
    p = L.TARGET_PLATE
    y0 = p["t"] / 2 + 0.0015
    visuals.append(visual("header", pose6(0, y0, 0.082),
                          geom_box((0.200, 0.004, 0.026)), "qr_orange", 0.02))
    visuals.append(visual("text_1", pose6(0, y0, 0.052),
                          geom_box((0.150, 0.004, 0.008)), "qr_dark", 0.02))
    mod_n, mod_s, mod_p = 9, 0.0115, 0.0126
    rng = random.Random(zlib.crc32(key.encode()))
    finder = ((0, 0), (0, 6), (6, 0))
    for ix in range(mod_n):
        for iz in range(mod_n):
            dark = rng.random() < 0.44
            for fx, fz in finder:
                if fx <= ix < fx + 3 and fz <= iz < fz + 3:
                    dark = not (fx + 1 == ix and fz + 1 == iz)
            if not dark:
                continue
            x = (ix - (mod_n - 1) / 2) * mod_p
            z = -0.020 - (iz - (mod_n - 1) / 2) * mod_p
            visuals.append(visual("qr_%d_%d" % (ix, iz),
                                  pose6(x, y0 + 0.0015, z),
                                  geom_box((mod_s, 0.003, mod_s)), "qr_dark", 0.02))
    return model_sdf(key, visuals, [])


def build_touch_ring(key="touch_ring"):
    """圆环触碰点（图 8）：蓝色圆环（16 段拼圆）+ 黑色圆心。板面法线 +y。"""
    sp = L.RING_SPEC
    visuals = []
    seg = 16
    r_mid = sp["outer_r"] - sp["tube"] / 2
    for i in range(seg):
        phi = 2 * math.pi * i / seg
        visuals.append(visual("ring_seg_%d" % i,
                              pose6(r_mid * math.cos(phi), 0, r_mid * math.sin(phi),
                                    0, -(phi + math.pi / 2), 0),
                              geom_box((2 * math.pi * r_mid / seg * 1.18,
                                        sp["tube"], sp["tube"])),
                              "ring_blue", 0.02))
    visuals.append(visual("ring_center", pose6(0, 0.002, 0, math.pi / 2, 0, 0),
                          geom_cyl(sp["center_r"], 0.006), "ring_black", 0.02))
    return model_sdf(key, visuals, [])


# ------------------------------------------------------------------ 标牌 / 门柱 / 出生点
FONT3x5 = {
    "I": ("111", "010", "010", "010", "111"),
    "N": ("101", "111", "111", "101", "101"),
    "O": ("111", "101", "101", "101", "111"),
    "U": ("101", "101", "101", "101", "111"),
    "T": ("111", "010", "010", "010", "010"),
}


def build_sign(key, text, color_key):
    sp = L.SIGN_SPEC
    visuals = []
    for side in (-1, 1):
        visuals.append(visual("post_%d" % side,
                              pose6(side * sp["post_dx"], 0, sp["post_h"] / 2),
                              geom_cyl(sp["post_r"], sp["post_h"]), "post_white", 0.02))
    visuals.append(visual("board", pose6(0, 0, sp["board_z"]),
                          geom_box((sp["board_w"], sp["board_t"], sp["board_h"])),
                          "sign_white", 0.10))
    bw, bh, bt_ = sp["board_w"], sp["board_h"], sp["board_t"]
    for i, (dx, dz, sx, sz) in enumerate(((-bw / 2, 0, 0.02, bh),
                                         (bw / 2, 0, 0.02, bh),
                                         (0, bh / 2, bw, 0.02),
                                         (0, -bh / 2, bw, 0.02))):
        visuals.append(visual("frame_%d" % i,
                              pose6(dx, -bt_ / 2 - 0.0012, sp["board_z"] + dz),
                              geom_box((sx, 0.003, sz)), color_key, 0.02))
    cell = sp["cell"]
    total_w = len(text) * 4 * cell - cell
    x0 = -total_w / 2 + cell / 2
    for ci, ch in enumerate(text):
        for row, line in enumerate(FONT3x5[ch]):
            for col, bit in enumerate(line):
                if bit != "1":
                    continue
                visuals.append(visual(
                    "font_%d_%d_%d" % (ci, row, col),
                    pose6(x0 + ci * 4 * cell + col * cell, -bt_ / 2 - 0.0012,
                          sp["board_z"] + (2 - row) * cell),
                    geom_box((cell * 0.96, 0.003, cell * 0.96)), color_key, 0.02))
    return model_sdf(key, visuals, [])


def build_gate_post():
    visuals = [
        visual("post", pose6(0, 0, 0.25), geom_cyl(0.028, 0.50), "gate_red", 0.02),
        visual("band", pose6(0, 0, 0.40), geom_cyl(0.030, 0.10), "post_white", 0.02),
    ]
    collisions = [collision("post_col", pose6(0, 0, 0.25), geom_cyl(0.028, 0.50))]
    return model_sdf("gate_post", visuals, collisions)


def build_spawn_marker():
    visuals = [
        visual("disc_outer", pose6(0, 0, 0.0020), geom_cyl(0.36, 0.003),
               "marker_green", 0.02),
        visual("disc_inner", pose6(0, 0, 0.0036), geom_cyl(0.30, 0.003),
               "post_white", 0.02),
        visual("arrow_shaft", pose6(0.04, 0, 0.0048),
               geom_box((0.40, 0.05, 0.004)), "marker_green", 0.02),
        visual("arrow_head_up", pose6(-0.20, 0.048, 0.0048, 0, 0, math.radians(37)),
               geom_box((0.16, 0.045, 0.004)), "marker_green", 0.02),
        visual("arrow_head_dn", pose6(-0.20, -0.048, 0.0048, 0, 0, math.radians(-37)),
               geom_box((0.16, 0.045, 0.004)), "marker_green", 0.02),
    ]
    return model_sdf("spawn_marker", visuals, [])


# ------------------------------------------------------------------ 世界文件
def _include(model, name, x, y, z=0.0, yaw=0.0):
    return ("    <include>\n"
            "      <uri>model://%s</uri>\n"
            "      <name>%s</name>\n"
            "      <pose>%s</pose>\n"
            "    </include>" % (model, name, pose6(x, y, z, 0, 0, yaw)))


def build_world():
    lines = [
        '<?xml version="1.0" ?>',
        '<sdf version="1.6">',
        '  <world name="zhirong_arena">',
        '    <!-- 反恐搜救赛项比赛场地：16 个 1.25 m 单元格（5 m x 5 m 范围，行 A 北->D 南、列 1 西->4 东）；x 东 / y 北 / 原点=场地中心 -->',
        '    <scene>',
        '      <ambient>0.45 0.45 0.45 1</ambient>',
        '      <background>0.76 0.83 0.92 1</background>',
        '      <shadows>true</shadows>',
        '      <grid>false</grid>',
        '    </scene>',
        '',
        '    <!-- 物理：固定 1 ms 步长，1 kHz 更新 -->',
        '    <physics type="ode">',
        '      <max_step_size>0.001</max_step_size>',
        '      <real_time_factor>1.0</real_time_factor>',
        '      <real_time_update_rate>1000</real_time_update_rate>',
        '      <ode>',
        '        <solver><type>quick</type><iters>50</iters><sor>1.3</sor></solver>',
        '        <constraints>',
        '          <cfm>0.0</cfm><erp>0.2</erp>',
        '          <contact_max_correcting_vel>100</contact_max_correcting_vel>',
        '          <contact_surface_layer>0.001</contact_surface_layer>',
        '        </constraints>',
        '      </ode>',
        '    </physics>',
        '    <gravity>0 0 -9.8</gravity>',
        '',
        '    <!-- 太阳光 -->',
        '    <light type="directional" name="sun">',
        '      <cast_shadows>true</cast_shadows>',
        '      <pose>0 0 12 0 0 0</pose>',
        '      <diffuse>0.88 0.85 0.78 1</diffuse>',
        '      <specular>0.15 0.15 0.15 1</specular>',
        '      <attenuation><range>1000</range><constant>0.9</constant>'
        '<linear>0.01</linear><quadratic>0.001</quadratic></attenuation>',
        '      <direction>-0.55 0.35 -0.75</direction>',
        '    </light>',
        '',
        '    <!-- GUI 相机预设：正俯视、与图 2 同方向（+x 东 / +y 北） -->',
        '    <gui fullscreen="0">',
        '      <camera name="user_camera">',
        '        <pose>0 0 6.0 0 1.5708 1.5708</pose>',
        '        <view_controller>orbit</view_controller>',
        '      </camera>',
        '    </gui>',
        '',
        '    <!-- ============ 地面 / 场地 / 网格 / 红边界 ============ -->',
    ]
    lines.append(_include("ground_8x8", "ground", 0, 0))
    lines.append(_include("arena_floor", "arena_floor",
                          L.FLOOR_CENTER[0], L.FLOOR_CENTER[1]))
    lines.append(_include("cell_grid", "cell_grid", 0, 0))
    lines.append(_include("boundary_red", "boundary_red", 0, 0))
    lines.append('')
    lines.append('    <!-- ============ 分区地面 ============ -->')
    lines.append(_include("zone_yellow", "zone_yellow", 0, 0))
    lines.append(_include("zone_orange_ramp1", "zone_orange_ramp_1",
                          L.world_xy(L.BLOCK_BY_NAME["ramp_1"])[0],
                          L.world_xy(L.BLOCK_BY_NAME["ramp_1"])[1]))
    lines.append(_include("zone_orange_ramp2", "zone_orange_ramp_2",
                          L.world_xy(L.BLOCK_BY_NAME["ramp_2"])[0],
                          L.world_xy(L.BLOCK_BY_NAME["ramp_2"])[1]))
    lines.append(_include("zone_red", "zone_red",
                          L.RED_ZONE["center"][0], L.RED_ZONE["center"][1]))
    lines.append('')
    lines.append('    <!-- ============ 分块布局：墙体 / 障碍 / 斜坡 ============ -->')
    for inst in L.instances():
        lines.append(_include(inst["model"], inst["name"], inst["x"], inst["y"],
                              0.0, inst["yaw"]))
    lines.append('')
    lines.append('    <!-- ============ 目标物（身靶 / 胸靶 / 二维码，自动贴墙） ============ -->')
    for t in L.TARGETS:
        x, y, z, yaw = L.attach_pose(t["wall"], t["panel"], t["face"],
                                     t["along"], t["z"], L.TARGET_PLATE["offset"])
        lines.append(_include(t["model"], t["name"], x, y, z, yaw))
    lines.append('')
    lines.append('    <!-- ============ 触碰圆环（5 个，自动贴墙） ============ -->')
    for r in L.TOUCH_RINGS:
        x, y, z, yaw = L.attach_pose(r["wall"], r["panel"], r["face"],
                                     r["along"], r["z"], L.RING_SPEC["offset"])
        lines.append(_include("touch_ring", r["name"], x, y, z, yaw))
    lines.append('')
    lines.append('    <!-- ============ 入口 / 出口标牌、门柱、出生点 ============ -->')
    for s in L.SIGNS:
        lines.append(_include(s["model"], s["name"], s["pos"][0], s["pos"][1],
                              0.0, s["yaw"]))
    for g in L.GATE_POSTS:
        lines.append(_include("gate_post", g["name"], g["pos"][0], g["pos"][1]))
    lines.append(_include("spawn_marker", "spawn_marker", L.SPAWN["x"], L.SPAWN["y"]))
    lines += ['  </world>', '</sdf>', '']
    return "\n".join(lines)


# ------------------------------------------------------------------ 2D 占据栅格
MAP_RES = 0.05
MAP_HALF = 4.0


def build_map():
    import numpy as np
    n = int(round(MAP_HALF * 2 / MAP_RES))
    grid = np.full(n * n, 254, dtype=np.uint8)

    def mark_rect(cx, cy, sx, sy, yaw=0.0):
        c, s = math.cos(yaw), math.sin(yaw)
        ex = abs(sx / 2 * c) + abs(sy / 2 * s)
        ey = abs(sx / 2 * s) + abs(sy / 2 * c)
        i0 = max(0, int((cx - ex + MAP_HALF) / MAP_RES) - 1)
        i1 = min(n - 1, int((cx + ex + MAP_HALF) / MAP_RES) + 1)
        j0 = max(0, int((cy - ey + MAP_HALF) / MAP_RES) - 1)
        j1 = min(n - 1, int((cy + ey + MAP_HALF) / MAP_RES) + 1)
        for j in range(j0, j1 + 1):
            cy_ = -MAP_HALF + (j + 0.5) * MAP_RES
            for i in range(i0, i1 + 1):
                cx_ = -MAP_HALF + (i + 0.5) * MAP_RES
                dx, dy = cx_ - cx, cy_ - cy
                u = dx * c + dy * s
                v = -dx * s + dy * c
                if abs(u) <= sx / 2 and abs(v) <= sy / 2:
                    grid[(n - 1 - j) * n + i] = 0

    for r in L.iter_wall_rects():
        mark_rect(r["center"][0], r["center"][1], r["size"][0], r["size"][1], r["yaw"])
    for b in L.BLOCKS:
        if b["model"] == "ramp_single_120":
            sp = L.RAMP_SINGLE_SPEC
        elif b["model"] == "ramp_double_120":
            sp = L.RAMP_DOUBLE_SPEC
        else:
            continue
        x, y = L.world_xy(b)
        mark_rect(x, y, sp["length"], sp["width"], b.get("yaw", 0.0))
    for s in L.SIGNS:
        mark_rect(s["pos"][0], s["pos"][1], L.SIGN_SPEC["board_w"], 0.2, s["yaw"])
    for g in L.GATE_POSTS:
        mark_rect(g["pos"][0], g["pos"][1], 0.06, 0.06)
    return n, grid


def write_map(path_dir):
    n, grid = build_map()
    os.makedirs(path_dir, exist_ok=True)
    with open(os.path.join(path_dir, "zhirong_arena.pgm"), "wb") as fh:
        fh.write(b"P5\n# zhirong_arena occupancy grid, 0.05 m/px, origin (-4,-4)\n")
        fh.write(("%d %d\n255\n" % (n, n)).encode())
        fh.write(grid.tobytes())
    with open(os.path.join(path_dir, "zhirong_arena.yaml"), "w") as fh:
        fh.write("\n".join([
            "image: zhirong_arena.pgm",
            "resolution: 0.050000",
            "origin: [-4.000000, -4.000000, 0.000000]",
            "negate: 0",
            "occupied_thresh: 0.65",
            "free_thresh: 0.196", ""]))
    return n, grid


# ------------------------------------------------------------------ 自检
def _point_in_polygon(pt, poly):
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xin:
                inside = not inside
    return inside


def red_polygon():
    """把两条红边界折线（含缺口）闭合成一个多边形，用于点内/外判断。"""
    chainA = [[n for n in L.px2world(*p)] for p in L.BOUNDARY_CHAINS_PX[0]]
    chainB = [[n for n in L.px2world(*p)] for p in L.BOUNDARY_CHAINS_PX[1]]
    return chainA + chainB


def sanity_checks():
    problems = []
    boxes = []
    half_ground = L.GROUND_SIZE / 2 - 0.05
    for inst in L.instances():
        b = L.instance_bbox(inst)
        boxes.append((inst["name"], b, inst["cell"]))
        if b[0] < -half_ground or b[2] > half_ground or \
           b[1] < -half_ground or b[3] > half_ground:
            problems.append("越出 8m 地面: %s bbox=%s" % (inst["name"], b))
    # 障碍间不重叠（bbox 近似）
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0.01 and oy > 0.01:
                problems.append("障碍重叠: %s <-> %s (%.3f x %.3f m)"
                                % (boxes[i][0], boxes[j][0], ox, oy))
    # 单元格归属：非 OUT 障碍的 bbox 必须与声明 cell 有交叠（允许跨块，图 2 中多面墙跨格）
    straddle = []
    for inst in L.instances():
        cell = inst["cell"]
        if cell.startswith("OUT"):
            continue
        cx, cy = L.CELLS[cell]
        cell_box = (cx - L.CELL / 2, cy - L.CELL / 2, cx + L.CELL / 2, cy + L.CELL / 2)
        b = L.instance_bbox(inst)
        ox = min(b[2], cell_box[2]) - max(b[0], cell_box[0])
        oy = min(b[3], cell_box[3]) - max(b[1], cell_box[1])
        if ox <= 0.001 or oy <= 0.001:
            problems.append("块归属偏差: %s 声明 %s，但 bbox 与之不相交" % (inst["name"], cell))
        # 统计跨块（bbox 覆盖多个单元格）
        cols = {int((x + L.FIELD_HALF) // L.CELL) for x in (b[0], b[2])}
        rows = {3 - int((y + L.FIELD_HALF) // L.CELL) for y in (b[1], b[3])}
        if len(cols) + len(rows) > 2:
            straddle.append("%s(%s)" % (inst["name"], cell))
    if straddle:
        print("[自检] 跨单元格墙（与图 2 一致）：" + "、".join(straddle))
    # 目标板 / 圆环：按贴墙规则生成，检查不与墙体重心冲突、z 在墙高内
    for t in L.TARGETS + L.TOUCH_RINGS:
        if not (0.10 <= t["z"] <= L.WALL_H - 0.05):
            problems.append("%s 高度 %.2f 超出墙高" % (t["name"], t["z"]))
    # 出生点：在 8m 地面内、红边界外
    poly = red_polygon()
    if _point_in_polygon((L.SPAWN["x"], L.SPAWN["y"]), poly):
        problems.append("出生点落在红边界内")
    if not (abs(L.SPAWN["x"]) < half_ground and abs(L.SPAWN["y"]) < half_ground):
        problems.append("出生点超出 8m 地面")
    # 斜坡 2：Λ 形（西板 pitch<0、东板 pitch>0），脊高 = rise
    sp = L.RAMP_DOUBLE_SPEC
    alpha = L.RAMP_PITCH
    zc = sp["rise"] / 2 + (sp["board_t"] / 2) * math.cos(alpha)
    ridge_w = zc + (math.hypot(sp["half_run"], sp["rise"]) / 2) * math.sin(alpha)
    if not (abs(ridge_w - (sp["rise"] + sp["board_t"] * math.cos(alpha))) < 0.02):
        problems.append("斜坡2 脊高异常: %.3f" % ridge_w)
    # 桔区半径应与斜坡 footprint 半长边一致（图 2 橙椭圆 ≈ 斜坡占地）
    for key, spec, r in (
            ("ramp_1", L.RAMP_SINGLE_SPEC, L.ZONE_ORANGE_SPEC["ramp1_r"]),
            ("ramp_2", L.RAMP_DOUBLE_SPEC, L.ZONE_ORANGE_SPEC["ramp2_r"])):
        half = max(spec["length"], spec["width"]) / 2
        if abs(r - half) > 0.07:
            problems.append("%s 桔区半径 %.2f 与 footprint 半长边 %.2f 不一致"
                            % (key, r, half))
    return problems


# ------------------------------------------------------------------ main
MODEL_BUILDERS = {}


def _register_models():
    for key, spec in L.WALL_MODELS.items():
        MODEL_BUILDERS[key] = (lambda k=key, s=spec: build_wall_model(k, s), spec["desc"])
    MODEL_BUILDERS["ground_8x8"] = (build_ground, "8 m × 8 m 承载地面（水泥）")
    MODEL_BUILDERS["arena_floor"] = (build_arena_floor,
                                     "场地铺装（沥青，%.1f m × %.1f m，覆盖红边界 bbox）"
                                     % (L.FLOOR_SIZE, L.FLOOR_SIZE))
    MODEL_BUILDERS["zone_yellow"] = (build_zone_yellow, "黄区（图 2 黄色十字填充）")
    MODEL_BUILDERS["zone_orange_ramp1"] = (
        lambda: build_zone_orange("zone_orange_ramp1", L.ZONE_ORANGE_SPEC["ramp1_r"]),
        "桔区-斜坡1（橙色圆盘 r=%.2f，图 2 橙椭圆 1.13×1.04）"
        % L.ZONE_ORANGE_SPEC["ramp1_r"])
    MODEL_BUILDERS["zone_orange_ramp2"] = (
        lambda: build_zone_orange("zone_orange_ramp2", L.ZONE_ORANGE_SPEC["ramp2_r"]),
        "桔区-斜坡2（橙色圆盘 r=%.2f，图 2 橙椭圆 1.03×0.53）"
        % L.ZONE_ORANGE_SPEC["ramp2_r"])
    MODEL_BUILDERS["zone_red"] = (build_zone_red, "红区（工型障碍附近红色地面）")
    MODEL_BUILDERS["cell_grid"] = (build_cell_grid, "16 单元格网格线（贴地细条）")
    MODEL_BUILDERS["boundary_red"] = (build_boundary,
                                      "红色比赛边界（图 2 不规则折线 + 东偏北入口/西中部出口缺口）")
    MODEL_BUILDERS["ramp_single_120"] = (build_ramp_single,
                                         "单面斜坡 1.2×1.2×0.019 m，坡度 ≈9.5°，坡向 +x")
    MODEL_BUILDERS["ramp_double_120"] = (build_ramp_double,
                                         "双面斜坡：两块 0.6×1.2 板拼成 Λ，脊高 0.20 m")
    MODEL_BUILDERS["target_hostage"] = (build_target_hostage, "身靶（模拟恐怖份子）目标板")
    MODEL_BUILDERS["target_chest"] = (build_target_chest, "胸靶（待救援对象）目标板")
    MODEL_BUILDERS["target_qr"] = (build_target_qr, "二维码危险品目标板")
    MODEL_BUILDERS["touch_ring"] = (build_touch_ring, "圆环触碰点（蓝环 + 黑圆心）")
    MODEL_BUILDERS["sign_in"] = (lambda: build_sign("sign_in", "IN", "sign_green"),
                                 "入口文字标牌（IN）")
    MODEL_BUILDERS["sign_out"] = (lambda: build_sign("sign_out", "OUT", "sign_red"),
                                  "出口文字标牌（OUT）")
    MODEL_BUILDERS["gate_post"] = (build_gate_post, "入口/出口门柱")
    MODEL_BUILDERS["spawn_marker"] = (build_spawn_marker, "机器人出生点地面标记")


def main():
    _register_models()
    models_dir = os.path.join(PKG, "models")
    world_dir = os.path.join(PKG, "worlds")
    maps_dir = os.path.join(PKG, "maps")
    for d in (models_dir, world_dir, maps_dir):
        os.makedirs(d, exist_ok=True)

    # 清理旧版残留模型目录
    for name in sorted(os.listdir(models_dir)):
        p = os.path.join(models_dir, name)
        if os.path.isdir(p) and name not in MODEL_BUILDERS:
            for fn in ("model.config", "model.sdf"):
                fp = os.path.join(p, fn)
                if os.path.exists(fp):
                    os.remove(fp)
            try:
                os.rmdir(p)
                print("[clean ] 移除旧模型目录 %s" % name)
            except OSError:
                pass

    for name, (builder, desc) in sorted(MODEL_BUILDERS.items()):
        mdir = os.path.join(models_dir, name)
        os.makedirs(mdir, exist_ok=True)
        with open(os.path.join(mdir, "model.config"), "w") as fh:
            fh.write(model_config(name, desc))
        with open(os.path.join(mdir, "model.sdf"), "w") as fh:
            fh.write(builder())
    print("[models] %d 个模型 -> %s" % (len(MODEL_BUILDERS), models_dir))

    with open(os.path.join(world_dir, "zhirong_arena.world"), "w") as fh:
        fh.write(build_world())
    print("[world ] worlds/zhirong_arena.world")

    n, grid = write_map(maps_dir)
    occ = int((grid == 0).sum())
    print("[map   ] maps/zhirong_arena.pgm  %dx%d px, 占用 %d px (%.1f m^2)"
          % (n, n, occ, occ * MAP_RES * MAP_RES))

    problems = sanity_checks()
    print("\n[自检]")
    if problems:
        for p in problems:
            print("  ! " + p)
    else:
        print("  全部通过：障碍均在 8m 地面内、互不重叠、块归属正确、目标/圆环高度合法、"
              "出生点在红边界外、斜坡2 为 Λ 形；桔区半径与斜坡 footprint 一致。")

    print("\n[分块布局摘要]")
    for cell, names in sorted(L.blocks_per_cell().items()):
        print("  %-6s : %s" % (cell, "、".join(names) if names else "（空）"))
    print("\n[障碍世界位姿]")
    for inst in L.instances():
        b = L.instance_bbox(inst)
        print("  %-22s cell=%-6s model=%-18s pos=(%6.3f,%6.3f) yaw=%5.3f bbox=(%.2f,%.2f)-(%.2f,%.2f)"
              % (inst["name"], inst["cell"], inst["model"], inst["x"], inst["y"],
                 inst["yaw"], b[0], b[1], b[2], b[3]))
    print("\n[红色边界]")
    for i, chain in enumerate(L.boundary_world_chains()):
        print("  chain%d: %s" % (i, " -> ".join("(%.2f,%.2f)" % p for p in chain)))
    e1, e2, x1, x2 = L.boundary_gap_points()
    print("  入口缺口 %.2f m: (%.2f,%.2f) - (%.2f,%.2f)"
          % (math.hypot(e2[0] - e1[0], e2[1] - e1[1]), e1[0], e1[1], e2[0], e2[1]))
    print("  出口缺口 %.2f m: (%.2f,%.2f) - (%.2f,%.2f)"
          % (math.hypot(x2[0] - x1[0], x2[1] - x1[1]), x1[0], x1[1], x2[0], x2[1]))
    print("  出生点 spawn = (%.2f, %.2f, z=%.2f, yaw=%.2f)"
          % (L.SPAWN["x"], L.SPAWN["y"], L.SPAWN["z"], L.SPAWN["yaw"]))
    print("\n[斜坡 / 桔区]")
    sp1, sp2 = L.RAMP_SINGLE_SPEC, L.RAMP_DOUBLE_SPEC
    print("  ramp_1 单面 footprint %.1f×%.1f m，rise %.2f m，坡角 %.2f°，坡向 +x，pitch=-%.4f"
          % (sp1["length"], sp1["width"], sp1["rise"],
             math.degrees(L.RAMP_SINGLE_PITCH), L.RAMP_SINGLE_PITCH))
    print("  ramp_2 双面 Λ footprint %.1f×%.1f m，rise %.2f m（每侧坡 %.1f m），坡角 %.2f°，"
          "西板 pitch=-%.4f / 东板 pitch=+%.4f"
          % (sp2["length"], sp2["width"], sp2["rise"], sp2["half_run"],
             math.degrees(L.RAMP_PITCH), L.RAMP_PITCH, L.RAMP_PITCH))
    print("  桔区半径：ramp1 %.2f m / ramp2 %.2f m"
          % (L.ZONE_ORANGE_SPEC["ramp1_r"], L.ZONE_ORANGE_SPEC["ramp2_r"]))


if __name__ == "__main__":
    main()
