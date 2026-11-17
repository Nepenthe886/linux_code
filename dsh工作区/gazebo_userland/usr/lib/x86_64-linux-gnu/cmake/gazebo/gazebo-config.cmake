if (GAZEBO_CONFIG_INCLUDED)
  return()
endif()
set(GAZEBO_CONFIG_INCLUDED TRUE)
set(GAZEBO_VERSION 11.10)
set(GAZEBO_MAJOR_VERSION 11)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was gazebo-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)

# Use original install prefix when loaded through a "/usr move"
# cross-prefix symbolic link such as /lib -> /usr/lib.
get_filename_component(_realCurr "${CMAKE_CURRENT_LIST_DIR}" REALPATH)
get_filename_component(_realOrig "/usr/lib/x86_64-linux-gnu/cmake/gazebo/" REALPATH)
if(_realCurr STREQUAL _realOrig)
  set(PACKAGE_PREFIX_DIR "/usr")
endif()
unset(_realOrig)
unset(_realCurr)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

# Including Dartsim will overwrite the PACKAGE_PREFIX_DIR, therefore make gazebo-specific vars
set(GAZEBO_INSTALL_DATAROOT_DIR ${PACKAGE_PREFIX_DIR}/share)
set(GAZEBO_INSTALL_LIB_DIR ${PACKAGE_PREFIX_DIR}/lib/x86_64-linux-gnu)
set(GAZEBO_INSTALL_INCLUDE_DIR ${PACKAGE_PREFIX_DIR}/include)

set(GAZEBO_PLUGIN_PATH "${GAZEBO_INSTALL_LIB_DIR}/gazebo-11/plugins")

# The media path contains the location on disk where images,
# materials scripts, shaders, and other related resources are stored.
set(GAZEBO_MEDIA_PATH "${GAZEBO_INSTALL_DATAROOT_DIR}/gazebo-11/media")

# The model path contains the location on disk where models are stored.
set(GAZEBO_MODEL_PATH "${GAZEBO_INSTALL_DATAROOT_DIR}/gazebo-11/models")

# Set whether Gazebo was built with Bullet support
set (GAZEBO_HAS_BULLET TRUE)

# Set whether Gazebo was built with Simbody support
set (GAZEBO_HAS_SIMBODY TRUE)

# Set whether Gazebo was built with Simbody support
set (GAZEBO_HAS_DART TRUE)
set (GAZEBO_DART_MIN_REQUIRED_VERSION 6.6)
set (GAZEBO_HAS_DART_BULLET TRUE)

# Set whether Gazebo was built with Ignition Fuel Tools support
set (GAZEBO_HAS_IGNITION_FUEL_TOOLS )

include (FindPkgConfig)

#################################################
# GAZEBO_PROTO_PATH, GAZEBO_PROTO_INCLUDE_DIRS, and
# GAZEBO_PROTO_LIBRARIES
#
# These three variables allow Gazebo messages to be used in other projects.
#
# The following examples are for demonstration purposes and are
# incomplete. The first example shows how to use a Gazebo message in a
# custom  proto file. The second example shows how to run 'protoc' against
# custom proto files that make use Gazebo message definitions. The third
# example shows how to include the correct directory when compiling a library
# or executable that uses your custom messages.
#
# 1. Use a Gazebo message in a custom proto file:
#
# package my.msgs;
# import "vector3d.proto";
#
# message MyMessage
# {
#   required gazebo.msgs.Vector3d p = 1;
# }
#
# 2. Run protoc from a CMakeLists.txt to generate your message's
#    header and source files:
#
#  add_custom_command(
#    OUTPUT
#      "${proto_filename}.pb.cc"
#      "${proto_filename}.pb.h"
#    COMMAND protoc
#    ARGS --proto_path ${GAZEBO_PROTO_PATH} ${proto_file_out}
#    COMMENT "Running C++ protocol buffer compiler on ${proto_filename}"
#    VERBATIM)
#
# 3. When compiling your library or executable, make sure to use the following
#    in the CMakeLists.txt file:
#
# include_directories(GAZEBO_PROTO_INCLUDE_DIRS)
# target_link_libraries(your_package GAZEBO_PROTO_LIBRARIES)
#
set(GAZEBO_PROTO_PATH
  "${GAZEBO_INSTALL_INCLUDE_DIR}/gazebo-11/gazebo/msgs/proto")
