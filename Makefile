ifdef VIRTUALENV
	USER_FLAG=--user
else
	USER_FLAG=""
endif

all: testimport

install:
	python setup.py install $(USER_FLAG)

uninstall:
	@pip uninstall .

testimport:
	@python -c import\ collect

clean:
	@rm -rf build *.egg-info dist **/__pycache__
