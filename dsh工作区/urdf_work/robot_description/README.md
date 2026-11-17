# robot_description

Zhirong Cup 全向机器人（四轮全向底盘）的 URDF 描述包。当前为**初版几何/参数提案**，轮系、传感器位置均可在评审后调整。

- 主体：圆柱体，半径 **0.250 m**（Ø500）、高 **0.200 m**
- 底盘：4 个对称布置的麦克纳姆轮（每轮 9×45° 滚子视觉；碰撞用圆柱包络）
- 顶部：Livox Mid-360 激光雷达（65 × 65 × 60 mm，265 g）
- 前部：深度相机（RealSense D435i 尺寸 90 × 25 × 25 mm）

## 文件结构

```text
robot_description/
├── urdf/omni_robot.urdf          # 机器人 URDF（纯基本几何，无外部 mesh）
├── launch/display.launch.py      # robot_state_publisher + 关节状态 + RViz
├── rviz/omni_robot.rviz          # RViz2 显示配置
├── scripts/zero_joint_states.py  # joint_state_publisher 缺失时的零位回退
├── package.xml
├── CMakeLists.txt
└── README.md
```

## 快速可视化

依赖：ROS 2 Humble、`rviz2`、`robot_state_publisher`。
`joint_state_publisher` 为可选依赖：已安装时使用标准节点，未安装时 launch 自动启用
`scripts/zero_joint_states.py` 把四个轮关节固定在 0 位，保证 TF 树完整。

```bash
# 可选：安装标准 joint_state_publisher（缺失时也能启动）
sudo apt install ros-humble-joint-state-publisher

# 方式 A：直接在源码目录启动（无需编译）
cd ".../robot/robot_description"
ros2 launch ./launch/display.launch.py

# 方式 B：如果本包已放进你的 colcon 工作区 src/，按常规构建即可：
# colcon build --packages-select robot_description --symlink-install
# source install/setup.bash
# ros2 launch robot_description display.launch.py
```

> 注意：不要直接在 `Zhirong Cup/robot` 下执行 `colcon build`，否则会在该目录生成
> `build/ install/ log/`，破坏现有工程结构。方式 A 不需要编译，推荐直接使用。

RViz 中 Fixed Frame 为 `base_footprint`，RobotModel 从 `/robot_description` 话题读取模型。

## 当前设计参数（初版）

| 项目 | 参数 | 说明 |
| --- | --- | --- |
| 车体 | 圆柱 R0.250 m × H0.200 m | 底面离地 0.140 m，顶面 0.340 m |
| 轮子 | 4 × 麦克纳姆轮 | 半径 0.065 m，宽 0.040 m |
| 滚子 | 每轮 9 × 45° 滚子 | R0.010 m、长 0.028 m；左侧 +45°，右侧 -45°；仅 visual |
| 轮心位置 | x = ±0.170, y = ±0.170, z = 0.065 | 轴距 = 轮距 = 0.340 m |
| 轮顶 / 车底间隙 | 0.130 / 0.140 m | 仅 10 mm，后续可加高车体或开轮拱 |
| 激光雷达 | Livox Mid-360 | 安装于车体顶面中心，顶面 z = 0.406 m |
| 深度相机 | 90 × 25 × 25 mm | 车体正前方，光心 z = 0.270 m |
| 总高 | 0.406 m | 含雷达 |
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
2. 车体、雷达、相机均为基本几何近似（box/cylinder），没有外观倒角、支架、走线。
3. 惯性参数按均匀密度估算，仅供 Gazebo/仿真起步，精确实车参数需重新标定。
4. 未添加 `<gazebo>`、`<transmission>`、ros2_control 配置，本包只负责描述与可视化。
5. 雷达坐标系取安装面中心；若 Livox 驱动/标定要求不同原点，可在 `livox_mid360_joint` 或驱动外参中补偿。
