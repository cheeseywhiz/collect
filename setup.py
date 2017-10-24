import setuptools
from collect import config

setuptools.setup(
    name='collect',
    version=config.VERSION,
    packages=['collect'],
    install_requires=['python-magic', 'requests'],
    entry_points={
        "console_scripts": ["collect=collect.__main__:main"]
    },)
