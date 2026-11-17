#!/usr/bin/env python3
"""Add 9 mecanum rollers (visual only) to each wheel link of the URDF."""
import math
import re
import sys

import numpy as np

URDF = "robot_description/urdf/omni_robot.urdf"

WHEEL_R = 0.065
WHEEL_W = 0.040
CORE_R = 0.050
CORE_W = 0.036
PLATE_R = 0.050
PLATE_W = 0.003
PLATE_Y = 0.0195
HUB_R = 0.026
HUB_W = 0.046
ROLLER_R = 0.010
ROLLER_L = 0.028
ROLLER_RC = 0.054
ROLLER_COUNT = 9

def rot_z_to(a):
    a = np.asarray(a, dtype=float)
    a = a / np.linalg.norm(a)
    z = np.array([0.0, 0.0, 1.0])
    if abs(float(a @ z)) > 0.999999:
        u = np.array([1.0, 0.0, 0.0])
    else:
        u = np.cross(a, z)
        u /= np.linalg.norm(u)
    v = np.cross(a, u)
    R = np.column_stack([u, v, a])
    pitch = math.asin(max(-1.0, min(1.0, -R[2, 0])))
    roll = math.atan2(R[2, 1], R[2, 2])
    yaw = math.atan2(R[1, 0], R[0, 0])
    return roll, pitch, yaw

def fmt(v):
    if abs(v) < 1e-12:
        v = 0.0
    return f"{v:.8f}".rstrip("0").rstrip(".")

def roller_origins(side):
    s = 1.0 if side == "left" else -1.0
    out = []
    for i in range(ROLLER_COUNT):
        theta = math.radians(-90.0 + i * 360.0 / ROLLER_COUNT)
        c, sn = math.cos(theta), math.sin(theta)
        p = np.array([ROLLER_RC * c, 0.0, ROLLER_RC * sn])
        tangent = np.array([-sn, 0.0, c])
        axle = math.cos(math.radians(45.0)) * tangent + s * math.sin(math.radians(45.0)) * np.array([0.0, 1.0, 0.0])
        roll, pitch, yaw = rot_z_to(axle)
        out.append((p, (roll, pitch, yaw)))
    return out

def visual_cylinder(xyz, rpy, radius, length, material):
    return (f'''    <visual>
      <origin xyz="{fmt(xyz[0])} {fmt(xyz[1])} {fmt(xyz[2])}" rpy="{fmt(rpy[0])} {fmt(rpy[1])} {fmt(rpy[2])}"/>
      <geometry>
        <cylinder radius="{radius}" length="{length}"/>
      </geometry>
      <material name="{material}"/>
    </visual>
''')

def wheel_block(name, side):
    visuals = []
    # main wheel core (the rollers sit on this disc)
    visuals.append(visual_cylinder((0, 0, 0), (math.pi / 2, 0, 0), CORE_R, CORE_W, "wheel_black"))
    # two side plates
    visuals.append(visual_cylinder((0, PLATE_Y, 0), (math.pi / 2, 0, 0), PLATE_R, PLATE_W, "wheel_plate"))
    visuals.append(visual_cylinder((0, -PLATE_Y, 0), (math.pi / 2, 0, 0), PLATE_R, PLATE_W, "wheel_plate"))
    # hub / axle
    visuals.append(visual_cylinder((0, 0, 0), (math.pi / 2, 0, 0), HUB_R, HUB_W, "hub_gray"))
    # rollers
    for p, rpy in roller_origins(side):
        visuals.append(visual_cylinder(tuple(p), rpy, ROLLER_R, ROLLER_L, "roller_gray"))

    return f'''  <link name="{name}">
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.4"/>
      <!-- cylinder axis along Y -->
      <inertia ixx="0.0004758" ixy="0.0" ixz="0.0"
               iyy="0.0008450" iyz="0.0" izz="0.0004758"/>
    </inertial>
{''.join(visuals)}    <collision>
      <origin xyz="0 0 0" rpy="1.57079632679 0 0"/>
      <geometry>
        <cylinder radius="0.065" length="0.040"/>
      </geometry>
    </collision>
  </link>'''

text = open(URDF, encoding="utf-8").read()

# add the two extra materials once
if '<material name="wheel_plate">' not in text:
    text = text.replace('''  <material name="hub_gray">
    <color rgba="0.45 0.47 0.50 1.0"/>
  </material>''','''  <material name="hub_gray">
    <color rgba="0.45 0.47 0.50 1.0"/>
  </material>
  <material name="wheel_plate">
    <color rgba="0.30 0.32 0.35 1.0"/>
  </material>
  <material name="roller_gray">
    <color rgba="0.27 0.28 0.30 1.0"/>
  </material>''')

for name, side in [
    ("wheel_front_left_link", "left"),
    ("wheel_front_right_link", "right"),
    ("wheel_rear_left_link", "left"),
    ("wheel_rear_right_link", "right"),
]:
    pattern = re.compile(r'  <link name="' + name + r'">.*?\n  </link>', re.S)
    new = wheel_block(name, side)
    if not pattern.search(text):
        raise SystemExit(f"link not found: {name}")
    text = pattern.sub(lambda m: new, text, count=1)

open(URDF, "w", encoding="utf-8").write(text)
print("rollers added")
