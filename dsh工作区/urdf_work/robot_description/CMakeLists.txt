cmake_minimum_required(VERSION 3.8)
project(robot_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY urdf launch rviz
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS scripts/zero_joint_states.py
  DESTINATION share/${PROJECT_NAME}/scripts
)

ament_package()
