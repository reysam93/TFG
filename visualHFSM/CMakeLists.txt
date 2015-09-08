cmake_minimum_required(VERSION 2.6)
project(automatagui)

INCLUDE(FindPkgConfig)

set(SOURCES 	msmain.cpp 
		automatagui.cpp 
		automatagui.h)

#dependencies
pkg_check_modules(GTKMM REQUIRED gtkmm-3.0)
include_directories(${GTKMM_INCLUDE_DIRS})
link_directories(${GTKMM_LIBRARY_DIRS})

add_executable(../automatagui ${SOURCES})

target_link_libraries(../automatagui ${GTKMM_LIBRARIES})
