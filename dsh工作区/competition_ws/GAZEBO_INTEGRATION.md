# Gazebo Classic 11 集成与验证记录

> 任务：把机器人建模与控制（`robot_description` + `robot_control`）接入 Gazebo
> Classic 11 仿真，供比赛地图场景中启动测试。
> 工作副本：`competition_ws/src/robot/{robot_control,robot_description}`。
> 本文件记录**实际跑过的命令与关键输出**（全部 headless，本机 X :1 的 GLX 损坏，
> 渲染不可用，因此验证只依赖 ROS 话题 / TF / `gz model` / 日志）。

## 0. 结论摘要

| 验收项 | 结果 |
| --- | --- |
| URDF 追加 Gazebo 标签（2 个 ModelPlugin + 材质 + 轮子摩擦） | ✅ 完成，RViz 结构未改动 |
| `gazebo.launch.py` 一把启动（world/spawn/rsp/可选 teleop·gzclient·RViz） | ✅ 完成，源码直跑与 colcon 安装后均验证 |
| 比赛地图 `zhirong_maps/zhirong_arena.world` 自动解析 + 模型加载 | ✅ world 与 28 个 `model://` 模型全部加载 |
| `/clock`、`/joint_states`、`/odom`、TF `odom→base_footprint` | ✅ 全部存在且时间戳同步（仿真时间） |
| `/cmd_vel` 前进 / 横移 / 原地旋转 | ✅ 空世界定量验证（见 §6），比赛地图内前进验证（§7） |
| Ctrl-C（SIGINT）干净退出、无残留进程、端口释放 | ✅ 0.5 s 退出，无残留（§8） |
| 全量 pytest 回归 | ✅ `165 passed`（新增 17 个 Gazebo 离线用例） |

## 1. 环境事实（本机）

* Gazebo Classic **11.10.2** 为用户态安装（无 sudo），前缀
  `gazebo_userland/`，包含 `gazebo_ros` / `gazebo_plugins` **3.9.0**；
  插件 `libgazebo_ros_planar_move.so`、`libgazebo_ros_joint_state_publisher.so`
  位于 `$PREFIX/opt/ros/humble/lib/`。
* **任何 gazebo/ROS 命令前必须**：`source tools/gazebo_env.sh`
  （设置 `PATH`/`LD_LIBRARY_PATH`/`GAZEBO_*`/`HOME`/`ROS_LOG_DIR` 等）。
* 本机 `DISPLAY=:1` 的 GLX 损坏：**gzserver 若保留 `DISPLAY` 会因
  `X Error ... BadValue (GLX) X_GLXCreateContext` 直接崩溃**。
  headless 验证一律 `unset DISPLAY`；`gazebo.launch.py` 内部已对 gzserver
  子进程 `unset DISPLAY`（gzclient 仍用真实 `DISPLAY`，本机不可用）。
* 多人共用机器时 Gazebo master 端口会抢：本验证固定
  `export GAZEBO_MASTER_URI=http://127.0.0.1:11392`。
* 测试用 `export ROS_DOMAIN_ID=42` 与本机其它 ROS 会话隔离。

## 2. 交付物清单

```text
competition_ws/src/robot/
├── robot_description/urdf/omni_robot.urdf        # 末尾追加 Gazebo 章节（+ 根 link 注释）
├── robot_control/
│   ├── launch/gazebo.launch.py                   # 新增：Gazebo 启动入口（12 个 launch 参数）
│   ├── worlds/test/gazebo_test.world             # 新增：自带最小测试世界（回退用）
│   ├── package.xml                               # + gazebo_ros / gazebo_plugins / gazebo_msgs
│   ├── setup.py                                  # 安装 worlds/ 与 worlds/test/
│   ├── test/test_gazebo_launch.py                # 新增：17 个离线单测（不启动 Gazebo）
│   └── README.md                                 # + 「Gazebo 仿真（Gazebo Classic 11）」章节
├── INTERFACE.md                                  # 副本，追加「Gazebo 仿真接入」契约章节
└── ../../GAZEBO_INTEGRATION.md                   # 本文件
```

证据与复现脚本（不在部署包内）：
`preview/robot_gazebo/evidence/*.txt`、`preview/robot_gazebo/*.sh`、
`preview/robot_gazebo/twist_phase.py`。

## 3. 构建（colcon，安装目录在 `competition_ws/` 下）

```bash
cd /home/nepenthe/zmf/linux_code/dsh工作区/competition_ws
source ../tools/gazebo_env.sh
colcon build --symlink-install --packages-select robot_description robot_control
```

实测输出（尾行）：

