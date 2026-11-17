"""模拟四麦克纳姆轮底盘节点（节点名 ``mecanum_sim``）。

职责（与 ``robot_control_ws/INTERFACE.md`` 对齐）：

* 订阅 ``/wheel_cmd``（``std_msgs/Float64MultiArray``，顺序 FL FR RL RR，
  单位 rad/s），做加速度限幅后积分；
* 发布 ``/joint_states``：四个 ``wheel_*_joint`` 的位置（rad）与速度（rad/s），
  供 ``robot_state_publisher`` 生成轮子 TF 与 RViz 显示；
* 用正运动学得到车体速度，对里程计进行世界系积分，发布 ``/odom``
  （``frame_id=odom``，``child_frame_id=base_footprint``）；
* 用 ``tf2_ros.TransformBroadcaster`` 广播 ``odom -> base_footprint``
  （参数 ``publish_odom_tf`` 可关闭）；
* 超过 ``cmd_timeout`` 未收到新指令时，按 ``command_accel_limit`` 平滑斜坡
  回零（不会硬跳变），超时后继续输出零速关节/里程计。

本节点不依赖 ``robot_state_publisher``，可单独运行联调：

.. code-block:: bash

    python3 -m robot_control.sim_node
    # 另一个终端（20 Hz 持续发四轮 5 rad/s -> 前进）
    ros2 topic pub -r 20 /wheel_cmd std_msgs/msg/Float64MultiArray \
        "{data: [5.0, 5.0, 5.0, 5.0]}"
    ros2 topic echo --once /odom
    ros2 run tf2_ros tf2_echo odom base_footprint
"""

from __future__ import annotations

import math
import signal
import time

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from tf2_ros import TransformBroadcaster

from robot_control.mecanum import WHEEL_JOINTS, MecanumKinematics

#: 零轮速常量（四轮）。
ZERO_WHEELS = (0.0, 0.0, 0.0, 0.0)

#: 单周期积分时间上限 [s]：定时器偶发卡顿（例如系统负载高）时避免里程计跳变。
_MAX_INTEGRATION_DT = 0.25


def wrap_to_pi(angle: float) -> float:
    """把角度归一到 ``[-pi, pi]``。"""
    return math.atan2(math.sin(angle), math.cos(angle))


def diagonal_covariance(diagonal: tuple[float, ...]) -> list[float]:
    """把 6 个方差值展开成 36 元素的 6x6 对角协方差数组。"""
    covariance = [0.0] * 36
    for index, variance in enumerate(diagonal):
        covariance[index * 6 + index] = float(variance)
    return covariance


