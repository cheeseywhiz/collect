"""Global package settings"""
import pathlib

REDDIT_LINK = 'https://www.reddit.com/r/earthporn/hot/.json?limit=10'
CACHE_ROOT = pathlib.Path.home() / '.cache/collect'
CACHE_PATH = str(CACHE_ROOT / 'pickle')
SAVE_DIR = '/tmp/wal'
