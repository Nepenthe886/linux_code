# -*- coding: utf-8 -*-
"""由 scene_layout.py 生成 zhirong_maps 包的全部场景资源。

生成内容
--------
competition_ws/src/maps/zhirong_maps/
├── models/<model>/model.config, model.sdf   # 28 个纯 primitive 模型（离线可加载）
├── worlds/zhirong_arena.world               # SDF 1.6 世界（Gazebo Classic 11）
└── maps/zhirong_arena.pgm, zhirong_arena.yaml  # 0.05 m/px 2D 占据栅格（附加）

全部使用 box / cylinder 等基础几何拼装，不依赖任何外部 mesh、纹理或 fuel URI。
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

# 地面/分区贴片厚度与 z 中心（逐层抬高，避免共面闪烁）
FLOOR_Z = 0.0010
GRID_Z = 0.0072


# ------------------------------------------------------------------ 文本工具
def f(v):
    """浮点格式化：最多 4 位小数，去掉多余 0。"""
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


def link_xml(visuals, collisions):
    lines = ['    <link name="link">']
    lines += ["      " + v for v in visuals]
    lines += ["      " + c for c in collisions]
    lines.append('    </link>')
    return lines


def model_sdf(name, visuals, collisions):
    lines = ['<?xml version="1.0"?>', '<sdf version="1.6">',
             '  <model name="%s">' % name,
             '    <static>true</static>']
    lines += link_xml(visuals, collisions)
    lines += ['  </model>', '</sdf>', '']
    return "\n".join(lines)


def model_config(name, desc):
    return "\n".join([
        '<?xml version="1.0"?>',
        '<model>',
        '  <name>%s</name>' % name,
        '  <version>1.0</version>',
        '  <sdf version="1.6">model.sdf</sdf>',
        '  <author><name>scene-builder</name>'
        '<email>scene-builder@zhirong.local</email></author>',
        '  <description>%s</description>' % desc,
        '</model>',
        '',
    ])


# ------------------------------------------------------------------ 墙体
def camo_panels(model_name, panels, palette, body_color, patch_t=0.004):
    """把一组面板（轴对齐或带 yaw 的盒子）转成带迷彩补丁的 visual 列表。"""
    visuals, collisions = [], []
    for idx, panel in enumerate(panels):
        cx, cy, sx, sy = panel[0], panel[1], panel[2], panel[3]
        pyaw = panel[4] if len(panel) > 4 else 0.0
        # 墙体主体
        visuals.append(visual("%s_body_%d" % (model_name, idx),
                              pose6(cx, cy, L.WALL_H / 2, 0, 0, pyaw),
                              geom_box((sx, sy, L.WALL_H)), body_color))
        collisions.append(collision("%s_col_%d" % (model_name, idx),
                                    pose6(cx, cy, L.WALL_H / 2, 0, 0, pyaw),
                                    geom_box((sx, sy, L.WALL_H))))
        # 迷彩补丁：沿面板长边在两面各贴 1~3 块
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
                wx = cx + lu * c - lv * s
                wy = cy + lu * s + lv * c
                visuals.append(visual(
                    "%s_camo_%d_%d_%d" % (model_name, idx, 0 if face > 0 else 1, k),
                    pose6(wx, wy, zc, 0, 0, pyaw), geom_box(size), color))
    return visuals, collisions


def build_wall_model(key, spec):
    palette = L.CAMO_PATCH_COLORS if spec["material"] == "camo" else L.RED_PATCH_COLORS
    body = "camo_body" if spec["material"] == "camo" else "red_panel"
    visuals, collisions = camo_panels(key, spec["panels"], palette, body)
    return model_sdf(key, visuals, collisions)


def build_zone_yellow():
    visuals = []
    for i, (cx, cy, sx, sy, zc) in enumerate(L.YELLOW_BARS):
        visuals.append(visual("yellow_bar_%d" % i,
                              pose6(cx, cy, zc), geom_box((sx, sy, 0.002)),
                              "zone_yellow", 0.02))
    return model_sdf("zone_yellow_cross", visuals, [])


def build_zone_orange():
    r = L.ORANGE_ZONES[0]["r"]
    visuals = [visual("orange_disc", pose6(0, 0, L.ORANGE_ZONES[0]["z"]),
                      geom_cyl(r, 0.002), "zone_orange", 0.02)]
    return model_sdf("zone_orange_disc", visuals, [])


def build_zone_red():
    s = L.RED_ZONE["size"]
    visuals = [visual("red_patch", pose6(0, 0, L.RED_ZONE["z"]),
                      geom_box((s[0], s[1], 0.002)), "zone_red", 0.02)]
    return model_sdf("zone_red", visuals, [])


def build_cell_grid():
    visuals = []
    for i, g in enumerate(L.GRID_LINES):
        c, s = g["center"], g["size"]
        visuals.append(visual("grid_%d" % i, pose6(c[0], c[1], g["z"]),
                              geom_box((s[0], s[1], 0.002)), "grid", 0.02))
    return model_sdf("cell_grid", visuals, [])


def build_boundary():
    visuals = []
    for i, seg in enumerate(L.BOUNDARY_SEGMENTS):
        c, s = seg["center"], seg["size"]
        visuals.append(visual("boundary_%d" % i,
                              pose6(c[0], c[1], GRID_Z),
                              geom_box((s[0], s[1], 0.002)), "boundary_red", 0.02))
    return model_sdf("boundary_red", visuals, [])


# ------------------------------------------------------------------ 地面
def build_ground():
    g = L.GROUND_SIZE
    visuals = [visual("concrete", pose6(0, 0, -0.025),
                      geom_box((g, g, 0.05)), "concrete", 0.01)]
    collisions = [collision("concrete_col", pose6(0, 0, -0.025),
                            geom_box((g, g, 0.05)), 1.0)]
    return model_sdf("ground_8x8", visuals, collisions)


def build_arena_floor():
    h = L.FIELD_HALF * 2
    visuals = [visual("asphalt", pose6(0, 0, FLOOR_Z),
                      geom_box((h, h, 0.002)), "asphalt", 0.01)]
    return model_sdf("arena_floor_5x5", visuals, [])


# ------------------------------------------------------------------ 斜坡
def build_ramp_single():
    sp = L.RAMP_SINGLE_SPEC
    run, rise, bt = sp["length"], sp["rise"], sp["board_t"]
    alpha = math.atan2(rise, run)
    board_len = math.hypot(run, rise)
    # 板中心高度：坡面中点 rise/2 + 板厚一半沿法线方向的竖直分量
    zc = rise / 2 + (bt / 2) * math.cos(alpha)
    visuals = [visual("ramp_board", pose6(0, 0, zc, 0, -alpha, 0),
                      geom_box((board_len, sp["width"], bt)), "wood", 0.02)]
    collisions = [collision("ramp_board_col", pose6(0, 0, zc, 0, -alpha, 0),
                            geom_box((board_len, sp["width"], bt)), 0.7)]
    # 高边下方三个支撑木块（图 4：三个支撑木块）
    for i, y in enumerate((-0.42, 0.0, 0.42)):
        visuals.append(visual("support_%d" % i,
                              pose6(run / 2 - 0.055, y, (rise - 0.02) / 2),
                              geom_box((0.06, 0.08, rise - 0.02)), "wood_dark", 0.02))
        collisions.append(collision("support_%d_col" % i,
                                    pose6(run / 2 - 0.055, y, (rise - 0.02) / 2),
                                    geom_box((0.06, 0.08, rise - 0.02)), 0.7))
    return model_sdf("ramp_single_120", visuals, collisions)


def build_ramp_double():
    sp = L.RAMP_DOUBLE_SPEC
    run, rise, bt = sp["half_run"], sp["rise"], sp["board_t"]
    alpha = math.atan2(rise, run)
    board_len = math.hypot(run, rise)
    zc = rise / 2 + (bt / 2) * math.cos(alpha)
    visuals, collisions = [], []
    for side, sign in (("w", -1.0), ("e", 1.0)):
        cx = sign * run / 2
        pitch = sign * alpha  # 西侧板向 +x 升高；东侧板向 -x 升高
        visuals.append(visual("ramp_board_%s" % side,
                              pose6(cx, 0, zc, 0, -pitch, 0),
                              geom_box((board_len, sp["width"], bt)), "wood", 0.02))
        collisions.append(collision("ramp_board_%s_col" % side,
                                    pose6(cx, 0, zc, 0, -pitch, 0),
                                    geom_box((board_len, sp["width"], bt)), 0.7))
    # 脊线下方三个支撑木块
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
    # 头
    visuals.append(visual("head", pose6(0, y0, 0.062, math.pi / 2, 0, 0),
                          geom_cyl(0.030, 0.004), "target_dark", 0.02))
    # 肩 / 躯干
    visuals.append(visual("shoulder", pose6(0, y0, 0.036),
                          geom_box((0.150, 0.004, 0.024)), "target_dark", 0.02))
    visuals.append(visual("torso", pose6(0, y0 + 0.0002, 0.000),
                          geom_box((0.092, 0.004, 0.075)), "target_dark", 0.02))
    # 手臂
    for side in (-1, 1):
        visuals.append(visual("arm_%d" % side,
                              pose6(side * 0.064, y0, 0.006),
                              geom_box((0.020, 0.004, 0.070)), "target_dark", 0.02))
        visuals.append(visual("leg_%d" % side,
                              pose6(side * 0.024, y0, -0.072),
                              geom_box((0.026, 0.004, 0.070)), "target_dark", 0.02))
    # 胸口同心圆（自后向前叠放，形成明暗环）
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
    # 顶部橙色条 + 两行灰色文字条
    visuals.append(visual("header", pose6(0, y0, 0.082),
                          geom_box((0.200, 0.004, 0.026)), "qr_orange", 0.02))
    visuals.append(visual("text_1", pose6(0, y0, 0.052),
                          geom_box((0.150, 0.004, 0.008)), "qr_dark", 0.02))
    # 9×9 QR 模块
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
    """圆环触碰点（图 6）：蓝色圆环 + 黑色圆心，板面法线 +y。"""
    sp = L.RING_SPEC
    visuals = []
    seg = 16
    r_mid = sp["outer_r"] - sp["tube"] / 2
    for i in range(seg):
        phi = 2 * math.pi * i / seg
        x = r_mid * math.cos(phi)
        z = r_mid * math.sin(phi)
        pitch = -(phi + math.pi / 2)
        visuals.append(visual("ring_seg_%d" % i,
                              pose6(x, 0, z, 0, pitch, 0),
                              geom_box((2 * math.pi * r_mid / seg * 1.18,
                                        sp["tube"], sp["tube"])),
                              "ring_blue", 0.02))
    visuals.append(visual("ring_center",
                          pose6(0, 0.002, 0, math.pi / 2, 0, 0),
                          geom_cyl(sp["center_r"], 0.006), "ring_black", 0.02))
    return model_sdf(key, visuals, [])


# ------------------------------------------------------------------ 标牌
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
    # 立柱
    for side in (-1, 1):
        visuals.append(visual("post_%d" % side,
                              pose6(side * sp["post_dx"], 0, sp["post_h"] / 2),
                              geom_cyl(sp["post_r"], sp["post_h"]), "post_white", 0.02))
    # 牌面 + 彩色边框
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
    # 像素字
    cell = sp["cell"]
    total_w = len(text) * 4 * cell - cell
    x0 = -total_w / 2 + cell / 2
    for ci, ch in enumerate(text):
        pat = FONT3x5[ch]
        for row, line in enumerate(pat):
            for col, bit in enumerate(line):
                if bit != "1":
                    continue
                visuals.append(visual(
                    "font_%d_%d_%d" % (ci, row, col),
                    pose6(x0 + ci * 4 * cell + col * cell, -bt_ / 2 - 0.0012,
                          sp["board_z"] + (2 - row) * cell),
                    geom_box((cell * 0.96, 0.003, cell * 0.96)), color_key, 0.02))
    return model_sdf(key, visuals, [])


# ------------------------------------------------------------------ 其他
def build_gate_post():
    visuals = [
        visual("post", pose6(0, 0, 0.25), geom_cyl(0.028, 0.50), "gate_red", 0.02),
        visual("band", pose6(0, 0, 0.40), geom_cyl(0.030, 0.10), "post_white", 0.02),
    ]
    collisions = [collision("post_col", pose6(0, 0, 0.25), geom_cyl(0.028, 0.50))]
    return model_sdf("gate_post", visuals, collisions)


def build_spawn_marker():
    visuals = [
        visual("disc_outer", pose6(0, 0, 0.0020), geom_cyl(0.36, 0.003), "marker_green", 0.02),
        visual("disc_inner", pose6(0, 0, 0.0036), geom_cyl(0.30, 0.003), "post_white", 0.02),
        visual("arrow_shaft", pose6(0.04, 0, 0.0048),
               geom_box((0.40, 0.05, 0.004)), "marker_green", 0.02),
        visual("arrow_head_up", pose6(-0.20, 0.048, 0.0048, 0, 0, math.radians(37)),
               geom_box((0.16, 0.045, 0.004)), "marker_green", 0.02),
        visual("arrow_head_dn", pose6(-0.20, -0.048, 0.0048, 0, 0, math.radians(-37)),
               geom_box((0.16, 0.045, 0.004)), "marker_green", 0.02),
    ]
    return model_sdf("spawn_marker", visuals, [])


# ------------------------------------------------------------------ 世界文件
def build_world():
    lines = [
        '<?xml version="1.0" ?>',
        '<sdf version="1.6">',
        '  <world name="zhirong_arena">',
        '    <!-- 反恐搜救赛项比赛场地：5 m x 5 m，16 单元格；x 东 / y 北 / 原点=场地中心 -->',
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
        '    <!-- 太阳光（正午偏西南方向，带阴影） -->',
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
        '    <!-- GUI 相机预设：斜俯视整块场地（gui:=true 时可直接截图） -->',
        '    <gui fullscreen="0">',
        '      <camera name="user_camera">',
        '        <pose>-3.5 -4.5 5.5 0 0.75 0.55</pose>',
        '        <view_controller>orbit</view_controller>',
        '      </camera>',
        '    </gui>',
        '',
        '    <!-- ============ 地面与场地 ============ -->',
    ]

    def inc(model, name, x, y, z=0.0, yaw=0.0):
        return ("    <include>\n"
                "      <uri>model://%s</uri>\n"
                "      <name>%s</name>\n"
                "      <pose>%s</pose>\n"
                "    </include>" % (model, name, pose6(x, y, z, 0, 0, yaw)))

    lines.append(inc("ground_8x8", "ground", 0, 0))
    lines.append(inc("arena_floor_5x5", "arena_floor", 0, 0))
    lines.append(inc("zone_yellow_cross", "zone_yellow",
                     L.YELLOW_CENTER[0], L.YELLOW_CENTER[1]))
    lines.append(inc("zone_orange_disc", "zone_orange_ramp_1",
                     L.ORANGE_ZONES[0]["center"][0], L.ORANGE_ZONES[0]["center"][1]))
    lines.append(inc("zone_orange_disc", "zone_orange_ramp_2",
                     L.ORANGE_ZONES[1]["center"][0], L.ORANGE_ZONES[1]["center"][1]))
    lines.append(inc("zone_red", "zone_red",
                     L.RED_ZONE["center"][0], L.RED_ZONE["center"][1]))
    lines.append(inc("cell_grid", "cell_grid", 0, 0))
    lines.append(inc("boundary_red", "boundary_red", 0, 0))
    lines.append('')
    lines.append('    <!-- ============ 迷彩围挡 / 障碍 ============ -->')
    for w in L.WORLD_WALLS:
        lines.append(inc(w["model"], w["name"], w["x"], w["y"], 0.0, w["yaw"]))
    lines.append('')
    lines.append('    <!-- ============ 斜坡（桔区） ============ -->')
    for r in L.RAMPS:
        lines.append(inc(r["model"], r["name"], r["x"], r["y"], 0.0, r["yaw"]))
    lines.append('')
    lines.append('    <!-- ============ 目标物（身靶 / 胸靶 / 二维码） ============ -->')
    for t in L.TARGETS:
        lines.append(inc(t["model"], t["name"], t["x"], t["y"], t["z"], t["yaw"]))
    lines.append('')
    lines.append('    <!-- ============ 触碰圆环（5 个） ============ -->')
    for r in L.TOUCH_RINGS:
        lines.append(inc("touch_ring", r["name"], r["x"], r["y"], r["z"], r["yaw"]))
    lines.append('')
    lines.append('    <!-- ============ 入口 / 出口标牌、门柱、出生点 ============ -->')
    for s in L.SIGNS:
        lines.append(inc(s["model"], s["name"], s["x"], s["y"], 0.0, s["yaw"]))
    for g in L.GATE_POSTS:
        lines.append(inc("gate_post", g["name"], g["x"], g["y"]))
    lines.append(inc("spawn_marker", "spawn_marker", L.SPAWN["x"], L.SPAWN["y"]))
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
        i0 = max(0, int((cx - (abs(sx / 2 * c) + abs(sy / 2 * s)) + MAP_HALF) / MAP_RES) - 1)
        i1 = min(n - 1, int((cx + (abs(sx / 2 * c) + abs(sy / 2 * s)) + MAP_HALF) / MAP_RES) + 1)
        j0 = max(0, int((cy - (abs(sx / 2 * s) + abs(sy / 2 * c)) + MAP_HALF) / MAP_RES) - 1)
        j1 = min(n - 1, int((cy + (abs(sx / 2 * s) + abs(sy / 2 * c)) + MAP_HALF) / MAP_RES) + 1)
        for j in range(j0, j1 + 1):
            cy_ = -MAP_HALF + (j + 0.5) * MAP_RES
            for i in range(i0, i1 + 1):
                cx_ = -MAP_HALF + (i + 0.5) * MAP_RES
                dx, dy = cx_ - cx, cy_ - cy
                u = dx * c + dy * s
                v = -dx * s + dy * c
                if abs(u) <= sx / 2 and abs(v) <= sy / 2:
                    row = n - 1 - j          # 图像第 0 行 = y 最大处
                    grid[row * n + i] = 0

    for r in L.iter_wall_rects():
        mark_rect(r["center"][0], r["center"][1], r["size"][0], r["size"][1], r["yaw"])
    for r in L.RAMPS:
        spec = L.RAMP_SINGLE_SPEC if r["model"] == "ramp_single_120" else L.RAMP_DOUBLE_SPEC
        mark_rect(r["x"], r["y"], spec["length"], spec["width"], r["yaw"])
    for s in L.SIGNS:
        mark_rect(s["x"], s["y"], L.SIGN_SPEC["board_w"], 0.2, s["yaw"])
    for g in L.GATE_POSTS:
        mark_rect(g["x"], g["y"], 0.06, 0.06)
    return n, grid


def write_map(path_dir):
    n, grid = build_map()
    os.makedirs(path_dir, exist_ok=True)
    pgm = os.path.join(path_dir, "zhirong_arena.pgm")
    with open(pgm, "wb") as fh:
        fh.write(b"P5\n# zhirong_arena occupancy grid, 0.05 m/px, origin (-4,-4)\n")
        fh.write(("%d %d\n255\n" % (n, n)).encode())
        fh.write(grid.tobytes())
    yaml_txt = "\n".join([
        "image: zhirong_arena.pgm",
        "resolution: 0.050000",
        "origin: [-4.000000, -4.000000, 0.000000]",
        "negate: 0",
        "occupied_thresh: 0.65",
        "free_thresh: 0.196",
        "",
    ])
    with open(os.path.join(path_dir, "zhirong_arena.yaml"), "w") as fh:
        fh.write(yaml_txt)
    return n, grid


# ------------------------------------------------------------------ 自检
def sanity_checks():
    """几何自检：墙体是否越界、障碍之间是否重叠、目标/圆环是否贴在墙面上。"""
    problems = []
    boxes = []
    for w in L.WORLD_WALLS:
        b = L.wall_world_bbox(w["model"], w["x"], w["y"], w["yaw"])
        boxes.append((w["name"], b))
        if b[0] < -L.FIELD_HALF - 0.01 or b[2] > L.FIELD_HALF + 0.01 or \
           b[1] < -L.FIELD_HALF - 0.01 or b[3] > L.FIELD_HALF + 0.01:
            problems.append("墙体越出场地: %s bbox=%s" % (w["name"], b))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0.005 and oy > 0.005:
                problems.append("墙体重叠: %s <-> %s (%.3f x %.3f m)"
                                % (boxes[i][0], boxes[j][0], ox, oy))
    # 目标板 / 圆环是否贴在某个墙面上
    rects = list(L.iter_wall_rects())
    for item in L.TARGETS + L.TOUCH_RINGS:
        nx, ny = -math.sin(item["yaw"]), math.cos(item["yaw"])
        best = 1e9
        for r in rects:
            c, (sx, sy), yaw = r["center"], r["size"], r["yaw"]
            dx, dy = item["x"] - c[0], item["y"] - c[1]
            cc, ss = math.cos(yaw), math.sin(yaw)
            u, v = dx * cc + dy * ss, -dx * ss + dy * cc
            du = max(abs(u) - sx / 2, 0.0)
            dv = max(abs(v) - sy / 2, 0.0)
            best = min(best, math.hypot(du, dv))
        if best > 0.02:
            problems.append("%s 离最近墙面 %.3f m（应贴墙）" % (item["name"], best))
    # 出生点必须在场地外、8 m 地面内
    sx_, sy_ = L.SPAWN["x"], L.SPAWN["y"]
    if not (L.FIELD_HALF < sx_ < L.GROUND_SIZE / 2 - 0.4 and
            abs(sy_) < L.GROUND_SIZE / 2 - 0.4):
        problems.append("出生点不在入口外侧地面内: (%.2f, %.2f)" % (sx_, sy_))
    return problems


# ------------------------------------------------------------------ main
MODEL_BUILDERS = {}

# 用一次性注册的方式填充模型清单
def _register_models():
    for key, spec in L.WALL_MODELS.items():
        MODEL_BUILDERS[key] = (lambda k=key, s=spec: build_wall_model(k, s), spec["desc"])
    MODEL_BUILDERS["zone_yellow_cross"] = (build_zone_yellow, "黄区（十字形黄色地面）")
    MODEL_BUILDERS["zone_orange_disc"] = (build_zone_orange, "桔区（斜坡下方橙色圆形地面）")
    MODEL_BUILDERS["zone_red"] = (build_zone_red, "红区（南侧中部红色地面）")
    MODEL_BUILDERS["cell_grid"] = (build_cell_grid, "16 单元格网格线（贴地细条）")
    MODEL_BUILDERS["boundary_red"] = (build_boundary, "红色比赛边界线（含入口/出口缺口）")
    MODEL_BUILDERS["ground_8x8"] = (build_ground, "8 m × 8 m 承载地面（水泥）")
    MODEL_BUILDERS["arena_floor_5x5"] = (build_arena_floor, "5 m × 5 m 场地地面（沥青）")
    MODEL_BUILDERS["ramp_single_120"] = (build_ramp_single,
                                         "单面斜坡 1.2×1.2×0.019 m，坡度 ≈9.5°，高边 0.20 m")
    MODEL_BUILDERS["ramp_double_120"] = (build_ramp_double,
                                         "双面斜坡（两块 0.6×1.2 对拼 A 字），脊高 0.20 m")
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
        print("  全部通过：墙体均在场内、障碍互不重叠、目标/圆环贴墙、出生点在入口外侧。")

    print("\n[布局摘要]")
    for w in L.WORLD_WALLS:
        print("  %-22s %-24s bbox=%s" % (w["name"], w["model"],
                                         tuple(round(v, 3) for v in
                                               L.wall_world_bbox(w["model"], w["x"],
                                                                 w["y"], w["yaw"]))))
    print("  出生点 spawn = (%.2f, %.2f, z=%.2f, yaw=%.2f)"
          % (L.SPAWN["x"], L.SPAWN["y"], L.SPAWN["z"], L.SPAWN["yaw"]))


if __name__ == "__main__":
    main()