class MecanumSim(Node):
    """模拟麦轮底盘：轮速指令 -> 关节状态 / 里程计 / TF。"""

    def __init__(self) -> None:
        super().__init__("mecanum_sim")

        # ---------------- 参数（默认值见 INTERFACE.md） ----------------
        self.wheel_radius = float(self.declare_parameter("wheel_radius", 0.065).value)
        self.wheel_base_x = float(self.declare_parameter("wheel_base_x", 0.170).value)
        self.wheel_base_y = float(self.declare_parameter("wheel_base_y", 0.170).value)
        self.max_wheel_speed = float(
            self.declare_parameter("max_wheel_speed", 30.0).value
        )
        self.publish_rate = float(self.declare_parameter("publish_rate", 50.0).value)
        self.cmd_timeout = float(self.declare_parameter("cmd_timeout", 0.5).value)
        self.command_accel_limit = float(
            self.declare_parameter("command_accel_limit", 60.0).value
        )
        self.odom_frame = str(self.declare_parameter("odom_frame", "odom").value)
        self.base_frame = str(self.declare_parameter("base_frame", "base_footprint").value)
        self.wheel_cmd_topic = str(
            self.declare_parameter("wheel_cmd_topic", "/wheel_cmd").value
        )
        self.joint_states_topic = str(
            self.declare_parameter("joint_states_topic", "/joint_states").value
        )
        self.odom_topic = str(self.declare_parameter("odom_topic", "/odom").value)
        self.publish_odom_tf = bool(
            self.declare_parameter("publish_odom_tf", True).value
        )

        # ---------------- 参数校验（错误信息要清晰） ----------------
        if self.publish_rate <= 0.0:
            raise ValueError("publish_rate 必须为正数（Hz）")
        if self.cmd_timeout < 0.0:
            raise ValueError("cmd_timeout 不能为负数（s）")
        if self.command_accel_limit < 0.0:
            raise ValueError("command_accel_limit 不能为负数（rad/s^2，0 表示不限幅）")
        if self.max_wheel_speed <= 0.0:
            raise ValueError("max_wheel_speed 必须为正数（rad/s）")

        # 运动学模型（与 URDF 完全一致的几何参数，见 mecanum.py）。
        self.kinematics = MecanumKinematics(
            wheel_radius=self.wheel_radius,
            wheel_base_x=self.wheel_base_x,
            wheel_base_y=self.wheel_base_y,
            max_wheel_speed=self.max_wheel_speed,
        )

        # ---------------- 运行时状态 ----------------
        self._wheel_angles = [0.0, 0.0, 0.0, 0.0]
        self._wheel_velocities = [0.0, 0.0, 0.0, 0.0]  # 加速度限幅后的"真实"轮速
        self._target_wheels = ZERO_WHEELS
        self._last_cmd_time: float | None = None
        self._last_update_time = time.monotonic()
        self._x = 0.0
        self._y = 0.0
        self._theta = 0.0
        self._last_warn_time: dict[str, float] = {}

        # ---------------- ROS 接口 ----------------
        self._joint_pub = self.create_publisher(
            JointState, self.joint_states_topic, 10
        )
        self._odom_pub = self.create_publisher(Odometry, self.odom_topic, 10)
        self._wheel_sub = self.create_subscription(
            Float64MultiArray, self.wheel_cmd_topic, self._on_wheel_cmd, 10
        )

        self._tf_broadcaster: TransformBroadcaster | None = None
        if self.publish_odom_tf:
            self._tf_broadcaster = TransformBroadcaster(self)

        self._timer = self.create_timer(1.0 / self.publish_rate, self._on_timer)

        # ---------------- 启动日志：参数 + 轮序说明 ----------------
        self.get_logger().info(
            "mecanum_sim 启动: "
            f"r={self.wheel_radius} m, bx={self.wheel_base_x} m, "
            f"by={self.wheel_base_y} m, max_wheel_speed={self.max_wheel_speed} rad/s, "
            f"publish_rate={self.publish_rate} Hz, cmd_timeout={self.cmd_timeout} s, "
            f"command_accel_limit={self.command_accel_limit} rad/s^2"
        )
        self.get_logger().info(
            "轮序固定 FL FR RL RR = " + ", ".join(WHEEL_JOINTS)
            + "（axis=+Y，正轮速 -> 向车头 +X 滚动）"
        )
        self.get_logger().info(
            f"订阅 {self.wheel_cmd_topic} [Float64MultiArray, rad/s] -> "
            f"发布 {self.joint_states_topic}, {self.odom_topic}"
            + (
                f", 广播 TF {self.odom_frame} -> {self.base_frame}"
                if self.publish_odom_tf
                else ", 不广播 TF（publish_odom_tf=false）"
            )
        )

    # ------------------------------------------------------------------ #
    # 订阅回调
    # ------------------------------------------------------------------ #
    def _on_wheel_cmd(self, msg: Float64MultiArray) -> None:
        """接收四轮角速度指令；非法数据告警后忽略（不刷新超时计时）。"""
        if len(msg.data) != 4:
            self._warn_throttled(
                f"{self.wheel_cmd_topic} 数据长度非法: {len(msg.data)}（应为 4，"
                "顺序 FL FR RL RR），已忽略"
            )
            return
        values = tuple(float(value) for value in msg.data)
        if not all(math.isfinite(value) for value in values):
            self._warn_throttled(
                f"{self.wheel_cmd_topic} 含 NaN/Inf 数据 {values}，已忽略"
            )
            return

        # 轮速上限：按比例整体缩放，保持运动方向不变。
        limited = self.kinematics.clamp_wheels(values)
        if any(abs(a - b) > 1e-9 for a, b in zip(limited, values)):
            self._warn_throttled(
                f"轮速指令 {values} 超过上限 ±{self.max_wheel_speed} rad/s，"
                f"已按比例限幅为 {limited}"
            )

        self._target_wheels = limited
        self._last_cmd_time = time.monotonic()

    # ------------------------------------------------------------------ #
    # 定时器：积分 + 发布
    # ------------------------------------------------------------------ #
    def _on_timer(self) -> None:
        now = time.monotonic()
        dt = now - self._last_update_time
        self._last_update_time = now
        dt = min(max(dt, 0.0), _MAX_INTEGRATION_DT)

        self._update_wheel_velocities(now, dt)
        self._integrate_wheel_angles(dt)
        body = self.kinematics.wheels_to_body(self._wheel_velocities)
        self._integrate_odometry(body, dt)

        stamp = self.get_clock().now().to_msg()
        self._publish_joint_states(stamp)
        self._publish_odometry(stamp, body)
        self._broadcast_tf(stamp)

    def _update_wheel_velocities(self, now: float, dt: float) -> None:
        """按加速度限幅把当前轮速斜坡逼近目标轮速（含超时回零）。"""
        if self._last_cmd_time is None or (
            now - self._last_cmd_time > self.cmd_timeout
        ):
            target = ZERO_WHEELS
        else:
            target = self._target_wheels

        if self.command_accel_limit <= 0.0:
            # 0 表示不限制加速度：直接跟踪目标。
            self._wheel_velocities = list(target)
            return

        max_step = self.command_accel_limit * dt
        self._wheel_velocities = [
            current + max(-max_step, min(max_step, goal - current))
            for current, goal in zip(self._wheel_velocities, target)
        ]

    def _integrate_wheel_angles(self, dt: float) -> None:
        for index, velocity in enumerate(self._wheel_velocities):
            self._wheel_angles[index] = wrap_to_pi(
                self._wheel_angles[index] + velocity * dt
            )

    def _integrate_odometry(self, body, dt: float) -> None:
        """世界系里程计积分：body 速度转到 odom 坐标系后累加。"""
        cos_theta = math.cos(self._theta)
        sin_theta = math.sin(self._theta)
        self._x += (body.vx * cos_theta - body.vy * sin_theta) * dt
        self._y += (body.vx * sin_theta + body.vy * cos_theta) * dt
        self._theta = wrap_to_pi(self._theta + body.wz * dt)

    # ------------------------------------------------------------------ #
    # 发布
    # ------------------------------------------------------------------ #
    def _publish_joint_states(self, stamp) -> None:
        msg = JointState()
        msg.header.stamp = stamp
        msg.name = list(WHEEL_JOINTS)
        msg.position = list(self._wheel_angles)
        msg.velocity = list(self._wheel_velocities)
        self._joint_pub.publish(msg)

    def _publish_odometry(self, stamp, body) -> None:
        msg = Odometry()
        msg.header.stamp = stamp
        msg.header.frame_id = self.odom_frame
        msg.child_frame_id = self.base_frame

        msg.pose.pose.position.x = self._x
        msg.pose.pose.position.y = self._y
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = math.sin(self._theta / 2.0)
        msg.pose.pose.orientation.w = math.cos(self._theta / 2.0)

        # twist 在 child_frame（base_footprint）下表达。
        msg.twist.twist.linear.x = body.vx
        msg.twist.twist.linear.y = body.vy
        msg.twist.twist.linear.z = 0.0
        msg.twist.twist.angular.x = 0.0
        msg.twist.twist.angular.y = 0.0
        msg.twist.twist.angular.z = body.wz

        # 模拟底盘：位姿方差给中等值，速度方差略小；z/roll/pitch 认为无误差。
        msg.pose.covariance = diagonal_covariance(
            (0.02, 0.02, 1e-6, 1e-6, 1e-6, 0.02)
        )
        msg.twist.covariance = diagonal_covariance(
            (0.01, 0.01, 1e-6, 1e-6, 1e-6, 0.01)
        )
        self._odom_pub.publish(msg)

    def _broadcast_tf(self, stamp) -> None:
        if self._tf_broadcaster is None:
            return
        transform = TransformStamped()
        transform.header.stamp = stamp
        transform.header.frame_id = self.odom_frame
        transform.child_frame_id = self.base_frame
        transform.transform.translation.x = self._x
        transform.transform.translation.y = self._y
        transform.transform.translation.z = 0.0
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = math.sin(self._theta / 2.0)
        transform.transform.rotation.w = math.cos(self._theta / 2.0)
        self._tf_broadcaster.sendTransform(transform)

    # ------------------------------------------------------------------ #
    # 工具 / 退出
    # ------------------------------------------------------------------ #
    def _warn_throttled(self, message: str, period: float = 1.0) -> None:
        """同一类告警最多每 ``period`` 秒打印一次，避免刷屏。"""
        now = time.monotonic()
        if now - self._last_warn_time.get(message, -math.inf) >= period:
            self._last_warn_time[message] = now
            self.get_logger().warn(message)

    def shutdown(self) -> None:
        """节点退出：停定时器、发一次零速关节状态、关闭 TF 广播。"""
        if getattr(self, "_timer", None) is not None:
            self._timer.cancel()
        try:
            stamp = self.get_clock().now().to_msg()
            self._wheel_velocities = [0.0, 0.0, 0.0, 0.0]
            msg = JointState()
            msg.header.stamp = stamp
            msg.name = list(WHEEL_JOINTS)
            msg.position = list(self._wheel_angles)
            msg.velocity = [0.0, 0.0, 0.0, 0.0]
            self._joint_pub.publish(msg)
            self.get_logger().info("mecanum_sim 退出：已发布零速 joint_states，关闭 TF 广播")
        except Exception:  # 节点已失效时退出流程不再抛异常
            pass
        self._tf_broadcaster = None


def main(args=None) -> None:
    rclpy.init(args=args)

    # 自行接管 SIGINT/SIGTERM：先让 tick 循环退出，再发布零速 joint_states、
    # 关闭 TF，最后才 rclpy.shutdown()（避免 rclpy 默认处理器提前 shutdown
    # 掉 context 导致退出时无法发布）。
    stop_requested = {"flag": False}

    def _request_stop(signum, frame) -> None:  # noqa: ARG001
        stop_requested["flag"] = True

    signal.signal(signal.SIGINT, _request_stop)
    signal.signal(signal.SIGTERM, _request_stop)

    node: MecanumSim | None = None
    try:
        node = MecanumSim()
        while rclpy.ok() and not stop_requested["flag"]:
            rclpy.spin_once(node, timeout_sec=0.1)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.shutdown()
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
