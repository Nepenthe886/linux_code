# bring_up —— 戎智杯反恐搜救赛项「一键启动」包

一条命令拉起完整仿真链路（Gazebo 比赛场景 + 机器人 + TF + 里程计 + 可选遥控/可视化）：

```bash
cd "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
bash scripts/build.sh                     # 首次或改动后构建
source install/setup.bash

# 一键启动（headless，服务器/SSH 默认）
ros2 launch bring_up bring_up.launch.py
```

## 1. 它做了什么

`bring_up.launch.py` 是对 `robot_control/gazebo.launch.py` 的统一入口封装，
一条命令完成：

| 步骤 | 内容 |
| --- | --- |
| 1 | `gzserver` 加载比赛场景 `zhirong_maps/worlds/zhirong_arena.world`（5m×5m、16 单元格、黄/桔/红区、L/T/工型障碍、双斜坡、目标板、圆环、入口/出口） |
| 2 | 机器人 `robot_description`（URDF + Gazebo 插件）spawn 到入口外侧 `(2.90, 1.60, yaw=π)` |
| 3 | `robot_state_publisher` 发布 URDF→TF 树 |
| 4 | Gazebo 插件发布 `/clock`、`/joint_states`、`/odom`、TF `odom→base_footprint` |
| 5 | **Mid-360 激光雷达 + IMU 模拟**（`robot_state_publicer/mid360_sim.launch.py`）：`/livox/lidar`（10 Hz、20000 点/帧、PointCloud2）、`/livox/imu`（~150–200 Hz），`lidar:=false` 可关 |
| 6 | 可选：`teleop:=keyboard|gui` 遥控、`rviz:=true`、`gui:=true`（gzclient） |

## 2. 启动方式

```bash
# 1) 默认：headless（无显示器/服务器）
ros2 launch bring_up bring_up.launch.py

# 2) 有显示器：Gazebo 客户端 + RViz + 图形遥控面板（演示模式）
ros2 launch bring_up demo.launch.py

# 3) 指定世界文件 / 出生点
ros2 launch bring_up bring_up.launch.py world:=/abs/path/zhirong_arena.world x:=0 y:=0 yaw:=0

# 4) 终端键盘遥控（建议另开终端）
ros2 launch bring_up bring_up.launch.py teleop:=keyboard

# 5) 只开 RViz（无 gzclient）
ros2 launch bring_up bring_up.launch.py rviz:=true
```

## 3. launch 参数（与 robot_control/gazebo.launch.py 一致）

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `world` | `''` | 世界文件绝对路径；留空自动解析 `zhirong_maps`（找不到回退 `robot_control` 自带测试世界并 warning） |
| `x` / `y` / `z` / `yaw` | `2.9` / `1.6` / `0.05` / `π` | 机器人 spawn 位姿（入口外侧、面向场内） |
| `use_sim_time` | `true` | Gazebo 模式必须为 true（使用 `/clock`） |
| `gui` | `false` | 是否启动 gzclient（需要可用显示器/OpenGL） |
| `rviz` | `false` | 是否启动 RViz2（Fixed Frame=odom） |
| `teleop` | `none` | `none` / `keyboard` / `gui` |
| `verbose` | `false` | gzserver `--verbose` |
| `model_name` | `zhirong_robot` | Gazebo 模型名（`gz model -m zhirong_robot -p` 可查位姿） |
| `pause` | `false` | gzserver 是否以暂停状态启动 |
| `lidar` | `true` | 是否启动 Mid-360 激光雷达/IMU 模拟（`robot_state_publicer`） |

### 3.1 激光雷达（Mid-360）说明

`lidar_sim` 决定数据源（默认 `gazebo`）：

