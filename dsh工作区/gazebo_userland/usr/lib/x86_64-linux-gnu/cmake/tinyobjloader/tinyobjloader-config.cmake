
####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was tinyobjloader-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)

# Use original install prefix when loaded through a "/usr move"
# cross-prefix symbolic link such as /lib -> /usr/lib.
get_filename_component(_realCurr "${CMAKE_CURRENT_LIST_DIR}" REALPATH)
get_filename_component(_realOrig "/usr/lib/x86_64-linux-gnu/cmake/tinyobjloader" REALPATH)
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

####################################################################################

set(TINYOBJLOADER_VERSION "2.0.0")

set_and_check(TINYOBJLOADER_INCLUDE_DIRS "${PACKAGE_PREFIX_DIR}/include")
set_and_check(TINYOBJLOADER_LIBRARY_DIRS "${PACKAGE_PREFIX_DIR}/lib/x86_64-linux-gnu")
set(TINYOBJLOADER_LIBRARIES tinyobjloader::tinyobjloader)

include("${CMAKE_CURRENT_LIST_DIR}/tinyobjloader-targets.cmake")

include(FindPackageHandleStandardArgs)
set(tinyobjloader_CONFIG ${CMAKE_CURRENT_LIST_FILE})
find_package_handle_standard_args(tinyobjloader CONFIG_MODE)

