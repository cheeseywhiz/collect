"""Global package settings"""
import pathlib

__all__ = ['CACHE_ROOT', 'IMG_DIR', 'PICKLE_PATH', 'REDDIT_LINK']

REDDIT_LINK = 'https://www.reddit.com/r/earthporn/hot/.json?limit=10'

CACHE_ROOT = None
PICKLE_PATH = None
IMG_DIR = None


def set_cache_root(value):
    """Change the config state all at once."""
    global CACHE_ROOT, PICKLE_PATH, IMG_DIR
    cache_root_tmp = pathlib.Path(value)
    PICKLE_PATH = str(cache_root_tmp / 'collect.pkl')
    IMG_DIR = str(cache_root_tmp / 'img')
    CACHE_ROOT = str(cache_root_tmp)


set_cache_root(pathlib.Path.home() / '.cache/collect')
