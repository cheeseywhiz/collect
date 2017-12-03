"""Automate downloading an image from the Reddit json API."""
from .collect import *
from .collect import __all__ as _collect_all
from .logger import Logger
from .path import *
from .path import __all__ as _path_all

__all__ = _collect_all + _path_all

Logger.name = __name__
