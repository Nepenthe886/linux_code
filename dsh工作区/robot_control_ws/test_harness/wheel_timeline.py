#!/usr/bin/env python3
"""Print /wheel_cmd timestamps for a few seconds: wheel_timeline.py <seconds>"""
import sys
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class Probe(Node):
    def __init__(self):
        super().__init__("wheel_timeline")
        self.rows = []
        self.t0 = time.monotonic()
        self.create_subscription(Float64MultiArray, "/wheel_cmd", self._cb, 10)

    def _cb(self, msg):
        self.rows.append((time.monotonic() - self.t0, list(msg.data)))


def main():
    seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
    rclpy.init()
    node = Probe()
    end = time.time() + seconds
    while time.time() < end:
        rclpy.spin_once(node, timeout_sec=0.02)
    # collapse identical consecutive rows, keep every change
    prev = None
    for t, data in node.rows:
        if data != prev:
            print(f"t={t:5.2f}s  {['%+.2f' % v for v in data]}")
            prev = data
    print(f"total msgs={len(node.rows)}")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
