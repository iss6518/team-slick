#common makefile will be used as common template for our top level makefile. We'll import this file into our main makefile 
export LINTER = flake8
export PYLINFLAGS = --exclude=__main__.py

PYTHONFILES = $(shell ls *.py)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

MAIL_METHOD = api

FORCE:

tests : lint pytests

%.pylint:
	$(PYLINT) $(PYLINFLAGS) $*.py

pytests: FORCE
	export TEST_DB = 1; pytest $(PYTESTFLAGS) --cov=$(PKG)


# testing a python file: 
%.py: FORCE	
	$(PYLINT) $(PYLINFLAGS) $@
	export TEST_DB=1; pytest $(PYTESTFLAGS) tests/test_$*.py

nocrud: 
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~