#!/usr/bin/env python3
"""Offline software renderer for the robot URDF.

Parses primitive-geometry <visual> elements from the URDF and renders them
with a small z-buffer rasteriser (numpy only).  No GPU / OpenGL / RViz needed.
"""

import argparse
import math
import os
import struct

import numpy as np
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# math helpers
# --------------------------------------------------------------------------
def normalize(v):
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.maximum(n, 1e-12)


def rpy_to_matrix(roll, pitch, yaw):
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]], dtype=np.float64)
    ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]], dtype=np.float64)
    rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]], dtype=np.float64)
    return rz @ ry @ rx


def origin_to_matrix(el):
    t = np.eye(4, dtype=np.float64)
    if el is None:
        return t
    xyz = np.array([float(v) for v in el.get("xyz", "0 0 0").split()])
    rpy = [float(v) for v in el.get("rpy", "0 0 0").split()]
    t[:3, :3] = rpy_to_matrix(*rpy)
    t[:3, 3] = xyz
    return t


# --------------------------------------------------------------------------
# URDF parsing
# --------------------------------------------------------------------------
def parse_urdf(path):
    root = etree.parse(path).getroot()

    materials = {}
    for mat in root.findall("material"):
        col = mat.find("color")
        if col is not None:
            materials[mat.get("name")] = tuple(
                float(v) for v in col.get("rgba").split()
            )

    links = {}
    for link in root.findall("link"):
        name = link.get("name")
        visuals = []
        for vis in link.findall("visual"):
            geom_el = vis.find("geometry")[0]
            tag = geom_el.tag
            if tag == "cylinder":
                geom = ("cylinder", float(geom_el.get("radius")),
                        float(geom_el.get("length")))
            elif tag == "box":
                geom = ("box", *[float(v) for v in geom_el.get("size").split()])
            elif tag == "sphere":
                geom = ("sphere", float(geom_el.get("radius")))
            elif tag == "mesh":
                filename = geom_el.get("filename", "")
                scale = float(geom_el.get("scale", "1"))
                pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(path)))
                rel = filename
                if filename.startswith("package://robot_description/"):
                    rel = filename[len("package://robot_description/"):]
                elif filename.startswith("file://"):
                    rel = filename[len("file://"):]
                geom = ("mesh", os.path.join(pkg_root, rel), scale)
            else:
                continue

            mat_el = vis.find("material")
            color, mat_name = (0.7, 0.7, 0.7, 1.0), "default"
            if mat_el is not None:
                mat_name = mat_el.get("name", "default")
                col_el = mat_el.find("color")
                if col_el is not None:
                    color = tuple(float(v) for v in col_el.get("rgba").split())
                elif mat_name in materials:
                    color = materials[mat_name]
            visuals.append({
                "T": origin_to_matrix(vis.find("origin")),
                "geom": geom,
                "color": color,
                "material": mat_name,
            })
        links[name] = {"visuals": visuals, "T": None}

    joints = []
    for jnt in root.findall("joint"):
        joints.append({
            "name": jnt.get("name"),
            "parent": jnt.find("parent").get("link"),
            "child": jnt.find("child").get("link"),
            "T": origin_to_matrix(jnt.find("origin")),
        })
    by_parent = {}
    for j in joints:
        by_parent.setdefault(j["parent"], []).append(j)

    roots = set(links) - {j["child"] for j in joints}
    root_link = "base_footprint" if "base_footprint" in roots else sorted(roots)[0]

    def walk(link_name, transform):
        links[link_name]["T"] = transform
        for j in by_parent.get(link_name, []):
            walk(j["child"], transform @ j["T"])

    walk(root_link, np.eye(4, dtype=np.float64))
    return links


