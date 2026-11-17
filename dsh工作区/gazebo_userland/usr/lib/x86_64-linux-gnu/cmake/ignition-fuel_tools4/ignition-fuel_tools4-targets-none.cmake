#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ignition-fuel_tools4::ignition-fuel_tools4" for configuration "None"
set_property(TARGET ignition-fuel_tools4::ignition-fuel_tools4 APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(ignition-fuel_tools4::ignition-fuel_tools4 PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_NONE "ignition-msgs5::ignition-msgs5"
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-fuel_tools4.so.4.4.0"
  IMPORTED_SONAME_NONE "libignition-fuel_tools4.so.4"
  )

list(APPEND _IMPORT_CHECK_TARGETS ignition-fuel_tools4::ignition-fuel_tools4 )
list(APPEND _IMPORT_CHECK_FILES_FOR_ignition-fuel_tools4::ignition-fuel_tools4 "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libignition-fuel_tools4.so.4.4.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
