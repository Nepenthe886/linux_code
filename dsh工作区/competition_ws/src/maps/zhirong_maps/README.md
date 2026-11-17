# zhirong_maps —— 反恐搜救赛项 Gazebo 比赛场景包（v2：分块布局）

按 2026“戎智杯”人形机器人开发设计大赛《**3.反恐搜救赛项规则**》图 2（比赛场地简略图）
复现的 **16 单元格（5 m × 5 m 范围）**反恐搜救比赛场地，供 **Gazebo Classic 11 / SDF 1.6** 加载，
用于环境探索、目标识别、圆环触碰/物资运输等科目的仿真联调。当前版本 **v3（微调）**。

- world：`worlds/zhirong_arena.world`（世界名 `zhirong_arena`，42 个 include）
- 全部场景元素只用 `box` / `cylinder` 等 **primitive 几何拼装**，**不依赖外部 mesh、纹理或 fuel URI**，完全离线可加载。
- 纯 Gazebo 资源包，**world 内不含 ROS 系统插件**（`libgazebo_ros_init.so` 等 SystemPlugin 只能由 `gzserver -s ...` 命令行加载）。

## v3 变更要点（相对 v2，用户第二轮反馈“斜坡太大”）

1. **斜坡与桔区按图 2 橙色椭圆缩小**（常量集中在 `scene_layout.py`）：
   - `RAMP_SINGLE_SPEC`：footprint **1.1(x)×1.0(y)** m、rise **0.18** m（坡向 +x，坡角 ≈9.3°）；
   - `RAMP_DOUBLE_SPEC`：footprint **1.0×1.0** m（脊沿 y、每侧坡 0.5 m）、rise **0.18** m，仍为 **Λ** 形；
   - `ZONE_ORANGE_SPEC`：桔区半径 **ramp1=0.56 m**（≈1.12 m 直径）、**ramp2=0.52 m**（≈1.04 m 直径），
     对应图 2 橙色椭圆（约 1.13×1.04 / 1.03×0.53 m），比 v2 的 r=0.80 明显缩小。
   - 说明：图 4 的 1200×1200×19 / 600×1200×19 mm 是**整块木板规格**；图 2 中实际摆放只是很小的橙色椭圆，
     故按图 2 缩放到上述 footprint。改回整板规格只需改这两个常量（模型/世界/平面图/栅格全部由它们派生）。
2. **黄区十字形状修正**：横带 `x∈[-2.16,0.16], y∈[1.33,2.52]`（2.32×1.19）+
   竖带 `x∈[-1.08,0.16], y∈[0.13,1.33]`（1.24×1.20），删除 v2 偏低的左臂块。
3. **红区地面**：`x∈[-1.47,0.85], y∈[-2.50,-1.67]`（2.32×0.83，v2 高 0.69）。
4. **块内残差校正**：A3 L 墙中心 → (1.28,1.46)；C2 Z 墙中心 → (−0.14,−0.40)；
   斜坡 2 中心 x 回到 **−0.65**（缩小后仅 y 方向避让 Z 墙到 −1.23）；A 字架保持 y=2.10（出生点安全偏移）。
5. 新增 **叠加校验图** `preview/scene/overlay_diff.png`（图 2 红线+障碍轮廓按 Lead 映射仿射叠加到 plan.png），
   残差表 `preview/scene/overlay_residuals.txt`；重新生成 `compare_topdown.png`。
6. 自检：斜坡 2 仍为 Λ、桔区半径与斜坡 footprint 半长边一致（|r−half|≤0.07 m）。

## v2 变更要点（相对 v1）

1. **改为“先分块、再建模”**：`scene_layout.BLOCKS` 表按 4×4=16 个 1.25 m 单元格登记每条障碍
   （`cell` + 相对格心的局部偏移 `(dx, dy)` + 模型 + 朝向），`world_xy()` 负责换算世界坐标；
   不再沿用 v1“红边界 bbox 双尺度拉伸 + 随手偏移”的做法。
2. **墙体尺寸严格用图 2 文字标注**（0.95×0.61、1.30×0.52、1.13×0.49、1.12×0.60、0.73×0.58 ×2、
   1.14×0.48、1.43×0.57、薄墙 0.85×0.08、A 字架 0.41×0.27、工型 0.89×0.49 m），墙高 0.55、厚 0.06。
