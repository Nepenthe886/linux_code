# -*- coding: utf-8 -*-
"""zhirong_arena 场景布局唯一数据源（v2：按 16 单元格“先分块、再建模”）。

坐标系
------
世界原点 = 场地中心；x 向东，y 向北，z 向上。
16 个 1.25 m 单元格：行 A(北)→D(南)，列 1(西)→4(东)。
单元格 A1 在西北角、D4 在东南角；cell 名称如 "B3"。

分块方法（本版核心）
--------------------
每条障碍在 BLOCKS 表中登记：``cell``（A1..D4，或 "OUT-*" 表示红边界外）
+ 相对该单元格中心的局部偏移 ``(dx, dy)``（米）+ 模型 + 朝向。
``world_xy()`` 负责把“块 + 局部偏移”换算成世界坐标，build_scene.py 只从该表生成，
不再使用早期“红边界 bbox 双尺度拉伸 + 随手偏移”的做法。

图上像素 → 世界坐标
------------------
Lead 给定映射：x = (px - 507.5) * 0.0082645，y = (552.5 - py) * 0.0057143。
障碍**尺寸一律用图 2 的文字标注**（图 2 把障碍画得比实物大约 1.2~1.3 倍），
位置用该映射换算后按单元格归位。
"""

import math

# ---------------------------------------------------------------- 常量
FIELD_HALF = 2.5          # 16 单元格覆盖范围 5 m × 5 m
CELL = 1.25               # 单元格边长
WALL_H = 0.55             # 围挡墙高
WALL_T = 0.06             # 围挡墙厚
GROUND_SIZE = 8.0         # 承载地面 8 m × 8 m
FLOOR_SIZE = 5.5          # 场地铺装尺寸（略大于 5 m，用于容纳图 2 的红边界折线 bbox 5.09×5.22）
FLOOR_CENTER = (0.0, 0.0)

PX_SX = 0.0082645         # 图 2 像素 -> 世界 x 比例（Lead 提供）
PX_SY = 0.0057143         # 图 2 像素 -> 世界 y 比例
PX_CX = 507.5
PX_CY = 552.5

CELL_ROWS = ("A", "B", "C", "D")   # 北 -> 南
CELL_COLS = (1, 2, 3, 4)           # 西 -> 东


def px2world(px, py):
    """图 2 像素坐标 -> 世界坐标（米）。"""
    return ((px - PX_CX) * PX_SX, (PX_CY - py) * PX_SY)


def cell_name(col, row):
    """col: 1..4（西->东），row: 0..3（北->南）。"""
    return "%s%d" % (CELL_ROWS[row], CELL_COLS[col - 1])


def cell_center(name):
    """'A1'..'D4' -> 单元格中心世界坐标。"""
    row = CELL_ROWS.index(name[0])
    col = int(name[1])
    return (-FIELD_HALF + (col - 0.5) * CELL,
            FIELD_HALF - (row + 0.5) * CELL)


CELLS = {cell_name(c, r): cell_center(cell_name(c, r))
         for r in range(4) for c in (1, 2, 3, 4)}


def world_xy(block):
    """块表条目 -> 世界坐标 (x, y)。cell 为 OUT 时直接使用绝对坐标。"""
    if block.get("cell", "").startswith("OUT"):
        return block["pos"]
    cx, cy = CELLS[block["cell"]]
    return (cx + block["dx"], cy + block["dy"])


