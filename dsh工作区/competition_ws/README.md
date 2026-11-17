# “戎智杯”反恐搜救赛项 —— 仿真工作空间

ROS 2 Humble + Gazebo Classic 11 的比赛仿真工作空间：按规则文档图 2 复现的
5 m×5 m 反恐搜救比赛场景，以及参赛机器人的建模、遥控与 Gazebo 接入。

## 目录结构

```text
competition_ws/
├── scripts/                      # 环境/构建/启动 统一脚本（迁移到新机器只需这三个）
│   ├── install_environment.sh    # 系统依赖安装（Gazebo Classic 11 + gazebo_ros 桥接 + rosdep）
│   ├── build.sh                  # colcon build --symlink-install
│   └── run_sim.sh                # 启动比赛场景 + 机器人
├── src/
│   ├── bring_up/                 # ★ 一键启动包（bringup）：一条命令拉起场景+机器人+TF+遥控
│   ├── maps/zhirong_maps/        # 比赛场景包（world / models / launch / plan.png / 2D 栅格地图）
│   └── robot/
│       ├── robot_description/    # 机器人 URDF（含 Gazebo 插件/材质/摩擦标签）
│       ├── robot_control/        # 遥控/GUI、Gazebo launch、单测、文档
│       └── INTERFACE.md          # 内部接口契约（话题/TF/参数/launch 约定）
└── requirements.txt              # Python 侧依赖（ROS 依赖见 package.xml / scripts）
```

## 环境统一安装（推荐，一次性）

```bash
# 系统统一安装：apt 装 ROS 2/Gazebo 系统依赖 + 按 requirements.txt 装 Python 依赖
sudo bash scripts/install_environment.sh
```

脚本会：
1. `apt-get install gazebo gazebo-common ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins ros-humble-gazebo-ros`
   —— ROS 2 / Gazebo 是系统级二进制，**不能通过 pip/requirements.txt 安装**；
2. 校验 `gzserver` 与 `ros2 pkg prefix gazebo_ros`；
3. `rosdep install --from-paths src --ignore-src -r -y` 按各包 `package.xml` 补齐剩余 ROS 依赖；
4. 调用 `scripts/setup_python_env.sh`：创建带 `--system-site-packages` 的 `.venv`（仍可 import `rclpy`），
   并按 **`requirements.txt`** 用 pip 安装全部 Python 依赖（含本机无 pip 时的自动引导）。

安装后 **不需要任何 Gazebo 环境脚本**，`/opt/ros/humble` 标准环境即可运行。

### 只装 Python 依赖（requirements.txt）

已有 ROS 2 + Gazebo 环境时，单独安装 Python 侧依赖：

```bash
bash scripts/setup_python_env.sh          # 创建 .venv 并 pip install -r requirements.txt
source .venv/bin/activate                 # 使用该环境
```

> 说明：本机（当前这台开发机）沙箱没有 sudo 权限，验证时采用了“用户态解包安装”
> 的临时方案（`dsh工作区/gazebo_userland` + 环境脚本）。`scripts/run_sim.sh` 与
> `robot_control` 的 launch 会自动识别这种用户态前缀，所以上述临时方案下也能直接
> 运行；统一安装后该逻辑自动不生效。

## 构建与启动

```bash
bash scripts/build.sh

# ★ 一键启动（headless，服务器/SSH 默认）
ros2 launch bring_up bring_up.launch.py
# 或等价的封装脚本（会自动清理上次残留进程）
bash scripts/run_sim.sh
# 有显示器：演示模式（Gazebo 客户端 + RViz + 图形遥控面板）
ros2 launch bring_up demo.launch.py
# 或： bash scripts/run_sim.sh gui:=true rviz:=true
# 附带终端键盘遥控（Gazebo 下按键发 /cmd_vel）
bash scripts/run_sim.sh teleop:=keyboard

# 本机无可用 OpenGL（Gazebo GUI/RViz 打不开）时的实时画面：
# Xvfb 软件渲染 Gazebo 相机 -> rqt_image_view 显示（无需 OpenGL）
sudo apt install -y xvfb     # 首次（或 sudo bash scripts/install_environment.sh）
bash scripts/view_sim.sh
```

