import sys, struct, time, math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
rclpy.init()
n=Node('cloud_probe'); got=[]
n.create_subscription(PointCloud2,'/livox/lidar',lambda m: got.append(m),10)
t0=time.time()
while time.time()-t0<8 and not got: rclpy.spin_once(n,timeout_sec=0.1)
if not got:
    print('no cloud'); sys.exit(1)
m=got[-1]
print('frame',m.header.frame_id,'width',m.width,'height',m.height,'point_step',m.point_step,'fields',[(f.name,f.offset,f.datatype) for f in m.fields])
pts=[]; step=m.point_step; npts=m.width*m.height
for i in range(npts):
    x,y,z,inten=struct.unpack_from('<ffff',m.data,i*step); pts.append((x,y,z,inten))
zs=sorted(p[2] for p in pts)
print('z min/max',zs[0],zs[-1],'p10/p50/p90',zs[len(zs)//10],zs[len(zs)//2],zs[9*len(zs)//10])
print('x range',min(p[0] for p in pts),max(p[0] for p in pts),'y range',min(p[1] for p in pts),max(p[1] for p in pts))
print('n pts z>0.3:',sum(1 for p in pts if p[2]>0.3),'z>0.5:',sum(1 for p in pts if p[2]>0.5))
print('sample',pts[:3])
