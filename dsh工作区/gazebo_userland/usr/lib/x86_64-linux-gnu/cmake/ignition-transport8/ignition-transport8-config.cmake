# - Config file for the ignition-transport8 package.
#
# For finding and loading ignition-transport8 from your project, type:
#
# find_package(ignition-transport8)
#
# This creates the following targets:
#
#   Core library target                     - ignition-transport8::ignition-transport8
#   Alternative target name                 - ignition-transport8::core
#   Core library + all requested components - ignition-transport8::requested
#
# Use target_link_libraries() to link your library or executable to one of the
# above targets.
#
# We also provide the following variables for backwards compatibility, but use
# of these is discouraged:
#
#   ignition-transport8_CORE_LIBRARY - Core library (actually contains ignition-transport8::core)
#   ignition-transport8_LIBRARIES    - All libraries to link against (actually contains ignition-transport8::requested).
#   ignition-transport8_INCLUDE_DIRS - Include directories for ignition-transport8 and its dependencies.
#
# We will also set ignition-transport8_FOUND to indicate that the package was found.
#
################################################################################

# We explicitly set the desired cmake version to ensure that the policy settings
# of users or of toolchains do not result in the wrong behavior for our modules.
# Note that the call to find_package(~) will PUSH a new policy stack before
# taking on these version settings, and then that stack will POP after the
# find_package(~) has exited, so this will not affect the cmake policy settings
# of a caller.
cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

if(NOT ignition-transport8_FIND_QUIETLY)
  message(STATUS "Looking for ignition-transport8 -- found version 8.2.1")
endif()

if(ignition-transport8_CONFIG_INCLUDED)

  # Check that each of the components requested in this call to find_package(~)
  # have already been found.
  set(ignition-transport8_all_requested_components_found true)
  foreach(component ${ignition-transport8_FIND_COMPONENTS})
    if(NOT ignition-transport8-${component}_FOUND)
      set(ignition-transport8_all_requested_components_found false)
      break()
    endif()
  endforeach()

  # If this ignition-transport8-config.cmake file has been called before,
  # and all the requested components are already found, then exit early.
  if(ignition-transport8_all_requested_components_found)
    return()
  endif()
endif()
set(ignition-transport8_CONFIG_INCLUDED TRUE)

# Get access to the find_dependency utility
include(CMakeFindDependencyMacro)
# Find ignition-cmake, because we need its modules in order to find the rest of
# our dependencies.
find_dependency(ignition-cmake2)

# Set the REQUIRED flag for the find_package(~) calls on this project's
# dependencies.
if(ignition-transport8_FIND_REQUIRED)
  set(ign_package_required REQUIRED)
else()
  set(ign_package_required "")
endif()

# Set the QUIET flag for the find_package(~) calls on this project's
# dependencies.
if(ignition-transport8_FIND_QUIETLY)
  set(ign_package_quiet QUIET)
else()
  set(ign_package_quiet "")
endif()

# --------------------------------
# Find each required dependency of this project (if nothing is below, then the
# project has no external dependencies). We use find_package(~) instead of
# find_dependency(~) here so that we can support COMPONENT arguments.
#
# TODO: When we migrate to cmake-3.9+, change these to find_dependency(~),
#       because at that point the find_dependency(~) function will support
#       the COMPONENT argument.
if(NOT ignition-transport8_FIND_QUIETLY)
  message(STATUS "Searching for dependencies of ignition-transport8")
endif()
find_package(IgnProtobuf 3 ${ign_package_quiet} ${ign_package_required})
find_package(ZeroMQ 4 ${ign_package_quiet} ${ign_package_required})
find_package(CPPZMQ ${ign_package_quiet} ${ign_package_required})
find_package(UUID ${ign_package_quiet} ${ign_package_required})
find_package(ignition-msgs5 5.6 ${ign_package_quiet} ${ign_package_required})
# --------------------------------


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was ignition-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)

# Use original install prefix when loaded through a "/usr move"
# cross-prefix symbolic link such as /lib -> /usr/lib.
get_filename_component(_realCurr "${CMAKE_CURRENT_LIST_DIR}" REALPATH)
get_filename_component(_realOrig "/usr/lib/x86_64-linux-gnu/cmake/ignition-transport8" REALPATH)
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

