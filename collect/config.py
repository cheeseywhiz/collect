"""Global package settings"""
import os

from . import path

__all__ = ['DIRECTORY', 'REDDIT_URL', 'WINDOWS']

VERSION = '1.3'
REDDIT_URL = 'r/earthporn/hot?limit=10'
WINDOWS = os.name == 'nt'

if WINDOWS:
    DIRECTORY = str(path.Path.home() / 'Pictures/collect')
else:
    DIRECTORY = str(path.Path.home() / '.cache/collect')
