# zhirong_maps v3 验证记录（scene-builder / task-4）

环境：Ubuntu 22.04 / ROS 2 Humble / 用户态 Gazebo Classic **11.10.2**（`tools/gazebo_env.sh`）。
headless：`unset DISPLAY`；gazebo master 隔离端口 `http://127.0.0.1:11391`。
渲染：`Xvfb :99 -screen 0 1280x1280x24 -ac` + `DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient`（llvmpipe）。

v3 变更（相对 v2）：斜坡/桔区按图 2 橙椭圆缩小（ramp1 1.1×1.0 rise 0.18、ramp2 1.0×1.0 rise 0.18；
桔区 r=0.56/0.52）、黄区改为横带+竖带十字、红区 0.83 m、A3/C2 块内残差按图 2 校正、
新增 overlay_diff 叠加校验。

## 1. 静态校验

```bash
cd competition_ws/src/maps/zhirong_maps
python3 - <<'EOF'
import glob, xml.etree.ElementTree as ET
files = glob.glob('models/*/model.config') + glob.glob('models/*/model.sdf') + glob.glob('worlds/*.world')
for p in files: ET.parse(p)
print('OK', len(files))
EOF
```

结果：`OK 61`（30 模型 ×2 + 1 world），0 错误；
world `zhirong_arena`：**42 个 `<include>`**、1 sun、physics(1 ms)、scene、gui 相机预设齐全；
无 http/fuel/mesh/纹理引用；`zone_orange_disc` 旧模型已清理，新增 `zone_orange_ramp1/2`。

## 2. colcon 构建（隔离于 preview/scene/colcon_test，不触碰 competition_ws/install）

```bash
cd competition_ws
colcon --log-base ../preview/scene/colcon_test/log build --base-paths src/maps \
  --build-base ../preview/scene/colcon_test/build \
  --install-base ../preview/scene/colcon_test/install
```

结果：`Summary: 1 package finished`；share 下 worlds/models(30)/launch/maps/docs 齐全，
models 目录无旧 `zone_orange_disc` 残留。

## 3. gzserver headless 加载 + 全部模型检查

```bash
source tools/gazebo_env.sh; unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11391
export GAZEBO_MODEL_PATH="$PWD/models:$GAZEBO_MODEL_PATH"
gzserver worlds/zhirong_arena.world &
# world 中 42 个 <include><name> 逐个 gz model -m <name> -p（每次间隔 0.15 s 防 transport 抖动）
```

结果：**42/42 个实例全部存在、位姿正确、missing=0**；日志无 SDF/模型错误。
关键位姿：

```text
wall_l_113_049      1.280  1.460  0      （v3 校正；bbox (0.71,1.21)-(1.84,1.71)）
wall_z_112_060     -0.140 -0.400  0      （v3 校正）
ramp_1              0.980  0.254  0
ramp_2             -0.650 -1.230  0
obstacle_i_089_049 -0.285 -2.097  0
target_hostage_1   -1.805  1.971  0.30
ring_3              0.778  1.460  0.32   （随 A3 墙移动自动贴墙）
spawn_marker        2.900  1.600  0
```

> 说明：本轮首次逐点查询时 gzserver 曾因 Gazebo transport 的 boost shared_ptr 断言偶发崩溃
> （连续 36 次 `gz model` 连接抖动，非世界内容问题）；改为每次查询间隔 0.15 s + 失败重试 1 次后
> **42/42 全部通过**，日志无 `[Err]`。

## 4. 斜坡 / 桔区数值自检

| 项 | 结果 |
| --- | --- |
| ramp1 footprint / rise / pitch | 1.1×1.0 m / 0.18 m / −0.1622（坡向 +x，坡角 9.29°） |
| ramp2 Λ | 西板 pose pitch **−0.3456**、东板 **+0.3456**（每侧坡 0.5 m，脊高 0.18 m，两侧落地） |
| ramp2 支撑木块 | 3 个（z=0.08），位置保持 |
| 桔区半径 | ramp1 0.56 / ramp2 0.52（`|r − max(l,w)/2|` = 0.01 / 0.02 ≤ 0.07） |
| 几何自检 | `全部通过：障碍均在 8m 地面内、互不重叠、块归属正确、目标/圆环高度合法、出生点在红边界外、斜坡2 为 Λ 形；桔区半径与斜坡 footprint 一致` |