# ---------------------------------------------------------------- 材质色
MATERIALS = {
    "concrete":     (0.56, 0.54, 0.50),   # 场外地面：水泥
    "asphalt":      (0.40, 0.39, 0.37),   # 场地内铺装：沥青
    "grid":         (0.16, 0.16, 0.16),   # 单元格网格线
    "boundary_red": (0.85, 0.06, 0.06),   # 红色比赛边界线
    "zone_yellow":  (0.96, 0.84, 0.06),   # 黄区
    "zone_orange":  (0.98, 0.55, 0.02),   # 桔区
    "zone_red":     (0.72, 0.09, 0.09),   # 红区
    "camo_body":    (0.31, 0.34, 0.28),   # 迷彩墙基色（深橄榄灰）
    "red_panel":    (0.80, 0.08, 0.07),   # 红区障碍涂装
    "wood":         (0.66, 0.52, 0.32),   # 斜坡木工板
    "wood_dark":    (0.45, 0.34, 0.20),   # 斜坡支撑木块
    "plate_white":  (0.95, 0.95, 0.92),   # 目标板白底
    "target_dark":  (0.10, 0.13, 0.10),   # 目标人形/同心圆墨色
    "target_red":   (0.62, 0.10, 0.08),   # 胸靶外圈
    "qr_dark":      (0.05, 0.05, 0.05),   # 二维码黑块
    "qr_orange":    (0.93, 0.55, 0.05),   # 危险品标签色条
    "ring_blue":    (0.07, 0.17, 0.42),   # 触碰圆环蓝
    "ring_black":   (0.03, 0.03, 0.03),   # 触碰圆环圆心
    "sign_white":   (0.93, 0.93, 0.90),   # 标牌底板
    "sign_green":   (0.05, 0.42, 0.16),   # 入口绿
    "sign_red":     (0.75, 0.08, 0.07),   # 出口红
    "post_white":   (0.88, 0.88, 0.86),   # 立柱白
    "gate_red":     (0.80, 0.10, 0.08),   # 门柱红
    "marker_green": (0.05, 0.55, 0.20),   # 出生点标记绿
}

CAMO_PATCH_COLORS = (
    (0.72, 0.68, 0.55),   # 卡其
    (0.62, 0.65, 0.61),   # 灰绿
    (0.45, 0.48, 0.42),   # 中绿灰
    (0.16, 0.18, 0.16),   # 深灰
    (0.80, 0.77, 0.66),   # 浅沙
)
RED_PATCH_COLORS = (
    (0.60, 0.05, 0.05),
    (0.92, 0.18, 0.12),
    (0.72, 0.08, 0.06),
)


# ---------------------------------------------------------------- 障碍模型
# 面板 panel = (cx, cy, sx, sy[, yaw])：模型局部坐标（原点 = 障碍 bbox 中心）
#   （cx, cy）为面板中心，sx / sy 为盒子局部 x / y 尺寸，yaw 为该面板偏航角。
# 形状严格按图 2 放大裁剪图（z1..z4 / map_grid2）逐条判读：
#   l_wall_095x061  ┌ 顶横臂 + 左竖臂（开口朝 SE）
#   l_wall_130x052  ⌐ 顶横臂 + 右竖臂（开口朝 SW）
#   l_wall_113x049  └ 底横臂 + 左竖臂（开口朝 NE）
#   l_wall_114x048  ⌐ 顶横臂 + 右竖臂（开口朝 SW）
#   wall_z_112x060  Z 形：左上竖臂 + 中横臂 + 右下竖臂（图 2 实测，非简单 L）
#   t_wall_073x058  ⊢ 左竖臂通高 + 中横臂向东（图 2 实测；两处同形）
#   t_wall_143x057  ⊢ 左竖臂通高 + 中横臂向东
WALL_MODELS = {
    "l_wall_095x061": dict(
        desc="L 型迷彩墙 0.95×0.61 m（A1，西北；顶横臂+左竖臂，开口 SE）",
        dims=(0.95, 0.61), material="camo", shape="L",
        panels=[(0.0, 0.275, 0.95, WALL_T),
                (-0.445, 0.0, WALL_T, 0.61)],
    ),
    "l_wall_130x052": dict(
        desc="L 型迷彩墙 1.30×0.52 m（A2，北边界；顶横臂+右竖臂，开口 SW）",
        dims=(1.30, 0.52), material="camo", shape="L",
        panels=[(0.0, 0.230, 1.30, WALL_T),
                (0.620, 0.0, WALL_T, 0.52)],
    ),
    "l_wall_113x049": dict(
        desc="L 型迷彩墙 1.13×0.49 m（A3，东北；底横臂+左竖臂，开口 NE）",
        dims=(1.13, 0.49), material="camo", shape="L",
        panels=[(0.0, -0.215, 1.13, WALL_T),
                (-0.535, 0.0, WALL_T, 0.49)],
    ),
    "l_wall_114x048": dict(
        desc="L 型迷彩墙 1.14×0.48 m（C4，东南；顶横臂+右竖臂，开口 SW）",
        dims=(1.14, 0.48), material="camo", shape="L",
        panels=[(0.0, 0.210, 1.14, WALL_T),
                (0.540, 0.0, WALL_T, 0.48)],
    ),
    "wall_z_112x060": dict(
        desc="Z 型迷彩墙 1.12×0.60 m（C2；左上竖臂+中横臂+右下竖臂）",
        dims=(1.12, 0.60), material="camo", shape="Z",
        panels=[(-0.530, 0.150, WALL_T, 0.30),
                (0.0, 0.0, 1.12, WALL_T),
                (0.530, -0.150, WALL_T, 0.30)],
    ),
    "t_wall_073x058": dict(
        desc="T 型迷彩墙 0.73×0.58 m（B1/C1；左竖臂通高 + 中横臂向东）",
        dims=(0.73, 0.58), material="camo", shape="T",
        panels=[(-0.335, 0.0, WALL_T, 0.58),
                (0.0, 0.0, 0.73, WALL_T)],
    ),
    "t_wall_143x057": dict(
        desc="T 型迷彩墙 1.43×0.57 m（东南红线外；左竖臂通高 + 中横臂向东）",
        dims=(1.43, 0.57), material="camo", shape="T",
        panels=[(-0.685, 0.0, WALL_T, 0.57),
                (0.0, 0.0, 1.43, WALL_T)],
    ),
    "thin_wall_085x008": dict(
        desc="薄墙板 0.85×0.08 m（东侧红线外）",
        dims=(0.85, 0.08), material="camo", shape="bar",
        panels=[(0.0, 0.0, 0.85, 0.08)],
    ),
    "horiz_wall_100x006": dict(
        desc="背景横墙 1.00×0.06 m（东北红线外，图 2 右上角）",
        dims=(1.00, 0.06), material="camo", shape="bar",
        panels=[(0.0, 0.0, 1.00, WALL_T)],
    ),
    "a_frame_041x027": dict(
        desc="A 字架障碍 0.41×0.27 m（东北红线外）",
        dims=(0.41, 0.27), material="camo", shape="A",
        panels=[(-0.1025, 0.0, 0.34, WALL_T, math.radians(52.8)),
                (0.1025, 0.0, 0.34, WALL_T, math.radians(-52.8))],
    ),
    "i_obstacle_089x049": dict(
        desc="工型障碍 0.89×0.49 m（D2，红区，红色涂装）",
        dims=(0.89, 0.49), material="red", shape="I",
        panels=[(0.0, 0.195, 0.89, 0.10), (0.0, 0.0, 0.14, 0.49),
                (0.0, -0.195, 0.89, 0.10)],
    ),
    "red_barrier": dict(
        desc="红区围挡块 0.30×0.72 m（工型障碍左右，红色涂装）",
        dims=(0.30, 0.72), material="red", shape="block",
        panels=[(0.0, 0.0, 0.30, 0.72)],
    ),
}

