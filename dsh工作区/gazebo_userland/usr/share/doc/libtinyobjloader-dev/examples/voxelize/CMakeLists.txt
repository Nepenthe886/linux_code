project(voxelize)

find_package(tinyobjloader REQUIRED)

add_executable(${PROJECT_NAME} main.cc)
target_link_libraries(${PROJECT_NAME} tinyobjloader::tinyobjloader)

