# robot_control 内部接口契约（Lead 维护，teammate 必读）

工作区：`/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws`
包路径：`src/robot_control/`（ament_python 包，可直接用 `python3 -m robot_control.xxx` 调试，
最终由 Lead 用 colcon 构建验证后部署到
`/home/nepenthe/zmf/linux_code/competitions/Zhirong Cup/src/robot/robot_control`）。

> 说明：会话文件沙箱只允许写 `dsh工作区`。所有开发都在本工作区完成，Lead 最后统一部署。
> 部署前不要尝试写 `Zhirong Cup` 目录。

## 包结构（固定）

```text
src/robot_control/
├── package.xml                     # Lead
├── setup.py / setup.cfg            # Lead（entry_points 已固定，不要改）
├── resource/robot_control          # Lead
├── robot_control/
│   ├── __init__.py                 # Lead
│   ├── mecanum.py                  # Lead：运动学 + 键位映射（已可用）
│   ├── sim_node.py                 # A：模拟底盘（轮速 -> joint_states/odom/TF）
│   ├── teleop_keyboard.py          # A：终端键盘遥控
│   └── gui_teleop.py               # B：Tkinter 可视化操作界面
├── launch/
│   ├── teleop_gui.launch.py        # B
│   └── teleop_keyboard.launch.py   # B
├── config/teleop.yaml              # B（可选，供 launch 读取默认参数）
├── rviz/teleop.rviz                # B
├── test/
│   ├── test_mecanum.py             # A
│   └── test_gui.py                 # B（无显示时自动 skip）
├── docs/                           # Lead 放截图
└── README.md                       # B
```

**写入范围（避免并发冲突）**：A 只写 `robot_control/sim_node.py`、`robot_control/teleop_keyboard.py`、
`test/test_mecanum.py`；B 只写 `robot_control/gui_teleop.py`、`launch/*`、`config/*`、`rviz/*`、
`README.md`、`test/test_gui.py`。公共文件（setup.py、mecanum.py、package.xml、docs）只有 Lead 写。

## 底盘参数（与 URDF 一致，不要改）

- 轮半径 `wheel_radius = 0.065 m`
- 轮心偏移 `wheel_base_x = 0.170 m`（前后），`wheel_base_y = 0.170 m`（左右）
- 旋转力臂 `lever_arm = wheel_base_x + wheel_base_y = 0.340 m`
- 四轮顺序固定 **FL, FR, RL, RR**，关节名见 `mecanum.WHEEL_NAMES`
- URDF 中四轮 `axis="0 1 0"`，正轮速 = 向车头滚动；`r/4` 等公式见 `mecanum.py` docstring

## ROS 接口（跨节点契约）

| 话题 | 类型 | 方向 | 说明 |
| --- | --- | --- | --- |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | teleop/GUI -> 外部 | 车体速度指令（自动驾驶/导航也用它），`linear.x` 前向、`linear.y` 左向、`angular.z` 逆时针 |
| `/wheel_cmd` | `std_msgs/msg/Float64MultiArray` | teleop/GUI -> sim/driver | 四轮角速度指令 [rad/s]，顺序 FL, FR, RL, RR；`layout.dim[0].label = "wheel_fl, wheel_fr, wheel_rl, wheel_rr"` |
| `/joint_states` | `sensor_msgs/msg/JointState` | sim -> robot_state_publisher | 四个轮关节的 `position`（rad，连续累积可回绕）与 `velocity`（rad/s） |
| `/odom` | `nav_msgs/msg/Odometry` | sim -> RViz/外部 | `frame_id=odom`, `child_frame_id=base_footprint`，含 pose/twist |
| `/livox/lidar` | `sensor_msgs/msg/PointCloud2` | 激光雷达 -> 感知/定位 | 默认 Gazebo ray 传感器对比赛场景的真实射线（10 Hz、240×8 线、0.35–40 m，`frame_id=livox_mid360_link`）；`lidar_sim:=python` 时为合成点云（20000 点/帧、`point_step=26`） |
| `/livox/imu` | `sensor_msgs/msg/Imu` | 激光雷达 -> 感知/定位 | 默认 Gazebo imu 传感器 200 Hz；python 模式为合成 IMU ~150–160 Hz；`frame_id=livox_mid360_link`，含重力 9.80665 |
| `/livix/lidar` | `sensor_msgs/msg/PointCloud2` | 同 `/livox/lidar` | 按需求文档拼写保留的别名话题 |
| TF `odom -> base_footprint` | `tf2` | sim -> RViz | 模拟底盘积分位姿；`base_footprint -> base_link` 由 robot_state_publisher 发布 |

