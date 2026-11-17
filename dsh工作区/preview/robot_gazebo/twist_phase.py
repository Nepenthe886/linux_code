#!/usr/bin/env python3
"""验证用：定时发布一段 /cmd_vel，然后发布零速并退出（避免 ros2 CLI 启动延迟干扰计时）。

用法：python3 twist_phase.py VX VY WZ DURATION
"""
import sys
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


def main() -> int:
    vx = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    vy = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    wz = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    duration = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0

    rclpy.init()
    node = Node("twist_phase_probe")
    publisher = node.create_publisher(Twist, "/cmd_vel", 10)
    command = Twist()
    command.linear.x = vx
    command.linear.y = vy
    command.angular.z = wz
    zero = Twist()

    end = time.monotonic() + duration
    while time.monotonic() < end and rclpy.ok():
        publisher.publish(command)
        time.sleep(0.05)
    # 停车：连续发 0.6 s 零速，确保插件一定收到
    end = time.monotonic() + 0.6
    while time.monotonic() < end and rclpy.ok():
        publisher.publish(zero)
        time.sleep(0.05)
    node.get_logger().info(
        "phase done: vx=%.2f vy=%.2f wz=%.2f duration=%.1fs" % (vx, vy, wz, duration)
    )
    node.destroy_node()
    rclpy.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
