import setuptools
from collect import config

setuptools.setup(
    name='collect',
    version=config.VERSION,
    packages=['collect'],
    install_requires=['python-magic', 'requests'],
)
