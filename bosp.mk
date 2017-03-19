
ifdef CONFIG_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP

# Targets provided by this project
.PHONY: rtlib_python_bindings_testapp clean_rtlib_python_bindings_testapp

# Add this to the "contrib_testing" target
testing: rtlib_python_bindings_testapp
clean_testing: clean_rtlib_python_bindings_testapp

MODULE_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP=contrib/testing/rtlib-python-bindings-testapp

rtlib_python_bindings_testapp: external
	@echo
	@echo "==== Building RTLib Python Bindings Test Application ===="
	@echo " Sysroot      : $(PLATFORM_SYSROOT)"
	@echo " BOSP Options : $(CMAKE_COMMON_OPTIONS)"
	@[ -d $(MODULE_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP)/build/$(BUILD_TYPE) ] || \
		mkdir -p $(MODULE_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP)/build/$(BUILD_TYPE) || \
		exit 1
	@cd $(MODULE_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP)/build/$(BUILD_TYPE) && \
		cmake $(CMAKE_COMMON_OPTIONS) ../.. || \
		exit 1
	@cd $(MODULE_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP)/build/$(BUILD_TYPE) && \
		make -j$(CPUS) install || \
		exit 1

clean_rtlib_python_bindings_testapp:
	@echo
	@echo "==== Clean-up RTLib Python Bindings Test Application ===="
	@[ ! -f $(BUILD_DIR)/usr/bin/bbque-python-bindings-testapp ] || \
		rm -f $(BUILD_DIR)/etc/bbque/recipes/BbqRTLibPythonBindingsTestApp*; \
		rm -f $(BUILD_DIR)/usr/bin/bbque-python-bindings-testapp*
	@rm -rf $(MODULE_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP)/build
	@echo

else # CONFIG_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP

rtlib_python_bindings_testapp:
	$(warning contib TestApp module disabled by BOSP configuration)
	$(error BOSP compilation failed)

endif # CONFIG_CONTRIB_TESTING_PYTHON_BINDINGS_TESTAPP
