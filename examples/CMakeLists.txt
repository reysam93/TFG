project (AUTOMATA)

cmake_minimum_required(VERSION 2.8)
include(FindPkgConfig)

SET( SOURCE_FILES_AUTOMATA 
	example1.cpp
	../visualHFSM/automatagui.cpp
	../visualHFSM/point.cpp
	../visualHFSM/node.cpp
	../visualHFSM/transition.cpp
	../visualHFSM/subautomata.cpp
	../visualHFSM/guinode.cpp
	../visualHFSM/guitransition.cpp
	../visualHFSM/guisubautomata.cpp
	../visualHFSM/popups/editnodedialog.cpp
	../visualHFSM/popups/edittransitiondialog.cpp
	../visualHFSM/popups/edittransitioncodedialog.cpp
	../visualHFSM/popups/renamedialog.cpp
	../visualHFSM/popups/renametransitiondialog.cpp
)

pkg_check_modules(GTKMM REQUIRED gtkmm-3.0)

SET( INTERFACES_CPP_DIR /usr/local/include )
SET( LIBS_DIR /usr/local/lib )

SET( CMAKE_CXX_FLAGS "-pthread" ) # Opciones para el compilador

SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_CURRENT_SOURCE_DIR})

SET(goocanvasmm_INCLUDE_DIRS
	/usr/include/goocanvasmm-2.0
	/usr/lib/goocanvasmm-2.0/include
	/usr/include/goocanvas-2.0
)

include_directories (
	/usr/local/include/jderobot
	${INTERFACES_CPP_DIR}
	${LIBS_DIR}
	${CMAKE_CURRENT_SOURCE_DIR}
	${GTKMM_INCLUDE_DIRS}
	${goocanvasmm_INCLUDE_DIRS}
)

link_directories(${GTKMM_LIBRARY_DIRS})

add_executable (automata ${SOURCE_FILES_AUTOMATA})

SET(goocanvasmm_LIBRARIES goocanvasmm-2.0 goocanvas-2.0)

TARGET_LINK_LIBRARIES ( automata 
	${GTKMM_LIBRARIES}
	${goocanvasmm_LIBRARIES}
	${LIBS_DIR}/jderobot/libJderobotInterfaces.so
	${LIBS_DIR}/jderobot/libjderobotutil.so
	Ice
	IceUtil
)