# --------------------------------------------------------------------------
# primitive meshes (local coordinates, per-vertex normals)
# --------------------------------------------------------------------------
def box_mesh(sx, sy, sz):
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    verts, norms, tris = [], [], []

    def face(normal, corners):
        base = len(verts)
        for c in corners:
            verts.append(c)
            norms.append(normal)
        tris.append((base, base + 1, base + 2))
        tris.append((base, base + 2, base + 3))

    face((1, 0, 0), [(hx, -hy, -hz), (hx, hy, -hz), (hx, hy, hz), (hx, -hy, hz)])
    face((-1, 0, 0), [(-hx, hy, -hz), (-hx, -hy, -hz), (-hx, -hy, hz), (-hx, hy, hz)])
    face((0, 1, 0), [(-hx, hy, -hz), (hx, hy, -hz), (hx, hy, hz), (-hx, hy, hz)])
    face((0, -1, 0), [(hx, -hy, -hz), (-hx, -hy, -hz), (-hx, -hy, hz), (hx, -hy, hz)])
    face((0, 0, 1), [(-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)])
    face((0, 0, -1), [(-hx, hy, -hz), (hx, hy, -hz), (hx, -hy, -hz), (-hx, -hy, -hz)])

    return (np.array(verts, dtype=np.float64),
            np.array(norms, dtype=np.float64),
            np.array(tris, dtype=np.int32))


def cylinder_mesh(radius, length, segments=72):
    hz = length / 2.0
    ang = np.linspace(0.0, 2.0 * np.pi, segments, endpoint=False)
    c, s = np.cos(ang), np.sin(ang)

    verts, norms, tris = [], [], []

    # side: two rings with radial normals
    for i in range(segments):
        for z, nz in ((-hz, 0), (hz, 0)):
            verts.append((radius * c[i], radius * s[i], z))
            norms.append((c[i], s[i], 0.0))
    for i in range(segments):
        j = (i + 1) % segments
        b0, t0 = 2 * i, 2 * i + 1
        b1, t1 = 2 * j, 2 * j + 1
        tris.append((b0, b1, t1))
        tris.append((b0, t1, t0))

    # caps
    for z, nz in ((hz, 1.0), (-hz, -1.0)):
        base = len(verts)
        verts.append((0.0, 0.0, z))
        norms.append((0.0, 0.0, nz))
        for i in range(segments):
            verts.append((radius * c[i], radius * s[i], z))
            norms.append((0.0, 0.0, nz))
        for i in range(segments):
            j = (i + 1) % segments
            if nz > 0:
                tris.append((base, base + 1 + i, base + 1 + j))
            else:
                tris.append((base, base + 1 + j, base + 1 + i))

    return (np.array(verts, dtype=np.float64),
            np.array(norms, dtype=np.float64),
            np.array(tris, dtype=np.int32))


def sphere_mesh(radius, segments=32, rings=16):
    verts, norms, tris = [], [], []
    for i in range(rings + 1):
        phi = -math.pi / 2.0 + math.pi * i / rings
        cp, sp = math.cos(phi), math.sin(phi)
        for j in range(segments):
            theta = 2.0 * math.pi * j / segments
            n = (cp * math.cos(theta), cp * math.sin(theta), sp)
            verts.append((radius * n[0], radius * n[1], radius * n[2]))
            norms.append(n)
    for i in range(rings):
        for j in range(segments):
            a = i * segments + j
            b = i * segments + (j + 1) % segments
            c = (i + 1) * segments + j
            d = (i + 1) * segments + (j + 1) % segments
            tris.append((a, b, d))
            tris.append((a, d, c))
    return (np.array(verts, dtype=np.float64),
            np.array(norms, dtype=np.float64),
            np.array(tris, dtype=np.int32))


