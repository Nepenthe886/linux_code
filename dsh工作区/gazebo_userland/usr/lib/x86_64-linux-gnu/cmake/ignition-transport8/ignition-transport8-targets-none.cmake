#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ignition-transport8::ignition-transport8" for configuration "None"
set_property(TARGET ignition-transport8::ignition-transport8 APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(ignition-transport8::ignition-transport8 PROPERTIES
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-transport8.so.8.2.1"
  IMPORTED_SONAME_NONE "libignition-transport8.so.8"
  )

list(APPEND _IMPORT_CHECK_TARGETS ignition-transport8::ignition-transport8 )
list(APPEND _IMPORT_CHECK_FILES_FOR_ignition-transport8::ignition-transport8 "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-transport8.so.8.2.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
