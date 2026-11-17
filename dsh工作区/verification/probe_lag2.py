import threading, time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import PointCloud2
rclpy.init(); n=Node('lag2')
st={'clock':None,'clock_t':0,'cloud':None,'cloud_t':0}
qos=QoSProfile(depth=100, reliability=ReliabilityPolicy.BEST_EFFORT)
def clk(m):
    st['clock']=m.clock.sec+m.clock.nanosec*1e-9; st['clock_t']=time.time()
def cl(m):
    st['cloud']=m.header.stamp.sec+m.header.stamp.nanosec*1e-9; st['cloud_t']=time.time()
n.create_subscription(Clock,'/clock',clk,qos)
n.create_subscription(PointCloud2,'/livox/lidar',cl,10)
threading.Thread(target=rclpy.spin,args=(n,),daemon=True).start()
t0=time.time()
print("wall  simclock  cloud_stamp  lag(clock-cloud)  cloud_age(wall)")
while time.time()-t0<8:
    time.sleep(1.0)
    if st['clock'] and st['cloud']:
        print(f"{time.time()-t0:4.1f}  {st['clock']:9.2f}  {st['cloud']:11.2f}  {st['clock']-st['cloud']:+8.2f}  {time.time()-st['cloud_t']:.2f}")