# ---------------------------------------------------------------- 分块布局表
# 每条障碍 = 所在 cell + 相对单元格中心的局部偏移 (dx, dy)。
# cell 以 "OUT-" 开头表示位于红边界之外（用 pos 给绝对世界坐标）。
# 世界坐标由 px2world() 换算后再按 1.25 m 块归位；必要时做 ≤0.1 m 的块内微调，
# 微调原因写在 note 里。
BLOCKS = [
    # -------- A 行（北） --------
    dict(name="wall_l_095_061", model="l_wall_095x061", cell="A1",
         dx=-0.030, dy=-0.146, yaw=0.0,
         px=(277, 250), note="图2 西北 L 墙；顶边略压红边界（与图2 一致）"),
    dict(name="wall_l_130_052", model="l_wall_130x052", cell="A2",
         dx=0.369, dy=0.656, yaw=0.0,
         px=(477, 110), note="图2 北边界 L 墙，跨出北侧红折线（与图2 一致）"),
    dict(name="wall_l_113_049", model="l_wall_113x049", cell="A3",
         dx=0.655, dy=-0.415, yaw=0.0,
         px=(644, 308), note="图2 东北 L 墙，横臂压在红折线上；v3 按图 2 中心校正到 (1.28,1.46)"),
    dict(name="wall_a_frame_041_027", model="a_frame_041x027", cell="OUT-NE",
         pos=(3.05, 2.10), yaw=0.0, px=(862, 233),
         note="图2 右上红线外 A 字架；为避开出生点，较图像位置北移约 0.22 m"),
    dict(name="wall_horiz_100x006", model="horiz_wall_100x006", cell="OUT-NE",
         pos=(3.341, 2.749), yaw=0.0, px=(912, 71),
         note="图2 右上角背景横墙（图被裁切，长度取 1.0 m）"),
    # -------- B 行 --------
    dict(name="wall_t_073_058_nw", model="t_wall_073x058", cell="B1",
         dx=-0.137, dy=0.024, yaw=0.0,
         px=(264, 439), note="图2 西侧中 T 墙（竖臂通高、横臂居中东向）"),
    # -------- C 行 --------
    dict(name="wall_t_073_058_sw", model="t_wall_073x058", cell="C1",
         dx=-0.166, dy=-0.501, yaw=0.0,
         px=(260, 750), note="图2 西侧下 T 墙（同形）"),
    dict(name="wall_z_112_060", model="wall_z_112x060", cell="C2",
         dx=0.485, dy=0.225, yaw=0.0,
         px=(491, 623),
         note="图2 中南 Z 形墙；v3 按图 2 中心校正到 (-0.14,-0.40)"),
    dict(name="ramp_2", model="ramp_double_120", cell="C2",
         dx=-0.025, dy=-0.605, yaw=0.0,
         px=(429, 758),
         note="图2 斜坡2（双面 A 字，v3 缩小为 1.0×1.0）；中心 x 回到 -0.65（y 避让 Z 墙 -1.23）"),
    dict(name="wall_l_114_048", model="l_wall_114x048", cell="C4",
         dx=-0.144, dy=-0.564, yaw=0.0,
         px=(717, 760), note="图2 东南 L 墙（顶横臂+右竖臂）"),
    dict(name="ramp_1", model="ramp_single_120", cell="B3",
         dx=0.355, dy=-0.371, yaw=0.0,
         px=(621, 508),
         note="图2 斜坡1（单面，v3 缩小为 1.1×1.0），坡向 +x；x 微调 +0.04 避让 C2 Z 墙"),
    dict(name="wall_thin_085_008", model="thin_wall_085x008", cell="OUT-E",
         pos=(2.657, 0.632), yaw=0.0, px=(829, 442),
         note="图2 东侧薄墙（横跨东侧红折线，红线外）"),
    # -------- D 行（南） --------
    dict(name="obstacle_i_089_049", model="i_obstacle_089x049", cell="D2",
         dx=0.340, dy=-0.222, yaw=0.0,
         px=(473, 920), note="图2 南侧中部工型障碍（红区），跨南侧红边界一带"),
    dict(name="red_barrier_left", model="red_barrier", cell="D1",
         dx=0.575, dy=-0.225, yaw=0.0,
         px=(365, 917), note="图2 工型障碍左侧红块"),
    dict(name="red_barrier_right", model="red_barrier", cell="D3",
         dx=-0.034, dy=-0.225, yaw=0.0,
         px=(579, 917), note="图2 工型障碍右侧红块"),
    dict(name="wall_t_143_057", model="t_wall_143x057", cell="OUT-SE",
         pos=(3.215, -2.03), yaw=0.0, px=(907, 908),
         note="图2 右下 T 墙（横臂在图边被裁切）；为不超出 8 m 地面，整体西移 0.17 m"),
]
BLOCK_BY_NAME = {b["name"]: b for b in BLOCKS}


