# robot_description

Zhirong Cup 全向机器人（四轮全向底盘）的 URDF 描述包。当前为**初版几何/参数提案**；雷达采用开源 Mid-360 STL，轮系和传感器位置可在评审后调整。

工作空间级依赖清单见 [`requirements.txt`](../../../requirements.txt)。

- 主体：圆柱体，半径 **0.250 m**（Ø500）、高 **0.200 m**
- 底盘：4 个对称布置的麦克纳姆轮（每轮 9×45° 滚子视觉；碰撞用圆柱包络）
- 顶部：Livox Mid-360 激光雷达（65 × 65 × 60 mm，265 g）
- 前部：深度相机（RealSense D435i 尺寸 90 × 25 × 25 mm）

## 文件结构

```text
robot_description/
├── urdf/omni_robot.urdf          # 机器人 URDF（纯基本几何，无外部 mesh）
├── launch/view_robot.launch.py   # 一键查看机器人（推荐）
├── launch/display.launch.py      # 兼容别名，等价于 view_robot
├── rviz/omni_robot.rviz          # RViz2 显示配置
├── meshes/                       # Mid-360 开源 STL（按材质拆分）
│   ├── mid360_base.stl           # 银色散热底座/连接器
│   ├── mid360_dome.stl           # 蓝色半球罩
│   ├── mid360_top.stl            # 顶部黑色 logo 区域
│   └── LICENSE_mid360.txt        # MIT 许可证
├── scripts/zero_joint_states.py  # joint_state_publisher 缺失时的零位回退
├── package.xml
├── CMakeLists.txt
└── README.md
```

## 工作空间布局

```text
Zhirong Cup/                        # colcon 工作空间根目录（在此执行 colcon build）
├── requirements.txt                # Python / ROS 依赖清单
├── src/
│   ├── robot/
│   │   ├── robot_control/          # 预留
│   │   └── robot_description/      # 本包
│   ├── drivers/
│   ├── localization_and_mapping/
│   ├── maps/
│   ├── object_identification/
│   └── robotic arm control/
├── build/                          # colcon 构建后生成
├── install/                        # colcon 构建后生成
└── log/                            # colcon 构建后生成
```

## 依赖安装

```bash
# Python 依赖
cd "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
pip install -r requirements.txt

# ROS 2 依赖（rosdep；或按 requirements.txt 底部列出的 apt 包安装）
rosdep install --from-paths src --ignore-src -r -y
```

## 快速可视化

依赖：ROS 2 Humble、`rviz2`、`robot_state_publisher`。
`joint_state_publisher` 为可选依赖：已安装时使用标准节点，未安装时 launch 自动启用
`scripts/zero_joint_states.py` 把四个轮关节固定在 0 位，保证 TF 树完整。

```bash
# 可选：安装标准 joint_state_publisher（缺失时也能启动）
sudo apt install ros-humble-joint-state-publisher

# 方式 A：从工作空间根目录构建并启动（推荐）
cd ".../Zhirong Cup"
colcon build --packages-select robot_description --symlink-install
source install/setup.bash
ros2 launch robot_description view_robot.launch.py

# 方式 B：不编译，直接从源码目录启动
cd ".../src/robot/robot_description"
ros2 launch ./launch/view_robot.launch.py
```

> `view_robot.launch.py` 在启动时会把 URDF 中的 `package://robot_description/...`
> 临时重写为 URL 编码的 `file://` 路径，因此从源码目录直接启动也能加载 `meshes/`；
> URDF 文件本身仍保留 `package://`，安装后同样可用。
>
> `view_robot.launch.py` 会加载 URDF、启动 `robot_state_publisher`、关节状态发布和 RViz；
> 可用参数：`rviz:=true/false`、`use_sim_time:=true/false`。`display.launch.py` 保留为兼容别名。

> `build/`、`install/`、`log/` 是 colcon 在 `Zhirong Cup` 根目录生成的工作空间产物，
> 不应提交到 Git；方式 B 不产生这些目录。

RViz 中 Fixed Frame 为 `base_footprint`，RobotModel 从 `/robot_description` 话题读取模型。

