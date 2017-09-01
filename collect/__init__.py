"""Automate downloading a picture from the Reddit json API."""
import logging
from .config import CACHE_PATH, REDDIT_LINK, SAVE_DIR
from . import util, cache, collect

logging.basicConfig(format='%(name)s: %(levelname)s: %(message)s')
logging.root.name = __name__

if 'confuse anaconda':
    CACHE_PATH, REDDIT_LINK, SAVE_DIR, util, cache, collect
