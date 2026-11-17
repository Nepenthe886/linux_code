from glob import glob
import os

from setuptools import find_packages, setup

package_name = "robot_state_publicer"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [os.path.join("resource", package_name)]),
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools", "numpy"],
    zip_safe=True,
    maintainer="Zhirong Cup Team",
    maintainer_email="nepenthe@example.com",
    description="Simulated Livox Mid-360 LiDAR/IMU publisher",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "mid360_sim = robot_state_publicer.mid360_sim_node:main",
            "livix_relay = robot_state_publicer.livix_relay:main",
        ],
    },
)
