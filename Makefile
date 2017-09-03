all: pip testimport clean

install:
	@python setup.py install --record files.txt

uninstall:
	@cat files.txt | xargs rm -rf

pip:
	@pip install -r requirements.txt

testimport:
	@python -c 'import collect; from collect import __main__, config'

clean:
	@rm -rf build *.egg-info dist **/__pycache__
