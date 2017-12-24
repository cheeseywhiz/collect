"""Global package settings"""
import os

from . import _path

__all__ = ['DIRECTORY', 'REDDIT_URL', 'WINDOWS', 'VERSION']

VERSION = '1.4'
REDDIT_URL = 'r/earthporn/hot?limit=10'
WINDOWS = os.name == 'nt'

if WINDOWS:
    DIRECTORY = str(_path.Path.home() / 'Pictures/collect')
else:
    DIRECTORY = str(_path.Path.home() / '.cache/collect')
