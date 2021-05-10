# https://stackoverflow.com/questions/13703647/how-to-properly-add-include-directories-with-cmake
# https://cmake.org/cmake/help/latest/guide/tutorial/index.html

# Minimum version of CMake
cmake_minimum_required(VERSION 3.12) # version can be different

# Project name
project(MoveZeros) #name of your project

#
# Main App
#

# Add executable
#add_library(mainAppLibrary
#            )
set(mainAppSOURCES
    src/main.cpp
    ) 
add_executable(mainApp ${mainAppSOURCES})  