3. **形状按图 2 放大裁剪图（z1..z4 / map_grid2）逐条判读并修正**：A1 L 墙（顶横+左竖）、A2 L 墙（顶横+右竖）、
   A3 L 墙（底横+左竖）、C4 L 墙（顶横+右竖）、C2 **Z 形墙**（左上竖+中横+右下竖）、
   B1/C1 **T 墙（竖臂通高 + 横臂居中东向）**、东南 T 墙、A 字架、薄墙、背景横墙。
4. **红边界按图 2 红色线像素（RGB≈240,74,74）提取折点后重建成不规则折线**（不再是矩形），
   保留东偏北入口缺口 0.80 m、西中部出口缺口 0.80 m；图 2 出口内侧的短折线也按图保留（贴地红线，无碰撞）。
5. **修复斜坡 2 坡面倒置**：两块 0.6×1.2 板改为 **Λ 形**（西板 pitch = −0.3218、东板 pitch = +0.3218，
   x 为坡向，脊高 0.20 m、两侧落地，脊下 3 个支撑木块保持）；斜坡 1 单面坡向 +x（东）。
   （注：v3 已按图 2 橙色椭圆把斜坡缩小为 ramp1 1.1×1.0、ramp2 1.0×1.0、rise 0.18，见上。v2 的 Λ 形修正保持不变。）
6. 目标板 6 个、圆环 5 个改为 **按“墙体实例 + 面板 + 面朝向”自动贴墙**（`attach_pose()`），墙体移动后自动跟随。
7. 重新生成 `docs/plan.png`、`maps/zhirong_arena.pgm/.yaml`；新增 Gazebo 正俯视渲染
   `preview/scene/render_topdown.png` 与对比图 `preview/scene/compare_topdown.png`。

---

## 1. 数据来源与依据

| 依据 | 文件/图 | 用于 |
| --- | --- | --- |
| 规则正文 | `3.反恐搜救赛项规则.docx` 第四章 | 5 m×5 m、16 单元格、红线内为比赛边界、一个入口一个出口、黄/桔/红三区 |
| **图 2 场地简略图** | `preview/docx_media/image2.png`（971×1042） | 障碍种类/尺寸标注/开向、分区、入口出口、红边界折线 |
| 图 2 放大裁剪 | `preview/docx_media/z1..z4.png`、`map_grid2.png` | 逐块判读 L/Z/T/工型墙形状与红边界折点 |
| 图 4 斜坡规格 | `image4.png` | 单面 1200×1200×19；双面 600×1200×19（两块对拼）+ 三个支撑木块 |
| 图 5/6/7/8 | `image5..8` | 身靶 / 胸靶 / 二维码危险品 / 圆环触碰点样式 |

**像素 → 世界映射**（Lead 提供）：`x = (px − 507.5) × 0.0082645`，`y = (552.5 − py) × 0.0057143`。
图 2 为手绘示意图：纵横比例不一致（≈121 vs ≈175 px/m）、障碍画得比实物大约 1.2~1.3 倍，
因此**尺寸一律以文字标注为准**，位置按该映射换算后**按单元格归位**。

---

## 2. 目录结构

```text
competition_ws/src/maps/zhirong_maps/
├── package.xml / CMakeLists.txt      # ament_cmake 资源包（install worlds models launch maps docs）
├── README.md
├── worlds/zhirong_arena.world        # SDF 1.6，42 个 include
├── launch/zhirong_arena.launch.py    # gazebo_ros gzserver + 可选 gzclient（gui 默认 false）
├── models/                           # 30 个模型，每个 model.config + model.sdf
│   ├── ground_8x8/  arena_floor/  cell_grid/  boundary_red/
│   ├── zone_yellow/  zone_orange_ramp1/  zone_orange_ramp2/  zone_red/
│   ├── l_wall_095x061/  l_wall_130x052/  l_wall_113x049/  l_wall_114x048/  wall_z_112x060/
│   ├── t_wall_073x058/  t_wall_143x057/  thin_wall_085x008/  horiz_wall_100x006/  a_frame_041x027/
│   ├── i_obstacle_089x049/  red_barrier/
│   ├── ramp_single_120/  ramp_double_120/
│   ├── target_hostage/  target_chest/  target_qr/  touch_ring/
│   └── sign_in/  sign_out/  gate_post/  spawn_marker/
├── maps/zhirong_arena.pgm + .yaml    # 0.05 m/px，160×160，origin [-4,-4,0]
└── docs/plan.png                     # 俯视布置图（4200×4200 px，300 dpi）
```