# ---------------------------------------------------------------- 红色比赛边界
# 由 image2 的红色线像素（RGB≈240,74,74）提取折点后，用 px2world() 映射。
# 两条折线（chain）之间的“断口”即入口 / 出口；缺口宽度按验收要求统一为 0.80 m。
# 入口：东北角门洞（图2 “入口”标注处），宽 0.80 m；
# 出口：西侧中部缺口，宽 0.80 m（图2 “出口”标注处）。
BOUNDARY_CHAINS_PX = [
    # chain A：出口缺口北端 -> 西边界 -> 西北 -> 北侧凸台 -> 入口缺口北端
    [(194, 537), (194, 188), (359, 188), (359, 86), (552, 86), (552, 166)],
    # chain B：入口缺口南端 -> 东侧折线 -> 东南 -> 南边界 -> 西边界 -> 出口缺口南端
    [(581, 300), (581, 324), (741, 324), (741, 711), (810, 711), (810, 810),
     (617, 810), (617, 1000), (326, 1000), (327, 813), (194, 812), (194, 677)],
]
# 图2 中从出口内侧伸出的短折线（贴地红线，无碰撞；按图保留以利比对）
BOUNDARY_SPUR_PX = [(194, 501), (361, 500), (360, 650), (547, 648), (545, 684)]

