"""Provides general utility functions"""
import functools
import inspect
import os
import pathlib
import random
import subprocess
from urllib.parse import urlparse

import requests

from . import config
from . import logging

__all__ = [
    'disown', 'filter_dict', 'get', 'make_repr', 'partial', 'path_type',
    'ping', 'random_map', 'url_make_path']


# copy/paste from pywal.util with slight modification
def disown(*cmd):
    """Call a system command in the background, disown it and hide it's
    output."""
    return subprocess.Popen(
        ["nohup", *cmd],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp)


def filter_dict(__func, *args, **kwargs):
    """Filter adaptation for dicts. __func is the filter function a la filter()
    and args and kwargs are passed to dict(). if __func is None than it filters
    based on the bool value of the value of each item."""
    if __func is None:
        __func = (lambda key, value: bool(value))

    return {
        key: value
        for key, value in dict(*args, **kwargs).items()
        if __func(key, value)}


def make_repr(cls, *args, **kwargs):
    """Format a repr from args and kwargs and a class instance."""
    name = '.'.join((cls.__module__, cls.__name__))
    parts = list(map(repr, args))
    parts.extend(f'{name}={value !r}' for name, value in kwargs.items())

    return f"{name}({', '.join(parts)})"


_no_doc_module = list(functools.WRAPPER_ASSIGNMENTS)
_removed = ['__doc__', '__module__']

for name in _removed:
    _no_doc_module.remove(name)


@functools.wraps(functools.partial, assigned=_no_doc_module)
def partial(func, *args, **kwargs):
    """functools.partial as a decorator for top level functions. Able to wrap
    itself with 0-2 yield statements where the second yields a function that
    takes the result as an argument."""
    partial_func = functools.partial(func, *args, **kwargs)
    func_sig = inspect.signature(partial_func)

    def decorator(wrapped):
        @functools.wraps(wrapped, assigned=('__module__', '__qualname__'))
        @functools.wraps(func)
        def wrapper(*wargs, **wkwargs):
            return partial_func(*wargs, **wkwargs)

        wrapper.__signature__ = func_sig

        if wrapped.__doc__:
            wrapper.__doc__ = wrapped.__doc__

        return wrapper

    return decorator


@partial(requests.get, headers={'User-Agent': 'u/cheeseywhiz'})
def _get(*args, **kwargs):
    pass


@functools.wraps(_get)
def get(*args, **kwargs):
    result = _get(*args, **kwargs)
    logging.debug('Reason: %s', result.reason)
    return result


def path_type(path):
    """Apply both os.path.abspath and os.path.expanduser to the path."""
    return os.path.abspath(os.path.expanduser(path))


def ping(ip_address='8.8.8.8'):
    """Test internet connection."""
    return not disown('ping', '-c 1', '-w 1', ip_address).wait()


def random_map(func, *iterables):
    """Implement map() by sending in arguments in a random order"""
    args = list(zip(*iterables))
    random.shuffle(args)
    return map(func, *zip(*args))


def url_make_path(url):
    """Return pathlib.Path object for a new downloaded file in the
    directory."""
    return pathlib.Path(config.IMG_DIR) / urlparse(url).path.split('/')[-1]
