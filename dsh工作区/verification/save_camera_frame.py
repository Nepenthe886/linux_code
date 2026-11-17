#!/usr/bin/env python3
"""订阅 Gazebo 相机 sensor_msgs/Image，保存一帧为 PNG。

用法: save_camera_frame.py <image_topic> <out.png> [等待超时秒]
依赖: rclpy / sensor_msgs / cv2（或 numpy+PIL 回退）
"""
import sys
import time

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class Saver(Node):
    def __init__(self, topic, out, timeout):
        super().__init__("save_camera_frame")
        self.out = out
        self.timeout = timeout
        self.frame = None
        self.create_subscription(Image, topic, self.cb, qos_profile_sensor_data)

    def cb(self, msg):
        if self.frame is not None:
            return
        enc = msg.encoding
        h, w = msg.height, msg.width
        buf = np.frombuffer(msg.data, dtype=np.uint8)
        if enc in ("rgb8", "bgr8"):
            arr = buf.reshape(h, w, 3)
            if enc == "bgr8":
                arr = arr[:, :, ::-1]
        elif enc in ("rgba8", "bgra8"):
            arr = buf.reshape(h, w, 4)[:, :, :3]
        elif enc in ("mono8", "8UC1"):
            arr = buf.reshape(h, w)
        else:
            raise RuntimeError(f"unsupported encoding: {enc}")
        self.frame = arr
        try:
            import cv2

            cv2.imwrite(self.out, cv2.cvtColor(arr, cv2.COLOR_RGB2BGR))
        except Exception:
            from PIL import Image as PILImage

            PILImage.fromarray(arr).save(self.out)
        print(f"saved {self.out} {w}x{h} encoding={enc}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    topic, out = sys.argv[1], sys.argv[2]
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0
    rclpy.init()
    node = Saver(topic, out, timeout)
    t0 = time.time()
    while rclpy.ok() and node.frame is None and time.time() - t0 < timeout:
        rclpy.spin_once(node, timeout_sec=0.2)
    ok = node.frame is not None
    node.destroy_node()
    rclpy.shutdown()
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
