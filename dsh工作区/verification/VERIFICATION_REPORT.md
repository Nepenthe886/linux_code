# “戎智杯”反恐搜救赛项 —— Gazebo 场景 + 机器人建模/控制 启动测试报告

日期：2026-11-17 ｜ 环境：Ubuntu 22.04 + ROS 2 Humble + Gazebo Classic 11.10.2
（本机验证时因沙箱无 sudo 采用用户态安装；工作空间已提供统一的系统级安装脚本
`scripts/install_environment.sh`：apt/rosdep 安装 Gazebo+ROS 系统依赖，并按 `requirements.txt`
用 pip 建立 Python venv；在有 sudo 的机器上执行后即成为标准系统环境，无需任何环境脚本）
交付位置：`/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup/src/`
（`maps/zhirong_maps` + `robot/robot_description` + `robot/robot_control`）

---

## 1. 任务与交付物

| 要求 | 交付 |
| --- | --- |
| 仿真平台 Gazebo | Gazebo Classic 11 + `gazebo_ros`/`gazebo_plugins` 3.9；工作空间 `scripts/install_environment.sh` 一键系统级安装（apt + rosdep），安装后不依赖任何环境脚本，便于整体迁移 |
| 按 Word 地图创建场景 | `src/maps/zhirong_maps`：world `worlds/zhirong_arena.world`（SDF 1.6，41 个 include），28 个模型（全部 box/cylinder 拼装、无外部 mesh/纹理/fuel 依赖），俯视布置图 `docs/plan.png`，2D 占据栅格 `maps/zhirong_arena.pgm/.yaml` |
| 地图放在 `.../src/maps` | ✅ `Zhirong Cup/src/maps/zhirong_maps/` |
| 把工作区完成的机器人建模和控制放进去 | `src/robot/robot_description`（URDF + Gazebo 标签）与 `src/robot/robot_control`（`gazebo.launch.py`、插件配置、遥控节点、166 个单测、文档） |
| 启动测试 | 在 `Zhirong Cup` 工作空间 `colcon build` + `ros2 launch robot_control gazebo.launch.py` 全流程 headless 实测通过（见第 4 节） |

场景依据：规则文档图 2「比赛场地简略图」（5 m×5 m、16 单元格、红边界、黄/桔/红三区、
L/T/工型障碍、斜坡 1/2、入口/出口）、图 4 斜坡规格（1200×1200×19 / 600×1200×19 mm）、
图 5/6/7 目标物（身靶、胸靶、二维码危险品）、图 8 圆环触碰点。障碍尺寸取图上标注，
位置按像素比例近似（图 2 为手绘示意图，±0.2 m）。

## 2. 场景内容（`zhirong_arena.world`，v2 分块布局）

> 2026-11-17 按用户反馈重做：先分块（16 个 1.25 m 单元格）再在块上建模，修正障碍尺寸/位置偏差，
> 修复斜坡2 倒置（Λ 形）。对比图：`docs/sim_verification/compare_topdown.png`。

* 场地 5 m×5 m 居中（x 东、y 北、原点场地中心），4×4=16 个 1.25 m 单元格，
  网格线贴地；8 m×8 m 承载地面（含入口外侧出生区）；
* 红色比赛边界线（宽 0.06 m）：东侧偏北入口缺口 0.8 m、西侧中部出口缺口 0.8 m，
  门柱 + IN/OUT 标牌；
* 黄区（左上十字形）、桔区×2（斜坡下橙色圆盘）、红区（南侧中部）；
* 障碍：L 型军绿迷彩墙 ×5（0.95×0.61 / 1.30×0.52 / 1.13×0.49 / 1.12×0.60 / 1.14×0.48）、
  T 型墙 ×2（0.73×0.58 ×2、1.43×0.57）、薄墙 0.85×0.08、A 字架 0.41×0.27（墙高 0.55 m、厚 0.06 m）；
* 工型障碍 0.89×0.49 + 红区围挡；
* 斜坡 1：单面斜坡 1.2×1.2（坡≈9.5°、高边 0.20 m）；斜坡 2：双面 A 字斜坡 2×(0.6×1.2)；
* 目标板 6 个（身靶×2 / 胸靶×2 / 二维码×2）、圆环触碰点 5 个；
* 机器人出生点标记 `spawn_marker`（入口外侧 0.4 m，`x=2.90, y=1.60, yaw=π`）。

## 3. 机器人建模/控制接入 Gazebo

* URDF 追加 Gazebo 章节（不改原 RViz 可见结构）：
  * `libgazebo_ros_planar_move.so`：订阅 `/cmd_vel`，发布 `/odom` 与 TF `odom→base_footprint`
    （支持前进 x、横移 y、自转 z，适配全向底盘）；
  * `libgazebo_ros_joint_state_publisher.so`：发布四轮 `/joint_states`；
  * 各 link 材质、轮子低摩擦 `mu1/mu2=0.1`、`self_collide=false`。
* 网格解析：URDF 保留 `package://robot_description/meshes/*`，spawn 时
  `-package_to_model` 转 `model://`，由 `robot_control/models/robot_description/`
  （自动加入 `GAZEBO_MODEL_PATH`）解析 —— 修复了工作区中文/空格路径在 urdf→sdf
  转换中把 `file://` URI 破坏导致 `[Err] No mesh specified` 的问题。