if(NOT TARGET ignition-transport8::ignition-transport8)
  include("${CMAKE_CURRENT_LIST_DIR}/ignition-transport8-targets.cmake")

  # Create a simplified imported target name for the core library.
  # You can link to this target instead of the core library.
  add_library(ignition-transport8::core INTERFACE IMPORTED)
  set_target_properties(ignition-transport8::core PROPERTIES
    INTERFACE_LINK_LIBRARIES ignition-transport8::ignition-transport8)
  # Note: In a future version of cmake, we can replace this with an ALIAS target

  # In case someone tries to link against the plain library name, we want to
  # intercept that and have them link against a target instead. This is
  # effectively the same as ignition-transport8::core, but it does not have the
  # benefit of unambiguously being a target name.
  add_library(ignition-transport8 INTERFACE IMPORTED)
  set_target_properties(ignition-transport8 PROPERTIES
    INTERFACE_LINK_LIBRARIES ignition-transport8::ignition-transport8)

endif()

# Create the "all" target if it does not already exist
if(NOT TARGET ignition-transport8::requested)
  add_library(ignition-transport8::requested INTERFACE IMPORTED)
endif()

# Link the core library to the "all" target. We set the property explicitly
# because target_link_libraries cannot be called on an imported target.
get_target_property(ign_all_components ignition-transport8::requested INTERFACE_LINK_LIBRARIES)
if(NOT ign_all_components)
  # If ignition-transport8::requested has not been given any libraries yet, then cmake will
  # set ign_all_components to ign_all_components-NOTFOUND, which is something we
  # should NOT pass into the INTERFACE_LINK_LIBRARIES property.
  set_target_properties(ignition-transport8::requested PROPERTIES
    INTERFACE_LINK_LIBRARIES "ignition-transport8::ignition-transport8")
else()
  set_target_properties(ignition-transport8::requested PROPERTIES
    INTERFACE_LINK_LIBRARIES "${ign_all_components};ignition-transport8::ignition-transport8")
endif()

# On windows we produce .dll libraries with no prefix
if(WIN32)
  set(CMAKE_FIND_LIBRARY_PREFIXES "")
  set(CMAKE_FIND_LIBRARY_SUFFIXES ".lib" ".dll")
endif()

# Package variables. Note that ignition-transport8_LIBRARIES and ignition-transport8_CORE_LIBRARY
# contain imported targets, so ignition-transport8_INCLUDE_DIRS is never needed.
set(ignition-transport8_CORE_LIBRARY ignition-transport8::core)
set(ignition-transport8_LIBRARIES ignition-transport8::requested)
set_and_check(ignition-transport8_INCLUDE_DIRS "${PACKAGE_PREFIX_DIR}/include/ignition/transport8")

# Backwards compatibility variables
set(IGNITION-TRANSPORT_LIBRARIES ${ignition-transport8_LIBRARIES})
set(IGNITION-TRANSPORT_INCLUDE_DIRS ${ignition-transport8_INCLUDE_DIRS})

# This macro is used by ignition-cmake to automatically configure the pkgconfig
# files for ignition projects.
ign_pkg_config_entry(ignition-transport8 "ignition-transport8")

# Find each of the components requested by find_package(~)
foreach(component ${ignition-transport8_FIND_COMPONENTS})

  if(NOT ignition-transport8_FIND_QUIETLY)
    message(STATUS "Searching for <ignition-transport8> component [${component}]")
  endif()

  if(ignition-transport8_FIND_REQUIRED_${component})

    # Find the component package using find_dependency(~). If the user specified
    # REQUIRED or QUIET, those will automatically get forwarded to
    # find_dependency(~)
    find_dependency(ignition-transport8-${component} 8.2.1 EXACT)

  else()

    # If this is an optional component, use find_package(~) instead of
    # find_dependency(~) so we can ensure that the use of REQUIRED does not get
    # forwarded to it.
    find_package(ignition-transport8-${component} 8.2.1 EXACT ${ign_package_quiet})

  endif()

endforeach()

# Specify the doxygen tag file
set(IGNITION-TRANSPORT_DOXYGEN_TAGFILE "${PACKAGE_PREFIX_DIR}/share/ignition/ignition-transport8/ignition-transport8.tag.xml")

# Specify the API url. This is where the doxygen tag file will resolve URLS to.
set(IGNITION-TRANSPORT_API_URL "https://ignitionrobotics.org/api/transport/8.2")
