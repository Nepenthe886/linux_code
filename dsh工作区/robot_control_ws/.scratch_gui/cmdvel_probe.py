import time

import rclpy
from geometry_msgs.msg import Twist

rclpy.init()
node = rclpy.create_node('cmdvel_probe')
start = time.monotonic()


def callback(message):
    print(
        f"{time.monotonic() - start:.3f}  vx={message.linear.x:+.3f} "
        f"vy={message.linear.y:+.3f} wz={message.angular.z:+.3f}",
        flush=True,
    )


node.create_subscription(Twist, '/cmd_vel', callback, 10)
end = start + 6.0
while time.monotonic() < end:
    rclpy.spin_once(node, timeout_sec=0.02)
rclpy.shutdown()