# --------------------------------------------------------------------------
# mesh accumulation in world space
# --------------------------------------------------------------------------
def load_binary_stl(path):
    """Load a binary STL as flat-shaded triangles."""
    data = open(path, "rb").read()
    if len(data) < 84:
        raise ValueError(f"not a binary STL: {path}")
    count = struct.unpack_from("<I", data, 80)[0]
    records = np.frombuffer(data, dtype=np.uint8, count=count * 50, offset=84).reshape(count, 50)
    tris = records[:, 12:48].copy().view("<f4").reshape(count, 3, 3).astype(np.float64)
    e1 = tris[:, 1] - tris[:, 0]
    e2 = tris[:, 2] - tris[:, 0]
    normals = np.cross(e1, e2)
    lengths = np.linalg.norm(normals, axis=1)
    ok = lengths > 1e-12
    tris = tris[ok]
    normals = normals[ok] / lengths[ok, None]
    verts = tris.reshape(-1, 3)
    norms = np.repeat(normals, 3, axis=0)
    idx = np.arange(len(verts), dtype=np.int32).reshape(-1, 3)
    return verts, norms, idx


MAT_SPEC = {
    "body_gray": (0.04, 20.0),
    "accent_orange": (0.12, 28.0),
    "wheel_black": (0.03, 14.0),
    "wheel_plate": (0.15, 30.0),
    "roller_gray": (0.28, 34.0),
    "hub_gray": (0.22, 36.0),
    "lidar_black": (0.12, 26.0),
    "lidar_blue": (0.70, 110.0),
    "lidar_silver": (0.45, 55.0),
    "lidar_glass": (0.60, 90.0),
    "camera_dark": (0.12, 28.0),
    "lens_blue": (0.80, 120.0),
}


class Mesh:
    def __init__(self):
        self.verts = []
        self.norms = []
        self.tris = []
        self.colors = []
        self.spec = []
        self.shin = []

    def add(self, verts, norms, tris, T, color, material):
        rot = T[:3, :3]
        world_v = verts @ rot.T + T[:3, 3]
        world_n = norms @ rot.T
        base = sum(len(v) for v in self.verts)

        spec, shin = MAT_SPEC.get(material, (0.15, 30.0))
        self.verts.append(world_v)
        self.norms.append(world_n)
        self.tris.append(tris + base)
        self.colors.append(np.tile(np.array(color[:3], dtype=np.float64), (len(tris), 1)))
        self.spec.append(np.full(len(tris), spec))
        self.shin.append(np.full(len(tris), shin))

    def finish(self):
        return {
            "v": np.vstack(self.verts).astype(np.float32),
            "n": np.vstack(self.norms).astype(np.float32),
            "t": np.vstack(self.tris).astype(np.int32),
            "col": np.vstack(self.colors).astype(np.float32),
            "spec": np.concatenate(self.spec).astype(np.float32),
            "shin": np.concatenate(self.shin).astype(np.float32),
        }


def add_quad(mesh, p0, p1, p2, p3, color, material="floor"):
    verts = np.array([p0, p1, p2, p3], dtype=np.float64)
    normal = np.cross(verts[1] - verts[0], verts[2] - verts[0])
    normal /= np.linalg.norm(normal)
    norms = np.tile(normal, (4, 1))
    tris = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int32)
    T = np.eye(4)
    mesh.add(verts, norms, tris, T, tuple(color) + (1.0,), material)


def build_robot_mesh(links):
    mesh = Mesh()
    for link in links.values():
        for vis in link["visuals"]:
            geom = vis["geom"]
            if geom[0] == "box":
                verts, norms, tris = box_mesh(*geom[1:])
            elif geom[0] == "cylinder":
                verts, norms, tris = cylinder_mesh(geom[1], geom[2])
            elif geom[0] == "sphere":
                verts, norms, tris = sphere_mesh(geom[1])
            elif geom[0] == "mesh":
                verts, norms, tris = load_binary_stl(geom[1])
                if geom[2] != 1.0:
                    verts = verts * geom[2]
            else:
                continue
            T = link["T"] @ vis["T"]
            mesh.add(verts, norms, tris, T, vis["color"], vis["material"])
    return mesh.finish()