BOUNDARY_GAPS = dict(
    entrance=dict(px=((552, 166), (581, 300)), width=0.80),
    exit=dict(px=((194, 677), (194, 537)), width=0.80),
)


def boundary_world_chains():
    """返回世界坐标折线链 [[(x,y),...], ...]。"""
    return [[px2world(px, py) for px, py in chain] for chain in BOUNDARY_CHAINS_PX]


def boundary_world_spur():
    return [px2world(px, py) for px, py in BOUNDARY_SPUR_PX]


def boundary_gap_points():
    """返回 (入口P1, 入口P2, 出口P1, 出口P2) 世界坐标，用于门柱/标牌。"""
    e1, e2 = [px2world(*p) for p in BOUNDARY_GAPS["entrance"]["px"]]
    x1, x2 = [px2world(*p) for p in BOUNDARY_GAPS["exit"]["px"]]
    return e1, e2, x1, x2


# ---------------------------------------------------------------- 地面分区（图 2 填色区）
# 黄区：图 2 黄色填充 = 十字（横带 + 竖带，v3 修正左臂偏低问题）
YELLOW_ZONES = [   # (xmin, ymin, xmax, ymax) 世界坐标
    (-2.16, 1.33, 0.16, 2.52),    # 横带 2.32 × 1.19
    (-1.08, 0.13, 0.16, 1.33),    # 竖带 1.24 × 1.20
]
# 桔区半径见 ZONE_ORANGE_SPEC（斜坡下方橙色圆盘）
# 红区：工型障碍/红块附近的红色地面（图 2 红区 x[-1.47,0.85] y[-2.50,-1.67]）
RED_ZONE = dict(center=(-0.31, -2.085), size=(2.32, 0.83), z=0.0054)

# 单元格网格线（贴地细条，16 格）
GRID_LINES = [dict(center=(x, 0.0), size=(0.02, FIELD_HALF * 2), z=0.0072)
              for x in (-CELL, 0.0, CELL)] + \
             [dict(center=(0.0, y), size=(FIELD_HALF * 2, 0.02), z=0.0072)
              for y in (-CELL, 0.0, CELL)]

# ---------------------------------------------------------------- 斜坡（v3 按图 2 橙色椭圆缩小）
# 说明：图 4 的 1200×1200×19 / 600×1200×19 mm 是“整块木板规格”；
# 图 2 中斜坡实际摆放只是很小的橙色椭圆区域（ramp1 ≈1.13×1.04 m、ramp2 ≈1.03×0.53 m），
# 因此实际 footprint 按图 2 缩放为下方的 RAMP_SINGLE_SPEC / RAMP_DOUBLE_SPEC。
# 若需恢复成整板规格，只需改这两个常量（models/world/plan/栅格全部由它们派生）。
RAMP_SINGLE_SPEC = dict(width=1.0, length=1.1, rise=0.18, board_t=0.019)
RAMP_DOUBLE_SPEC = dict(width=1.0, length=1.0, rise=0.18, board_t=0.019,
                        half_run=0.5)
RAMP_SINGLE_PITCH = math.atan2(RAMP_SINGLE_SPEC["rise"],
                               RAMP_SINGLE_SPEC["length"])
RAMP_PITCH = math.atan2(RAMP_DOUBLE_SPEC["rise"], RAMP_DOUBLE_SPEC["half_run"])

# 桔区：斜坡下方橙色圆盘半径，约等于斜坡半长边（图 2 橙椭圆 1.13×1.04 / 1.03×0.53 m）
ZONE_ORANGE_SPEC = dict(ramp1_r=0.56, ramp2_r=0.52, z=0.0046)


