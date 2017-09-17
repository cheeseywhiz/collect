ifdef VIRTUAL_ENV
	USER_FLAG=
else
	USER_FLAG=--user
endif

all: testimport clean

install:
	@python setup.py install --record files.txt $(USER_FLAG)

uninstall:
	@cat files.txt | xargs rm -rf

testimport:
	@python -c "import collect"

clean:
	@rm -rf build *.egg-info dist **/__pycache__