def build_environment(mesh_builder, floor_half=14.0, with_arrow=True):
    # floor (two big triangles)
    floor_col = (0.735, 0.750, 0.770)
    verts = np.array([
        [-floor_half, -floor_half, 0.0],
        [floor_half, -floor_half, 0.0],
        [floor_half, floor_half, 0.0],
        [-floor_half, floor_half, 0.0],
    ], dtype=np.float64)
    norms = np.tile(np.array([0.0, 0.0, 1.0]), (4, 1))
    tris = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int32)
    mesh_builder.add(verts, norms, tris, np.eye(4), floor_col + (1.0,), "floor")

    # grid lines
    minor = (0.615, 0.635, 0.665)
    major = (0.545, 0.565, 0.600)
    span = 4.0
    step = 0.25
    n = int(round(span / step))
    for k in range(-n, n + 1):
        x = k * step
        is_major = abs(k % 4) == 0
        w = 0.007 if is_major else 0.004
        c = major if is_major else minor
        z = 0.0007
        add_quad(mesh_builder, (x - w / 2, -span, z), (x + w / 2, -span, z),
                 (x + w / 2, span, z), (x - w / 2, span, z), c, "floor")
        add_quad(mesh_builder, (-span, x - w / 2, z), (span, x - w / 2, z),
                 (span, x + w / 2, z), (-span, x + w / 2, z), c, "floor")

    # soft contact shadow: concentric annuli
    base = np.array(floor_col)
    rings = 16
    r_out, r_in = 0.16, 0.0
    seg = 48
    z = 0.0015
    ang = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    for i in range(rings):
        t0 = i / rings
        t1 = (i + 1) / rings
        r0 = r_out + (r_in - r_out) * t0
        r1 = r_out + (r_in - r_out) * t1
        f = 1.0 - 0.38 * (t0 ** 1.5)
        col = tuple(np.clip(base * f, 0, 1))
        for j in range(seg):
            a0, a1 = ang[j], ang[(j + 1) % seg]
            p0 = (r0 * math.cos(a0), r0 * math.sin(a0), z)
            p1 = (r0 * math.cos(a1), r0 * math.sin(a1), z)
            p2 = (r1 * math.cos(a1), r1 * math.sin(a1), z)
            p3 = (r1 * math.cos(a0), r1 * math.sin(a0), z)
            add_quad(mesh_builder, p0, p1, p2, p3, col, "floor")

    # front direction arrow on the floor (only where it reads clearly)
    if with_arrow:
        arrow_col = (0.90, 0.38, 0.08)
        z = 0.0025
        add_quad(mesh_builder, (0.13, -0.004, z), (0.21, -0.004, z),
                 (0.21, 0.004, z), (0.13, 0.004, z), arrow_col, "floor")
        verts = np.array([[0.21, -0.016, z], [0.21, 0.016, z], [0.25, 0.0, z]])
        norms = np.tile(np.array([0.0, 0.0, 1.0]), (3, 1))
        mesh_builder.add(verts, norms, np.array([[0, 1, 2]], dtype=np.int32),
                         np.eye(4), arrow_col + (1.0,), "floor")


# --------------------------------------------------------------------------
# camera + rasteriser
# --------------------------------------------------------------------------
class Camera:
    def __init__(self, eye, target, up, vfov_deg, width, height):
        self.eye = np.array(eye, dtype=np.float64)
        self.f = normalize(np.array(target, dtype=np.float64) - self.eye)
        self.r = normalize(np.cross(self.f, np.array(up, dtype=np.float64)))
        self.u = np.cross(self.r, self.f)
        self.focal = (height / 2.0) / math.tan(math.radians(vfov_deg) / 2.0)
        self.cx, self.cy = width / 2.0, height / 2.0
        self.w, self.h = width, height

    def project(self, p):
        p = np.asarray(p, dtype=np.float64)
        d = p - self.eye
        z = float(d @ self.f)
        if z <= 1e-6:
            return None
        x = float(d @ self.r)
        y = float(d @ self.u)
        return (self.cx + self.focal * x / z, self.cy - self.focal * y / z, z)


