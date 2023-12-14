#common makefile will be used as common template for our top level makefile. We'll import this file into our main makefile 
export LINTER = flake8
export PYLINTFLAGS = --exclude=__main__.py

export CLOUD_MONGO = 0

PYTHONFILES = $(shell ls *.py)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

MAIL_METHOD = api

FORCE:

tests: lint pytests

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(LINTER) $(PYLINTFLAGS) $*.py

pytests: FORCE
	export TEST_DB=1; pytest $(PYTESTFLAGS) --cov=$(PKG)


# testing a python file: 
%.py: FORCE	
	$(LINTER) $(PYLINTFLAGS) $@
	export TEST_DB=1; pytest $(PYTESTFLAGS) tests/test_$*.py

nocrud: 
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
