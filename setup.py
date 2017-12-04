import setuptools
from collect import _config

setuptools.setup(
    name='collect',
    version=_config.VERSION,
    packages=['collect'],
    install_requires=['requests', 'praw'],
    extras_require={
        'magic': ['python-magic'],
    },
)
