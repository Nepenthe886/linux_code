#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "tinyobjloader::tinyobjloader" for configuration "None"
set_property(TARGET tinyobjloader::tinyobjloader APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(tinyobjloader::tinyobjloader PROPERTIES
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libtinyobjloader.so.2.0.0"
  IMPORTED_SONAME_NONE "libtinyobjloader.so.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS tinyobjloader::tinyobjloader )
list(APPEND _IMPORT_CHECK_FILES_FOR_tinyobjloader::tinyobjloader "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libtinyobjloader.so.2.0.0" )

# Import target "tinyobjloader::tinyobjloader_double" for configuration "None"
set_property(TARGET tinyobjloader::tinyobjloader_double APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(tinyobjloader::tinyobjloader_double PROPERTIES
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libtinyobjloader_double.so.2.0.0"
  IMPORTED_SONAME_NONE "libtinyobjloader_double.so.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS tinyobjloader::tinyobjloader_double )
list(APPEND _IMPORT_CHECK_FILES_FOR_tinyobjloader::tinyobjloader_double "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libtinyobjloader_double.so.2.0.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
