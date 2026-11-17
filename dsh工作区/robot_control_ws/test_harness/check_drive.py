#!/usr/bin/env python3
"""Headless integration check for the simulated mecanum drivetrain.

Publishes /wheel_cmd in three phases (forward, strafe-left, rotate-left),
records /odom, /joint_states and TF, and asserts the expected motion.
"""
import math
import sys
import time

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from tf2_ros import Buffer, TransformListener

WHEEL_NAMES = [
    "wheel_front_left_joint",
    "wheel_front_right_joint",
    "wheel_rear_left_joint",
    "wheel_rear_right_joint",
]

# wheel commands [FL, FR, RL, RR] rad/s for the three test phases
PHASES = [
    ("forward", [5.0, 5.0, 5.0, 5.0], 1.2),
    ("stop", [0.0, 0.0, 0.0, 0.0], 0.8),
    ("strafe_left", [-4.6, 4.6, 4.6, -4.6], 1.2),
    ("stop", [0.0, 0.0, 0.0, 0.0], 0.8),
    ("rotate_left", [-5.2, 5.2, -5.2, 5.2], 1.2),
    ("stop", [0.0, 0.0, 0.0, 0.0], 0.8),
]


class CheckNode(Node):
    def __init__(self):
        super().__init__("drive_check")
        self.pub = self.create_publisher(Float64MultiArray, "/wheel_cmd", 10)
        self.create_subscription(Odometry, "/odom", self._odom_cb, 10)
        self.create_subscription(JointState, "/joint_states", self._js_cb, 10)
        self.odom = None
        self.joint_states = None
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_timer(0.02, self._publish)

    def _odom_cb(self, msg):
        self.odom = msg

    def _js_cb(self, msg):
        self.joint_states = msg

    def _publish(self):
        zero = self.get_clock().now()
        msg = Float64MultiArray()
        msg.data = [float(v) for v in self._wheel]
        self.pub.publish(msg)

    _wheel = [0.0, 0.0, 0.0, 0.0]


def spin_for(node, seconds):
    end = time.time() + seconds
    while time.time() < end:
        rclpy.spin_once(node, timeout_sec=0.02)


def main():
    rclpy.init()
    node = CheckNode()
    failures = []

    def phase(name, wheels, duration):
        node._wheel = wheels
        t0 = time.time()
        spin_for(node, duration)
        if node.odom is None:
            failures.append(f"{name}: no /odom received")
            print(f"[{name}] no /odom")
            return None
        p = node.odom.pose.pose.position
        q = node.odom.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
        tw = node.odom.twist.twist
        print(f"[{name}] t={time.time()-t0:.2f}s odom x={p.x:+.3f} y={p.y:+.3f} "
              f"yaw={yaw:+.3f} twist vx={tw.linear.x:+.3f} vy={tw.linear.y:+.3f} wz={tw.angular.z:+.3f}")
        return (p.x, p.y, yaw)

    print("waiting for /odom and /joint_states ...")
    deadline = time.time() + 15.0
    while time.time() < deadline and (node.odom is None or node.joint_states is None):
        spin_for(node, 0.1)
    if node.odom is None:
        failures.append("no /odom within 15s")
    if node.joint_states is None:
        failures.append("no /joint_states within 15s")
    else:
        missing = [n for n in WHEEL_NAMES if n not in node.joint_states.name]
        if missing:
            failures.append(f"joint_states missing {missing}")
        else:
            print("joint_states:", ", ".join(
                f"{n}={node.joint_states.position[node.joint_states.name.index(n)]:+.2f}"
                for n in WHEEL_NAMES))

    start = phase("stop0", [0.0] * 4, 0.3)
    forward = phase("forward", PHASES[0][1], PHASES[0][2])
    phase(*PHASES[1])
    strafe = phase("strafe_left", PHASES[2][1], PHASES[2][2])
    phase(*PHASES[3])
    rotate = phase("rotate_left", PHASES[4][1], PHASES[4][2])
    phase(*PHASES[5])

    # TF odom -> base_footprint
    tf_ok = False
    deadline = time.time() + 5.0
    while time.time() < deadline:
        spin_for(node, 0.1)
        try:
            tf = node.tf_buffer.lookup_transform("odom", "base_footprint", rclpy.time.Time())
            tf_ok = True
            tr = tf.transform.translation
            print(f"TF odom->base_footprint: x={tr.x:+.3f} y={tr.y:+.3f}")
            break
        except Exception:
            pass
    if not tf_ok:
        failures.append("TF odom->base_footprint not available")

    if start and forward:
        if forward[0] - start[0] < 0.15:
            failures.append(f"forward: dx={forward[0]-start[0]:.3f} too small (expect ~0.55)")
    if forward and strafe:
        if strafe[1] - forward[1] < 0.08:
            failures.append(f"strafe_left: dy={strafe[1]-forward[1]:.3f} too small")
    if strafe and rotate:
        dyaw = rotate[2] - strafe[2]
        if dyaw < 0.25:
            failures.append(f"rotate_left: dyaw={dyaw:.3f} too small (expect ~0.9)")
    if node.odom is not None:
        if abs(node.odom.twist.twist.linear.x) > 0.05:
            failures.append("robot did not stop after cmd timeout")

    node.destroy_node()
    rclpy.shutdown()
    if failures:
        print("FAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print("ALL DRIVE CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
