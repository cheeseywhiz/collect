"""Automate downloading an image from the Reddit json API."""
import logging

from . import collect
from . import util

__all__ = ['collect', 'logging', 'util']

logging.basicConfig(format='%(name)s: %(levelname)s: %(message)s')
logging.root.name = __name__
