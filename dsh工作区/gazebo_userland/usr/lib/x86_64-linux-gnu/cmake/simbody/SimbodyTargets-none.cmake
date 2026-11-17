#----------------------------------------------------------------
# Generated CMake target import file for configuration "None".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SimTKcommon" for configuration "None"
set_property(TARGET SimTKcommon APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(SimTKcommon PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_NONE "/usr/lib/x86_64-linux-gnu/libblas.so;/usr/lib/x86_64-linux-gnu/liblapack.so;/usr/lib/x86_64-linux-gnu/libblas.so;pthread;rt;dl;m"
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libSimTKcommon.so.3.6"
  IMPORTED_SONAME_NONE "libSimTKcommon.so.3.6"
  )

list(APPEND _IMPORT_CHECK_TARGETS SimTKcommon )
list(APPEND _IMPORT_CHECK_FILES_FOR_SimTKcommon "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libSimTKcommon.so.3.6" )

# Import target "SimTKmath" for configuration "None"
set_property(TARGET SimTKmath APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(SimTKmath PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_NONE "SimTKcommon;/usr/lib/x86_64-linux-gnu/libblas.so;/usr/lib/x86_64-linux-gnu/liblapack.so;/usr/lib/x86_64-linux-gnu/libblas.so;pthread;rt;dl;m"
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libSimTKmath.so.3.6"
  IMPORTED_SONAME_NONE "libSimTKmath.so.3.6"
  )

list(APPEND _IMPORT_CHECK_TARGETS SimTKmath )
list(APPEND _IMPORT_CHECK_FILES_FOR_SimTKmath "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libSimTKmath.so.3.6" )

# Import target "SimTKsimbody" for configuration "None"
set_property(TARGET SimTKsimbody APPEND PROPERTY IMPORTED_CONFIGURATIONS NONE)
set_target_properties(SimTKsimbody PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_NONE "SimTKmath;SimTKcommon;/usr/lib/x86_64-linux-gnu/libblas.so;/usr/lib/x86_64-linux-gnu/liblapack.so;/usr/lib/x86_64-linux-gnu/libblas.so;pthread;rt;dl;m"
  IMPORTED_LOCATION_NONE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libSimTKsimbody.so.3.6"
  IMPORTED_SONAME_NONE "libSimTKsimbody.so.3.6"
  )

list(APPEND _IMPORT_CHECK_TARGETS SimTKsimbody )
list(APPEND _IMPORT_CHECK_FILES_FOR_SimTKsimbody "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libSimTKsimbody.so.3.6" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
