"""Provides objects for caching"""
import collections
import contextlib
import functools
import pickle

from . import logging
from . import util

__all__ = ['cache', 'Cache', 'CacheFunc', 'DownloadResult', 'PickleIO']

DownloadResult = collections.namedtuple('DownloadResult', (
    'url', 'invalid', 'message', 'path'))


class PickleIO:
    """Given a path, read or write the pickle of an object at that path."""

    def __init__(self, *args, path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    def read(self):
        """Parse the pickle at the given path."""
        try:
            file = open(self.path, 'rb')
        except FileNotFoundError:
            return {}

        with file:
            try:
                return pickle.load(file)
            except EOFError:
                return {}

    def write(self, object):
        """Write the pickle an object at the given path."""
        with open(self.path, 'wb') as file:
            return pickle.dump(object, file, pickle.HIGHEST_PROTOCOL)

    def re_init_cache(self):
        """Reinitialize the cache file."""
        logging.debug('Clearing cache at %s', self.path)

        for cmd in 'rm', 'touch':
            util.disown(cmd, self.path)

        return self

    def __repr__(self):
        return util.make_repr(self.__class__, path=self.path)


class CacheFunc:
    """functools.lru_cache(max_size=None, typed=False) implementation with an
    accessible cache attribute."""

    def __init__(self, *args, func=None, cache=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.func = func
        self.cache = {}

        if cache is not None:
            self.cache.update(cache)

    def __call__(self, *args, **kwargs):
        key = self.key(*args, **kwargs)

        try:
            result = self.cache[key]
        except KeyError:
            result = self.cache[key] = self.func(*args, **kwargs)

        return result

    def key(self, *args, **kwargs):
        """Return a hashable representation of the given args and kwargs."""
        return functools._make_key(args, kwargs, False)

    def remove(self, *args, **kwargs):
        """Remove the given function call from the cache."""
        key = self.key(*args, **kwargs)
        return self.cache.pop(key)

    def __repr__(self):
        kwargs = util.filter_dict(
            lambda k, v: v is not None,
            func=self.func, cache=self.cache)
        return util.make_repr(self.__class__, self.func, **kwargs)


class Cache(PickleIO, CacheFunc):
    """Class with PickleIO and CacheFunc mixed in. Instantiate by reading from
    a filepath or a preexisting function cache."""

    def __init__(self, func=None, *, path=None, cache=None):
        super().__init__(func=func)
        self.load_cache(path=path, cache=cache)

    def load_cache(self, func=None, *, path=None, cache=None):
        """Reinitialize essentially the entire object"""
        if func is None:
            func = self.func

        super().__init__(func=func, path=path)
        self._loaded = False
        self._cache = {}
        self._path_arg = path is not None
        self._cache_arg = cache is not None

        if self._cache_arg:
            self._loaded = True
            self._cache.update(cache)

        return self

    @property
    def cache(self):
        """Getter to delay pickle read until the first get of self.cache."""
        # using self.cache to invoke loading and self._cache otherwise
        if not self._loaded and self._path_arg:
            self._loaded = True
            self._cache.update(
                (functools._HashedSeq(key), value)
                for key, value in self.read())

        return self._cache

    @cache.setter
    def cache(self, value):
        self._loaded = True
        self._cache = value

    @contextlib.contextmanager
    def saving(self):
        """Context manager: save the cache at the end of the scope."""
        try:
            yield self
        finally:
            self.save()

    def save(self):
        """Save the cache to the specified file."""
        return super().write([
            (tuple(key), value)
            for key, value in self.cache.items()])

    def re_init_cache(self):
        """Reinit the file and currently loaded cache."""
        super().re_init_cache()
        self._cache = {}
        return self

    def __repr__(self):
        kwargs = util.filter_dict(
            lambda k, v: v is not None,
            path=self.path, cache=self._cache)
        return util.make_repr(self.__class__, self.func, **kwargs)


def cache(*, path=None, load=None):
    """Reimplementation of functools.lru_cache(maxsize=None, typed=False) that
    has an accessible cache"""
    def decorator(wrapped):
        return Cache(wrapped, path=path, cache=load)

    return decorator