生成/验证脚本在同仓库 `preview/scene/`：
`scene_layout.py`（唯一数据源：分块表/红边界/贴墙规则）、`build_scene.py`（生成 models/world/map + 自检）、
`make_plan.py`（plan.png）、`render_topdown.py`（Xvfb + gzclient 渲染 + compare 图）。
产物：`preview/scene/{render_topdown.png, compare_topdown.png, render_raw.png, layout_report.txt, VERIFICATION.md}`。

---

## 3. 坐标系与分块方法

- 世界原点 = 场地中心；**x 东 / y 北 / z 上**；右手系。
- 16 个单元格：边长 **1.25 m**，`行 A(北)→D(南)`、`列 1(西)→4(东)`，A1=西北、D4=东南。
  单元格中心：x = −2.5 + 1.25·(col−0.5)，y = 2.5 − 1.25·(row+0.5)。

| 行\列 | 1 (x=-1.875) | 2 (x=-0.625) | 3 (x=+0.625) | 4 (x=+1.875) |
| --- | --- | --- | --- | --- |
| **A** (y=+1.875) | A1 | A2 | A3 | A4 |
| **B** (y=+0.625) | B1 | B2 | B3 | B4 |
| **C** (y=-0.625) | C1 | C2 | C3 | C4 |
| **D** (y=-1.875) | D1 | D2 | D3 | D4 |

**分块建模**：`BLOCKS` 每条障碍 = `cell`（A1..D4 或 `OUT-*` 表示红边界外）+ 相对格心偏移 `(dx, dy)`（米）
+ 模型 + yaw。世界坐标 = 格心 + 偏移；`build_scene.py` 只从该表生成世界与模型，`make_plan.py` 共用同一数据源。

分块布局摘要（当前 `build_scene.py` 自检输出）：

| 单元格 | 放置内容 |
| --- | --- |
| A1 | `wall_l_095_061`（L 墙 0.95×0.61） |
| A2 | `wall_l_130_052`（L 墙 1.30×0.52，跨北侧红折线） |
| A3 | `wall_l_113_049`（L 墙 1.13×0.49，中心校正到 (1.28,1.46)，横臂压红折线，跨 A3/A4） |
| B1 | `wall_t_073_058_nw`（T 墙 0.73×0.58） |
| B3 | `ramp_1`（斜坡 1） |
| C1 | `wall_t_073_058_sw`（T 墙 0.73×0.58） |
| C2 | `wall_z_112_060`（Z 墙 1.12×0.60，中心 (−0.14,−0.40)）+ `ramp_2`（斜坡 2，1.0×1.0） |
| C4 | `wall_l_114_048`（L 墙 1.14×0.48） |
| D1 | `red_barrier_left`（红区围挡） |
| D2 | `obstacle_i_089_049`（工型障碍 0.89×0.49） |
| D3 | `red_barrier_right`（红区围挡） |
| 红线外 | `wall_thin_085_008`（东侧）、`wall_a_frame_041x027`（东北）、`wall_horiz_100x006`（东北角）、`wall_t_143_057`（东南） |

---

## 4. 墙体 / 障碍清单（世界坐标，单位 m）

墙高 **0.55 m**、厚 **0.06 m**；L/T 型墙的局部原点 = 整体 bbox 中心。
`k` 列 = 相对单元格中心的局部偏移（与 `scene_layout.BLOCKS` 一致）。