find_library(gazebo_proto_msgs_lib gazebo_msgs
  PATHS "${GAZEBO_INSTALL_LIB_DIR}" NO_DEFAULT_PATH)
list(APPEND GAZEBO_PROTO_LIBRARIES ${gazebo_proto_msgs_lib})
list(APPEND GAZEBO_PROTO_INCLUDE_DIRS
  "${GAZEBO_INSTALL_INCLUDE_DIR}/gazebo-11/gazebo/msgs")
# End GAZEBO_PROTO_PATH, GAZEBO_PROTO_INCLUDE_DIRS, and
# GAZEBO_PROTO_LIBRARIES

list(APPEND GAZEBO_INCLUDE_DIRS ${GAZEBO_INSTALL_INCLUDE_DIR})
list(APPEND GAZEBO_INCLUDE_DIRS ${GAZEBO_INSTALL_INCLUDE_DIR}/gazebo-11)

list(APPEND GAZEBO_LIBRARY_DIRS ${GAZEBO_INSTALL_LIB_DIR})
list(APPEND GAZEBO_LIBRARY_DIRS ${GAZEBO_INSTALL_LIB_DIR}/gazebo-11/plugins)

list(APPEND GAZEBO_CFLAGS -I${GAZEBO_INSTALL_INCLUDE_DIR})
list(APPEND GAZEBO_CFLAGS -I${GAZEBO_INSTALL_INCLUDE_DIR}/gazebo-11)

if (GAZEBO_HAS_BULLET)
  if (PKG_CONFIG_FOUND)
    pkg_check_modules(BULLET bullet>=2.82)
    if (NOT BULLET_FOUND)
       pkg_check_modules(BULLET bullet2.82>=2.82)
    endif()

    if (BULLET_FOUND)
      add_definitions(-DLIBBULLET_VERSION=${BULLET_VERSION})
    else()
      message(FATAL_ERROR "Error: Bullet > 2.82 not found, please install libbullet2.82-dev.")
    endif()

    if (BULLET_VERSION VERSION_GREATER 2.82)
      add_definitions(-DLIBBULLET_VERSION_GT_282)
    endif()

    list(APPEND GAZEBO_INCLUDE_DIRS ${BULLET_INCLUDE_DIRS})
    list(APPEND GAZEBO_LIBRARY_DIRS ${BULLET_LIBRARY_DIRS})
    list(APPEND GAZEBO_LIBRARIES ${BULLET_LIBRARIES})
  else()
    message(FATAL_ERROR "Error: pkg-config not found.")
  endif()
endif()

if (GAZEBO_HAS_SIMBODY)
  find_package(Simbody REQUIRED)
  list(APPEND GAZEBO_INCLUDE_DIRS ${Simbody_INCLUDE_DIR})
  list(APPEND GAZEBO_LIBRARIES ${Simbody_LIBRARIES})
endif()

if (GAZEBO_HAS_DART)
  find_package(DART ${GAZEBO_DART_MIN_REQUIRED_VERSION} REQUIRED CONFIG)
  list(APPEND GAZEBO_INCLUDE_DIRS ${DART_INCLUDE_DIRS})
  list(APPEND GAZEBO_LIBRARIES ${DART_LIBRARIES})
endif()

