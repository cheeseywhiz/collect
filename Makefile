PWD:=$(realpath $(dir $(lastword $(MAKEFILE_LIST))))

INSTALL_FLAGS=

ifdef VIRTUAL_ENV
	PRE:=$(VIRTUAL_ENV)
else
	INSTALL_FLAGS+=--user
	PRE:=/usr
endif

BIN=$(PRE)/bin

all: setup docs

setup: $(PWD)/setup.py
	python $< install $(INSTALL_FLAGS)

$(PRE)/%:
	mkdir -p $@

$(BIN)/collect: $(PWD)/collect.sh $(BIN)
	install $< $@

install: $(BIN)/collect

uninstall:
	rm -rf $(BIN)/collect
	pip uninstall --yes collect

clean:
	rm -rf build *.egg-info dist **/__pycache__

%.md: $(PWD)/doc.py
	python $< collect > $@

docs: $(PWD)/DOC.md

cleandocs:
	rm -f $(PWD)/DOC.md

.PHONY: all setup install uninstall clean docs cleandocs
