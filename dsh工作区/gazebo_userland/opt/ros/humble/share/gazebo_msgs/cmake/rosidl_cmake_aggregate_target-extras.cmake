# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target gazebo_msgs::gazebo_msgs
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${gazebo_msgs_TARGETS}.
if(gazebo_msgs_TARGETS AND NOT TARGET gazebo_msgs::gazebo_msgs)
  add_library(gazebo_msgs::gazebo_msgs INTERFACE IMPORTED)
  set_target_properties(gazebo_msgs::gazebo_msgs PROPERTIES
    INTERFACE_LINK_LIBRARIES "${gazebo_msgs_TARGETS}")
endif()