# ---------------------------------------------------------------- 目标板 / 圆环（自动贴墙）
# 贴墙规则：给出（墙体实例名，面板序号，面朝向，沿面切向偏移）。
#   face: N/S/E/W = 该面板朝外法线方向；along = 沿面板长边（切向）的偏移（米）
# build_scene.py 根据面板在世界中的实际矩形计算目标板/圆环位姿，墙体移动时自动跟随。
TARGET_PLATE = dict(w=0.30, h=0.21, t=0.006, z=0.30, offset=0.003)
TARGETS = [
    dict(model="target_hostage", name="target_hostage_1",
         wall="wall_l_095_061", panel=0, face="S", along=0.10, z=0.30,
         note="身靶（模拟恐怖份子）：A1 L 墙顶横臂南面"),
    dict(model="target_chest", name="target_chest_1",
         wall="wall_l_130_052", panel=0, face="S", along=0.10, z=0.30,
         note="胸靶（待救援对象）：A2 L 墙顶横臂南面"),
    dict(model="target_qr", name="target_qr_1",
         wall="wall_l_113_049", panel=0, face="N", along=0.20, z=0.30,
         note="二维码危险品：A3 L 墙底横臂北面"),
    dict(model="target_hostage", name="target_hostage_2",
         wall="wall_z_112_060", panel=1, face="S", along=0.25, z=0.30,
         note="身靶：C2 Z 墙中横臂南面"),
    dict(model="target_qr", name="target_qr_2",
         wall="wall_l_114_048", panel=0, face="S", along=-0.20, z=0.30,
         note="二维码危险品：C4 L 墙顶横臂南面"),
    dict(model="target_chest", name="target_chest_2",
         wall="wall_t_143_057", panel=1, face="N", along=-0.25, z=0.30,
         note="胸靶：东南红线外 T 墙横臂北面"),
]
RING_SPEC = dict(outer_r=0.118, tube=0.014, center_r=0.042, z=0.32, offset=0.003)
TOUCH_RINGS = [
    dict(name="ring_1", wall="wall_l_095_061", panel=1, face="E", along=0.0,
         z=0.32, note="A1 L 墙左竖臂东面"),
    dict(name="ring_2", wall="wall_t_073_058_nw", panel=0, face="E", along=0.0,
         z=0.32, note="B1 T 墙竖臂东面"),
    dict(name="ring_3", wall="wall_l_113_049", panel=1, face="E", along=0.0,
         z=0.32, note="A3 L 墙左竖臂东面"),
    dict(name="ring_4", wall="wall_t_073_058_sw", panel=0, face="E", along=0.0,
         z=0.32, note="C1 T 墙竖臂东面"),
    dict(name="ring_5", wall="wall_l_114_048", panel=1, face="W", along=0.0,
         z=0.32, note="C4 L 墙右竖臂西面"),
]

# ---------------------------------------------------------------- 标牌 / 门柱 / 出生点
SIGN_SPEC = dict(board_w=0.72, board_h=0.42, board_t=0.02, post_h=1.05,
                 post_r=0.03, post_dx=0.27, board_z=1.00, cell=0.048)
SIGNS = [
    dict(model="sign_in", name="sign_entrance",
         pos=(1.15, 2.30), yaw=math.radians(135),
         note="入口标牌（IN）：东北门洞外侧，牌面朝向门洞"),
    dict(model="sign_out", name="sign_exit",
         pos=(-2.85, -0.31), yaw=math.radians(-90),
         note="出口标牌（OUT）：西侧出口缺口外侧，牌面朝东"),
]
_e1, _e2, _x1, _x2 = boundary_gap_points()
GATE_POSTS = [
    dict(name="gate_entrance_n", pos=_e1),
    dict(name="gate_entrance_s", pos=_e2),
    dict(name="gate_exit_n", pos=_x1),
    dict(name="gate_exit_s", pos=_x2),
]

# 出生点：入口（东北门洞）外侧的东北通道，朝场地内（-x，yaw = pi）
SPAWN = dict(x=2.90, y=1.60, z=0.05, yaw=math.pi)


# ---------------------------------------------------------------- 几何工具
def rot2(x, y, yaw):
    c, s = math.cos(yaw), math.sin(yaw)
    return (x * c - y * s, x * s + y * c)


def panel_world_rect(inst, panel):
    """模型局部面板 -> 世界矩形 dict(center, size, yaw)。inst 含 x,y,yaw。"""
    cx, cy, sx, sy = panel[0], panel[1], panel[2], panel[3]
    pyaw = panel[4] if len(panel) > 4 else 0.0
    ox, oy = rot2(cx, cy, inst["yaw"])
    return dict(center=(inst["x"] + ox, inst["y"] + oy),
                size=(sx, sy), yaw=inst["yaw"] + pyaw)


