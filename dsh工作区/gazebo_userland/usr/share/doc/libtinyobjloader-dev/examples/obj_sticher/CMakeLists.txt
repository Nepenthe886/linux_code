project(obj_sticher)

find_package(tinyobjloader REQUIRED)

add_executable(${PROJECT_NAME} obj_sticher.cc obj_writer.cc)
target_link_libraries(${PROJECT_NAME} tinyobjloader::tinyobjloader)

