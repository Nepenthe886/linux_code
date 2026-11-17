import struct, sys, time
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2

out = sys.argv[1] if len(sys.argv) > 1 else 'verification/shots/lidar_cloud_frame.png'
rclpy.init(); n = Node('cloud_snap'); got = []
n.create_subscription(PointCloud2, '/livox/lidar', lambda m: got.append(m), 10)
t0 = time.time()
while time.time() - t0 < 8 and not got:
    rclpy.spin_once(n, timeout_sec=0.1)
m = got[-1]
npts = m.width * m.height
arr = np.frombuffer(m.data, dtype=np.uint8).reshape(npts, m.point_step)
xyz = arr[:, :12].copy().view('<f4').reshape(npts, 3)
inten = arr[:, 12:16].copy().view('<f4').reshape(npts)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
ax = axes[0]
ax.scatter(xyz[:, 0], xyz[:, 1], c=xyz[:, 2], s=4, cmap='viridis')
ax.set_title(f'Mid-360 /livox/lidar frame (n={npts}, frame={m.header.frame_id})')
ax.set_xlabel('x [m]'); ax.set_ylabel('y [m]'); ax.set_aspect('equal'); ax.grid(alpha=0.3)
ax = axes[1]
ax.scatter(np.arange(npts), xyz[:, 2], s=2, c='tab:blue', alpha=0.6)
ax.set_title('z distribution (sensor frame)'); ax.set_xlabel('point index'); ax.set_ylabel('z [m]'); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(out, dpi=110); print('saved', out, 'n=', npts)