键盘 -> 车体速度统一调用 `mecanum.keys_to_body()`，轮速统一调用
`mecanum.MecanumKinematics.body_to_limited_wheels()`，**不要重复实现公式**。

## 节点参数（`config/teleop.yaml` 与 launch 默认值保持一致）

`sim_node`（节点名 `mecanum_sim`）：

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `wheel_radius` | 0.065 | 轮半径 |
| `wheel_base_x` / `wheel_base_y` | 0.170 | 轮心偏移 |
| `max_wheel_speed` | 30.0 | 轮速上限 rad/s |
| `publish_rate` | 50.0 | 状态发布 Hz |
| `cmd_timeout` | 0.5 | s，超时未收到 `/wheel_cmd` 自动停车 |
| `command_accel_limit` | 60.0 | rad/s²，指令斜坡（0 表示不限制） |
| `odom_frame` / `base_frame` | `odom` / `base_footprint` | |
| `wheel_cmd_topic` | `/wheel_cmd` | |
| `joint_states_topic` | `/joint_states` | |
| `odom_topic` | `/odom` | |
| `publish_odom_tf` | true | 是否广播 odom->base_footprint |

`gui_teleop` / `teleop_keyboard` 公共参数：`cmd_vel_topic=/cmd_vel`、`wheel_cmd_topic=/wheel_cmd`、
`linear_speed=0.30`、`lateral_speed=0.30`、`angular_speed=1.00`、`max_wheel_speed=30.0`、
`publish_rate=20.0`；GUI 额外：`window_title`、`cmd_timeout`(0.5s 失焦/无按键自动停)。

## launch 契约

- `ros2 launch robot_control teleop_gui.launch.py`：robot_state_publisher（加载
  robot_description 的 `urdf/omni_robot.urdf`）+ `sim_node` + `gui_teleop` + `rviz2`。
- `ros2 launch robot_control teleop_keyboard.launch.py`：同上，但用终端 `teleop_keyboard`，默认不开 GUI。
- 两个 launch 都必须支持参数：`rviz:=true/false`（默认 true）、`use_sim_time:=false`。
- **无显示 / CI 验证**：`ros2 launch robot_control teleop_gui.launch.py rviz:=false gui:=false`
  必须能正常起 robot_state_publisher + sim_node（GUI 节点在无 DISPLAY 时报错退出不算失败，
  所以验证时用 `gui:=false`）。
- launch 必须能在 colcon 安装后运行（`get_package_share_directory`），也要能从源码目录直接运行
  （参考 `robot_description/launch/view_robot.launch.py` 的做法：把 `package://` 临时重写为
  `file://` URL）。URDF 通过 `robot_description` 包获取，找不到 share 时回退到
  `../../robot_description`（即 `src/robot/robot_description`）。

## 验证命令（Lead 会跑）

```bash
cd /home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select robot_control --symlink-install
source install/setup.bash
python3 -m pytest src/robot_control/test -q
ros2 launch robot_control teleop_keyboard.launch.py rviz:=false   # 另一个终端发指令
ros2 topic pub -r 20 /wheel_cmd std_msgs/msg/Float64MultiArray "{data: [5.0,5.0,5.0,5.0]}"
ros2 topic echo --once /odom
ros2 run tf2_ros tf2_echo odom base_footprint
```