## 当前设计参数（初版）

| 项目 | 参数 | 说明 |
| --- | --- | --- |
| 车体 | 圆柱 R0.250 m × H0.200 m | 底面离地 0.140 m，顶面 0.340 m |
| 轮子 | 4 × 麦克纳姆轮 | 半径 0.065 m，宽 0.040 m |
| 滚子 | 每轮 9 × 45° 滚子 | R0.010 m、长 0.028 m；左侧 +45°，右侧 -45°；仅 visual |
| 轮心位置 | x = ±0.170, y = ±0.170, z = 0.065 | 轴距 = 轮距 = 0.340 m |
| 轮顶 / 车底间隙 | 0.130 / 0.140 m | 仅 10 mm，后续可加高车体或开轮拱 |
| 激光雷达 | Livox Mid-360（开源 STL） | 安装于车体顶面中心，顶面 z = 0.400 m |
| 深度相机 | 90 × 25 × 25 mm | 车体正前方，光心 z = 0.270 m |
| 总高 | 0.400 m | 含雷达 |
| 估计质量 | 约 9.96 kg | 车体 8.0 + 轮 4×0.4 + 雷达 0.265 + 相机 0.09 |

轮距较车体直径小，四个轮子基本藏在圆柱投影内（俯视时轮缘会从圆柱轮廓外露出约 4 cm），有利于缩小转弯包络；如需更高稳定性，可将 `0.170` 增大到 `0.18~0.19`，但轮子外露会更多。

## 坐标系约定

- `base_footprint`：地面投影点，z = 0
- `base_link`：车体几何中心，z = 0.240
- `+X`：车头（相机方向）；`+Y`：左侧；`+Z`：向上（REP-103）
- `livox_mid360_link`：雷达安装面中心（车体顶面），x 朝前
- `camera_link`：相机外壳中心，x 朝前、y 朝左、z 朝上
- `camera_optical_frame`：相机光学坐标系，z 朝前、x 朝右、y 朝下

## 轮系运动学（麦克纳姆轮）

设 `vx, vy` 为车体前向/左向速度，`wz` 为绕 z 轴角速度，`r = 0.065`，`lx + ly = 0.340`：

```text
w_FL = ( vx - vy - 0.340 * wz ) / r
w_FR = ( vx + vy + 0.340 * wz ) / r
w_RL = ( vx + vy - 0.340 * wz ) / r
w_RR = ( vx - vy + 0.340 * wz ) / r
```

符号与麦轮滚子旋向有关，实车标定后可能需要整体取反或调整某一对角轮。

## 初版简化说明（评审时请确认）

1. **轮子视觉**由轮芯（R0.050）、两侧板（R0.050）和 9 个 45° 滚子组成，左侧轮滚子 +45°、右侧轮 -45°。
   碰撞体仍用 R0.065 × W0.040 的圆柱包络，算法/仿真使用简单几何；视觉滚子不参与碰撞。
2. 车体、相机为基本几何近似；雷达使用开源 STL（仅按材质拆成底座/球罩/顶盖，几何未改）。
3. 惯性参数按均匀密度估算，仅供 Gazebo/仿真起步，精确实车参数需重新标定。
4. 未添加 `<gazebo>`、`<transmission>`、ros2_control 配置，本包只负责描述与可视化。
5. 雷达坐标系取安装面中心；若 Livox 驱动/标定要求不同原点，可在 `livox_mid360_joint` 或驱动外参中补偿。

## 第三方模型与许可

`meshes/mid360_*.stl` 来源于开源的 Livox Mid-360 STL 模型：

- 下载页面：<https://gitee.com/Wzichen/livox_laser_simulation>（`meshes/mid360.STL`）
- 上游项目：<https://github.com/Livox-SDK/livox_laser_simulation>
- 许可证：MIT，Copyright (c) 2021 livox，全文见 `meshes/LICENSE_mid360.txt`

The STL was split into base/dome/top by triangle position only to assign three URDF
materials; the geometry itself is unchanged. If you replace or redistribute the
mesh, keep the MIT license notice.