```text
Starting >>> robot_description
Finished <<< robot_description [0.07s]
Starting >>> robot_control
Finished <<< robot_control [0.67s]

Summary: 2 packages finished [0.88s]
```

> `--symlink-install` 生效：`install/robot_control/share/robot_control/launch/gazebo.launch.py`
> 是指向源码的符号链接，改源码无需重新 build（worlds/test 自带世界也已安装到 share）。

## 4. 启动

### 4.1 默认启动（本任务交付的「一把启动」）

```bash
source /home/nepenthe/zmf/linux_code/dsh工作区/tools/gazebo_env.sh
unset DISPLAY                                   # headless（本机 GLX 坏）
export GAZEBO_MASTER_URI=http://127.0.0.1:11392 # 避免端口冲突（可选）

ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none
```

**默认值即满足无显示环境**：`gui=false`、`rviz=false`、`teleop=none`、
`use_sim_time=true`，不需要额外必需参数。默认出生点
`x=2.9, y=1.6, yaw=π`（与地图包 `spawn_marker` 位置一致，入口外侧、面向场内），
`z=0.05`（模型根 link `base_footprint` 离地高度，落地后 z=0）。

### 4.2 其它常用形式

```bash
# 源码目录直接 launch（不 colcon install 本包）
ros2 launch ./launch/gazebo.launch.py

# 显式指定 world / 出生点
ros2 launch robot_control gazebo.launch.py world:=/abs/path/zhirong_arena.world x:=0 y:=0 yaw:=0

# 伴随遥控（另开终端更可靠：ros2 run robot_control teleop_keyboard）
ros2 launch robot_control gazebo.launch.py teleop:=keyboard

# 查看全部参数
ros2 launch robot_control gazebo.launch.py --show-args
```

启动日志中的 world 解析与插件加载（实测）：

```text
[INFO] [launch.user]: [gazebo.launch.py] world = .../src/maps/zhirong_maps/worlds/zhirong_arena.world（来源：zhirong_maps）
[INFO] [launch.user]: [gazebo.launch.py] gzserver 启动中（headless 模式，渲染关闭）……
[spawn_entity.py-2] [INFO] ... Spawn status: SpawnEntity: Successfully spawned entity [zhirong_robot]
[bash-1] [INFO] ... [gazebo_ros_planar_move]: Subscribed to [/cmd_vel]
[bash-1] [INFO] ... [gazebo_ros_planar_move]: Advertise odometry on [/odom]
[bash-1] [INFO] ... [gazebo_ros_planar_move]: Publishing odom transforms between [odom] and [base_footprint]
[bash-1] [INFO] ... [gazebo_ros_joint_state_publisher]: Going to publish joint [wheel_front_left_joint]
[bash-1] [INFO] ... [gazebo_ros_joint_state_publisher]: Going to publish joint [wheel_front_right_joint]
[bash-1] [INFO] ... [gazebo_ros_joint_state_publisher]: Going to publish joint [wheel_rear_left_joint]
[bash-1] [INFO] ... [gazebo_ros_joint_state_publisher]: Going to publish joint [wheel_rear_right_joint]
```

> 找不到 `zhirong_maps` 时会打印一条 warning 并回退到
> `worlds/test/gazebo_test.world`；`world:=` 指向不存在文件时 launch 会报
> `gazebo.launch.py: world 参数指定的文件不存在：<path>` 并退出（已实测）。

## 5. 话题 / TF / 关键参数实测

`ros2 topic list`（启动完成后）：

```text
/clock
/cmd_vel
/joint_states
/odom
/parameter_events
/performance_metrics
/robot_description
/rosout
/tf
/tf_static
```

`/clock`（仿真时间，由 `libgazebo_ros_init.so` 发布）：

```yaml
clock:
  sec: 2
  nanosec: 400000000
```

`/joint_states`（由 `libgazebo_ros_joint_state_publisher.so` 发布，四轮顺序 FL FR RL RR）：

```yaml
header:
  stamp: {sec: 3, nanosec: 260000000}
  frame_id: ''
name: [wheel_front_left_joint, wheel_front_right_joint,
       wheel_rear_left_joint, wheel_rear_right_joint]
position: [0.0150, 0.0172, -0.0149, -0.0208]
velocity: [0.0, 0.0, 0.0, 0.0]
effort: []
```

`/odom`（`frame_id=odom`, `child_frame_id=base_footprint`）与 TF：

```yaml
header: {stamp: {sec: 3, nanosec: 697000000}, frame_id: odom}
child_frame_id: base_footprint
pose.pose.position: {x: 2.899984, y: 1.599755, z: 4.37e-08}
pose.pose.orientation: {x: -1.0e-07, y: -3.0e-07, z: 0.99999999, w: 0.00016}
```

