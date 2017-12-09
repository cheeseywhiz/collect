"""Automate downloading an image using the Reddit API."""
from ._collect import *
from ._collect import __all__ as _collect_all
from ._path import *
from ._path import __all__ as _path_all
from ._logger import Logger

__all__ = _collect_all + _path_all

Logger.name = __name__
