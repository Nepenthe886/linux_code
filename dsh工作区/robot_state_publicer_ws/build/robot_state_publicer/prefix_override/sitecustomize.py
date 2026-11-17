import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/nepenthe/zmf/linux_code/dsh工作区/robot_state_publicer_ws/install/robot_state_publicer'
