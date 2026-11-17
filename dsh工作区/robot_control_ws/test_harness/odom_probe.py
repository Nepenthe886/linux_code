#!/usr/bin/env python3
"""Print /odom and /wheel_cmd after a delay: odom_probe.py <seconds>"""
import sys
import time

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class Probe(Node):
    def __init__(self):
        super().__init__("odom_probe")
        self.odom = None
        self.wheels = None
        self.create_subscription(Odometry, "/odom", self._odom, 10)
        self.create_subscription(Float64MultiArray, "/wheel_cmd", self._wheel, 10)

    def _odom(self, msg):
        self.odom = msg

    def _wheel(self, msg):
        self.wheels = list(msg.data)


def main() -> int:
    seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
    rclpy.init()
    node = Probe()
    end = time.time() + seconds
    while time.time() < end:
        rclpy.spin_once(node, timeout_sec=0.05)
    if node.odom is None:
        print("NO ODOM")
        return 1
    p = node.odom.pose.pose.position
    q = node.odom.pose.pose.orientation
    tw = node.odom.twist.twist
    print(f"odom x={p.x:+.3f} y={p.y:+.3f} qz={q.z:+.3f} vx={tw.linear.x:+.3f} "
          f"vy={tw.linear.y:+.3f} wz={tw.angular.z:+.3f}")
    print(f"wheel_cmd={['%+.2f' % v for v in node.wheels] if node.wheels else None}")
    node.destroy_node()
    rclpy.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
