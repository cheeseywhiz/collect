install:
	@python setup.py install

clean:
	@rm -rf build collect.egg-info dist **/__pycache__
