#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ignition-common3::ignition-common3-graphics" for configuration "None"
set_property(TARGET ignition-common3::ignition-common3-graphics APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(ignition-common3::ignition-common3-graphics PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_NONE "tinyobjloader::tinyobjloader"
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-common3-graphics.so.3.14.0"
  IMPORTED_SONAME_NONE "libignition-common3-graphics.so.3"
  )

list(APPEND _IMPORT_CHECK_TARGETS ignition-common3::ignition-common3-graphics )
list(APPEND _IMPORT_CHECK_FILES_FOR_ignition-common3::ignition-common3-graphics "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-common3-graphics.so.3.14.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