单测/调试代码时直接 `cd src/robot_control && python3 -m robot_control.mecanum` 不需要安装；
GUI 调试用 `DISPLAY=:1 python3 -m robot_control.gui_teleop`（本机有 X11 :1）。

## 共同要求

- 代码注释/文档用中文（界面文案中文），变量名英文；Python 3.10。
- 节点启动日志打印一次键位表和关键参数；异常要有清晰报错。
- GUI 必须能在没有 `rclpy` 回调线程竞争的情况下安全退出（Ctrl-C / 关窗口时发布零速）。
- 不要修改 `mecanum.py` 的公开 API；如确实不够用，发消息给 Lead，不要直接改。

---

## 追加需求：专注模式（K 键切换，全局键盘控制）

用户要求：现在必须让 GUI 窗口或终端持有键盘焦点才能遥控；新增「专注模式」，
按 `k` 切换。进入后无论焦点在哪个窗口（其它应用、桌面、别的终端），WASD/方向键
都能控制机器人；再按 `k` 退出。实现基于 X11 主动键盘抓取。

### 已由 Lead 完成：`robot_control/focus_grab.py`

```python
from robot_control.focus_grab import X11KeyboardGrab, TOGGLE_KEY, is_toggle_key

grab = X11KeyboardGrab(on_key, logger=print)   # on_key(name, pressed, ctrl) 在后台线程回调
ok, msg = grab.start()      # (bool, 中文说明)：成功即在 X11 全局抓取键盘
grab.active                 # 是否处于专注模式
grab.stop()                 # 退出并释放键盘（可重复调用）
X11KeyboardGrab.availability() -> (bool, str)   # 环境检查（纯 Wayland/无 DISPLAY 不可用）
```

* `on_key` 回调在**后台线程**执行，必须把事件投递回主线程（GUI 用 `queue` +
  `root.after` 轮询；终端节点用 `queue` + 主循环消费），禁止在回调里直接碰
  Tk 控件。
* 回调名与 `mecanum.KEY_ALIASES` 兼容：`w/a/s/d/q/e`、`" "`、`Up/Down/Left/Right`、
  `Escape`；`ctrl=True` 表示按住了 Ctrl（终端节点用它实现 Ctrl-C 退出）。
* 抓取期间键盘被独占（其它程序收不到键盘事件），这是专注模式的本意；`k`
  退出键必须始终可用。抓取失败（AlreadyGrabbed/NotViewable/无 DISPLAY）时返回
  失败原因，界面/终端要显示清楚。
* 仅支持 X11（Xorg/XWayland 的 X11 窗口）；纯 Wayland 下全局抓取不完整，README
  要写明限制。

### GUI（`gui_teleop.py`，B 负责）

1. 新增 `FocusModeController`（放在 `gui_teleop.py` 里，与 `TeleopPanel` 解耦、可
   注入假 grab 供测试）：持有 `X11KeyboardGrab`，维护队列；用 `root.after(30)` 轮询
   队列在主线程 dispatch；`toggle()`/`enable()`/`disable()`；enable 失败时通过面板
   显示中文原因并保持关闭；disable/关闭窗口时必须 `grab.stop()` 并 `panel.stop_motion()`。
2. `TeleopPanel` 增加：
   - 构造参数 `on_toggle_focus: Optional[Callable[[], None]] = None`；
   - `_on_key_press_event` 中 `keysym.lower() == 'k'` 时调用 `on_toggle_focus()` 并 return
     （不再当运动键）；
   - `set_focus_mode(enabled: bool, message: str = "")` 更新界面状态；暴露只读属性
     `focus_mode`（bool）供测试；
   - 顶部右侧增加「专注模式：关（按 K 开启）/ 开（全局键盘，按 K 退出）」状态徽标，
     开启时用醒目颜色；并在键位说明里加一行 `K  专注模式（全局键盘）`。
3. 主流程 `main()` 组装 controller；`panel.close()` 路径要保证退出专注模式（可通过
   panel 的 `on_close_callback` 或 finally 里 controller.disable()）。
