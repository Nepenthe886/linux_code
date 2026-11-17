# -*- coding: utf-8 -*-
"""zhirong_arena 场景布局唯一数据源（SI 单位：米 / 弧度）。

坐标系约定
----------
世界原点 = 5 m × 5 m 比赛场地中心；x 指向东，y 指向北，z 向上。
场地范围 x,y ∈ [-2.5, 2.5]，划分为 4×4 = 16 个 1.25 m 见方的单元格：
    行 A（北）、B、C、D（南）；列 1（西）、2、3、4（东）。
    单元格 A1 在西北角，D4 在东南角。

依据
----
所有尺寸取自《3.反恐搜救赛项规则.docx》：
  - 图 2 场地简略图（尺寸标注、分区、入口出口、障碍布置）
  - 图 4 斜坡规格：单面斜坡 1200×1200×19 mm，双面斜坡 600×1200×19 mm
  - 图 6 圆环触碰点：蓝色圆环 + 黑色圆心
  - 图 5/6/7 目标物：身靶、胸靶、二维码危险品
位置按图 2 的像素比例近似换算（红边界 bbox ↔ 5 m×5 m），允许 ±0.2 m 近似。

本模块只含纯数据与几何换算，不写文件；build_scene.py / make_plan.py 共用。
"""

import math

# ---------------------------------------------------------------- 场地常量
FIELD_HALF = 2.5          # 场地半边长（m），场地 5 m × 5 m
CELL = 1.25               # 单元格边长（m），4×4
WALL_H = 0.55             # 迷彩围挡墙高（m）
WALL_T = 0.06             # 围挡墙标准厚度（m）
GROUND_SIZE = 8.0         # 承载机器人的整块地面（m）
CELL_ROWS = ("A", "B", "C", "D")   # 北 -> 南
CELL_COLS = (1, 2, 3, 4)           # 西 -> 东


def cell_name(col, row):
    """col: 1..4（西->东），row: 0..3（北->南） -> 'A1' 等。"""
    return "%s%d" % (CELL_ROWS[row], CELL_COLS[col - 1])


def cell_center(col, row):
    """单元格中心的世界坐标（m）。"""
    x = -FIELD_HALF + (col - 0.5) * CELL
    y = FIELD_HALF - (row + 0.5) * CELL
    return (x, y)


