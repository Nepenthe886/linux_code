#!/usr/bin/env python3
"""Gazebo 启动验收：/cmd_vel -> 底盘运动闭环检查。

检查项：
  1. /clock 推进（仿真时间在走）；/joint_states 含 4 个轮关节；/odom 有数据；
  2. TF odom -> base_footprint 存在；
  3. 依次发 forward / strafe_left / rotate_left 指令，按 /odom 位姿变化判定
     前进、横移、自转是否生效（planar_move 插件支持全向运动）。

用法:
    ros2 run <包> 或直接 python3 check_gazebo_drive.py
退出码: 0 = 全部通过, 1 = 失败。
"""
import math
import sys
import time

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import JointState
from tf2_ros import Buffer, TransformListener

WHEEL_JOINTS = [
    "wheel_front_left_joint",
    "wheel_front_right_joint",
    "wheel_rear_left_joint",
    "wheel_rear_right_joint",
]


def yaw_of(q):
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))


class DriveCheck(Node):
    def __init__(self):
        super().__init__("gazebo_drive_check", parameter_overrides=[])
        self.set_parameters([rclpy.parameter.Parameter("use_sim_time", value=True)])
        qos = QoSProfile(depth=20, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.odom = None
        self.joints = None
        self.clock = None
        self.create_subscription(Odometry, "/odom", self._odom, 20)
        self.create_subscription(JointState, "/joint_states", self._joints, qos)
        # gzserver(libgazebo_ros_init) 的 /clock 是 BEST_EFFORT，必须用 BEST_EFFORT 订阅
        clock_qos = QoSProfile(depth=20, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.create_subscription(Clock, "/clock", self._on_clock, clock_qos)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def _odom(self, m):
        self.odom = m

    def _joints(self, m):
        self.joints = m

    def _on_clock(self, m):
        # 注意：不能用 _clock 作方法名，rclpy 的 use_sim_time 会用 ROSClock 覆盖它
        self.clock = m.clock

    def spin_for_sim(self, seconds, timeout=30.0):
        """按仿真时间等待 seconds 秒（期间持续处理回调）。"""
        start = self.clock.sec + self.clock.nanosec * 1e-9 if self.clock else None
        t0 = time.time()
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.02)
            if self.clock is None:
                if time.time() - t0 > timeout:
                    return False
                continue
            now = self.clock.sec + self.clock.nanosec * 1e-9
            if start is None:
                start = now
            if now - start >= seconds:
                return True
            if time.time() - t0 > timeout:
                return False
        return False

    def drive(self, lin_x=0.0, lin_y=0.0, ang_z=0.0, seconds=1.5):
        msg = Twist()
        msg.linear.x = lin_x
        msg.linear.y = lin_y
        msg.angular.z = ang_z
        end = None
        t0 = time.time()
        while rclpy.ok():
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.02)
            if end is None and self.clock is not None:
                end = self.clock.sec + self.clock.nanosec * 1e-9 + seconds
            if end is not None and self.clock is not None:
                now = self.clock.sec + self.clock.nanosec * 1e-9
                if now >= end:
                    break
            if time.time() - t0 > 30:
                break
        # 停车
        stop = Twist()
        for _ in range(10):
            self.pub.publish(stop)
            rclpy.spin_once(self, timeout_sec=0.02)
        return self.pose()

    def pose(self):
        if self.odom is None:
            return None
        p = self.odom.pose.pose
        return (p.position.x, p.position.y, p.position.z, yaw_of(p.orientation))


def main():
    rclpy.init()
    node = DriveCheck()
    failures = []
    print("[1/5] 等待 /clock ...")
    t0 = time.time()
    while rclpy.ok() and node.clock is None and time.time() - t0 < 30:
        rclpy.spin_once(node, timeout_sec=0.1)
    if node.clock is None:
        print("FAIL: 30s 内没有收到 /clock")
        return 1
    print(f"      OK /clock = {node.clock.sec}.{node.clock.nanosec:09d}")
    print("[2/5] 等待 /odom /joint_states ...")
    t0 = time.time()
    while rclpy.ok() and (node.odom is None or node.joints is None) and time.time() - t0 < 30:
        rclpy.spin_once(node, timeout_sec=0.1)
    if node.odom is None:
        failures.append("没有 /odom")
        print("      FAIL 无 /odom")
    else:
        print(f"      OK /odom frame_id={node.odom.header.frame_id} child={node.odom.child_frame_id}")
    if node.joints is None:
        failures.append("没有 /joint_states")
        print("      FAIL 无 /joint_states")
    else:
        missing = [j for j in WHEEL_JOINTS if j not in node.joints.name]
        print(f"      OK /joint_states joints={list(node.joints.name)}")
        if missing:
            failures.append(f"/joint_states 缺关节 {missing}")
    print("[3/5] 检查 TF odom->base_footprint ...")
    have_tf = False
    t0 = time.time()
    while time.time() - t0 < 10:
        rclpy.spin_once(node, timeout_sec=0.1)
        try:
            if node.tf_buffer.can_transform("odom", "base_footprint", rclpy.time.Time()):
                have_tf = True
                break
        except Exception:
            pass
    if have_tf:
        print("      OK TF odom->base_footprint")
    else:
        failures.append("缺少 TF odom->base_footprint")
        print("      FAIL 缺少 TF")

    print("[4/5] 运动测试 ...")
    node.spin_for_sim(1.0)
    p0 = node.pose()
    if p0 is None:
        print("FAIL: 无 odom，无法运动测试")
        return 1
    print(f"      起点 odom: x={p0[0]:.3f} y={p0[1]:.3f} yaw={p0[3]:.3f}")
    p1 = node.drive(lin_x=0.3, seconds=2.0)
    d_forward = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    print(f"      前进 2s 后: 位移={d_forward:.3f} m  -> {'OK' if d_forward > 0.20 else 'FAIL'}")
    if d_forward <= 0.20:
        failures.append(f"前进位移过小 {d_forward:.3f} m")
    p2 = node.drive(lin_y=0.3, seconds=2.0)
    d_strafe = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    print(f"      横移 2s 后: 位移={d_strafe:.3f} m  -> {'OK' if d_strafe > 0.20 else 'FAIL'}")
    if d_strafe <= 0.20:
        failures.append(f"横移位移过小 {d_strafe:.3f} m")
    p3 = node.drive(ang_z=0.8, seconds=1.5)
    d_yaw = abs(p3[3] - p2[3])
    if d_yaw > math.pi:
        d_yaw = 2 * math.pi - d_yaw
    print(f"      自转 1.5s 后: yaw 变化={d_yaw:.3f} rad -> {'OK' if d_yaw > 0.30 else 'FAIL'}")
    if d_yaw <= 0.30:
        failures.append(f"自转 yaw 变化过小 {d_yaw:.3f} rad")
    p4 = node.drive(seconds=1.0)
    print(f"[5/5] 终点位姿: x={p4[0]:.3f} y={p4[1]:.3f} yaw={p4[3]:.3f}")

    node.destroy_node()
    rclpy.shutdown()
    if failures:
        print("\n=== RESULT: FAIL ===")
        for f in failures:
            print(" -", f)
        return 1
    print("\n=== RESULT: PASS（仿真启动 + 全向运动控制闭环全部通过）===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