def block_instance(block):
    """块表条目 -> 带世界位姿的实例 dict（供 build/plan 使用）。"""
    x, y = world_xy(block)
    return dict(name=block["name"], model=block["model"], x=x, y=y,
                yaw=block.get("yaw", 0.0), cell=block.get("cell", ""),
                note=block.get("note", ""))


def instances():
    return [block_instance(b) for b in BLOCKS]


def iter_wall_rects(with_model=False):
    """遍历全部墙体面板的世界矩形（供平面图/占据栅格）。"""
    for inst in instances():
        spec = WALL_MODELS.get(inst["model"])
        if spec is None:        # 斜坡等非墙体模型由 build/map 单独处理
            continue
        for idx, panel in enumerate(spec["panels"]):
            r = panel_world_rect(inst, panel)
            r["name"] = "%s#%d" % (inst["name"], idx)
            r["material"] = spec["material"]
            r["desc"] = spec["desc"]
            if with_model:
                r["model"] = inst["model"]
            yield r


def wall_world_bbox(model_key, x, y, yaw):
    inst = dict(x=x, y=y, yaw=yaw)
    xs, ys = [], []
    for panel in WALL_MODELS[model_key]["panels"]:
        r = panel_world_rect(inst, panel)
        c, (sx, sy), pyaw = r["center"], r["size"], r["yaw"]
        ex = abs(sx / 2 * math.cos(pyaw)) + abs(sy / 2 * math.sin(pyaw))
        ey = abs(sx / 2 * math.sin(pyaw)) + abs(sy / 2 * math.cos(pyaw))
        xs += [c[0] - ex, c[0] + ex]
        ys += [c[1] - ey, c[1] + ey]
    return (min(xs), min(ys), max(xs), max(ys))


def instance_bbox(inst):
    """实例世界 bbox；斜坡用 1.2×1.2 足迹，其余用面板 bbox。"""
    if inst["model"] == "ramp_single_120":
        size = (RAMP_SINGLE_SPEC["length"], RAMP_SINGLE_SPEC["width"])
    elif inst["model"] == "ramp_double_120":
        size = (RAMP_DOUBLE_SPEC["length"], RAMP_DOUBLE_SPEC["width"])
    else:
        return wall_world_bbox(inst["model"], inst["x"], inst["y"], inst["yaw"])
    hx, hy = size[0] / 2, size[1] / 2
    return (inst["x"] - hx, inst["y"] - hy, inst["x"] + hx, inst["y"] + hy)


def attach_pose(wall_name, panel_idx, face, along, z, offset):
    """按“墙体实例 + 面板 + 面 + 切向偏移”计算贴墙位姿 -> (x, y, z, yaw)。

    face: N/S/E/W（面板外法线方向）；along: 沿面板长边的偏移。
    """
    inst = {b["name"]: b for b in instances()}[wall_name]
    spec = WALL_MODELS[inst["model"]]
    panel = spec["panels"][panel_idx]
    rect = panel_world_rect(inst, panel)
    (cx, cy), (sx, sy), yaw = rect["center"], rect["size"], rect["yaw"]
    c, s = math.cos(yaw), math.sin(yaw)
    if face in ("N", "S"):
        tangent = (c, s)              # 面板局部 x 方向
        sign = 1.0 if face == "N" else -1.0
        normal = (-s * sign, c * sign)
        u = 0.0                      # 切向基向量为面板局部 x
        half = sy / 2
    else:
        tangent = (-s, c)             # 面板局部 y 方向
        sign = 1.0 if face == "E" else -1.0
        normal = (c * sign, s * sign)
        u = 0.0
        half = sx / 2
    # 沿切向偏移 along（沿面板长边）
    px_ = cx + tangent[0] * along + normal[0] * (half + offset)
    py_ = cy + tangent[1] * along + normal[1] * (half + offset)
    yaw_map = {"N": 0.0, "S": math.pi, "E": -math.pi / 2, "W": math.pi / 2}
    return (px_, py_, z, yaw_map[face])


def spawn_pose():
    return (SPAWN["x"], SPAWN["y"], SPAWN["z"], SPAWN["yaw"])


def blocks_per_cell():
    """按单元格汇总障碍，供 README / 自检输出。"""
    table = {c: [] for c in CELLS}
    for b in BLOCKS:
        if b.get("cell", "").startswith("OUT"):
            table.setdefault("红线外", []).append(b["name"])
        else:
            table[b["cell"]].append(b["name"])
    return table
