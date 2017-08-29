"""Provides objects for caching"""
import collections
import contextlib
import functools
import pickle

from . import util

_new_named_tuple_repr = """\
    def __repr__(self):
        module = self.__class__.__module__
        return f'<{{module}}.{typename} object at {{hex(id(self))}}>'
"""
collections._class_template = collections._class_template.replace(
    '    def __repr__(self):', _new_named_tuple_repr)
DownloadResult = collections.namedtuple('DownloadResult', (
    'url', 'time', 'succeeded', 'status', 'fname', 'content'))


def make_repr(cls, *args, **kwargs):
    """Format a repr from args and kwargs and a class instance."""
    name = '.'.join((cls.__module__, cls.__name__))
    parts = list(map(repr, args))
    parts.extend(f'{name}={value !r}' for name, value in kwargs.items())

    return f"{name}({', '.join(parts)})"


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
        for cmd in 'rm', 'touch':
            util.disown(cmd, self.path)

    def __repr__(self):
        return make_repr(self.__class__, path=self.path)


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
        key = functools._make_key(args, kwargs, False)

        try:
            result = self.cache[key]
        except KeyError:
            result = self.cache[key] = self.func(*args, **kwargs)
        finally:
            return result

    def __repr__(self):
        kwargs = util.filter_dict(
            lambda n, v: v is not None,
            func=self.func, cache=self.cache)
        return make_repr(self.__class__, self.func, **kwargs)


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
            self._cache.update(self.read())

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
        """Save the cache to the specified file"""
        return super().write(self.cache)

    def re_init_cache(self):
        """Reinit the file and currently loaded cache."""
        super().re_init_cache()
        self._cache = {}

    def __repr__(self):
        kwargs = util.filter_dict(
            lambda k, v: v is not None,
            path=self.path, cache=self._cache)
        return make_repr(self.__class__, self.func, **kwargs)


def cache(*, path=None, load=None):
    """Reimplementation of functools.lru_cache(maxsize=None, typed=False) that
    has an accessible cache"""
    def decorator(wrapped):
        return Cache(wrapped, path=path, cache=load)

    return decorator