| 世界名 | cell | 模型 | 标注尺寸 | k=(dx,dy) | 世界中心 | 世界 bbox | 形状（按图 2 判读） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `wall_l_095_061` | A1 | `l_wall_095x061` | 0.95×0.61 | (−0.030, −0.146) | (−1.905, 1.729) | (−2.38,1.42)–(−1.43,2.03) | L：顶横臂 + 左竖臂（开口 SE） |
| `wall_l_130_052` | A2 | `l_wall_130x052` | 1.30×0.52 | (+0.369, +0.656) | (−0.256, 2.531) | (−0.91,2.27)–(0.39,2.79) | L：顶横臂 + 右竖臂（开口 SW），跨北侧红折线 |
| `wall_l_113_049` | A3 | `l_wall_113x049` | 1.13×0.49 | (+0.655, −0.415) | (1.280, 1.460) | (0.71,1.21)–(1.84,1.71) | L：底横臂 + 左竖臂（开口 NE） |
| `wall_t_073_058_nw` | B1 | `t_wall_073x058` | 0.73×0.58 | (−0.137, +0.024) | (−2.012, 0.649) | (−2.38,0.36)–(−1.65,0.94) | T：竖臂通高 + 横臂居中东向 |
| `wall_t_073_058_sw` | C1 | `t_wall_073x058` | 0.73×0.58 | (−0.166, −0.501) | (−2.041, −1.126) | (−2.41,−1.42)–(−1.68,−0.84) | T：同形 |
| `wall_z_112_060` | C2 | `wall_z_112x060` | 1.12×0.60 | (+0.485, +0.225) | (−0.140, −0.400) | (−0.70,−0.70)–(0.42,−0.10) | Z：左上竖臂 + 中横臂 + 右下竖臂 |
| `wall_l_114_048` | C4 | `l_wall_114x048` | 1.14×0.48 | (−0.144, −0.564) | (1.731, −1.189) | (1.16,−1.43)–(2.30,−0.95) | L：顶横臂 + 右竖臂（开口 SW） |
| `obstacle_i_089_049` | D2 | `i_obstacle_089x049` | 工型 0.89×0.49 | (+0.340, −0.222) | (−0.285, −2.097) | (−0.73,−2.34)–(0.16,−1.85) | 工：上/下翼缘 + 中腹板（红色涂装） |
| `red_barrier_left` | D1 | `red_barrier` | 0.30×0.72 | (+0.575, −0.225) | (−1.300, −2.100) | (−1.45,−2.46)–(−1.15,−1.74) | 红区围挡块 |
| `red_barrier_right` | D3 | `red_barrier` | 0.30×0.72 | (−0.034, −0.225) | (0.591, −2.100) | (0.44,−2.46)–(0.74,−1.74) | 红区围挡块 |
| `wall_thin_085_008` | OUT-E | `thin_wall_085x008` | 0.85×0.08 | — | (2.657, 0.632) | (2.23,0.59)–(3.08,0.67) | 薄墙（横跨东侧红折线，红线外） |
| `wall_a_frame_041x027` | OUT-NE | `a_frame_041x027` | 0.41×0.27 | — | (3.050, 2.100) | (2.82,1.95)–(3.28,2.25) | ∧ 形（两块板 52.8°） |
| `wall_horiz_100x006` | OUT-NE | `horiz_wall_100x006` | 1.00×0.06 | — | (3.341, 2.749) | (2.84,2.72)–(3.84,2.78) | 图 2 右上角背景横墙（原图被裁切，长度取 1.0） |
| `wall_t_143_057` | OUT-SE | `t_wall_143x057` | 1.43×0.57 | — | (3.215, −2.030) | (2.50,−2.31)–(3.93,−1.74) | T：竖臂通高 + 横臂东向（横臂在图边被裁切） |

> **关于 0.73×0.58 两处形状**：v2 按图 2 放大裁剪图（4× 放大）逐像素判读，两处均为
> **竖臂通高 + 横臂居中东向（⊢ 形，T 型）**，不是 L 形——横臂在竖臂中部（约 45% 高度），
> 见 `preview/scene/analysis/zoom_W73_B1.png`。同理 C2 的 1.12×0.60 为 **Z 形**（左上竖+中横+右下竖），
> 见 `zoom_L112.png`。若验收希望改为 Lead 描述的 L 形，只需改 `scene_layout.WALL_MODELS` 里对应面板列表。

---

## 5. 红色比赛边界（按图 2 红色线像素重建）

红色线像素 RGB≈(240,74,74)，提取折点后用 `px2world()` 映射，两条折线之间的断口即入口/出口。
折线（世界坐标，单位 m）：

```text
chain0（出口缺口北端 → 西边界 → 西北凸台 → 入口缺口北端）:
  (-2.59,0.09) → (-2.59,2.08) → (-1.23,2.08) → (-1.23,2.67) → (0.37,2.67) → (0.37,2.21)
chain1（入口缺口南端 → 东侧折线 → 东南 → 南边界 → 西边界 → 出口缺口南端）:
  (0.61,1.44) → (0.61,1.31) → (1.93,1.31) → (1.93,-0.91) → (2.50,-0.91) → (2.50,-1.47)
  → (0.90,-1.47) → (0.90,-2.56) → (-1.50,-2.56) → (-1.49,-1.49) → (-2.59,-1.48) → (-2.59,-0.71)
```

| 缺口 | 位置 | 宽度 | 端点 |
| --- | --- | --- | --- |
| **入口** | 东北角门洞（图 2 “入口”标注处） | **0.80 m** | (0.37,2.21) – (0.61,1.44) |
| **出口** | 西侧中部（图 2 “出口”标注处） | **0.80 m** | (−2.59,−0.71) – (−2.59,0.09) |

