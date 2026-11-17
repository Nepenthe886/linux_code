cmake_minimum_required(VERSION 3.8)
project(bring_up)

find_package(ament_cmake REQUIRED)

# 纯 launch/配置资源包
install(DIRECTORY launch config
        DESTINATION share/${PROJECT_NAME})
install(FILES README.md package.xml
        DESTINATION share/${PROJECT_NAME})

ament_package()
