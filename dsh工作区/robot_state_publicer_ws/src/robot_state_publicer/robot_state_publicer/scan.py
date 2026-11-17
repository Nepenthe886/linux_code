"""Synthetic Livox Mid-360 scan generator.

The sensor is placed at the origin of ``livox_frame`` (x forward, y left,
z up).  A simple indoor scene is ray-cast for every scan:

* floor at z = -lidar_height
* ceiling at z = 2.2 m (relative to the sensor)
* four walls at x / y = +/-3.5 m
* two box obstacles and one cylinder

The generated cloud follows the point layout used by
``livox_ros_driver2`` when ``xfer_format=0`` (PointCloud2):

    float32 x, y, z, intensity
    uint8   tag, line
    float64 timestamp   # absolute nanoseconds

Reference: ``livox_ros_driver2/src/comm/comm.h`` (LivoxPointXyzrtlt,
packed, 26 bytes) and ``src/lddc.cpp`` (InitPointcloud2MsgHeader).
"""

from __future__ import annotations

import numpy as np

# Vertical field of view of the Mid-360 (deg).
VERTICAL_MIN = np.deg2rad(-7.0)
VERTICAL_MAX = np.deg2rad(52.0)

ROOM_X = 3.5
ROOM_Y = 3.5
CEILING_Z = 2.2          # in livox_frame

# material ids
MAT_GROUND = 0
MAT_CEILING = 1
MAT_WALL = 2
MAT_BOX = 3
MAT_CYLINDER = 4
MATERIAL_INTENSITY = np.array([35.0, 55.0, 75.0, 180.0, 150.0])

# axis-aligned boxes in livox_frame: (x0, x1, y0, y1, z0, z1)
BOXES = [
    (0.8, 1.5, -0.5, 0.4, -0.27, 0.65),
    (-2.0, -1.2, 0.8, 1.6, -0.27, 1.0),
]


def _aabb_hit(dx, dy, dz, box):
    """First positive ray parameter for an axis-aligned box."""
    tmin = np.full(dx.shape, -np.inf)
    tmax = np.full(dx.shape, np.inf)
    for d, lo, hi in ((dx, box[0], box[1]),
                      (dy, box[2], box[3]),
                      (dz, box[4], box[5])):
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = lo / d
            t2 = hi / d
        tlo = np.minimum(t1, t2)
        thi = np.maximum(t1, t2)
        tmin = np.maximum(tmin, tlo)
        tmax = np.minimum(tmax, thi)
    valid = (tmin <= tmax) & (tmin > 0.0) & np.isfinite(tmin)
    return np.where(valid, tmin, np.inf)


def _cylinder_hit(dx, dy, dz, cx, cy, radius, z0, z1):
    """First positive ray parameter for a vertical finite cylinder."""
    a = dx * dx + dy * dy
    b = 2.0 * (cx * dx + cy * dy)
    c = cx * cx + cy * cy - radius * radius
    disc = b * b - 4.0 * a * c
    valid = (a > 1e-12) & (disc >= 0.0)
    if not np.any(valid):
        return np.full(dx.shape, np.inf)
    sq = np.sqrt(np.maximum(disc, 0.0))
    with np.errstate(divide="ignore", invalid="ignore"):
        t0 = (-b - sq) / (2.0 * a)
        t1 = (-b + sq) / (2.0 * a)
    # if the origin is inside the cylinder, take the exit point
    t0 = np.where(t0 > 0.0, t0, t1)
    valid &= (t0 > 0.0) & (t0 * dz >= z0) & (t0 * dz <= z1)
    return np.where(valid, t0, np.inf)