另按图 2 保留出口内侧的短折线（贴地红线，无碰撞）：
`(-2.59,0.30) → (-1.23,0.30) → (-1.23,-0.56) → (0.33,-0.55) → (0.31,-0.75)`。

红折线 bbox ≈ x[−2.59, 2.50]、y[−2.56, 2.67]（≈5.09×5.22 m，与“整体 5m×5m 外包（约）”一致），
因此场地铺装取 **5.5 m × 5.5 m**（包住红折线），16 单元格仍为严格 5 m × 5 m。

---

## 6. 黄 / 桔 / 红三区

| 区域 | 范围（世界坐标，m） | 依据 |
| --- | --- | --- |
| **黄区** | 横带 x[−2.16,0.16] × y[1.33,2.52]（2.32×1.19）+ 竖带 x[−1.08,0.16] × y[0.13,1.33]（1.24×1.20） | 图 2 黄色十字填充（v3 修正） |
| **桔区** | 圆盘：斜坡 1 中心 (0.98,0.254) r=**0.56**、斜坡 2 中心 (−0.65,−1.23) r=**0.52** | 图 2 两个橙色椭圆（≈1.13×1.04 / 1.03×0.53 m） |
| **红区** | x[−1.47,0.85] × y[−2.50,−1.67]（2.32×0.83） | 图 2 工型障碍/红块所在红色区域（v3 加高） |

---

## 7. 斜坡与桔区（图 4 整板规格 + 图 2 椭圆缩放；v2 修复坡面倒置，v3 缩小）

> 图 4 中 单面斜坡 1200×1200×19 mm、双面 2×600×1200×19 mm 是**整块木板规格**；
> 图 2 中斜坡实际占位只是很小的橙色椭圆（约 1.13×1.04 / 1.03×0.53 m），
> 因此 v3 按图 2 缩放到下表 footprint（常量 `RAMP_SINGLE_SPEC` / `RAMP_DOUBLE_SPEC` /
> `ZONE_ORANGE_SPEC` 集中管理，可一键改回整板规格）。

| 世界名 | cell | 模型 | footprint / 规格 | 位姿 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `ramp_1` | B3 | `ramp_single_120` | 单面 **1.1(x)×1.0(y)** m，rise 0.18 m，板厚 0.019 | (0.980, 0.254, yaw=0) | 坡角 ≈9.3°，**坡向 +x（东）**（pitch −0.1622）；高边下 3 个支撑木块；桔区 r=0.56 |
| `ramp_2` | C2 | `ramp_double_120` | 双面 **1.0×1.0** m（每侧坡 0.5），rise 0.18 m | (−0.650, −1.230, yaw=0) | **Λ 形**：西板 pitch −0.3456、东板 pitch +0.3456，脊线沿 y、脊高 0.18 m，两侧落地；脊下 3 个支撑木块；桔区 r=0.52 |

**倒置修复说明**：v1 中两块板的 pitch 符号写反（西板 +0.3218 / 东板 −0.3218），两块板在中间凹成 **V**；
v2 改为 **Λ**：模型局部 x 为坡向，西板（x<0）pitch = −α 使 +x 端抬高，东板（x>0）pitch = +α 使 −x 端抬高，
两块板在 x=0 处汇于脊线（z≈0.209 m），两侧落在 z≈0.009 m。俯视渲染中可见两条坡面在中线对拼。

---

## 8. 目标物（6）与圆环（5）——自动贴墙

目标板白底 0.30×0.21×0.006 m，中心高 z=0.30 m；圆环外缘 r=0.118、黑圆心 r=0.042，z=0.32 m。
贴墙规则：`attach_pose(墙体实例, 面板序号, 面朝向 N/S/E/W, 沿面切向偏移)` → 位姿由墙体面板实际矩形计算，
墙体移动后自动跟随（不再手写坐标）。

| 目标 | 类型 | 贴附墙体/面 | 世界位姿 (x,y,z,yaw) |
| --- | --- | --- | --- |
| `target_hostage_1` | 身靶 | `wall_l_095_061` 顶横臂南面 | (−1.805, 1.971, 0.30, π) |
| `target_chest_1` | 胸靶 | `wall_l_130_052` 顶横臂南面 | (−0.156, 2.728, 0.30, π) |
| `target_qr_1` | 二维码危险品 | `wall_l_113_049` 底横臂北面 | (1.480, 1.278, 0.30, 0) |
| `target_hostage_2` | 身靶 | `wall_z_112_060` 中横臂南面 | (0.110, −0.433, 0.30, π) |
| `target_qr_2` | 二维码危险品 | `wall_l_114_048` 顶横臂南面 | (1.531, −1.012, 0.30, π) |
| `target_chest_2` | 胸靶 | `wall_t_143_057` 横臂北面 | (2.965, −1.997, 0.30, 0) |

