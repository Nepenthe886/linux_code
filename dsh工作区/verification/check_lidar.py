#!/usr/bin/env python3
"""检查激光雷达/IMU 数据源（bring_up 启动后运行）。

用法: python3 check_lidar.py [gazebo|python]
  gazebo = Gazebo ray 传感器真实场景点云 + 200 Hz IMU（默认）
  python = robot_state_publicer 合成点云/IMU

判定：话题有数据、frame 正确、帧率合理、点云结构/范围合理、时间戳来自 /clock。
退出码 0 = 全部通过。
"""

import os
import sys
import threading
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import Imu, PointCloud2

MODE = sys.argv[1] if len(sys.argv) > 1 else "gazebo"
EXPECT_FRAME = "livox_mid360_link"


def _stamp_s(stamp):
    return stamp.sec + stamp.nanosec * 1e-9


class Checker(Node):
    def __init__(self):
        super().__init__("lidar_check")
        self.lidar = []
        self.alias = 0
        self.imu = []
        self.clock_sim = None
        self.create_subscription(PointCloud2, "/livox/lidar", self._lidar_cb, 10)
        self.create_subscription(PointCloud2, "/livix/lidar", self._alias_cb, 10)
        self.create_subscription(Imu, "/livox/imu", self._imu_cb, 100)
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.create_subscription(Clock, "/clock", self._clock_cb, qos)

    def _lidar_cb(self, msg):
        # 保留全部用于取“最新一帧”（限制长度避免长时间运行涨内存）
        self.lidar.append((msg, time.time()))
        if len(self.lidar) > 300:
            del self.lidar[:-200]

    def _alias_cb(self, msg):
        self.alias += 1

    def _imu_cb(self, msg):
        self.imu.append((msg, time.time()))
        if len(self.imu) > 2000:
            del self.imu[:-1000]

    def _clock_cb(self, msg):
        self.clock_sim = _stamp_s(msg.clock)


def rate(walls):
    return (len(walls) - 1) / (walls[-1] - walls[0]) if len(walls) > 1 else 0.0


def pointcloud_bounds(msg):
    import struct
    step = msg.point_step
    n = msg.width * msg.height
    data = msg.data
    xs, ys, zs = [], [], []
    for i in range(0, min(n, 4000)):
        off = i * step
        x, y, z = struct.unpack_from("<fff", data, off)
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


def main():
    rclpy.init()
    node = Checker()
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    threading.Thread(target=executor.spin, daemon=True).start()
    deadline = time.time() + 10.0
    while time.time() < deadline:
        if node.lidar and len(node.imu) > 50 and node.clock_sim is not None:
            break
        time.sleep(0.1)
    time.sleep(5.0)

    ok = True
    print(f"模式={MODE}")
    if len(node.lidar) < 3:
        print("LIDAR 没有收到点云（/livox/lidar）")
        ok = False
    else:
        msg = node.lidar[-1][0]
        r = rate([w for _, w in node.lidar])
        print(f"LIDAR frame={msg.header.frame_id} width={msg.width} point_step={msg.point_step} rate={r:.1f}")
        if msg.header.frame_id != EXPECT_FRAME:
            print(f"  frame_id={msg.header.frame_id}（期望 {EXPECT_FRAME}）"); ok = False
        if not (7.0 <= r <= 13.0):
            print(f"  点云频率异常: {r:.1f} Hz（期望 ~10 Hz）"); ok = False
        if MODE == "gazebo":
            if msg.width < 200:
                print(f"  真实场景点云点数过少: {msg.width}"); ok = False
            try:
                x0, x1, y0, y1, z0, z1 = pointcloud_bounds(msg)
                print(f"  点云范围 x[{x0:.2f},{x1:.2f}] y[{y0:.2f},{y1:.2f}] z[{z0:.2f},{z1:.2f}]")
                if max(abs(x0), abs(x1), abs(y0), abs(y1)) > 8.0:
                    print("  点云范围超出场景（|x|/|y| > 8 m）"); ok = False
                if not (-1.5 <= z0 <= z1 <= 3.0):
                    print("  点云 z 范围异常"); ok = False
            except Exception as exc:  # noqa: BLE001
                print(f"  点云解析失败: {exc}"); ok = False
            if msg.point_step % 4 != 0:
                print(f"  point_step={msg.point_step} 异常"); ok = False
        else:  # python 合成数据：固定 20000 点、26 字节结构
            if msg.width != 20000:
                print(f"  点云宽度异常: {msg.width} != 20000"); ok = False
            if msg.point_step != 26:
                print(f"  point_step 异常: {msg.point_step} != 26"); ok = False
        if node.clock_sim is not None:
            drift = abs(_stamp_s(msg.header.stamp) - node.clock_sim)
            print(f"LIDAR 时间戳与 /clock 偏差={drift:.3f}s")
            if drift > 0.5:
                print("  时间戳不是仿真时间"); ok = False

    if len(node.imu) < 20:
        print("IMU 没有收到数据（/livox/imu）")
        ok = False
    else:
        msg = node.imu[-1][0]
        r = rate([w for _, w in node.imu])
        print(f"IMU   frame={msg.header.frame_id} rate={r:.1f} samples={len(node.imu)}")
        if msg.header.frame_id != EXPECT_FRAME:
            print(f"  frame_id={msg.header.frame_id}（期望 {EXPECT_FRAME}）"); ok = False
        if not (120.0 <= r <= 260.0):
            print(f"  IMU 频率异常: {r:.1f} Hz（期望 ~200 Hz）"); ok = False

    print(f"ALIAS /livix/lidar={'OK' if node.alias > 0 else 'MISSING'} (n={node.alias})")
    if MODE == "python" and node.alias == 0:
        ok = False
    print("RESULT:", "PASS" if ok else "FAIL")
    executor.shutdown()
    node.destroy_node()
    rclpy.shutdown()
    sys.stdout.flush()
    os._exit(0 if ok else 1)


if __name__ == "__main__":
    main()
