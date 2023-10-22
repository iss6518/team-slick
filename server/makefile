include common.mk

API_DIR = server

all_tests: tests

tests: lint pytests

lint: FORCE
	$(LINTER) $(API_DIR)/*.py

pytests: FORCE
	cd $(API_DIR); make tests