| 圆环 | 贴附墙体/面 | 世界位姿 (x,y,z,yaw) |
| --- | --- | --- |
| `ring_1` | `wall_l_095_061` 左竖臂东面 | (−2.317, 1.729, 0.32, −π/2) |
| `ring_2` | `wall_t_073_058_nw` 竖臂东面 | (−2.314, 0.649, 0.32, −π/2) |
| `ring_3` | `wall_l_113_049` 左竖臂东面 | (0.778, 1.460, 0.32, −π/2) |
| `ring_4` | `wall_t_073_058_sw` 竖臂东面 | (−2.343, −1.126, 0.32, −π/2) |
| `ring_5` | `wall_l_114_048` 右竖臂西面 | (2.238, −1.189, 0.32, +π/2) |

## 9. 入口 / 出口标牌、门柱、出生点

| 元素 | 世界名 | 位姿 | 说明 |
| --- | --- | --- | --- |
| 入口标牌 | `sign_entrance` (`sign_in`) | (1.15, 2.30, yaw=135°) | 白底绿框 + 像素字母 **IN**，牌面朝东北门洞 |
| 出口标牌 | `sign_exit` (`sign_out`) | (−2.85, −0.31, yaw=−90°) | 白底红框 + 像素字母 **OUT**，牌面朝东（场地内） |
| 门柱 ×4 | `gate_entrance_n/s`、`gate_exit_n/s` | 入口 (0.37,2.21)/(0.61,1.44)；出口 (−2.59,0.09)/(−2.59,−0.71) | 红柱白环 h=0.5 m，位于缺口两端 |
| 出生点标记 | `spawn_marker` | (2.90, 1.60, 0, 0) | 绿色圆盘 + 指向 −x 的箭头（地面标记，无碰撞） |

**机器人出生点（与 v1 相同，launch 参数未改）**：

```text
x = +2.90   y = +1.60   z = 0.05   yaw = 3.1416 (π，朝向 -x 即场地内)
```

出生点在入口外侧的东北通道上（红边界外、8 m 地面内），机器人径 0.25 m，距最近墙面（A 字架）> 0.3 m。
东偏北入口门洞位于 (0.37,2.21)–(0.61,1.44)，机器人从出生点向西进入门洞后即进入场地。

---

## 10. 启动与构建

```bash
# 首次构建（资源包，无编译依赖）
cd /home/nepenthe/zmf/linux_code/dsh工作区/competition_ws
source /opt/ros/humble/setup.bash
colcon build --base-paths src/maps
source install/setup.bash

# 环境（本仓库无 sudo 用户态 Gazebo 11；含 ROS、GAZEBO_*、可写 HOME）
source /home/nepenthe/zmf/linux_code/dsh工作区/tools/gazebo_env.sh

# headless（默认 gui:=false）
ros2 launch zhirong_maps zhirong_arena.launch.py

# 带 gzclient（需要可用 OpenGL/X；本机需 Xvfb + 软件渲染）
ros2 launch zhirong_maps zhirong_arena.launch.py gui:=true

# 覆盖 world / 隔离 gazebo master
ros2 launch zhirong_maps zhirong_arena.launch.py \
    world:=/abs/path/zhirong_arena.world gazebo_master_uri:=http://127.0.0.1:11391
```

launch 参数：`gui`(false) / `world` / `verbose` / `gazebo_master_uri` / `spawn_x,y,z,yaw`(2.90,1.60,0.05,3.1416)。
launch 会把本包 `models/` 追加进 `GAZEBO_MODEL_PATH`、`GAZEBO_RESOURCE_PATH`（world 用 `model://` 引用模型）。

不 build 直接加载 world（调试/CI）：

```bash
source tools/gazebo_env.sh
cd competition_ws/src/maps/zhirong_maps
unset DISPLAY                        # 本机 :1 GLX 损坏时必需；正常桌面可省略
export GAZEBO_MASTER_URI=http://127.0.0.1:11391
export GAZEBO_MODEL_PATH="$PWD/models:$GAZEBO_MODEL_PATH"
gzserver worlds/zhirong_arena.world --verbose
```

---

## 11. 俯视渲染与逐块比对

world 内已内置正俯视 GUI 相机预设（与图 2 同方向：+x 东=右、+y 北=上）：