def render(meshes, camera, bg_top=(0.94, 0.95, 0.96), bg_bottom=(0.83, 0.85, 0.87)):
    W, H = camera.w, camera.h
    yy = np.linspace(0.0, 1.0, H, dtype=np.float32).reshape(H, 1, 1)
    top = np.array(bg_top, dtype=np.float32).reshape(1, 1, 3)
    bot = np.array(bg_bottom, dtype=np.float32).reshape(1, 1, 3)
    img = np.broadcast_to(top * (1 - yy) + bot * yy, (H, W, 3)).copy()
    img = img.astype(np.float32)
    zbuf = np.full((H, W), np.inf, dtype=np.float32)

    light1 = normalize(np.array([0.35, -0.55, 0.95]))
    light2 = normalize(np.array([-0.65, 0.45, 0.35]))
    ambient = 0.32
    spec_color = np.array([1.0, 0.97, 0.92], dtype=np.float32)

    near = 0.02
    cx, cy, focal = camera.cx, camera.cy, camera.focal
    eye = camera.eye
    r_axis, u_axis, f_axis = camera.r, camera.u, camera.f

    for mesh in meshes:
        v = mesh["v"].astype(np.float64)
        n = mesh["n"].astype(np.float64)
        d = v - eye
        zc = d @ f_axis
        xc = d @ r_axis
        yc = d @ u_axis
        sx = cx + focal * xc / np.maximum(zc, 1e-9)
        sy = cy - focal * yc / np.maximum(zc, 1e-9)

        for k in range(len(mesh["t"])):
            i0, i1, i2 = mesh["t"][k]
            z0, z1, z2 = zc[i0], zc[i1], zc[i2]
            if z0 <= near or z1 <= near or z2 <= near:
                continue

            x0, y0 = sx[i0], sy[i0]
            x1, y1 = sx[i1], sy[i1]
            x2, y2 = sx[i2], sy[i2]

            bx0 = max(int(math.floor(min(x0, x1, x2))), 0)
            bx1 = min(int(math.ceil(max(x0, x1, x2))), W - 1)
            by0 = max(int(math.floor(min(y0, y1, y2))), 0)
            by1 = min(int(math.ceil(max(y0, y1, y2))), H - 1)
            if bx0 > bx1 or by0 > by1:
                continue

            det = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(det) < 1e-12:
                continue

            X = np.arange(bx0, bx1 + 1, dtype=np.float32) + 0.5
            Y = np.arange(by0, by1 + 1, dtype=np.float32) + 0.5
            Xg, Yg = np.meshgrid(X, Y)

            w0 = ((y1 - y2) * (Xg - x2) + (x2 - x1) * (Yg - y2)) / det
            w1 = ((y2 - y0) * (Xg - x2) + (x0 - x2) * (Yg - y2)) / det
            w2 = 1.0 - w0 - w1
            inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            if not inside.any():
                continue

            invz = w0 / z0 + w1 / z1 + w2 / z2
            depth = 1.0 / np.maximum(invz, 1e-9)

            sub_z = zbuf[by0:by1 + 1, bx0:bx1 + 1]
            mask = inside & (depth < sub_z)
            if not mask.any():
                continue

            w0m = w0[mask]
            w1m = w1[mask]
            w2m = w2[mask]
            dm = depth[mask]

            n0, n1, n2 = n[i0], n[i1], n[i2]
            nm = (w0m[:, None] * n0 + w1m[:, None] * n1 + w2m[:, None] * n2)
            nm = normalize(nm)

            # reconstruct world position from the camera ray
            xndc = (Xg[mask] - cx) / focal
            yndc = (cy - Yg[mask]) / focal
            pos = eye + dm[:, None] * (
                r_axis[None, :] * xndc[:, None] +
                u_axis[None, :] * yndc[:, None] +
                f_axis[None, :]
            )
            view = normalize(eye[None, :] - pos)

            ndotv = np.sum(nm * view, axis=1)
            diff = (0.68 * np.maximum(nm @ light1, 0) +
                    0.18 * np.maximum(nm @ light2, 0) +
                    0.08 * np.maximum(ndotv, 0))
            base_col = mesh["col"][k]
            col = base_col[None, :] * (ambient + diff)[:, None]

            half = normalize(light1[None, :] + view)
            ndoth = np.sum(nm * half, axis=1)
            spec = (mesh["spec"][k] *
                    np.maximum(ndoth, 0) ** mesh["shin"][k])
            col += spec[:, None] * spec_color[None, :]

            rim = 0.05 * (1.0 - np.abs(ndotv)) ** 3
            col += rim[:, None] * base_col[None, :]

            fog = np.clip((dm - 4.0) / 14.0, 0.0, 0.88)[:, None]
            fog_col = np.array([0.925, 0.935, 0.945], dtype=np.float32)
            col = col * (1.0 - fog) + fog_col[None, :] * fog

            col = np.clip(col, 0.0, 1.0).astype(np.float32)
            sub_img = img[by0:by1 + 1, bx0:bx1 + 1]
            sub_img[mask] = col
            sub_z[mask] = dm

    return (np.clip(img, 0, 1) * 255.0).astype(np.uint8)


