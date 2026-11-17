import time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import PointCloud2
rclpy.init(); n=Node('lag')
last={'clock':None,'cloud':None,'cloud_t':0}
qos=QoSProfile(depth=50, reliability=ReliabilityPolicy.BEST_EFFORT)
n.create_subscription(Clock,'/clock',lambda m: last.__setitem__('clock', m.clock.sec+m.clock.nanosec*1e-9), qos)
n.create_subscription(PointCloud2,'/livox/lidar',lambda m: last.update(cloud=m.header.stamp.sec+m.header.stamp.nanosec*1e-9, cloud_t=time.time()), 10)
t0=time.time()
while time.time()-t0<9:
    rclpy.spin_once(n,timeout_sec=0.02)
    if time.time()-t0>2 and last['clock'] and last['cloud'] and time.time()-last['cloud_t']<0.3:
        print(f"t={time.time()-t0:5.1f}s lag={last['clock']-last['cloud']:+.3f}s  (clock={last['clock']:.2f})")
        time.sleep(1.5)
