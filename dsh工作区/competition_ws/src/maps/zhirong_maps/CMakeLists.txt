cmake_minimum_required(VERSION 3.8)
project(zhirong_maps)

find_package(ament_cmake REQUIRED)

# 纯资源包：worlds / models / launch / maps / docs 全部安装到 share/zhirong_maps
# 说明：models 目录内的 model.config + model.sdf 通过 GAZEBO_MODEL_PATH 被
#       <include><uri>model://...</uri></include> 解析；launch 会设置该环境变量。
install(DIRECTORY worlds models launch maps docs
        DESTINATION share/${PROJECT_NAME})
install(FILES README.md package.xml
        DESTINATION share/${PROJECT_NAME})

ament_package()