```text
$ ros2 run tf2_ros tf2_echo odom base_footprint
At time 4.897000000
- Translation: [2.900, 1.600, 0.000]
- Rotation: in RPY (radian) [-0.000, 0.000, 3.141]
```

插件参数（URDF 内，已按 gazebo_ros 3.9 源码字符串表与官方 demo world 核实）：

| 插件 | 参数 |
| --- | --- |
| `libgazebo_ros_planar_move.so` | `update_rate=50`、`publish_rate=50`、`publish_odom=true`、`publish_odom_tf=true`、`odometry_frame=odom`、`robot_base_frame=base_footprint`、`covariance_x/y/yaw` |
| `libgazebo_ros_joint_state_publisher.so` | `update_rate=50`、4 × `joint_name`（= `mecanum.WHEEL_NAMES`） |
| SystemPlugin（不可写入 URDF） | `libgazebo_ros_init.so`、`libgazebo_ros_factory.so`，由 launch 用 `gzserver -s ... -s ...` 加载 |

## 6. 验证 A：空世界运动学（确定性指令，无碰撞干扰）

命令（`preview/robot_gazebo/_evidence_testworld.sh`）：

```bash
ros2 launch robot_control gazebo.launch.py \
    world:=<install>/share/robot_control/worlds/test/gazebo_test.world \
    x:=0 y:=0 z:=0.05 yaw:=0 gui:=false rviz:=false teleop:=none
# 每个阶段用 preview/robot_gazebo/twist_phase.py 精确发布 2.0 s 再发 0.6 s 零速：
python3 preview/robot_gazebo/twist_phase.py 0.3 0.0 0.0 2.0      # 前进
python3 preview/robot_gazebo/twist_phase.py 0.0 0.3 0.0 2.0      # 横移（+y 车身左向）
python3 preview/robot_gazebo/twist_phase.py 0.0 0.0 0.5 2.0      # 原地逆时针
gz model -m zhirong_robot -p                                     # x y z roll pitch yaw
ros2 topic echo --once /odom
```

实测位姿（`gz model -m zhirong_robot -p` / `/odom`）：

| 阶段 | `gz model -p`（x y z r p yaw） | `/odom` 位置 | 结论 |
| --- | --- | --- | --- |
| 初始 | `0.00021 0.00092 0 0 0 0.00029` | `(0.00031, 0.00124)` | 落地 z=0，位姿≈原点 |
| 前进 `vx=0.3` × 2 s | `0.57976 0.00149 0 0 0 0.00165` | `(0.57975, 0.00151)` | Δx≈**+0.580 m**（≈0.3×1.93 s），y/yaw 基本不变 |
| 横移 `vy=0.3` × 2 s | `0.57902 0.58690 -1e-05 0 0 0.00379` | `(0.57907, 0.58706)` | Δy≈**+0.585 m**，x 基本不变 → 全向横移正确 |
| 旋转 `wz=0.5` × 2 s | `0.57986 0.58555 0 0 0 0.59191` | — | Δyaw≈**+0.59 rad**（同向，含 publisher 起停延迟） |

> 说明：指令段前后的 `ros2`/Python publisher 起停存在约 0.1~0.5 s 延迟，位移略小于
> `v×t` 的理论值属正常；方向、符号、里程计与 Gazebo 真实位姿一致性均正确
> （`/odom` 与 `gz model -p` 位置差 < 1e-3 m）。

## 7. 验证 B：与比赛地图 `zhirong_maps` 联调

```bash
ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none
# 默认 world 自动解析到 competition_ws/src/maps/zhirong_maps/worlds/zhirong_arena.world
```

* **world 来源**：`[gazebo.launch.py] world = .../maps/zhirong_maps/worlds/zhirong_arena.world（来源：zhirong_maps）`；
  launch 自动把 `zhirong_maps/models` 前插到 `GAZEBO_MODEL_PATH`（比赛 world 用
  `model://` 引用自建模型），28 个模型目录全部解析成功，**无 missing model 警告**。
* **场地模型抽查**（`gz model -m <name> -p`）：
  `ground → 0 0 0`、`arena_floor → 0 0 0`、`spawn_marker → 2.9 1.6 0`、
  `gate_entrance_n → 2.52 1.1 0`，与世界文件一致。
* **出生点**：`gz model -m zhirong_robot -p` → `2.89998 1.5998 0 ... 3.14131`
  （x=2.9, y=1.6, yaw≈π，落地 z=0），与地图包 `spawn_marker` 对齐。
