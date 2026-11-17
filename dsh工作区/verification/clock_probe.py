import time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock
rclpy.init()
n = Node('clock_probe')
msgs = []
qos = QoSProfile(depth=200, reliability=ReliabilityPolicy.BEST_EFFORT)
n.create_subscription(Clock, '/clock', lambda m: msgs.append((m.clock.sec + m.clock.nanosec * 1e-9, time.time())), qos)
t0 = time.time()
while time.time() - t0 < 3:
    rclpy.spin_once(n, timeout_sec=0.05)
if len(msgs) > 1:
    sim = [m[0] for m in msgs]; wall = [m[1] for m in msgs]
    ds = [sim[i+1]-sim[i] for i in range(len(sim)-1)]
    dw = [wall[i+1]-wall[i] for i in range(len(wall)-1)]
    print(f"msgs={len(msgs)} Hz={len(msgs)/max(wall[-1]-wall[0],1e-9):.1f}")
    print(f"sim_delta min={min(ds):.5f} max={max(ds):.5f} mean={sum(ds)/len(ds):.5f}")
    print(f"RTF~{sum(ds)/sum(dw):.3f}")
else:
    print("no clock msgs", len(msgs))
