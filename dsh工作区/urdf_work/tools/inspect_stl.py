#!/usr/bin/env python3
import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import render_urdf as R

def load_stl(path):
    data = open(path, 'rb').read()
    if len(data) < 84:
        raise ValueError('not binary stl')
    n = struct.unpack_from('<I', data, 80)[0]
    rec = np.frombuffer(data, dtype=np.uint8, count=n*50, offset=84).reshape(n, 50)
    tri = rec[:, 12:48].copy().view('<f4').reshape(n, 3, 3).astype(np.float64)
    # recompute flat normals
    e1 = tri[:,1] - tri[:,0]
    e2 = tri[:,2] - tri[:,0]
    fn = np.cross(e1, e2)
    ln = np.linalg.norm(fn, axis=1)
    ok = ln > 1e-12
    tri = tri[ok]; fn = fn[ok] / ln[ok, None]
    verts = tri.reshape(-1,3)
    norms = np.repeat(fn, 3, axis=0)
    tris = np.arange(len(verts)).reshape(-1,3)
    return verts, norms, tris

stl = sys.argv[1] if len(sys.argv) > 1 else 'mesh_src/gitee_meshes_mid360.STL'
verts, norms, tris = load_stl(stl)
mn, mx = verts.min(0), verts.max(0)
center = np.array([(mn[0]+mx[0])/2, (mn[1]+mx[1])/2, mn[2]])
verts = verts - center
print('bbox', mn, mx, 'extent', mx-mn, 'triangles', len(tris))

builder = R.Mesh()
# replicate faces with one color
T = np.eye(4)
builder.add(verts, norms, tris, T, (0.62,0.64,0.67,1.0), 'lidar_silver')
mesh = builder.finish()

envb = R.Mesh()
R.build_environment(envb, with_arrow=False)
env = envb.finish()

W,H = 600,450
views = [
    ('iso', (0.18,-0.18,0.16), (0,0,0.03), (0,0,1), 35),
    ('front', (0.22,0,0.05), (0,0,0.03), (0,0,1), 30),
    ('side', (0,0.22,0.05), (0,0,0.03), (0,0,1), 30),
    ('top', (0,0,0.28), (0,0,0), (1,0,0), 30),
]
tiles=[]
for name,eye,target,up,vfov in views:
    cam=R.Camera(eye,target,up,vfov,W,H)
    img=R.render([mesh,env],cam)
    im=Image.fromarray(img,'RGB')
    ImageDraw.Draw(im).text((10,10),name,fill=(0,0,0))
    tiles.append(im)
sheet=Image.new('RGB',(W*2,H*2),(255,255,255))
for i,im in enumerate(tiles):
    sheet.paste(im,((i%2)*W,(i//2)*H))
sheet.save('renders/stl_inspect.png')
print('saved renders/stl_inspect.png')