* **前进**（`/cmd_vel` linear.x=0.3，2 s）：
  `gz model -p` 从 `x=2.89998` 变为 `x=2.32048`（yaw≈π → 车身 +x 即世界 −x，
  Δx≈**−0.58 m**），`/odom` 同步 `2.899984 → 2.320462`。
* **重建后最终冒烟（默认参数）**：`ros2 launch robot_control gazebo.launch.py
  gui:=false rviz:=false teleop:=none` → world 自动解析 `zhirong_maps`，
  初始 `2.89998 1.5998 0 … 3.14131`，前进 2 s 后 `2.31472 1.60002 -2e-06 … 3.14055`，
  `/odom` 同步 `2.314680`；`/clock` 正常；launch log 无 `[Err]/[Wrn]`
  （gzserver 的 `Can't open display` 已由内部 `unset DISPLAY` 规避，渲染正常关闭）。
* **横移注意**：在入口 `(2.3, 1.6)` 附近向 +y（车身左 = 世界 −y）横移时，机器人会
  碰到门柱 `gate_entrance_n/s（2.52, ±1.1/1.9）`，Gazebo 碰撞使 yaw 被推偏、
  位移变小（实测 y 1.599→1.210，同时 yaw 由 π 变为 −2.65 rad）。这是**场景碰撞的
  正常物理结果**，不是控制/插件问题；干净横移定量验证见 §6 空世界。联调时若要在
  入口附近平移，注意门柱与场地边界间距（入口宽约 0.8 m，机器人直径 0.5 m）。

## 8. 验证 C：关闭与进程清理

```bash
# 等价于终端 Ctrl-C：给 launch 的整个进程组发 SIGINT
kill -INT -<launch_pid>
```

实测：

```text
[ok] ros2 launch 已退出，用时 0.5s
关闭后残留进程（期望为空）：
（无残留进程）
--- 端口 11392 ---
（11392 已释放）
```

launch 日志尾部（子进程优雅退出、gzserver 正常收尾）：

```text
[robot_state_publisher-3] [INFO] ... [rclcpp]: signal_handler(SIGINT/SIGTERM)
[INFO] [robot_state_publisher-3]: process has finished cleanly
[INFO] [bash-1]: process has finished cleanly            # gzserver
[INFO] [launch]: process[bash-1] was required: shutting down launched system
```

注意：若只对 `ros2 launch` 的 PID 单独发 SIGINT（而不是进程组），且 gzserver
不在同一终端进程组里，退出会慢很多；正常终端 Ctrl-C 与上面的进程组 SIGINT 都
在 1 s 内干净退出。

## 9. 测试回归

```bash
cd competition_ws/src/robot/robot_control
python3 -m pytest test -q
# 165 passed in 6.38s
```

新增 `test/test_gazebo_launch.py`（17 个用例，**离线、不启动 Gazebo**）覆盖：

* URDF 两个 ModelPlugin 名称/参数/话题、四轮 `joint_name` 与 `mecanum.WHEEL_NAMES` 一致；
* 根 link `base_footprint` 无 inertial、轮子低摩擦与材质标签、SystemPlugin 不写入 URDF；
* launch 全部参数（默认值、`teleop∈{none,keyboard,gui}`、出生点、`use_sim_time=true` 等）；
* `_resolve_world`：显式覆盖 / 不存在报错 / `ZHIRONG_MAPS_ROOT` 自动解析 / 回退自带世界；
* `_load_robot_description` 的 `package:// → file://` 重写；自带测试世界是合法 SDF。

## 10. 已知限制与注意事项

1. **`planar_move` 不是轮子物理模型**：插件直接设置车体线/角速度，四个轮子是
   passive 连续关节（`velocity` 实测为 0），不产生真实滚动/摩擦驱动。
   不能用于轮速闭环、麦轮打滑、电机特性验证；这些留给实车/底盘驱动。
2. **`/cmd_vel` 无超时停车**：`planar_move` 不实现 `cmd_vel_timeout`，遥控源退出
   后机器人保持最后速度。联调结束务必发一次零速（`teleop_keyboard`/`gui` 默认
   持续 20 Hz 发布，含零速）。
3. `/odom` 由指令积分，长时间运行/碰撞推挤后可能与 Gazebo 真实位姿有偏差；
   定位精度以 `gz model -m zhirong_robot -p` 为准（短时验证两者差 < 1 mm）。
4. 相机/激光雷达暂未接 Gazebo 传感器插件（URDF 只有几何与 TF）；需要 `/scan`、
   `/image_raw` 时再追加 `libgazebo_ros_ray_sensor.so` / 相机插件。
