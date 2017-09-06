"""Global package settings"""
import os

from . import path

__all__ = ['DIRECTORY', 'REDDIT_URL', 'WINDOWS']

REDDIT_URL = 'https://www.reddit.com/r/earthporn/hot/.json?limit=10'
WINDOWS = os.name == 'nt'

if WINDOWS:
    DIRECTORY = str(path.Path.home() / 'Pictures/collect')
else:
    DIRECTORY = str(path.Path.home() / '.cache/collect')