4. `test/test_gui.py` 增加用例（假 grab，记录 start/stop；无 X11 也应能跑）：
   - `k` 按下 → controller.enable 被调用、面板 focus_mode=True、徽标文案包含“开”；
   - 再按 `k` → disable、focus_mode=False、面板收到零速；
   - 全局回调投递：模拟队列里 `('w', True, False)` → 轮询后 sink 收到前进指令；
     `('w', False, False)` → 零速；`('k', True, False)` → 切换（而不是运动）；
   - enable 失败（假 grab 返回 (False, "无 DISPLAY")）→ focus_mode 仍 False 且状态文案含原因；
   - 关闭窗口/`close()` 时 grab.stop() 被调用。
5. README：新增「专注模式（K）」小节（进入/退出、界面徽标、安全提示“键盘独占”、
   X11 限制、无 DISPLAY 时不可用、抓取失败排查），键位表加 K 行。

### 终端遥控（`teleop_keyboard.py`，A 负责）

1. 集成 `X11KeyboardGrab`：`k`（tty 输入或全局抓取）切换专注模式；进入后全局按键
   直接走现有动作处理（复用 `KeyParser`/`mecanum.key_action`/`keys_to_body` 与 hold 逻辑），
   `k` 再按退出；全局回调用队列，main 循环消费（注意线程安全）。
2. 状态行加 `[专注模式 开/关]`；启动帮助里加 `k`；无 DISPLAY / 抓取失败时按 `k`
   打印中文原因且不崩溃。
3. 专注模式中 Ctrl-C → 优雅退出（恢复 termios、发布零速、`grab.stop()`）。
4. 新增 `test/test_teleop_keyboard.py`（纯 Python，可用假 grab/不依赖 X11）：覆盖
   `k` 切换、全局按键驱动 motion 状态、Ctrl-C 退出标志、hold/stale 逻辑不回归。
5. 不改 GUI 文件、不动 `focus_grab.py`。

### 验收（Lead）

* 目标工作区安装后：GUI 进入专注模式、把焦点切到另一个窗口后按 W → `/wheel_cmd` 仍
  输出；按 K 退出后按 W 不再输出。
* 终端模式同样验证（pty 输入 k 进入，XTest 全局注入 w）。
* 全量 `pytest test -q` 通过；README 更新；重新部署到 Zhirong Cup 并 rebuild。

---

## 追加需求 2：专注模式默认开启

用户要求：程序启动后**默认就进入专注模式**，不用先点 GUI 窗口/终端再按 K。
`K` 仍用于退出/重新进入；同时保留关闭默认开启的开关，便于排查和特殊场景。

### GUI（`gui_teleop.py` + `launch/teleop_gui.launch.py`，B 负责）

1. `GuiTeleopNode` 新增 ROS 参数 `focus_mode_default`（bool，默认 **true**），启动日志打印。
2. `main()` 在 `panel.start()` 之后，用 `root.after(250, ...)` 调
   `FocusModeController.enable()`（可加 `auto_enable()` 薄封装：失败只写徽标/日志，
   不抛异常）。默认开启时启动日志应明确提示“默认进入专注模式”，失败（无 DISPLAY /
   AlreadyGrabbed）时徽标显示中文原因且程序正常运行。
3. 禁止在用户按 K 退出后自动重新进入（只在启动时触发一次）；关闭窗口/退出照旧释放抓取。
4. `launch/teleop_gui.launch.py` 增加 launch 参数 `focus_mode`（默认 `true`），映射到
   `gui_teleop` 节点的 `focus_mode_default`（用 `ParameterValue(..., value_type=bool)`）。
5. `test/test_gui.py` 增加用例（假 grab）：默认开启路径调用 grab.start、徽标=开；
   fake grab 失败时徽标=关且含原因；`focus_mode_default=false` 时不自动 enable；
   K 退出后不会自动重新 enable（手动调用 auto_enable 幂等/逻辑可测）。
6. README：专注模式小节补充“默认开启、K 退出、`focus_mode:=false` / `-p focus_mode_default:=false`
   关闭默认开启”，安全提示同步。