```xml
<gui fullscreen="0">
  <camera name="user_camera">
    <pose>0 0 6.0 0 1.5708 1.5708</pose>   <!-- roll=0, pitch=90°, yaw=90°：相机朝下、北朝上 -->
    <view_controller>orbit</view_controller>
  </camera>
</gui>
```

渲染方法（`preview/scene/render_topdown.py` 已封装）：

```bash
Xvfb :99 -screen 0 1280x1280x24 -ac &
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient &      # gzserver 由 launch 或 gzserver 起
DISPLAY=:99 xwd -root -out render_raw.xwd
python3 tools/xwd2png.py render_raw.xwd render_raw.png
python3 preview/scene/render_topdown.py             # 裁剪视口 + 拼 compare_topdown.png
```

产物（v3 已重新渲染）：
- `preview/scene/render_raw.png`：Xvfb 全屏截图（1280×1280）
- `preview/scene/render_topdown.png`：裁掉 GUI 后的正俯视渲染（995×1095）
- `preview/scene/compare_topdown.png`：**左 = 规则图 2，右 = Gazebo 俯视渲染**（2509×1498）

> 说明：正俯视渲染用透视相机（hfov 60°、高 6 m），靠边的墙顶会略向外倾（透视），不是布局偏差；
> 需要完全正交视角时可把相机 `pose` 的 z 调到 10~12 或改用正交相机插件。

---

## 12. 2D 占据栅格（maps/）

| 字段 | 值 |
| --- | --- |
| 文件 | `maps/zhirong_arena.pgm`（P5）+ `maps/zhirong_arena.yaml` |
| 分辨率 / 尺寸 | 0.05 m/px，160×160 px（覆盖 8 m×8 m） |
| origin | `[-4.0, -4.0, 0.0]` |
| 占据 | 白 254 自由；黑 0 占据（围挡/红块/斜坡/标牌立柱/门柱）；无未知区域 |

> 斜坡在 2D 栅格中按“占据”保守处理（实际可翻越）；nav2 中可把斜坡足迹覆盖为可通行。

---

## 13. 与图 2 的对应关系与已知偏差

**对应关系**：16 单元格划分、黄/桔/红三区、全部 L/Z/T/工型/A 字架/薄墙的位置与开向、
红边界不规则折线与两个 0.8 m 缺口、斜坡 1/2（v3 按图 2 橙椭圆缩小）、6 目标板/5 圆环贴墙位置
均按图 2 复现；尺寸取图 2 标注（斜坡另按图 2 橙椭圆缩放），目标/圆环取图 5~8 样式。

**叠加校验**：`preview/scene/overlay_diff.png` 把图 2 的红线（红）与障碍轮廓（黑）按
`x=(px−507.5)*0.0082645, y=(552.5−py)*0.0057143` 仿射到世界坐标，与 `docs/plan.png` 同尺度半透明叠加；
`preview/scene/overlay_residuals.txt` 给出各障碍中心残差表。**残差 >0.15 m 的项仅 2 个**：

| 障碍 | 残差 | 说明 |
| --- | --- | --- |
| `wall_a_frame_041x027` | 0.299 m | **安全偏移**：任务书要求 A 字架保持 y≥2.0，避免与出生点 (2.9,1.6) 的机器人碰撞 |
| `wall_l_113_049` | 0.164 m | v3 按 Lead 指定中心 **(1.28,1.46)** 校正（图 2 像素映射为 (1.128,1.397)）；该墙跨 A3/A4 边界，视觉上仍压在图 2 红折线上 |

其余 14 个障碍残差 ≤0.13 m（多数 <0.05 m），详见残差表。

**已知偏差与简化**：

1. **手绘比例失真**：图 2 横纵比例不一致（≈121 vs ≈175 px/m）且障碍放大 1.2~1.3 倍，
   本包以“标注尺寸 + 相对布局”为准，位置误差约 ±0.2 m。
2. **为避让/按指令做的微调**：
   - `wall_l_113_049` → (1.28,1.46)（Lead 指定，残差 0.164 m，见上表）；
   - `wall_z_112_060` → (−0.14,−0.40)（Lead 指定，残差 0.005 m）；
   - `ramp_1` x 0.938→0.980（+0.04 m，避让 C2 的 Z 墙，缩小后仍贴图 2 位置）；
   - `ramp_2` y −1.176→−1.230（−0.054 m，避让 Z 墙；x 保持 −0.65）；
   - `wall_t_143_057` 西移 0.17 m（1.43 m 横臂不超出 8 m 地面）；
   - `wall_a_frame_041x027` y=2.10（安全偏移，见上表）。
