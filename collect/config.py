"""Global package settings"""
import pathlib

__all__ = ['DIRECTORY', 'REDDIT_URL']

DIRECTORY = str(pathlib.Path.home() / '.cache/collect')
REDDIT_URL = 'https://www.reddit.com/r/earthporn/hot/.json?limit=10'
