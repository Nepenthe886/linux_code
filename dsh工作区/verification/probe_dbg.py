import threading, time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import PointCloud2
rclpy.init(); n=Node('dbg')
cloud=[]; clocks=[]; imu=[]
qos=QoSProfile(depth=20, reliability=ReliabilityPolicy.BEST_EFFORT)
n.create_subscription(Clock,'/clock',lambda m: clocks.append((m.clock.sec+m.clock.nanosec*1e-9, time.time())),qos)
n.create_subscription(PointCloud2,'/livox/lidar',lambda m: cloud.append((m.header.stamp.sec+m.header.stamp.nanosec*1e-9, time.time())),10)
n.create_subscription(PointCloud2,'/livix/lidar',lambda m: None,10)
from sensor_msgs.msg import Imu
n.create_subscription(Imu,'/livox/imu',lambda m: imu.append((m.header.stamp.sec+m.header.stamp.nanosec*1e-9, time.time())),100)
threading.Thread(target=rclpy.spin,args=(n,),daemon=True).start()
time.sleep(6)
print('cloud count', len(cloud), 'clock count', len(clocks), 'imu count', len(imu))
print('cloud last 5 stamps:', [round(c[0],2) for c in cloud[-5:]], 'wall ages:', [round(time.time()-c[1],3) for c in cloud[-5:]])
print('clock last 5:', [round(c[0],2) for c in clocks[-5:]], 'wall ages:', [round(time.time()-c[1],3) for c in clocks[-5:]])
print('drift(last cloud - last clock) =', round(cloud[-1][0]-clocks[-1][0],3))