| `lidar_sim` | 点云 | IMU | 说明 |
| --- | --- | --- | --- |
| `gazebo`（默认） | `gzserver` 里 Mid-360 ray 传感器对**比赛场景**做真实射线：`/livox/lidar`（10 Hz、240×8 线、0.35–40 m，PointCloud2）+ 别名 `/livix/lidar` | Gazebo imu 传感器：`/livox/imu`（**200 Hz**，含重力） | 传感器块随 URDF 一起 spawn（`lidar_sensors:=true`），落地即真实场景点云，适合建图/避障联调 |
| `python` | `robot_state_publicer` 合成点云：`/livox/lidar`、`/livix/lidar`（10 Hz、20000 点/帧、Livox 26 字节结构） | 合成 IMU：`/livox/imu`（~150–160 Hz） | 不需要 Gazebo 传感器，纯算法联调/无场景依赖时用（`lidar_sim:=python`） |
| `off` | 关闭（`lidar:=false` 等价） | 关闭 | 省 CPU |

公共约定：

* **frame 统一为 `livox_mid360_link`**（URDF 中 `base_link` 上方 0.10 m）；TF 由 `robot_state_publisher` 提供。
* `gazebo` 模式的点云是**比赛场景的真实射线结果**（围挡/工型/斜坡/边界都会出现在点云里）；
  `range.min=0.35 m` 是为了滤掉雷达自身/车体近场遮挡（车体到雷达约 0.25–0.30 m）。
* `python` 模式的合成点云是"通用室内占位"（地面/墙/箱体），**不是比赛场景**；此时节点
  内部定时器按真实时间跑、消息时间戳用 `/clock` 插值（Gazebo `/clock` 只有 ~10 Hz，
  用 `use_sim_time:=true` 会把 IMU 限制到 ~20 Hz）。
* 两种模式的 `/livox/lidar` 帧率都是 ~10 Hz；IMU 在 `gazebo` 模式是标准 200 Hz。

查看数据：

```bash
ros2 topic hz /livox/lidar     # ~10 Hz
ros2 topic hz /livox/imu       # gazebo 模式 ~200 Hz；python 模式 ~150-160 Hz
ros2 topic echo --once /livox/imu
# RViz2：Fixed Frame 选 livox_mid360_link 或 odom，添加 PointCloud2 -> /livox/lidar
```

## 4. 启动后自检 / 遥控

```bash
ros2 topic list | grep -E 'clock|odom|joint_states|cmd_vel'
ros2 topic echo --once /odom
ros2 run tf2_ros tf2_echo odom base_footprint

# 发速度（planar_move）：前进 / 横移 / 自转
ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}"
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}"    # 停车

gz model -m zhirong_robot -p                                    # Gazebo 位姿
```

## 5. 常见问题

* **`process has died ... exit code 255`**：上一次 Gazebo 没退干净占用 master 端口。
  运行 `bash scripts/kill_sim.sh` 或直接用 `bash scripts/run_sim.sh`（自动清理）。
  `bring_up.launch.py` 启动前也会主动检测端口并给出中文提示。
* **`gazebo_ros not found`**：系统未装 Gazebo/桥接包，执行
  `sudo bash scripts/install_environment.sh`。
* **`demo.launch.py` 启动后 Gazebo 一直「无响应」**（已修复：gzclient 缺
  `GAZEBO_MODEL_PATH` 导致卡在在线模型库更新；launch 现在会给 gzclient 注入
  与 gzserver 相同的模型路径。如仍出现，先按下面条目排查）：当前 DISPLAY 不能创建 OpenGL
  上下文（典型：NVIDIA 驱动异常）。`demo.launch.py` 现在会**提前检测并直接报错退出**
  （不再卡死）。可用替代方案：
  * `ros2 launch bring_up bring_up.launch.py`（headless，数据照常发布）；
  * `bash scripts/view_sim.sh`（Xvfb 软件渲染 + rqt_image_view 实时看 Gazebo 画面，
    不依赖本机 OpenGL）；
  * 或修复 GPU 驱动（`nvidia-smi` 检查，`sudo ubuntu-drivers autoinstall` 后重启）。

依赖声明见 `package.xml`（`robot_control` / `robot_description` / `zhirong_maps` /
`gazebo_ros` / `gazebo_plugins` / `robot_state_publisher`）。
