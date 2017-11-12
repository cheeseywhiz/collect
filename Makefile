ifdef VIRTUAL_ENV
	USER_FLAG=
	BIN_DIR=$(VIRTUAL_ENV)/bin
	EXE_FILE=$(BIN_DIR)/collect
else
	USER_FLAG=--user
	BIN_DIR=/usr/bin
	EXE_FILE=$(BIN_DIR)/collect
endif


all: chkdep clean
	python setup.py install --record files.txt --force $(USER_FLAG)

install:
	mkdir -p $(BIN_DIR)
	install collect.sh $(EXE_FILE)
	@echo $(EXE_FILE) >> files.txt

uninstall:
	@cat files.txt | xargs rm -rf

chkdep:
	python -c "import requests, magic"

clean:
	rm -rf build *.egg-info dist **/__pycache__
