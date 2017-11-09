ifdef VIRTUAL_ENV
	USER_FLAG=
	RM_EXISTING_EXE=
	LINK_EXE=
else
	USER_FLAG=--user
	RM_EXISTING_EXE=rm -f /usr/bin/collect
	LINK_EXE=ln -s $(HOME)/.local/bin/collect /usr/bin/collect
endif

all: clean

install:
	@python setup.py install --record files.txt --force $(USER_FLAG)
	@$(RM_EXISTING_EXE)
	@$(LINK_EXE)

uninstall:
	@cat files.txt | xargs rm -rf

clean:
	@rm -rf build *.egg-info dist **/__pycache__
