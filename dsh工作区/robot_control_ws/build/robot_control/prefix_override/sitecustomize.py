import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/nepenthe/zmf/linux_code/dsh工作区/robot_control_ws/install/robot_control'
