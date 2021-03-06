import setuptools
from collect import config

setuptools.setup(
    name='collect',
    version=config.VERSION,
    packages=['collect'],
    install_requires=['requests', 'praw'],
    extras_require={
        'magic': ['python-magic'],
    },
)