3. **形状判读**：B1/C1 的 0.73×0.58 按图 2 判读为 **T（⊢）**；C2 的 1.12×0.60 判读为 **Z 形**
   （v2 起维持，Lead 已认可证据）。
4. **1.14×0.48 / 1.43×0.57 归属**：`(631..803,716..805)` 的 ⌐ 形 L 墙 = **1.14×0.48（C4）**；
   图边裁切的右下 T 墙 = **1.43×0.57（红线外东南）**。
5. **斜坡尺寸**：图 4 整板规格按图 2 橙椭圆缩放到 1.1×1.0 / 1.0×1.0（rise 0.18），
   如需按整板规格（1.2×1.2 / 2×0.6×1.2、rise 0.20）摆放，改 `scene_layout.py` 三个常量即可。
6. 实景迷彩墙顶部为斜切/异形，本包统一矩形墙板；中文标牌用像素字模 IN/OUT。
7. 红边界折线 bbox 为 5.09×5.22 m（图 2 手绘），因此场地铺装取 5.5×5.5 m；**16 单元格仍为严格 5×5 m**。
8. 图 2 中若干障碍（薄墙、A 字架、背景横墙、东南 T 墙）位于红边界之外，本包按图保留在红线外（8 m 地面内）。
9. 正俯视渲染为透视相机（hfov 60°、高 6 m），靠边墙顶略外倾，属透视而非布局偏差。

## 14. 与其他包的接口约定

| 项 | 值 |
| --- | --- |
| world 相对路径 | `worlds/zhirong_arena.world`（源码与 install/share 一致） |
| `model://` 解析 | 需将 `<包>/models` 加入 `GAZEBO_MODEL_PATH`（本包 launch 自动完成） |
| 出生点 | `(x=+2.90, y=+1.60, z=0.05, yaw=π)`（与 v1 相同，未改 launch / 未改路径或 include 名规则） |
| `include` 名 | v2 有模型目录与 include 名变化（如 `arena_floor_5x5`→`arena_floor`、`zone_yellow_cross`→`zone_yellow`、新增 `wall_z_112x060` 等），已同步给 robot-integrator |
| ROS 系统插件 | 不在 world 内；机器人的 `libgazebo_ros_planar_move.so` 等由机器人 URDF/launch 加载 |
| gzserver 启动 | 本包 launch，或机器人 launch 直接 `gzserver <world>` 并自行设置 `GAZEBO_MODEL_PATH` |

机器人侧联调建议：

```bash
ros2 launch zhirong_maps zhirong_arena.launch.py gui:=false \
    gazebo_master_uri:=http://127.0.0.1:11392
ros2 run gazebo_ros spawn_entity.py -topic robot_description \
    -entity omni_robot -x 2.90 -y 1.60 -z 0.05 -Y 3.1416
gz model -m omni_robot -p
```

---

## 15. 维护与重新生成

| 脚本（`preview/scene/`） | 作用 |
| --- | --- |
| `scene_layout.py` | **唯一数据源**：常量/材质、分块表 `BLOCKS`、墙体面板、红边界折线、分区、目标/圆环贴墙规则、标牌/门柱/出生点 |
| `build_scene.py` | 生成 `models/*`、`worlds/zhirong_arena.world`、`maps/*.pgm|yaml`；执行几何自检并打印分块摘要 |
| `make_plan.py` | 生成 `docs/plan.png`（300 dpi 俯视布置图） |
| `render_topdown.py` | 裁剪 Gazebo 截图 + 拼接 `compare_topdown.png` |
| `overlay_diff.py` | 生成 `overlay_diff.png`（图 2 红线/障碍轮廓叠加到 plan.png）与 `overlay_residuals.txt` |

```bash
cd preview/scene
export MPLCONFIGDIR=/home/nepenthe/zmf/linux_code/dsh工作区/.mplconfig
python3 build_scene.py    # 重新生成模型/世界/栅格地图（打印自检 + 分块摘要）
python3 make_plan.py      # 重新生成 docs/plan.png
python3 render_topdown.py # 用 render_raw.png 重新拼对比图
```

自检输出（当前版本全部通过）：

```text
[自检]
  全部通过：障碍均在 8m 地面内、互不重叠、块归属正确、目标/圆环高度合法、出生点在红边界外、斜坡2 为 Λ 形；桔区半径与斜坡 footprint 一致。
```

---

## 16. 许可

Apache-2.0。场景几何按比赛规则文档复现，仅用于竞赛开发与仿真训练。