启动后 `gzserver` 加载 `src/maps/zhirong_maps/worlds/zhirong_arena.world`，
机器人 spawn 在入口外侧 `(2.90, 1.60, yaw=π)`，发布 `/clock`、`/joint_states`、
`/odom` 与 TF `odom→base_footprint`；向 `/cmd_vel` 发速度即可运动。

验收脚本（构建 + 启动 + 话题/TF + 全向运动 + 模型加载 + 清理）在开发工作区
`dsh工作区/verification/`，实测报告见
`src/maps/zhirong_maps/docs/sim_verification/VERIFICATION_REPORT.md`。

## 常见问题：`demo.launch.py` 启动后 Gazebo 无响应

**症状**：`ros2 launch bring_up demo.launch.py` 后 Gazebo 窗口出现但一直「未响应」，
只能强制关闭；RViz 同样打不开。

**原因有两类，按时间先后都遇到过：**

1. **OpenGL/驱动不可用**：`DISPLAY` 无法创建 GLX 上下文（NVIDIA 驱动未生效、
   `nvidia-smi` 报错）。`gzclient`/`rviz2` 都依赖 GLX，会卡死。已通过安装/重启驱动
   解决，并加了 GLX 预检（不可用时直接中文报错，不再卡死）。
2. **gzclient 缺 `GAZEBO_MODEL_PATH`（2026-11-17 定位并修复）**：世界里的机器人带
   `model://robot_description/meshes/*.stl` 网格，`gazebo.launch.py` 早期只把
   `GAZEBO_MODEL_PATH` 注入给 gzserver；gzclient 解析不到本地模型 → 回退请求在线
   模型库（models.gazebosim.org/Fuel），GUI 卡在
   `Waiting for model database update to complete...`，表现为窗口出现但一直「未响应」。
   **修复**：launch 现在给 gzclient 注入与 gzserver 相同的 `GAZEBO_MODEL_PATH`
   （`_model_path_env()`），并新增回归单测。

**现在 launch 会提前检测**：`demo.launch.py`/`gui:=true`/`rviz:=true` 在 GL 不可用时
直接给出中文报错并退出（不再卡死）。

**解决办法（任选其一）**

```bash
# 1) 无显示器方案（本机可用）：headless 仿真 + 数据话题
ros2 launch bring_up bring_up.launch.py

# 2) 实时画面（本机可用）：Xvfb 软件渲染 Gazebo 相机 -> rqt_image_view 显示
sudo apt install -y xvfb         # 首次（或 sudo bash scripts/install_environment.sh）
bash scripts/view_sim.sh

# 3) 修复 GPU 驱动后即可正常开 Gazebo GUI / RViz
nvidia-smi                       # 先确认驱动状态
sudo ubuntu-drivers autoinstall  # 或重装对应 NVIDIA 驱动，然后重启 X / 重启机器
```

> 若本机没有可用 GPU（如虚拟机/容器），Gazebo GUI 与 RViz 都无法使用，
> 请使用方案 1/2；方案 2 的相机画面与 Gazebo 客户端的渲染完全一致。

## 常见问题：`exit code 255` / 端口被占

若 launch 报 `process has died ... exit code 255`，通常是上一次 Gazebo 残留、
master 端口（默认 11345）被占用。运行：

```bash
bash scripts/kill_sim.sh      # 清理残留 gzserver/gzclient
# 或直接用（自动清理）：bash scripts/run_sim.sh
```

`gazebo.launch.py` 启动前会主动检测端口并给出中文提示。

## 迁移到其它机器

1. 拷贝整个工作空间目录（`src/` + `scripts/` + `requirements.txt`）；
2. `sudo bash scripts/install_environment.sh`；
3. `bash scripts/build.sh`；
4. `bash scripts/run_sim.sh`。

> 依赖划分：ROS 2 / Gazebo → `scripts/install_environment.sh`（apt + rosdep）；
> Python 库 → `requirements.txt`（pip，`scripts/setup_python_env.sh`）；
> 全部由 `scripts/install_environment.sh` 一个入口串起来。

所有路径均为工作空间相对路径（`package.xml` 声明依赖、launch 内部按
`ament` 索引/包根目录解析），不依赖特定用户名或绝对路径。
