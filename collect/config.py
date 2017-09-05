"""Global package settings"""
import os
import pathlib

__all__ = ['DIRECTORY', 'REDDIT_URL', 'WINDOWS']

REDDIT_URL = 'https://www.reddit.com/r/earthporn/hot/.json?limit=10'
WINDOWS = os.name == 'nt'

if WINDOWS:
    DIRECTORY = str(pathlib.Path.home() / 'Pictures/collect')
else:
    DIRECTORY = str(pathlib.Path.home() / '.cache/collect')
