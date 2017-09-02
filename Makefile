all: pip clean

install:
	@python setup.py install --record files.txt

uninstall:
	@cat files.txt | xargs rm -rf

pip:
	@pip install -r requirements.txt

clean:
	@rm -rf build *.egg-info dist **/__pycache__
