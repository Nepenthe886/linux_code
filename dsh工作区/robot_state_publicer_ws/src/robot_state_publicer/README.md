# robot_state_publicer

模拟 Livox Mid-360 的 LiDAR + IMU 数据发布包，用于在没有实机雷达时跑通感知/定位算法。

> **在比赛仿真里的默认数据源是 Gazebo 传感器**（`robot_control/config/livox_mid360_sensors.xml`：
> ray 传感器对比赛场景做真实射线 -> `/livox/lidar`，imu 传感器 200 Hz -> `/livox/imu`，随机器人 URDF 一起 spawn）。
> 本包是**合成数据源**，通过 `ros2 launch bring_up bring_up.launch.py lidar_sim:=python` 启用
> （点云是通用室内占位、不依赖 Gazebo 场景）；两者互斥，避免同话题双发布。

## 话题

| 话题 | 类型 | 频率 | 说明 |
|---|---|---|---|
| `/livox/imu` | `sensor_msgs/msg/Imu` | 标称 200 Hz（实测 ~150–200） | IMU 原始角速度/线加速度，frame=`livox_frame`（bring_up 集成时为 `livox_mid360_link`） |
| `/livox/lidar` | `sensor_msgs/msg/PointCloud2` | 10 Hz | 20000 点/帧，驱动兼容点结构 |
| `/livix/lidar` | `sensor_msgs/msg/PointCloud2` | 10 Hz | `/livox/lidar` 的别名（按需求中的拼写保留） |

> 本包使用 `PointCloud2`（`livox_ros_driver2` 的 `xfer_format=0` 格式），字段布局与驱动
> `LivoxPointXyzrtlt` 一致：`x/y/z/intensity` float32、`tag/line` uint8、`timestamp` float64，
> `point_step=26`。RViz 的标准 `PointCloud2` 显示可以直接使用。
>
> 如果算法必须使用 Livox 自定义 `CustomMsg`，可在此基础上再增加一个 CustomMsg 发布器，
> 但需要先构建 `livox_ros_driver2` 的消息包。

## 数据内容

每帧对以下场景做射线求交，生成带噪声的室内点云：

- 地面（z = -0.27 m）和天花板；
- 四面墙（±3.5 m）；
- 两个箱体和一个圆柱障碍物；
- 水平 360°、垂直 -7°~52°（Mid-360 FOV）；
- 距离噪声约 3 mm，强度按材质/反射率生成。

IMU 在静止状态下输出重力 `9.80665 m/s²`，带小幅噪声；不提供姿态估计
（`orientation_covariance[0] = -1`）。

## 运行

```bash
cd "/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup"
colcon build --packages-select robot_state_publicer --symlink-install
source install/setup.bash
ros2 launch robot_state_publicer mid360_sim.launch.py
```

或直接运行：

```bash
ros2 run robot_state_publicer mid360_sim
```

## 在比赛仿真中的集成（bring_up）

`ros2 launch bring_up bring_up.launch.py`（或 `demo.launch.py`）默认会一并拉起本节点
（`lidar:=true`），与 Gazebo、机器人共用同一套 TF/时间轴：

* `frame_id:=livox_mid360_link`、`publish_tf:=false`（TF 由 URDF/robot_state_publisher 提供，避免重复）；
* 时间戳：Gazebo 的 `/clock` 只有约 10 Hz，若节点 `use_sim_time:=true`，ROS 定时器会被
  时钟跳变限制到 ~20 Hz（IMU 无法达到标称频率）。本节点采用 **定时器按真实时间运行 +
  消息时间戳用 `/clock` 插值** 的方式（参数 `stamp_from_sim_clock:=true`，默认开），
  实测点云 10 Hz、IMU ~154 Hz、时间戳与 `/clock` 偏差 < 0.01 s。

可用 launch 参数：`use_sim_time`、`frame_id`、`publish_tf`、`stamp_from_sim_clock`。

检查数据：

```bash
ros2 topic list | grep -E 'livox|livix'
ros2 topic hz /livox/imu
ros2 topic hz /livox/lidar
ros2 topic echo /livox/imu --once
```

RViz 中 Fixed Frame 可设为 `livox_frame`，添加 `PointCloud2` 显示并选择
`/livox/lidar`。节点默认发布静态 TF `base_link -> livox_frame`（z=0.27 m）；
若已有 `robot_state_publisher`，该变换也可由 URDF/自己的 TF 提供，将
`publish_tf` 设为 `false` 即可。

## 参数

见 `config/mid360_sim.yaml`，可用 `ros2 param set` 或 `--ros-args -p name:=value` 覆盖：

| 参数 | 默认 | 说明 |
|---|---|---|
| `lidar_topic` | `/livox/lidar` | 主点云话题 |
| `lidar_alias_topic` | `/livix/lidar` | 别名点云话题 |
| `imu_topic` | `/livox/imu` | IMU 话题 |
| `frame_id` | `livox_frame` | 点云/IMU 坐标系 |
| `base_frame` | `base_link` | 静态 TF 父坐标系 |
| `lidar_rate` | 10.0 | 点云频率 |
| `imu_rate` | 200.0 | IMU 频率 |
| `points_per_frame` | 20000 | 每帧点数（实际按 200 列 × N 行生成） |
| `max_range` | 40.0 | 最大距离 |
| `lidar_height` | 0.27 | 雷达离地高度，用于地面建模和静态 TF |
| `publish_tf` | true | 是否发布 `base_link -> livox_frame` |
| `publish_alias` | true | 是否发布 `/livix/lidar` 别名 |
| `seed` | 1 | 场景随机种子 |

## 测试

```bash
python3 -m pytest test -q
```
