import numpy as np

from robot_state_publicer.scan import generate_scan


def test_scan_shape_and_finite_values():
    scan = generate_scan(points_per_frame=20000, lidar_height=0.27, seed=3)
    n = scan["x"].size
    assert 15000 <= n <= 20000
    for key in ("x", "y", "z", "intensity", "tag", "line", "offset_ns"):
        assert scan[key].shape == (n,)
        assert np.all(np.isfinite(scan[key]))
    assert np.all(scan["intensity"] >= 0.0)
    assert np.all(scan["intensity"] <= 255.0)
    assert np.all(scan["offset_ns"] >= 0.0)
