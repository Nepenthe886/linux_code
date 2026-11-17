#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_urdf as R
from PIL import Image, ImageDraw

urdf = "robot_description/urdf/omni_robot.urdf"
links = R.parse_urdf(urdf)
robot = R.build_robot_mesh(links)
env_builder = R.Mesh()
R.build_environment(env_builder, with_arrow=False)
env = env_builder.finish()

W, H = 1600, 1200
cam = R.Camera((0.36, -0.30, 0.18), (0.07, -0.07, 0.030), (0, 0, 1), 24, W, H)
img = R.render([robot, env], cam)
pil = Image.fromarray(img, "RGB")
draw = ImageDraw.Draw(pil)
font = R.load_font(34, bold=True)
sub = R.load_font(24)
draw.rectangle([0, H-90, W, H], fill=(20,24,30))
draw.text((24, H-72), "麦克纳姆轮细节：9 × 45° 滚子（R0.030 / W0.020）", font=font, fill=(255,255,255))
draw.text((24, 20), "R0.030 / W0.020 m", font=sub, fill=(70,75,82))
pil.save("renders/wheel_detail.png")
print("saved renders/wheel_detail.png")
