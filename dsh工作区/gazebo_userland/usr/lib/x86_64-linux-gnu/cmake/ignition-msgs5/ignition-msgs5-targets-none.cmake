#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ignition-msgs5::ignition-msgs5" for configuration "None"
set_property(TARGET ignition-msgs5::ignition-msgs5 APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(ignition-msgs5::ignition-msgs5 PROPERTIES
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-msgs5.so.5.8.1"
  IMPORTED_SONAME_NONE "libignition-msgs5.so.5"
  )

list(APPEND _IMPORT_CHECK_TARGETS ignition-msgs5::ignition-msgs5 )
list(APPEND _IMPORT_CHECK_FILES_FOR_ignition-msgs5::ignition-msgs5 "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-msgs5.so.5.8.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
