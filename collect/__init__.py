"""Automate downloading an image using the Reddit API."""
from ._collect import *
from ._collect import __all__ as _collect_all
from ._path import *
from ._path import __all__ as _path_all
from ._logger import Logger

__all__ = _collect_all + _path_all

Logger.name = __name__


def _doc_options():
    import enum
    gget = globals().get

    for name in __all__:
        obj = gget(name)
        if not isinstance(obj, enum.Enum):
            print('%s.%s+' % (__name__, name), end=' ')

    print()