def generate_scan(points_per_frame: int = 20000,
                  lidar_height: float = 0.27,
                  seed: int = 1,
                  max_range: float = 40.0,
                  lidar_rate: float = 10.0) -> dict:
    """Return a scan as numpy arrays in the LiDAR frame.

    The dictionary keys are x, y, z, intensity, tag, line, offset_ns.
    """
    n_cols = 200
    n_rows = max(1, int(points_per_frame) // n_cols)
    n = n_cols * n_rows
    rng = np.random.default_rng(seed)

    az = (np.arange(n_cols) + 0.5) * (2.0 * np.pi / n_cols)
    el = VERTICAL_MIN + (np.arange(n_rows) + 0.5) * (
        (VERTICAL_MAX - VERTICAL_MIN) / n_rows
    )
    az, el = np.meshgrid(az, el)

    # small jitter: Livox uses a non-repetitive scan, not a perfect grid
    az += rng.normal(0.0, np.deg2rad(0.35), az.shape)
    el += rng.normal(0.0, np.deg2rad(0.08), el.shape)
    az = az.ravel()
    el = el.ravel()

    dx = np.cos(el) * np.cos(az)
    dy = np.cos(el) * np.sin(az)
    dz = np.sin(el)

    t = np.full(n, np.inf)
    material = np.full(n, -1, dtype=np.int16)

    def update(mask, tt, mat_id):
        valid = mask & np.isfinite(tt) & (tt > 0.0) & (tt < t)
        t[valid] = tt[valid]
        material[valid] = mat_id

    ground = -float(lidar_height)
    # floor (only downward rays)
    with np.errstate(divide="ignore", invalid="ignore"):
        t_ground = ground / dz
    update(dz < -1e-6, t_ground, MAT_GROUND)

    # ceiling
    with np.errstate(divide="ignore", invalid="ignore"):
        t_ceil = CEILING_Z / dz
    hit_xy = (np.abs(t_ceil * dx) <= ROOM_X) & (np.abs(t_ceil * dy) <= ROOM_Y)
    update((dz > 1e-6) & hit_xy, t_ceil, MAT_CEILING)

    # four walls
    for sign, axis in ((1.0, "x"), (-1.0, "x"), (1.0, "y"), (-1.0, "y")):
        plane = sign * (ROOM_X if axis == "x" else ROOM_Y)
        d = dx if axis == "x" else dy
        with np.errstate(divide="ignore", invalid="ignore"):
            tt = plane / d
        u = tt * (dy if axis == "x" else dx)
        z = tt * dz
        limit = ROOM_Y if axis == "x" else ROOM_X
        inside = (np.abs(u) <= limit) & (z >= ground) & (z <= CEILING_Z)
        update((np.abs(d) > 1e-9) & (tt > 0.0) & inside, tt, MAT_WALL)

    # two boxes
    for box in BOXES:
        box = (box[0], box[1], box[2], box[3], ground, box[5])
        hit = _aabb_hit(dx, dy, dz, box)
        update(np.isfinite(hit), hit, MAT_BOX)

    # one cylinder at (0.8, -1.5), r=0.3, up to z=0.9
    cyl = _cylinder_hit(dx, dy, dz, 0.8, -1.5, 0.3, ground, 0.9)
    update(np.isfinite(cyl), cyl, MAT_CYLINDER)

    valid = np.isfinite(t) & (t > 0.1) & (t < max_range)
    t = t[valid]
    material = material[valid]
    dx, dy, dz = dx[valid], dy[valid], dz[valid]

    # realistic range noise: ~3 mm + 0.02 %
    t = t + rng.normal(0.0, 0.003 + 0.0002 * t)
    t = np.maximum(t, 0.1)

    x = t * dx
    y = t * dy
    z = t * dz

    base = MATERIAL_INTENSITY[np.clip(material, 0, len(MATERIAL_INTENSITY) - 1)]
    intensity = np.clip(base + rng.normal(0.0, 8.0, t.shape), 0.0, 255.0)
    line = (np.arange(t.size, dtype=np.uint8) % 4).astype(np.uint8)
    tag = np.zeros(t.size, dtype=np.uint8)
    offset_ns = np.linspace(
        0.0,
        1e9 / max(float(lidar_rate), 1e-6),
        t.size,
        endpoint=False,
    )

    return {
        "x": x.astype(np.float32),
        "y": y.astype(np.float32),
        "z": z.astype(np.float32),
        "intensity": intensity.astype(np.float32),
        "tag": tag,
        "line": line,
        "offset_ns": offset_ns.astype(np.float64),
    }