# --------------------------------------------------------------------------
# composition / labels
# --------------------------------------------------------------------------
def load_font(size, bold=False):
    path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else \
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    return ImageFont.truetype(path, size, index=2)


def draw_label(draw, xy, anchor_xy, text, font, fill, bg, scale=1.0):
    """Draw a label with a leader line. Coordinates are final-image pixels."""
    ax, ay = anchor_xy
    tx, ty = xy
    draw.line([(ax, ay), (tx, ty)], fill=fill, width=max(1, int(2 * scale)))
    draw.ellipse([ax - 3 * scale, ay - 3 * scale, ax + 3 * scale, ay + 3 * scale],
                 fill=fill)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 7
    draw.rounded_rectangle(
        [tx - pad, ty - th / 2 - pad, tx + tw + pad, ty + th / 2 + pad],
        radius=6, fill=bg,
    )
    draw.text((tx, ty - th / 2 - bbox[1]), text, font=font, fill=(25, 28, 33))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urdf")
    ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=1.5,
                    help="supersampling factor (1.5 -> 1500x1125 per tile)")
    ap.add_argument("--tile-w", type=int, default=1000)
    ap.add_argument("--tile-h", type=int, default=750)
    ap.add_argument("--views-only", action="store_true")
    args = ap.parse_args()

    links = parse_urdf(args.urdf)
    robot = build_robot_mesh(links)

    env_builder = Mesh()
    build_environment(env_builder, with_arrow=True)
    env = env_builder.finish()

    env_plain_builder = Mesh()
    build_environment(env_plain_builder, with_arrow=False)
    env_plain = env_plain_builder.finish()

    # per-view label anchors (world points)
    anchors = {
        "lidar": (0.0, 0.0, 0.305),
        "camera": (0.125, 0.0, 0.185),
        "wheel": (0.090, -0.090, 0.030),
    }

    W = int(args.tile_w * args.scale)
    H = int(args.tile_h * args.scale)

    views = [
        ("iso", dict(eye=(0.55, -0.62, 0.40), target=(0.0, 0.0, 0.14),
                     up=(0, 0, 1), vfov=30), "① 等轴视图（前右 45°）", True),
        ("front", dict(eye=(1.00, 0.0, 0.18), target=(0.0, 0.0, 0.15),
                       up=(0, 0, 1), vfov=24), "② 正视图（+X 前向）", False),
        ("side", dict(eye=(0.0, 1.00, 0.20), target=(0.0, 0.0, 0.15),
                      up=(0, 0, 1), vfov=24), "③ 侧视图（+Y 左侧）", False),
        ("top", dict(eye=(0.0, 0.0, 1.10), target=(0.0, 0.0, 0.0),
                     up=(1, 0, 0), vfov=28), "④ 俯视图（前向朝上）", True),
    ]

    rendered = []
    for key, cam_cfg, caption, arrow in views:
        cam = Camera(cam_cfg["eye"], cam_cfg["target"], cam_cfg["up"],
                     cam_cfg["vfov"], W, H)
        img = render([robot, env if arrow else env_plain], cam)
        pil = Image.fromarray(img, "RGB").resize(
            (args.tile_w, args.tile_h), Image.LANCZOS)
        anchors_px = {name: cam.project(p) for name, p in anchors.items()}
        rendered.append((key, pil, caption, anchors_px))

    # rescale anchors from supersampled pixels to tile pixels
    for _, _, _, apx in rendered:
        for k in apx:
            if apx[k] is not None:
                x, y, _ = apx[k]
                apx[k] = (x / args.scale, y / args.scale)

    # ---------------- compose 2x2 ----------------
    margin = 26
    gap = 18
    header_h = 108
    caption_h = 54
    fig_w = margin * 2 + args.tile_w * 2 + gap
    fig_h = header_h + args.tile_h * 2 + gap + caption_h + margin
    fig = Image.new("RGB", (fig_w, fig_h), (245, 246, 248))
    draw = ImageDraw.Draw(fig)

    title_font = load_font(42, bold=True)
    sub_font = load_font(23)
    cap_font = load_font(25, bold=True)
    label_font = load_font(21, bold=True)
    tag_font = load_font(17)

    draw.text((margin, 20), "Zhirong Cup 全向机器人 · URDF 几何模型", font=title_font,
              fill=(22, 26, 32))
    draw.text((margin, 72),
              "主体 Ø0.20 m × H0.20 m ｜ 4× 麦克纳姆轮 R0.030 m ｜ Livox Mid-360 ｜ 深度相机 D435i ｜ 单位：m",
              font=sub_font, fill=(80, 88, 98))

    label_specs = [
        ("lidar", "Livox Mid-360 激光雷达", (args.tile_w * 0.60, 88)),
        ("camera", "深度相机 D435i", (args.tile_w * 0.66, 300)),
        ("wheel", "麦轮 R30 / W20 ×4", (args.tile_w * 0.12, 330)),
    ]

    for idx, (key, pil, caption, apx) in enumerate(rendered):
        col = idx % 2
        row = idx // 2
        x = margin + col * (args.tile_w + gap)
        y = header_h + row * (args.tile_h + gap)

        # caption bar inside the tile (bottom)
        tile = pil.copy()
        tdraw = ImageDraw.Draw(tile, "RGBA")
        tdraw.rectangle([0, args.tile_h - caption_h, args.tile_w, args.tile_h],
                        fill=(20, 24, 30, 150))
        tdraw.text((18, args.tile_h - caption_h + 12), caption, font=cap_font,
                   fill=(255, 255, 255))

        # annotations on the isometric view
        if key == "iso":
            for akey, text, (tx, ty) in label_specs:
                p = apx.get(akey)
                if p is None:
                    continue
                # keep label inside the tile
                tx = min(max(tx, 14), args.tile_w - 300)
                ty = min(max(ty, 24), args.tile_h - caption_h - 24)
                draw_label(tdraw, (tx, ty), (p[0], p[1]), text, label_font,
                           fill=(230, 110, 30), bg=(250, 250, 252, 235), scale=1.0)

        # tile border
        bdraw = ImageDraw.Draw(tile)
        bdraw.rectangle([0, 0, args.tile_w - 1, args.tile_h - 1],
                        outline=(205, 208, 213), width=2)
        fig.paste(tile, (x, y))

    # front-view dimension annotations
    footer = "初版参数（待评审）· 2026-11-17 ｜ 车体底面离地 0.070 m ｜ 总高 0.330 m ｜ 轮距 0.140 m"
    draw.text((margin, fig_h - caption_h + 12), footer, font=tag_font,
              fill=(95, 100, 108))

    fig.save(args.out)
    print("saved", args.out, fig.size)


if __name__ == "__main__":
    main()
