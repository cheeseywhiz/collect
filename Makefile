all: testimport

install:
	ifdef VIRTUALENV
		@python setup.py install
	else
		@python setup.py install --user
	endif

uninstall:
	@pip uninstall .

testimport:
	@python -c import\ collect

clean:
	@rm -rf build *.egg-info dist **/__pycache__
