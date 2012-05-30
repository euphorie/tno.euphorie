PYTHON		?= python2.7

all: 

clean:

bin/buildout: bootstrap.py
	$(PYTHON) bootstrap.py

bin/test: bin/buildout buildout.cfg devel.cfg setup.py
	bin/buildout -c devel.cfg
	touch bin/test

check:: bin/test
	bin/test

jenkins: bin/test
	bin/test --xml -s tno.euphorie

.PHONY: all clean jenkins