# ---------------------------------------------------------------- 材质色
# (r, g, b)，alpha 固定 1.0
MATERIALS = {
    "concrete":     (0.56, 0.54, 0.50),   # 场外地面：水泥
    "asphalt":      (0.42, 0.41, 0.38),   # 场地内地面：沥青
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

# 迷彩补丁配色（在深橄榄灰墙体上拼贴的块状迷彩）
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


# ---------------------------------------------------------------- 墙体模型
# 每个模型 = 若干“面板”(panel)。面板在模型局部坐标系中给出：
#   (cx, cy, sx, sy[, yaw])
#   cx, cy : 面板中心（模型局部坐标，m）
#   sx, sy : 面板在自身局部 x / y 方向的尺寸（m），即未旋转时的盒子长宽
#   yaw    : 面板自身在模型局部系中的偏航角（弧度，缺省 0）
#            墙长沿 x 时 sx 取长度、sy 取厚度；墙长沿 y 时反之。迷彩补丁沿长边拼贴。
# 模型局部坐标系的 bbox 已按图中标注尺寸设计（长 × 宽 = dims）。
# 迷彩块由 build_scene.py 按面板长边自动拼贴（不依赖任何外部纹理/mesh）。
WALL_MODELS = {
    "l_wall_095x061": dict(
        desc="L 型迷彩墙 0.95×0.61 m（西北，黄区内）",
        dims=(0.95, 0.61), material="camo",
        panels=[(0.475, -0.03, 0.95, WALL_T), (0.03, -0.305, WALL_T, 0.61)],
    ),
    "l_wall_130x052": dict(
        desc="L 型迷彩墙 1.30×0.52 m（北边界中段）",
        dims=(1.30, 0.52), material="camo",
        panels=[(-0.65, -0.03, 1.30, WALL_T), (-0.03, -0.26, WALL_T, 0.52)],
    ),
    "l_wall_113x049": dict(
        desc="L 型迷彩墙 1.13×0.49 m（东北，入口内侧）",
        dims=(1.13, 0.49), material="camo",
        panels=[(0.565, 0.03, 1.13, WALL_T), (0.03, 0.245, WALL_T, 0.49)],
    ),
    "l_wall_112x060": dict(
        desc="L 型迷彩墙 1.12×0.60 m（中南部）",
        dims=(1.12, 0.60), material="camo",
        panels=[(0.56, 0.03, 1.12, WALL_T), (0.03, 0.30, WALL_T, 0.60)],
    ),
    "l_wall_114x048": dict(
        desc="L 型迷彩墙 1.14×0.48 m（东南）",
        dims=(1.14, 0.48), material="camo",
        panels=[(-0.57, -0.03, 1.14, WALL_T), (-0.03, -0.24, WALL_T, 0.48)],
    ),
    "t_wall_073x058": dict(
        desc="T 型迷彩墙 0.73×0.58 m（西侧两处）",
        dims=(0.73, 0.58), material="camo",
        panels=[(0.365, 0.0, 0.73, WALL_T), (0.03, 0.0, WALL_T, 0.58)],
    ),
    "t_wall_143x057": dict(
        desc="T 型迷彩墙 1.43×0.57 m（东南角）",
        dims=(1.43, 0.57), material="camo",
        panels=[(0.715, 0.0, 1.43, WALL_T), (0.03, 0.0, WALL_T, 0.57)],
    ),
    "thin_wall_085x008": dict(
        desc="薄墙板 0.85×0.08 m（东侧窄道）",
        dims=(0.85, 0.08), material="camo",
        panels=[(0.0, 0.0, 0.85, 0.08)],
    ),
    "a_frame_041x027": dict(
        desc="A 字架障碍 0.41×0.27 m（东北角）",
        dims=(0.41, 0.27), material="camo",
        # 两块板在平面内成 ∧ 形：顶点 (0, +0.135)，两只脚 (±0.205, -0.135)
        panels=[(-0.1025, 0.0, 0.34, WALL_T, math.radians(52.8)),
                (0.1025, 0.0, 0.34, WALL_T, math.radians(-52.8))],
    ),
    "i_obstacle_089x049": dict(
        desc="工型障碍 0.89×0.49 m（红区，红色涂装）",
        dims=(0.89, 0.49), material="red",
        panels=[(0.0, 0.195, 0.89, 0.10), (0.0, 0.0, 0.14, 0.49),
                (0.0, -0.195, 0.89, 0.10)],
    ),
    "red_barrier": dict(
        desc="红区围挡块 0.30×0.72 m（红色涂装，工型障碍左右）",
        dims=(0.30, 0.72), material="red",
        panels=[(0.0, 0.0, 0.30, 0.72)],
    ),
}

# 墙体/障碍在世界中的布置位姿。
# x, y = 模型局部原点（即上面 panels 坐标所在原点）的世界坐标；yaw = 绕 z 轴旋转。
WORLD_WALLS = [
    dict(model="l_wall_095x061", name="wall_l_095_061", x=-2.44, y=2.06, yaw=0.0,
         note="西北 L 墙，横臂沿北、竖臂沿西"),
    dict(model="t_wall_073x058", name="wall_t_073_058_nw", x=-2.41, y=0.649, yaw=0.0,
         note="西侧 T 墙（上）"),
    dict(model="t_wall_073x058", name="wall_t_073_058_sw", x=-2.41, y=-1.126, yaw=0.0,
         note="西侧 T 墙（下）"),
    dict(model="l_wall_130x052", name="wall_l_130_052", x=0.50, y=2.40, yaw=0.0,
         note="北边界 L 墙，竖臂在 -x 端向下"),
    dict(model="l_wall_113x049", name="wall_l_113_049", x=0.42, y=1.13, yaw=0.0,
         note="东北 L 墙，横臂沿东、竖臂沿北"),
    dict(model="l_wall_112x060", name="wall_l_112_060", x=-0.84, y=-0.35, yaw=0.0,
         note="中南部 L 墙，横臂沿东、竖臂沿北"),
    dict(model="l_wall_114x048", name="wall_l_114_048", x=2.40, y=-0.93, yaw=0.0,
         note="东南 L 墙，横臂沿西、竖臂沿南"),
    dict(model="t_wall_143x057", name="wall_t_143_057", x=2.35, y=-1.885, yaw=math.pi,
         note="东南 T 墙，横臂沿西、竖臂沿南"),
    dict(model="thin_wall_085x008", name="wall_thin_085_008", x=2.06, y=0.63, yaw=0.0,
         note="东侧薄墙板（贴近东边界）"),
    dict(model="a_frame_041x027", name="wall_a_frame_041_027", x=2.02, y=2.15, yaw=0.0,
         note="东北角 A 字架"),
    dict(model="i_obstacle_089x049", name="obstacle_i_089_049", x=-0.28, y=-1.98, yaw=0.0,
         note="红区工型障碍（南侧中部）"),
    dict(model="red_barrier", name="red_barrier_left", x=-1.30, y=-2.02, yaw=0.0,
         note="红区左侧围挡"),
    dict(model="red_barrier", name="red_barrier_right", x=0.60, y=-2.02, yaw=0.0,
         note="红区右侧围挡"),
]

# ---------------------------------------------------------------- 斜坡
RAMPS = [
    dict(model="ramp_single_120", name="ramp_1", x=0.95, y=0.35, yaw=0.0,
         note="斜坡 1：单面斜坡 1.2×1.2 m，坡度 ≈9.5°，坡向 +x（东），高边 0.20 m"),
    dict(model="ramp_double_120", name="ramp_2", x=-0.35, y=-1.05, yaw=0.0,
         note="斜坡 2：双面斜坡（两块 0.6×1.2 对拼成 A 字），脊线沿 x，脊高 0.20 m"),
]

# 斜坡规格（图 4）
RAMP_SINGLE_SPEC = dict(width=1.2, length=1.2, rise=0.20, board_t=0.019)
RAMP_DOUBLE_SPEC = dict(width=1.2, length=1.2, rise=0.20, board_t=0.019,
                        half_run=0.6)

# ---------------------------------------------------------------- 分区地面
# 黄区：左上十字形（图 2 中黄色填充区），中心在 (-1.25, +1.25)
YELLOW_CENTER = (-1.25, 1.25)
YELLOW_BARS = [           # (cx, cy, lx, ly, z_center) 相对十字中心
    (0.0, 0.0, 1.25, 2.50, 0.0030),   # 竖臂：宽 1.25，长 2.50（y 0 -> 2.5）
    (0.0, 0.0, 2.50, 1.25, 0.0038),   # 横臂：长 2.50（x -2.5 -> 0），高 1.25
]
# 桔区：斜坡下方的圆形橙色地面
ORANGE_ZONES = [
    dict(center=(0.95, 0.35), r=0.80, z=0.0046),
    dict(center=(-0.35, -1.05), r=0.80, z=0.0046),
]
# 红区：工型障碍所在的南侧中部红色地面
RED_ZONE = dict(center=(-0.30, -2.055), size=(2.30, 0.75), z=0.0054)

# 单元格网格线（细条贴地），单元格 4×4
GRID_LINES = [dict(center=(x, 0.0), size=(0.02, FIELD_HALF * 2), z=0.0072)
              for x in (-CELL, 0.0, CELL)] + \
             [dict(center=(0.0, y), size=(FIELD_HALF * 2, 0.02), z=0.0072)
              for y in (-CELL, 0.0, CELL)]

# 红色比赛边界线（宽 0.06 m 的贴地细条），
# 东侧 y∈[1.10,1.90] 留 0.80 m 入口缺口；西侧 y∈[-0.40,0.40] 留 0.80 m 出口缺口。
BOUNDARY_SEGMENTS = [
    dict(center=(0.0, FIELD_HALF), size=(FIELD_HALF * 2 + WALL_T, WALL_T)),   # 北
    dict(center=(0.0, -FIELD_HALF), size=(FIELD_HALF * 2 + WALL_T, WALL_T)),  # 南
    dict(center=(FIELD_HALF, 2.20), size=(WALL_T, 0.60)),                    # 东（缺口北侧）
    dict(center=(FIELD_HALF, -0.70), size=(WALL_T, 3.60)),                   # 东（缺口南侧）
    dict(center=(-FIELD_HALF, 1.45), size=(WALL_T, 2.10)),                   # 西（缺口北侧）
    dict(center=(-FIELD_HALF, -1.45), size=(WALL_T, 2.10)),                  # 西（缺口南侧）
]
ENTRANCE_GAP = dict(edge="east", x=FIELD_HALF, y=(1.10, 1.90), width=0.80)
EXIT_GAP = dict(edge="west", x=-FIELD_HALF, y=(-0.40, 0.40), width=0.80)

# ---------------------------------------------------------------- 目标物
# 白色目标板贴在墙面外侧（朝向场地），板面法线由 yaw 决定：
#   模型局部板面法线 = +y，世界法线 = (-sin(yaw), cos(yaw))
#   yaw = 0 -> 朝北(+y)；yaw = pi -> 朝南(-y)；yaw = -pi/2 -> 朝东(+x)；yaw = +pi/2 -> 朝西(-x)
TARGET_PLATE = dict(w=0.30, h=0.21, t=0.006, z_default=0.30)
TARGETS = [
    dict(model="target_hostage", name="target_hostage_1", x=-1.95, y=0.617, z=0.30,
         yaw=math.pi, note="身靶（模拟恐怖份子）：西侧 T 墙上横臂南面"),
    dict(model="target_chest", name="target_chest_1", x=-0.15, y=2.338, z=0.30,
         yaw=math.pi, note="胸靶（待救援对象）：北边界 L 墙南面"),
    dict(model="target_qr", name="target_qr_1", x=1.05, y=1.128, z=0.30,
         yaw=math.pi, note="二维码危险品：东北 L 墙南面"),
    dict(model="target_hostage", name="target_hostage_2", x=-0.30, y=-0.288, z=0.30,
         yaw=0.0, note="身靶：中南部 L 墙北面"),
    dict(model="target_qr", name="target_qr_2", x=1.85, y=-0.932, z=0.30,
         yaw=math.pi, note="二维码危险品：东南 L 墙南面"),
    dict(model="target_chest", name="target_chest_2", x=1.50, y=-1.853, z=0.30,
         yaw=0.0, note="胸靶：东南 T 墙北面"),
]

# ---------------------------------------------------------------- 圆环触碰点
RING_SPEC = dict(outer_r=0.118, tube=0.013, center_r=0.042, z_default=0.32)
TOUCH_RINGS = [
    dict(name="ring_1", x=-2.378, y=1.75, z=0.32, yaw=-math.pi / 2,
         note="西北 L 墙竖臂东面"),
    dict(name="ring_2", x=-1.90, y=0.681, z=0.32, yaw=0.0,
         note="西侧 T 墙上横臂北面"),
    dict(name="ring_3", x=0.482, y=1.40, z=0.32, yaw=-math.pi / 2,
         note="东北 L 墙竖臂东面"),
    dict(name="ring_4", x=-0.778, y=-0.05, z=0.32, yaw=-math.pi / 2,
         note="中南 L 墙竖臂东面"),
    dict(name="ring_5", x=2.338, y=-1.15, z=0.32, yaw=math.pi / 2,
         note="东南 L 墙竖臂西面"),
]

# ---------------------------------------------------------------- 标牌 / 门柱 / 出生点
SIGNS = [
    dict(model="sign_in", name="sign_entrance", x=2.78, y=2.30, yaw=math.radians(135),
         note="入口标牌（IN），位于东侧入口缺口外侧东北方向，牌面朝向场地内"),
    dict(model="sign_out", name="sign_exit", x=-2.78, y=0.0, yaw=math.radians(-90),
         note="出口标牌（OUT），位于西侧出口缺口外侧，牌面朝向场地内"),
]
SIGN_SPEC = dict(board_w=0.72, board_h=0.42, board_t=0.02, post_h=1.05,
                 post_r=0.03, post_dx=0.27, board_z=1.00, cell=0.048)

GATE_POSTS = [
    dict(name="gate_entrance_n", x=2.52, y=1.10),
    dict(name="gate_entrance_s", x=2.52, y=1.90),
    dict(name="gate_exit_n", x=-2.52, y=-0.40),
    dict(name="gate_exit_s", x=-2.52, y=0.40),
]

# 出生点：入口外侧（东边界外 0.4 m），朝向场地内（-x 方向，yaw = pi）
SPAWN = dict(x=2.90, y=1.60, z=0.05, yaw=math.pi)


# ---------------------------------------------------------------- 几何换算
def rot2(x, y, yaw):
    """二维绕原点旋转（逆时针，弧度）。"""
    c, s = math.cos(yaw), math.sin(yaw)
    return (x * c - y * s, x * s + y * c)


def panel_world_rect(inst, panel):
    """把模型局部的一个面板变换到世界坐标，返回 dict(center, size, yaw)。"""
    cx, cy, lx, ly = panel[0], panel[1], panel[2], panel[3]
    pyaw = panel[4] if len(panel) > 4 else 0.0
    ox, oy = rot2(cx, cy, inst["yaw"])
    return dict(center=(inst["x"] + ox, inst["y"] + oy),
                size=(lx, ly),
                yaw=inst["yaw"] + pyaw)


def iter_wall_rects(with_model=False):
    """遍历所有墙体面板的世界矩形（供平面图与占据栅格使用）。"""
    for inst in WORLD_WALLS:
        spec = WALL_MODELS[inst["model"]]
        for idx, panel in enumerate(spec["panels"]):
            r = panel_world_rect(inst, panel)
            r["name"] = "%s#%d" % (inst["name"], idx)
            r["material"] = spec["material"]
            r["desc"] = spec["desc"]
            if with_model:
                r["model"] = inst["model"]
            yield r


def wall_world_bbox(model_key, x, y, yaw):
    """给定模型与位姿，返回该墙体在世界系中的轴对齐 bbox (xmin,ymin,xmax,ymax)。"""
    inst = dict(x=x, y=y, yaw=yaw)
    xs, ys = [], []
    for panel in WALL_MODELS[model_key]["panels"]:
        r = panel_world_rect(inst, panel)
        c, (lx, ly), pyaw = r["center"], r["size"], r["yaw"]
        ext_x = abs(lx / 2 * math.cos(pyaw)) + abs(ly / 2 * math.sin(pyaw))
        ext_y = abs(lx / 2 * math.sin(pyaw)) + abs(ly / 2 * math.cos(pyaw))
        xs += [c[0] - ext_x, c[0] + ext_x]
        ys += [c[1] - ext_y, c[1] + ext_y]
    return (min(xs), min(ys), max(xs), max(ys))


def spawn_pose():
    """返回 (x, y, z, yaw)。"""
    return (SPAWN["x"], SPAWN["y"], SPAWN["z"], SPAWN["yaw"])
