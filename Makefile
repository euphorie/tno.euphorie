PYTHON		?= python2.7
TWINE_REPOSITORY ?= pypi

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

.PHONY: release
release:
	@echo "Releasing to repository: $(TWINE_REPOSITORY)"
	@echo "To release to a different repository, run \`make release TWINE_REPOSITORY=<repository>\`"
	TWINE_REPOSITORY="$(TWINE_REPOSITORY)" uvx \
		--from zest-releaser \
		--with zest-releaser\[recommended\] \
		--with zestreleaser-towncrier \
		fullrelease
