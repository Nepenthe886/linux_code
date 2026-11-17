# 仿真启动测试记录（Gazebo Classic 11 + robot_control）

本目录保存 **比赛场景 ↔ 机器人建模/控制** 联调启动测试的实测截图与结论，
对应日期 2026-11-17，环境 ROS 2 Humble + Gazebo Classic 11.10.2。

## 1. 一键启动

```bash
cd "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"

# 首次使用：统一安装（apt 装 Gazebo/ROS + pip 按 requirements.txt 装 Python 依赖）
sudo bash scripts/install_environment.sh

# 构建 + 启动
bash scripts/build.sh
bash scripts/run_sim.sh gui:=false rviz:=false teleop:=none
```

> 系统级安装后无需任何环境脚本；工作空间内 `scripts/` 三个脚本即可完成
> 安装 / 构建 / 启动，便于整体迁移。

默认行为：world 自动解析到本包 `worlds/zhirong_arena.world`（`--symlink-install`
后从 `install/zhirong_maps/share/...` 读取）；机器人 spawn 到入口外侧
`(x=+2.90, y=+1.60, yaw=π)`。

## 2. 实测结论（比赛工作空间内执行）

| 检查项 | 结果 |
| --- | --- |
| colcon build（robot_description / robot_control / zhirong_maps） | 3 packages finished |
| gzserver 加载 world（42 个 include / 30 个模型） | 无 SDF/模型错误，`Unable to find uri` = 0 |
| 关键模型逐个 `gz model -m <名> -p` 抽查（25 个） | 全部存在，位姿正确 |
| 机器人 spawn | `2.90015 1.59904 0`，yaw≈-π，与 `spawn_marker` 一致 |
| `/clock` `/joint_states`（四轮）`/odom` `/cmd_vel` `/tf` | 全部存在 |
| TF `odom -> base_footprint` | 正常 |
| `/cmd_vel` 前进 0.3 m/s × 2 s | 位移 0.579 m（odom 与 gz 位姿一致） |
| `/cmd_vel` 横移 0.3 m/s × 2 s | 位移 0.386 m（全向运动生效） |
| `/cmd_vel` 自转 0.8 rad/s × 1.5 s | yaw 变化 0.741 rad |
| 机器人网格（LiDAR STL） | `No mesh specified` = 0（model:// 解析修复后） |
| 退出（SIGINT） | 干净退出，无 gzserver 残留 |
| 单元测试 | `pytest` 166 passed |

验收脚本与日志：`/home/nepenthe/zmf/linux_code/dsh工作区/verification/`
（`run_acceptance.sh`、`check_gazebo_drive.py`、`logs/`）。

## 3. 场景 v2（2026-11-17 按用户反馈重做，分块建模）

> **v3 微调（同日第二轮反馈）**：用户指出“斜坡尺寸太大（图 2 里只是很小的橙色椭圆）”。
> 已将斜坡 footprint 缩为 ramp1 **1.1×1.0**、ramp2 **1.0×1.0**（rise 0.18），桔区半径缩为
> **0.56 / 0.52**（v2 为 0.80）；黄区改为横带+竖带十字、红区加高到 0.83 m；
> A3 L 墙、C2 Z 墙中心按图 2 残差校正，斜坡 2 仍为 **Λ** 形。
> 模型数 28→**30**（桔区拆为 `zone_orange_ramp1/2`），include 数 41→**42**。
> 校验图：`preview/scene/overlay_diff.png`（图 2 红线/轮廓叠加）、`preview/scene/compare_topdown.png`（v3 重渲染）。

用户对照图 2 指出“障碍尺寸/位置偏差大、斜坡2 倒置”，已按“先分块、再在分块上建模”重做：

- **分块表**：`scene_layout.BLOCKS`（每条障碍 = cell A1..D4 或红线外 + 相对格心偏移 + 模型 + yaw），
  `build_scene.py`/`make_plan.py` 共用；不再用 v1 的“红边界 bbox 双尺度拉伸”。
- **逐块落位**：A1=L 0.95×0.61，A2=L 1.30×0.52（跨北侧红折线），A3=L 1.13×0.49，
  B1=T 0.73×0.58，B3=斜坡1，C1=T 0.73×0.58，C2=Z 1.12×0.60 + 斜坡2，
  C4=⌐ 1.14×0.48，D1/D3=红区围挡，D2=工型 0.89×0.49；
  **红线外**：东侧薄墙 0.85×0.08、东北 A 字架 0.41×0.27 + 背景横墙、东南 T 1.43×0.57。
- **红边界**：按图 2 红色线像素折点重建为不规则折线（两条 chain + 出口内侧短折线），
  入口缺口 0.80 m（东北，`(0.37,2.21)-(0.61,1.44)`）、出口缺口 0.80 m（西中部，`(-2.59,-0.71)-(-2.59,0.09)`）。
- **斜坡2 倒置修复**：两块 0.6×1.2 板改为 **Λ**（西板 pitch −0.3218 / 东板 +0.3218，脊高 0.20 m 两侧落地）。
  特写见 `ramp2_closeup.png`。
- 目标板 6 / 圆环 5 改为“墙体实例 + 面板 + 面朝向”自动贴墙；门柱贴缺口端点。
- **v3**：斜坡 footprint 1.1×1.0 / 1.0×1.0（rise 0.18）、桔区 r=0.56/0.52、黄区横带+竖带、红区 0.83 m。

**对照图**：`compare_topdown.png`（左=规则图 2，右=Gazebo 正俯视渲染）。
块内为避让做了 ≤0.22 m 微调（C2 的 Z 墙与斜坡2、A 字架与出生点等），详见
`preview/scene/layout_report.txt` 与地图包 README 第 13 节。

## 3.1 截图

| 文件 | 内容 |
| --- | --- |
| `compare_topdown.png` | 图 2 vs Gazebo 正俯视渲染（**v3 微调**，斜坡/橙区已按图 2 椭圆缩小） |
| `ramp2_closeup.png` | 斜坡2 特写（Λ 形，中间脊、两侧落地） |
| `arena_sw_oblique.png` | 西南斜俯视全景：5m×5m 场地、16 格网格、红折线边界、黄/桔/红区、L/T/Z/工型障碍、双斜坡、目标板与圆环，机器人在入口内侧 |
| `arena_overview.png` | 正南斜俯视全景 |
| `arena_se_oblique.png` | 东南斜俯视全景 |
| `arena_topdown.png` | 正俯视（北朝上），与 `docs/plan.png` 对照用 |
| `arena_robot_closeup.png` | 机器人特写（入口处，车体 + 四轮 + LiDAR） |

> 截图由 Gazebo 相机传感器（`libgazebo_ros_camera.so`）在虚拟 X（Xvfb + 软件 OpenGL）
> 下渲染，物理与渲染均在同一 gzserver 内，非示意图。

## 4. 已知限制

* URDF 中底盘由 `libgazebo_ros_planar_move.so` 做速度级平面运动：**不含轮子电机/打滑物理**，
  无法用它验证轮速闭环；轮子在物理里是 passive 连续关节。
* `/cmd_vel` 无超时停车（上游插件行为）：联调结束请显式发零速。
* 本机（无显示器）截图需要虚拟 X；普通有 GPU/显示器的机器可直接 `gui:=true` 看 gzclient。
* 本机 Gazebo 为用户态安装（无 sudo）：换到正常机器建议
  `sudo apt install ros-humble-gazebo-ros-pkgs gazebo` 后直接 source ROS 即可，
  launch/包本身不需要改动。