### 终端遥控（`teleop_keyboard.py` + `launch/teleop_keyboard.launch.py`，A 负责）

1. `TeleopKeyboard` 新增参数 `focus_mode_default`（bool，默认 **true**）：节点就绪后
   自动尝试进入专注模式（打印中文结果）；无 DISPLAY/抓取失败只打印原因，继续普通终端遥控。
2. `K` 仍可退出/重新进入；专注模式中 Ctrl-C/退出流程不变；状态行正确显示开/关。
3. `launch/teleop_keyboard.launch.py` 增加 launch 参数 `focus_mode`（默认 `true`）映射到
   `focus_mode_default`。
4. `test/test_teleop_keyboard.py` 增加用例：默认 true 时启动即调用 grab.start；false 不调用；
   启动抓取失败路径不崩溃且状态为关；K 退出后不会自动重新进入。

### 验收（Lead）

* `ros2 launch robot_control teleop_gui.launch.py rviz:=false` 启动后**不点窗口**，
  直接把焦点放到另一个窗口，按 W → `/wheel_cmd` 仍输出；按 K 退出后按 W 不再输出。
* `ros2 run robot_control teleop_keyboard`（pty）启动后自动 `[专注模式 开]`，不聚焦终端
  也能全局遥控；K 可退出；`focus_mode_default:=false` 时不自动进入。
* 全量 pytest 通过，重新部署到 Zhirong Cup 并 rebuild + 目标安装验证。

---

## 追加需求 3：Gazebo Classic 11 仿真接入（robot-integrator）

在保持原有 `sim_node` 运动学仿真链路不变的前提下，新增 **Gazebo 模式**
（`ros2 launch robot_control gazebo.launch.py`）。两种模式互斥，不要同时启动。

### 模式切换（谁发布什么）

| 话题 / TF | `sim_node` 模式（原有 launch） | Gazebo 模式（`gazebo.launch.py`） |
| --- | --- | --- |
| 底盘运动来源 | `sim_node` 积分 `/wheel_cmd` | `libgazebo_ros_planar_move.so` 直接消费 `/cmd_vel` |
| `/joint_states` | `sim_node`（节点名 `mecanum_sim`） | `libgazebo_ros_joint_state_publisher.so`（4 个轮关节） |
| `/odom` | `sim_node` | `libgazebo_ros_planar_move.so`（`frame_id=odom`, `child_frame_id=base_footprint`） |
| TF `odom→base_footprint` | `sim_node` | `libgazebo_ros_planar_move.so`（`publish_odom_tf=true`） |
| `/clock` | 无 | gzserver（`libgazebo_ros_init.so`），`use_sim_time=true` |
| `/wheel_cmd` | 底盘控制输入 | **不参与**（`planar_move` 不消费 `/wheel_cmd`；teleop/GUI 仍会发布它，但 Gazebo 忽略） |

因此 Gazebo 模式下：`robot_state_publisher` 照旧加载 URDF 并发布
`base_footprint→base_link→轮子/雷达/相机` 的 TF，只是轮关节角度来自 Gazebo 插件；
**`sim_node` 绝对不能启动**（否则 `/joint_states`、`/odom`、`odom→base_footprint` 全部重复）。

### URDF 新增的 Gazebo 标签（`robot_description/urdf/omni_robot.urdf`）

* `<gazebo reference="<link>">`：Gazebo 材质（`Gazebo/Grey`、`FlatBlack` 等）、
  `self_collide=false`；四个轮子 `<mu1>/<mu2> = 0.1`；
* robot 级 `<gazebo><plugin>`（ModelPlugin）：
  * `libgazebo_ros_planar_move.so`：
    `update_rate=50`、`publish_rate=50`、`publish_odom=true`、`publish_odom_tf=true`、
    `odometry_frame=odom`、`robot_base_frame=base_footprint`、`covariance_x/y/yaw`；
    话题保持默认 `/cmd_vel` 与 `/odom`（没有 remapping）；
  * `libgazebo_ros_joint_state_publisher.so`：
    `update_rate=50` + 4 个 `joint_name`（= `mecanum.WHEEL_NAMES`：FL FR RL RR）；
