###############################################################################
# The Barbeque RTLib Python Bindings Test Application
################################################################################

# The name of this project.
project (RTLibPythonBindingsTestApp)

################################################################################
# Installation items
################################################################################

set (RTLIB_PYTHON_BINDINGS_TESTAPP_PATH_BINS    "usr/bin")
set (RTLIB_PYTHON_BINDINGS_TESTAPP_PATH_RECIPES "etc/bbque/recipes")

################################################################################
# Installation locations
################################################################################

# set default install prefix to project root directory
if (CMAKE_INSTALL_PREFIX STREQUAL "/usr/local")
	set (CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/out" )
endif (CMAKE_INSTALL_PREFIX STREQUAL "/usr/local")

################################################################################
# Subdirectories analysis
################################################################################

# Recurse into project subfolders
install(DIRECTORY "${PROJECT_SOURCE_DIR}/recipes/"
    DESTINATION "${RTLIB_PYTHON_BINDINGS_TESTAPP_PATH_RECIPES}"
    FILES_MATCHING PATTERN "*.recipe")
install(FILES "${PROJECT_SOURCE_DIR}/bbque-python-bindings-testapp.py"
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ
    DESTINATION "${RTLIB_PYTHON_BINDINGS_TESTAPP_PATH_BINS}")

################################################################################
# Configuration resume
################################################################################

# display status message for important variables
message ( STATUS )
message ( STATUS "=====[ Barbeque RTLib TestApp - Building System Configuration ]"
                 "=================" )
message ( STATUS "Installation prefix... ${CMAKE_INSTALL_PREFIX}" )
message ( STATUS "   Binary............. <prefix>/${RTLIB_PYTHON_BINDINGS_TESTAPP_PATH_BINS}" )
message ( STATUS "   Recipes............ <prefix>/${RTLIB_PYTHON_BINDINGS_TESTAPP_PATH_RECIPES}" )
message ( STATUS )
message ( STATUS "Default values could be changes at command line, with:")
message ( STATUS "  cmake -D<Variable>=<Value>" )
message ( STATUS "or use the '-i' cmake flag to run in interactive mode" )
message ( STATUS "======================================================"
                 "==========================" )
message(STATUS)
