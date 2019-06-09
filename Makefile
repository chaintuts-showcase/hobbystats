# This file contains a make script for the HobbyStats application
#
# Author: Josh McIntyre
#

# This block defines makefile variables
SRC_FILES=src/core/*.py src/ui/*.py
LOG_FILES=logs

BUILD_DIR=bin/hobbystats

# This rule builds the application
build: $(SRC_FILES) $(LOG_FILES)
	mkdir -p $(BUILD_DIR)
	cp $(SRC_FILES) $(BUILD_DIR)
	cp -r $(LOG_FILES) $(BUILD_DIR)

# This rule cleans the build directory
clean: $(BUILD_DIR)
	rm -r $(BUILD_DIR)/*
	rmdir $(BUILD_DIR)