* 原有 visual/collision/关节定义**未改动**，RViz 显示与
  `robot_state_publisher` 解析不受影响；
* `base_footprint` 是 URDF 根 link，**不加 `<inertial>`**：KDL 不支持根 link 惯性，
  Gazebo 端由固定关节 lumping 自动补质量（实测无警告、落地高度正确）。

### `gazebo_ros` 3.9 插件参数核实结论

* SystemPlugin（`libgazebo_ros_init.so`、`libgazebo_ros_factory.so`）**只能**
  通过 gzserver 命令行 `-s` 加载，写进 URDF/SDF 的 `<plugin>` 会报
  `incorrect plugin type`；`gazebo.launch.py` 已固定加载；
* `planar_move` 的 SDF 参数名：`update_rate`、`publish_rate`、`publish_odom`、
  `publish_odom_tf`、`odometry_frame`、`robot_base_frame`、
  `covariance_x|y|yaw`；话题 `cmd_vel`、`odom`；
* `joint_state_publisher` 的 SDF 参数名：`update_rate`、可重复的 `joint_name`；
  话题 `joint_states`；
* 依据：`$PREFIX/opt/ros/humble/lib/libgazebo_ros_planar_move.so` 字符串表、
  `share/gazebo_plugins/worlds/gazebo_ros_planar_move_demo.world` 与
  `gazebo_ros_joint_state_publisher_demo.world`。

### launch 契约（`gazebo.launch.py`）

* 参数（全部 `DeclareLaunchArgument`，`ros2 launch ... --show-args` 可见）：
  `world`（默认空=自动解析 `zhirong_maps`，回退自带 `worlds/test/gazebo_test.world`）、
  `x=2.9`、`y=1.6`、`z=0.05`、`yaw=π`、`use_sim_time=true`、`gui=false`、
  `rviz=false`、`teleop=none|keyboard|gui`、`verbose=false`、
  `model_name=zhirong_robot`、`pause=false`；
* 启动内容：`gzserver -s libgazebo_ros_init.so -s libgazebo_ros_factory.so <world>` +
  `spawn_entity.py -topic robot_description` + `robot_state_publisher` +
  可选 teleop/gzclient/RViz2；
* 源码目录直跑与 colcon 安装后运行都支持（URDF 的 `package://` 由 `spawn_entity.py`
  的 `-package_to_model` 转 `model://`，配合包内 `models/robot_description/` 解析；
  world 从源码树 `<ws>/src/maps/zhirong_maps/` 或 ament share 解析）；
* 自动把 `zhirong_maps/models` 前插到 `GAZEBO_MODEL_PATH`（比赛 world 用
  `model://` 引用自建模型）；
* 对 gzserver 内部 `unset DISPLAY`（本机 GLX 损坏时 headless 可跑），gzclient 仍用真实 DISPLAY。

### 验证命令（headless）

```bash
source tools/gazebo_env.sh
unset DISPLAY
export GAZEBO_MASTER_URI=http://127.0.0.1:11392      # 多人共用机器时换端口
ros2 launch robot_control gazebo.launch.py gui:=false rviz:=false teleop:=none

# 另开终端：
ros2 topic list | grep -E 'clock|joint_states|odom'
ros2 topic echo --once /odom
ros2 run tf2_ros tf2_echo odom base_footprint
ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}"
gz model -m zhirong_robot -p
```

### 已知限制

* `planar_move` 是速度级车体运动，**不含轮子物理滚动/电机/麦轮滚子模型**，
  不能用来验证轮速闭环与打滑；
* `/cmd_vel` 无超时停车：遥控源退出后机器人保持最后速度，联调结束必须发零速；
* 相机/雷达未接 Gazebo 传感器插件；`gzclient` 需要可用 OpenGL。

完整验证记录见 `competition_ws/GAZEBO_INTEGRATION.md`。
