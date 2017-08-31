"""python setup.py install"""
import setuptools

setuptools.setup(
    name='collect',
    version='1.0',
    packages=['collect'],
    install_requires=['requests'],
    entry_points={
        "console_scripts": ["collect=collect.__main__:main"]
    },)