* `robot_control/launch/gazebo.launch.py`：一把启动 gzserver（自动 `-s` 加载
  `libgazebo_ros_init/factory`、自动设置 `GAZEBO_MODEL_PATH`、headless 内部 unset DISPLAY）
  + spawn_entity + robot_state_publisher + 可选 teleop/gzclient/RViz；12 个 launch 参数；
* 模式隔离：Gazebo 模式下不启动 `sim_node`（避免双 `/odom`/TF），原 `teleop_*` launch 保持可用。

## 4. 启动测试结果（在 `Zhirong Cup` 工作空间实测，headless）

命令（详见 `docs/sim_verification/README.md`）：

```bash
cd "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
sudo bash scripts/install_environment.sh   # 首次：统一安装系统依赖
bash scripts/build.sh                      # colcon build
bash scripts/run_sim.sh gui:=false rviz:=false teleop:=none
```

| # | 检查项 | 结果 |
| --- | --- | --- |
| 1 | colcon 构建 3 个包 | ✅ 3 packages finished |
| 2 | world 解析 | ✅ `install/zhirong_maps/share/zhirong_maps/worlds/zhirong_arena.world` |
| 3 | 模型加载（28 模型 / 41 include，抽查 25 个 `gz model -p`） | ✅ 缺失 0，无 `Unable to find uri`、无 SDF 错误 |
| 4 | 机器人 spawn | ✅ `2.90015 1.59904 0`，yaw≈-π，与出生点标记一致 |
| 5 | `/clock` | ✅ 仿真时钟运行 |
| 6 | `/joint_states`（FL/FR/RL/RR） | ✅ 四轮齐全 |
| 7 | `/odom` + TF `odom→base_footprint` | ✅ 正常 |
| 8 | `/cmd_vel` 前进 0.3 m/s×2 s | ✅ 位移 0.579 m |
| 9 | `/cmd_vel` 横移 0.3 m/s×2 s | ✅ 位移 0.386 m（全向） |
| 10 | `/cmd_vel` 自转 0.8 rad/s×1.5 s | ✅ yaw +0.741 rad |
| 11 | 机器人网格（LiDAR STL） | ✅ `No mesh specified` = 0 |
| 12 | 退出（SIGINT） | ✅ 干净退出，无 gzserver 残留 |
| 13 | 单元测试 | ✅ `pytest` 166 passed |

验收脚本：`verification/run_acceptance.sh`（含构建/启动/话题/TF/运动/模型/清理），
驱动闭环检查 `verification/check_gazebo_drive.py`，日志在 `verification/logs/`。
同一套检查在开发工作区（`competition_ws`）与交付工作区（`Zhirong Cup`）各跑一次，
均为 `ACCEPTANCE: PASS`。

## 4.1 激光雷达 / IMU（bring_up 集成，2026-11-17）

`bring_up` 默认拉起 `robot_state_publicer` 的 Mid-360 模拟节点（`lidar:=false` 可关）：

- `/livox/lidar`：PointCloud2，10 Hz、20000 点/帧、`point_step=26`，frame=`livox_mid360_link`
- `/livox/imu`：~150–200 Hz，frame=`livox_mid360_link`
- `/livix/lidar`：别名话题

Gazebo 的 `/clock` 只有 ~10 Hz：若节点 `use_sim_time:=true`，ROS 定时器会被限制到 ~20 Hz；
因此集成改为「定时器按真实时间运行 + 消息时间戳用 `/clock` 插值」（`stamp_from_sim_clock:=true`），
并用 MultiThreadedExecutor 把点云生成与 IMU 发布分到不同回调组。实测：点云 10.0 Hz、
IMU ~154 Hz、时间戳与 `/clock` 偏差 <0.05 s；`robot_control` 169 单测与
`robot_state_publicer` 1 单测通过；验收脚本已加入点云/IMU 检查（PASS=5 FAIL=0）。

## 5. 截图（Gazebo 相机实渲，非示意图，位于 `docs/sim_verification/`）

`arena_sw_oblique.png`（全景）、`arena_overview.png`、`arena_se_oblique.png`、
`arena_topdown.png`（北朝上，可与 `docs/plan.png` 对照）、`arena_robot_closeup.png`（机器人特写）。

## 6. 已知限制 & 建议

1. `planar_move` 是速度级车体运动：轮子为 passive 关节，不含电机/打滑物理，
   不能用于验证轮速闭环；若需轮子真实滚动，可改装 `ros2_control` + 轮电机模型。
2. `/cmd_vel` 无超时停车（插件行为）：遥控端退出后请显式发零速（或加 watchdog 节点）。
3. 本机无 GPU/显示（X :1 GLX 损坏）：GUI/相机渲染通过 Xvfb + 软件 OpenGL 完成；
   正常机器 `gui:=true` 即可看实时画面。
4. 本机 Gazebo 为用户态安装（沙箱无 sudo）。正式环境建议
   `sudo apt install ros-humble-gazebo-ros-pkgs gazebo`，其 launch/包完全兼容。
5. 场地布局按图 2 示意比例复现（±0.2 m 近似，局部为避让斜坡微调 0.15~0.25 m），
   详见 `zhirong_maps/README.md` 第 8 节“与图 2 的偏差说明”。
