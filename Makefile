all: clean install

install:
	@python setup.py install --record files.txt

uninstall:
	@cat files.txt | xargs rm -rf

clean:
	@rm -rf build *.egg-info dist **/__pycache__ files.txt