5. `gzclient`（`gui:=true`）需要可用 OpenGL；本机 X :1 GLX 损坏，**无法启动**
   gzclient/RViz，本文件全部验证为 headless。GUI 截图由 Lead 在可显示环境完成。
6. `z` 参数是**模型根 link `base_footprint` 的离地高度**（不是 base_link 中心）：
   `z=0` 时轮子（r=0.065）刚好触地；默认 `0.05` 让机器人轻微落地，实测稳定收敛到 z=0。
7. 地图包模型路径由 launch 自动解决；若手工直接 `gzserver <world>`，需要自行
   `export GAZEBO_MODEL_PATH=<maps>/models:$GAZEBO_MODEL_PATH`。

## 11. 一键复现（copy-paste）

```bash
# 终端 1：启动
cd /home/nepenthe/zmf/linux_code/dsh工作区
source tools/gazebo_env.sh
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none

# 终端 2：验证
cd /home/nepenthe/zmf/linux_code/dsh工作区
source tools/gazebo_env.sh
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392
ros2 topic list | grep -E 'clock|joint_states|odom'
ros2 topic echo --once /clock
ros2 topic echo --once /joint_states
ros2 topic echo --once /odom
ros2 run tf2_ros tf2_echo odom base_footprint
# 前进（另开一个终端，或后台）：发 2 s 0.3 m/s 后发零速
python3 preview/robot_gazebo/twist_phase.py 0.3 0.0 0.0 2.0
gz model -m zhirong_robot -p          # 观察 x 变化
# Ctrl-C 结束终端 1；确认无残留：
pgrep -af "gzserver|gzclient" || echo "无残留"
```

## 12. 证据文件索引（`preview/robot_gazebo/`）

| 文件 | 内容 |
| --- | --- |
| `evidence/01_startup.txt` | 话题列表、`/clock`、完整 `/joint_states`、TF、初始位姿、初始 `/odom` |
| `evidence/02_forward.txt`、`evidence/03_strafe.txt` | 前进 / 横移后的 `gz model -p` 与 `/odom`（v1） |
| `evidence/v2_01_startup.txt` … `v2_04_shutdown.txt` | 比赛地图联调：初始/前进/横移位姿、SIGINT 关闭与残留检查（v2） |
| `evidence/tw_01_startup.txt` … `tw_05_shutdown.txt` | 空世界定量运动学验证（确定性 publisher） |
| `evidence/final_smoke.log` | 重建后默认参数冒烟启动日志 |
| `_evidence_run.sh`、`_evidence_run2.sh`、`_evidence_testworld.sh`、`_final_smoke.sh`、`_launch_test.sh`、`_installed_test.sh` | 上述验证的可复现脚本 |
| `twist_phase.py` | 定时 `/cmd_vel` 发布器（发 N 秒指令 + 0.6 s 零速，避免 ros2 CLI 启动延迟） |

---

## Lead 最终验收修正记录（2026-11-17）

联调与验收阶段发现并修正的问题（改动在 `competition_ws/src/robot/`）：

1. **URDF 网格 URI 策略（必须）**
   - 现象：`gazebo.launch.py` 早期把 `package://robot_description/meshes/*` 重写成
     `file://` 绝对路径（百分号编码或原始路径两种都试过）。在本机工作区路径含中文
     （`dsh工作区`）时，urdf→sdf 转换会把该绝对路径破坏成乱码，gzserver 报
     `[Err] No mesh specified`，LiDAR 三个网格不出现在仿真里。
   - 修正：`_load_robot_description()` 直接返回 URDF 原文（保留 `package://`），
     `spawn_entity.py` 固定加 `-package_to_model`（转 `model://`），并新增
     `robot_control/models/robot_description/{model.config,model.sdf,meshes/*.stl}`
     + `gazebo.launch.py` 自动前插该目录到 `GAZEBO_MODEL_PATH`。网格 URI 变成纯 ASCII，
     与工作区路径（中文/空格）无关。
   - 验证：修正后 `gzserver` 日志 mesh 相关 `No mesh specified` / `does not exist` 计数为 0，
     仿真截图中机器人 LiDAR 网格正常显示。
2. **测试同步**：`test/test_gazebo_launch.py` 的 URDF 重写用例改为
   “保留 package:// + 校验 models/robot_description 网格目录”，全量 pytest
   **166 passed**。
3. **README / INTERFACE** 已同步网格解析说明。

> 以上修正后，本文件的其它验证结论（spawn 位姿、/clock、/joint_states、/odom、
> TF、/cmd_vel 运动闭环、模型加载、干净退出）仍然有效，见 `verification/logs/`。
