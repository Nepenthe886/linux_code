#!/usr/bin/env python3
import math, os, re, sys
import numpy as np

stage = sys.argv[1]
p = os.path.join(stage, 'urdf', 'omni_robot.urdf')
s = open(p, encoding='utf-8').read()

# ---------------- chassis ----------------
body = '''  <link name="base_link">
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="1.2"/>
      <!-- solid cylinder: Ixx=Iyy=m(3r^2+h^2)/12, Izz=m r^2/2 -->
      <inertia ixx="0.0070" ixy="0.0" ixz="0.0"
               iyy="0.0070" iyz="0.0" izz="0.0060"/>
    </inertial>

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.1" length="0.20"/>
      </geometry>
      <material name="body_gray"/>
    </visual>

    <!-- thin orange accent band, purely cosmetic -->
    <visual>
      <origin xyz="0 0 0.07" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.1008" length="0.02"/>
      </geometry>
      <material name="accent_orange"/>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.1" length="0.20"/>
      </geometry>
    </collision>
  </link>'''
s = re.sub(r'  <link name="base_link">.*?\n  </link>', lambda m: body, s, count=1, flags=re.S)

s = s.replace('<origin xyz="0 0 0.24" rpy="0 0 0"/>', '<origin xyz="0 0 0.17" rpy="0 0 0"/>')

# ---------------- wheels ----------------
WHEEL_R = 0.030
CORE_R, CORE_W = 0.022, 0.018
PLATE_R, PLATE_W, PLATE_Y = 0.023, 0.0015, 0.009
HUB_R, HUB_W = 0.012, 0.022
ROLLER_R, ROLLER_L, ROLLER_RC = 0.005, 0.014, 0.024
COUNT = 9

def fmt(v):
    if abs(v) < 1e-12:
        v = 0.0
    return f"{v:.8f}".rstrip('0').rstrip('.')

def rot_z_to(a):
    a = np.asarray(a, float); a /= np.linalg.norm(a)
    z = np.array([0.0, 0.0, 1.0])
    if abs(float(a @ z)) > 0.999999:
        u = np.array([1.0, 0.0, 0.0])
    else:
        u = np.cross(a, z); u /= np.linalg.norm(u)
    v = np.cross(a, u)
    R = np.column_stack([u, v, a])
    pitch = math.asin(max(-1.0, min(1.0, -R[2, 0])))
    roll = math.atan2(R[2, 1], R[2, 2])
    yaw = math.atan2(R[1, 0], R[0, 0])
    return roll, pitch, yaw

def visual(xyz, rpy, geom, mat):
    return f'''    <visual>
      <origin xyz="{fmt(xyz[0])} {fmt(xyz[1])} {fmt(xyz[2])}" rpy="{fmt(rpy[0])} {fmt(rpy[1])} {fmt(rpy[2])}"/>
      <geometry>
        {geom}
      </geometry>
      <material name="{mat}"/>
    </visual>
'''

def wheel(name, side):
    s_sign = 1.0 if side == 'left' else -1.0
    parts = []
    parts.append(visual((0,0,0), (math.pi/2,0,0), f'<cylinder radius="{CORE_R}" length="{CORE_W}"/>', 'wheel_black'))
    parts.append(visual((0, PLATE_Y, 0), (math.pi/2,0,0), f'<cylinder radius="{PLATE_R}" length="{PLATE_W}"/>', 'wheel_plate'))
    parts.append(visual((0,-PLATE_Y, 0), (math.pi/2,0,0), f'<cylinder radius="{PLATE_R}" length="{PLATE_W}"/>', 'wheel_plate'))
    parts.append(visual((0,0,0), (math.pi/2,0,0), f'<cylinder radius="{HUB_R}" length="{HUB_W}"/>', 'hub_gray'))
    for i in range(COUNT):
        theta = math.radians(-90.0 + i*360.0/COUNT)
        c, sn = math.cos(theta), math.sin(theta)
        pc = np.array([ROLLER_RC*c, 0.0, ROLLER_RC*sn])
        tangent = np.array([-sn, 0.0, c])
        axle = math.cos(math.radians(45))*tangent + s_sign*math.sin(math.radians(45))*np.array([0.0,1.0,0.0])
        parts.append(visual(pc, rot_z_to(axle), f'<cylinder radius="{ROLLER_R}" length="{ROLLER_L}"/>', 'roller_gray'))
    return f'''  <link name="{name}">
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.15"/>
      <!-- cylinder axis along Y -->
      <inertia ixx="0.00003875" ixy="0.0" ixz="0.0"
               iyy="0.00006750" iyz="0.0" izz="0.00003875"/>
    </inertial>
{''.join(parts)}    <collision>
      <origin xyz="0 0 0" rpy="1.57079632679 0 0"/>
      <geometry>
        <cylinder radius="{WHEEL_R}" length="0.020"/>
      </geometry>
    </collision>
  </link>'''

for name, side in [
    ('wheel_front_left_link', 'left'),
    ('wheel_front_right_link', 'right'),
    ('wheel_rear_left_link', 'left'),
    ('wheel_rear_right_link', 'right'),
]:
    pat = re.compile(r'  <link name="' + name + r'">.*?\n  </link>', re.S)
    assert pat.search(s), name
    s = pat.sub(lambda m, n=name, sd=side: wheel(n, sd), s, count=1)

# joint origins
for old, new in [
    ('xyz="0.17 0.17 -0.175"', 'xyz="0.06 0.06 -0.14"'),
    ('xyz="0.17 -0.17 -0.175"', 'xyz="0.06 -0.06 -0.14"'),
    ('xyz="-0.17 0.17 -0.175"', 'xyz="-0.06 0.06 -0.14"'),
    ('xyz="-0.17 -0.17 -0.175"', 'xyz="-0.06 -0.06 -0.14"'),
]:
    assert old in s, old
    s = s.replace(old, new)
s = s.replace('effort="20.0"', 'effort="2.0"')

# camera
s = s.replace('Body centre at x = 0.263 (back face 0.2505), z = 0.270.',
              'Body centre at x = 0.113 (back face 0.1005), z = 0.185.')
s = s.replace('<origin xyz="0.263 0 0.03" rpy="0 0 0"/>',
              '<origin xyz="0.113 0 0.015" rpy="0 0 0"/>')

# lidar height
s = s.replace('top of lidar at z = 0.400.', 'top of lidar at z = 0.330.')

open(p, 'w', encoding='utf-8').write(s)
print('resized URDF written')
