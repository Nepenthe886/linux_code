#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "sdformat9::sdformat9" for configuration "None"
set_property(TARGET sdformat9::sdformat9 APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(sdformat9::sdformat9 PROPERTIES
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libsdformat9.so.9.7.0"
  IMPORTED_SONAME_NONE "libsdformat9.so.9"
  )

list(APPEND _IMPORT_CHECK_TARGETS sdformat9::sdformat9 )
list(APPEND _IMPORT_CHECK_FILES_FOR_sdformat9::sdformat9 "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libsdformat9.so.9.7.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
