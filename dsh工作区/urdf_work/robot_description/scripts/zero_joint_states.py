#!/usr/bin/env python3
"""Fallback joint-state publisher used by display.launch.py.

The standard ``joint_state_publisher`` package is used when it is installed.
In a minimal ROS 2 installation it can be missing; this node keeps the four
wheel joints at 0 rad so that robot_state_publisher / RViz can build the TF
tree and display the complete robot.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

WHEEL_JOINTS = [
    "wheel_front_left_joint",
    "wheel_front_right_joint",
    "wheel_rear_left_joint",
    "wheel_rear_right_joint",
]


class ZeroJointStatePublisher(Node):
    def __init__(self) -> None:
        super().__init__("zero_joint_state_publisher")
        self._pub = self.create_publisher(JointState, "joint_states", 10)
        self._timer = self.create_timer(0.05, self._publish)
        self.get_logger().info(
            "joint_state_publisher not found, publishing zero wheel states"
        )

    def _publish(self) -> None:
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = WHEEL_JOINTS
        msg.position = [0.0] * len(WHEEL_JOINTS)
        self._pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = ZeroJointStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
