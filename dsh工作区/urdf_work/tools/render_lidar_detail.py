#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_urdf as R
from PIL import Image, ImageDraw

urdf = sys.argv[1] if len(sys.argv) > 1 else 'robot_description_mesh_stage/urdf/omni_robot.urdf'
links = R.parse_urdf(urdf)
robot = R.build_robot_mesh(links)
env_builder = R.Mesh()
R.build_environment(env_builder, with_arrow=False)
env = env_builder.finish()

W, H = 1400, 1050
cam = R.Camera((0.16, -0.13, 0.46), (0.0, 0.0, 0.295), (0, 0, 1), 26, W, H)
img = R.render([robot, env], cam)
pil = Image.fromarray(img, "RGB")
draw = ImageDraw.Draw(pil)
font = R.load_font(32, bold=True)
draw.rectangle([0, H-78, W, H], fill=(20,24,30))
draw.text((22, H-62), "Livox Mid-360：开源 STL（MIT），蓝色半球罩 + 银色散热底座", font=font, fill=(255,255,255))
pil.save('renders/lidar_detail.png')
print('saved renders/lidar_detail.png')
