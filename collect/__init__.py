"""Automate downloading a picture from the Reddit json API."""
import logging

from . import cache
from . import collect
from . import util

__all__ = ['cache', 'collect', 'logging', 'util']

logging.basicConfig(format='%(name)s: %(levelname)s: %(message)s')
logging.root.name = __name__
