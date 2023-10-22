include common.mk

DB_DIR = db

all_tests: tests

tests: lint pytests

lint: FORCE	
	$(LINTER) $(DB_DIR)/*.py

pytests: FORCE	
	cd $(DB_DIR); make tests
