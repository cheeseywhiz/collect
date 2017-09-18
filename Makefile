ifdef VIRTUAL_ENV
	USER_FLAG=
	LN_CMD=
else
	USER_FLAG=--user
	LINK_EXE=ln -s $(HOME)/.local/bin/collect /usr/bin/collect
	RM_EXISTING_EXE=rm /usr/bin/collect
endif

all: testimport clean

install:
	@python setup.py install --record files.txt --force $(USER_FLAG)
	@$(RM_EXISTING_EXE)
	@$(LINK_EXE)

uninstall:
	@cat files.txt | xargs rm -rf

testimport:
	@python -c "import collect"

clean:
	@rm -rf build *.egg-info dist **/__pycache__