完整输出：`preview/scene/layout_report.txt`。

## 5. 叠加校验 `overlay_diff.png` / 残差表

`scene_layout` 与 `make_plan` 共用同一 matplotlib 坐标系，`overlay_diff.py` 用
`imshow(extent=世界 bbox)` 把图 2 的红线（红，65%）与障碍轮廓（黑，45%）直接画到 plan 画布，
与 `docs/plan.png` 同尺度叠加（避免像素反推误差）。量化核对：图 2 红线映射到 plan 后
到 plan 红线的距离中位数 **0 px**（均值受入口/出口标签框等非场地红像素影响）。

残差 >0.15 m 的项（详见 `preview/scene/overlay_residuals.txt`）：

| 障碍 | 残差 | 说明 |
| --- | --- | --- |
| `wall_a_frame_041x027` | 0.299 m | 安全偏移：A 字架保持 y=2.10 ≥ 2.0，避免与出生点 (2.9,1.6) 机器人碰撞 |
| `wall_l_113_049` | 0.164 m | 按 Lead 指定中心 (1.28,1.46) 校正（图 2 像素映射 (1.128,1.397)），跨 A3/A4 |

其余 14 项 ≤0.13 m（多数 <0.05 m）。

## 6. Gazebo 正俯视渲染 + 对比图

流程：Xvfb :99 → gzserver(v3 world) → `DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient`（gui.ini 1280×1280）
→ `xwd` 截图 → `tools/xwd2png.py` → `preview/scene/render_topdown.py` 裁剪/拼接。

| 文件 | 内容 |
| --- | --- |
| `preview/scene/render_raw.png` | Xvfb 全屏原始截图 1280×1280 |
| `preview/scene/render_topdown.png` | 裁掉 GUI 的正俯视渲染 995×1095 |
| `preview/scene/compare_topdown.png` | 左=规则图 2 / 右=Gazebo v3 渲染（2505×1498；同时复制到 `docs/sim_verification/compare_topdown.png`） |
| `preview/scene/overlay_diff.png` | 图 2 红线+障碍轮廓叠加到 plan.png（4200×4200） |

world 内相机预设：`<pose>0 0 6.0 0 1.5708 1.5708</pose>`（正俯视、北朝上，与图 2 同方向）。

## 7. 产物清单

| 产物 | 路径 |
| --- | --- |
| world | `competition_ws/src/maps/zhirong_maps/worlds/zhirong_arena.world`（42 include） |
| models | `.../models/`（30 个，含 `zone_orange_ramp1/2`） |
| launch | `.../launch/zhirong_arena.launch.py`（未改；spawn 仍 2.90/1.60/0.05/π） |
| 平面图 | `.../docs/plan.png`（4200×4200，300 dpi，v3） |
| 2D 栅格 | `.../maps/zhirong_arena.{pgm,yaml}`（0.05 m/px，160×160，origin(-4,-4)） |
| 文档 | `.../README.md`（含 v3 变更/偏差/残差表）、`.../docs/sim_verification/{README.md,VERIFICATION_REPORT.md,compare_topdown.png}`（已更新 v3 数值/对比图） |
| 脚本 | `preview/scene/{scene_layout.py, build_scene.py, make_plan.py, render_topdown.py, overlay_diff.py}` |
| 数据 | `preview/scene/{layout_report.txt, overlay_residuals.txt, VERIFICATION.md}` + 日志/渲染原始图 |

## 8. 未在本机验证 / 需 Lead 完成

- Zhirong Cup 部署同步（按要求由 Lead 统一执行）。
- `docs/sim_verification/arena_*.png`（v2 时期由机器人相机传感器渲染的斜视图）未重渲染：
  场景内容（斜坡/橙区/黄区）已变，建议同步后由 Lead / robot-integrator 用其相机管线重拍；
  本轮已更新 `compare_topdown.png`（正俯视）与全部文字数值。
- 机器人侧复测：world 路径、spawn 不变，但 v3 桔区模型名改为 `zone_orange_ramp1/2`、
  模型数 29→30（include 数不变 42）；已私信 robot-integrator（其 launch 不依赖模型名）。
