import math, struct, time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
rclpy.init(); n=Node('p2'); got=[]
n.create_subscription(PointCloud2,'/livox/lidar',lambda m: got.append(m),10)
t0=time.time()
while time.time()-t0<8 and not got: rclpy.spin_once(n,timeout_sec=0.1)
m=got[-1]
pts=[]
for i in range(m.width*m.height):
    x,y,z,inten=struct.unpack_from('<ffff',m.data,i*m.point_step)
    pts.append((x,y,z,inten))
print('n',len(pts))
ds=sorted(math.sqrt(x*x+y*y+z*z) for x,y,z,_ in pts)
print('dist min/max',round(ds[0],3),round(ds[-1],3))
import collections
bins=[0,0.1,0.2,0.3,0.5,0.8,1.2,2,3,5,8,100]
h=collections.Counter()
for d in ds:
    for i in range(len(bins)-1):
        if bins[i]<=d<bins[i+1]: h[f'{bins[i]}-{bins[i+1]}']+=1; break
print('dist hist',dict(h))
# 按 z 分布
zs=sorted(p[2] for p in pts)
print('z', round(zs[0],3), round(zs[len(zs)//4],3), round(zs[len(zs)//2],3), round(zs[3*len(zs)//4],3), round(zs[-1],3))
# 远处点（>1.2m）z 分布
far=[p for p in pts if math.sqrt(p[0]**2+p[1]**2+p[2]**2)>1.2]
print('far n',len(far))
if far:
    fz=sorted(p[2] for p in far); print('far z min/med/max',round(fz[0],3),round(fz[len(fz)//2],3),round(fz[-1],3))
    print('far sample',[(round(x,2),round(y,2),round(z,2)) for x,y,z,_ in far[:5]])
