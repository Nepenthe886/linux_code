#!/usr/bin/env python3
"""把 ``/livox/lidar`` 转发到别名话题 ``/livix/lidar``。

用途：需求文档里同时出现过 ``/livox/lidar`` 与 ``/livix/lidar`` 两种拼写。
合成数据源（mid360_sim）本身会同时发布两者；Gazebo 传感器模式（真实场景
射线）由本节点补一个别名，保证算法无论订阅哪个名字都能拿到数据。
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2


class LivixRelay(Node):
    def __init__(self) -> None:
        super().__init__("livix_relay")
        self.pub = self.create_publisher(PointCloud2, "/livix/lidar", 10)
        self.create_subscription(PointCloud2, "/livox/lidar", self._cb, 10)
        self.get_logger().info("别名转发：/livox/lidar -> /livix/lidar")

    def _cb(self, msg: PointCloud2) -> None:
        self.pub.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = LivixRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
