#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dart-external-odelcpsolver" for configuration "None"
set_property(TARGET dart-external-odelcpsolver APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(dart-external-odelcpsolver PROPERTIES
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libdart-external-odelcpsolver.so.6.12.1"
  IMPORTED_SONAME_NONE "libdart-external-odelcpsolver.so.6.12"
  )

list(APPEND _IMPORT_CHECK_TARGETS dart-external-odelcpsolver )
list(APPEND _IMPORT_CHECK_FILES_FOR_dart-external-odelcpsolver "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libdart-external-odelcpsolver.so.6.12.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
