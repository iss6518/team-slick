include common.mk 
API_DIR = server
DB_DIR = db
REQ_DIR = .

PKG = $(API_DIR)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin master

all_tests: lint unit

unit: FORCE
	cd $(API_DIR); pytest $(PYTESTFLAGS) --cov=$(PKG)

lint: FORCE
	$(LINTER) $(API_DIR)/*.py
	$(LINTER) $(DB_DIR)/*.py

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

docs: FORCE
	cd $(API_DIR); make docs
