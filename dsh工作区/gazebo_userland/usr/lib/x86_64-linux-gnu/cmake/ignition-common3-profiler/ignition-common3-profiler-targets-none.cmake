#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ignition-common3::ignition-common3-profiler" for configuration "None"
set_property(TARGET ignition-common3::ignition-common3-profiler APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(ignition-common3::ignition-common3-profiler PROPERTIES
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-common3-profiler.so.3.14.0"
  IMPORTED_SONAME_NONE "libignition-common3-profiler.so.3"
  )

list(APPEND _IMPORT_CHECK_TARGETS ignition-common3::ignition-common3-profiler )
list(APPEND _IMPORT_CHECK_FILES_FOR_ignition-common3::ignition-common3-profiler "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-common3-profiler.so.3.14.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