if ("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang" AND
    "${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
  set(GAZEBO_CXX_FLAGS "${GAZEBO_CXX_FLAGS} -stdlib=libc++")
endif ()

foreach(lib gazebo;gazebo_client;gazebo_gui;gazebo_sensors;gazebo_rendering;gazebo_physics;gazebo_ode;gazebo_transport;gazebo_msgs;gazebo_util;gazebo_common;gazebo_gimpact;gazebo_opcode;gazebo_opende_ou)
  set(onelib "${lib}-NOTFOUND")
  find_library(onelib ${lib}
    PATHS "${GAZEBO_INSTALL_LIB_DIR}"
    NO_DEFAULT_PATH
    )
  if(NOT onelib)
    message(FATAL_ERROR "Library '${lib}' in package GAZEBO is not installed properly")
  endif()
  list(APPEND GAZEBO_LIBRARIES ${onelib})
endforeach()

# Get the install prefix for OGRE
execute_process(COMMAND ${PKG_CONFIG_EXECUTABLE} --variable=prefix OGRE
  OUTPUT_VARIABLE OGRE_INSTALL_PREFIX OUTPUT_STRIP_TRAILING_WHITESPACE)

# Add the OGRE cmake path to CMAKE_MODULE_PATH
set(CMAKE_MODULE_PATH
  "${OGRE_INSTALL_PREFIX}/share/OGRE/cmake/modules;${OGRE_INSTALL_PREFIX}/lib/OGRE/cmake;${OGRE_INSTALL_PREFIX}/CMake;${CMAKE_MODULE_PATH}")

# Find boost
find_package(Boost 1.40.0 REQUIRED thread system
  filesystem program_options regex iostreams date_time)
list(APPEND GAZEBO_INCLUDE_DIRS ${Boost_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARIES ${Boost_LIBRARIES})

# Find protobuf
find_package(Protobuf REQUIRED)
list(APPEND GAZEBO_INCLUDE_DIRS ${PROTOBUF_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARIES ${PROTOBUF_LIBRARIES})

# Find SDFormat
find_package(sdformat9 REQUIRED)
list(APPEND GAZEBO_INCLUDE_DIRS ${SDFormat_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARIES ${SDFormat_LIBRARIES})

# Find OGRE
find_package(OGRE REQUIRED COMPONENTS Terrain Paging)
list(APPEND GAZEBO_INCLUDE_DIRS ${OGRE_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARIES ${OGRE_LIBRARIES})
# When including OGRE, also include the Terrain and Paging components
list(APPEND GAZEBO_INCLUDE_DIRS
  ${OGRE_Terrain_INCLUDE_DIRS}
  ${OGRE_Paging_INCLUDE_DIRS}
  ${OGRE-Terrain_INCLUDE_DIRS}
  ${OGRE-Paging_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARIES
  ${OGRE_Terrain_LIBRARIES}
  ${OGRE_Paging_LIBRARIES}
  ${OGRE-Terrain_LIBRARIES}
  ${OGRE-Paging_LIBRARIES})

# Find Ignition Math
find_package(ignition-math6 REQUIRED)
list(APPEND GAZEBO_INCLUDE_DIRS ${IGNITION-MATH_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARY_DIRS ${IGNITION-MATH_LIBRARY_DIRS})
list(APPEND GAZEBO_LIBRARIES ${IGNITION-MATH_LIBRARIES})

# Find Ignition Transport
find_package(ignition-transport8 REQUIRED)
list(APPEND GAZEBO_INCLUDE_DIRS ${IGNITION-TRANSPORT_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARY_DIRS ${IGNITION-TRANSPORT_LIBRARY_DIRS})
list(APPEND GAZEBO_LIBRARIES ${IGNITION-TRANSPORT_LIBRARIES})

# Find Ignition Msgs
find_package(ignition-msgs5 REQUIRED)
list(APPEND GAZEBO_INCLUDE_DIRS ${IGNITION-MSGS_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARY_DIRS ${IGNITION-MSGS_LIBRARY_DIRS})
list(APPEND GAZEBO_LIBRARIES ${IGNITION-MSGS_LIBRARIES})

find_package(ignition-common3 REQUIRED COMPONENTS graphics)
list(APPEND GAZEBO_INCLUDE_DIRS ${ignition-common3_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARY_DIRS ${ignition-common3_LIBRARY_DIRS})
list(APPEND GAZEBO_LIBRARIES ignition-common3::ignition-common3-graphics)

find_package(ignition-fuel_tools4 REQUIRED)
list(APPEND GAZEBO_INCLUDE_DIRS ${IGNITION-FUEL_TOOLS_INCLUDE_DIRS})
list(APPEND GAZEBO_LIBRARY_DIRS ${IGNITION-FUEL_TOOLS_LIBRARY_DIRS})
list(APPEND GAZEBO_LIBRARIES ${IGNITION-FUEL_TOOLS_LIBRARIES})

list(APPEND GAZEBO_LDFLAGS -Wl,-rpath,${GAZEBO_INSTALL_LIB_DIR}/gazebo-11/plugins)
list(APPEND GAZEBO_LDFLAGS -L${GAZEBO_INSTALL_LIB_DIR})
list(APPEND GAZEBO_LDFLAGS -L${GAZEBO_INSTALL_LIB_DIR}/gazebo-11/plugins)

set (GAZEBO_HAS_TBB_GREATER_OR_EQUAL_2021 ON)
if (GAZEBO_HAS_TBB_GREATER_OR_EQUAL_2021)
  find_package(TBB CONFIG)
  if (TARGET tbb::tbb)
    list(APPEND GAZEBO_LIBRARIES TBB::tbb)
  endif ()
endif ()
