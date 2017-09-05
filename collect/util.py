"""Provides general utility functions"""
import functools
import inspect
import os
import random
import shlex
import shutil
import subprocess
import time

import requests

from . import logging
from . import config

__all__ = [
    'disown', 'extend_full_path', 'filter_dict', 'get', 'partial',
    'randomized', 'random_map', 'wait_for_connection']


# inspired by pywal.util.disown
def disown(cmd):
    """Call a system command in the background, disown it and hide it's
    output."""
    cmd = shlex.split(cmd)

    if shutil.which('nohup'):
        cmd.insert(0, 'nohup')

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        preexec_fn=getattr(os, 'setpgrp', None))
    proc.communicate()
    return proc


def extend_full_path(path):
    """Apply both os.path.abspath and os.path.expanduser to the path."""
    return os.path.abspath(os.path.expanduser(path))


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
def get(*args, **kwargs):
    pass


def randomized(iterable):
    """Shuffle the order of an iterable in place."""
    list_ = list(iterable)
    random.shuffle(list_)

    yield from list_


def random_map(func, *iterables):
    """Implement map() by sending in arguments in a random order"""
    return map(func, *zip(*randomized(zip(*iterables))))


def wait_for_connection(max_seconds=60, seconds_wait=5, ip_address='8.8.8.8'):
    count_flag = '-n' if config.WINDOWS else '-c'

    for n_try in range(max_seconds // seconds_wait):
        if disown(f'ping {count_flag} 1 -w 1 {ip_address}').wait():
            logging.warning('Connection not found')
            time.sleep(seconds_wait)
        elif n_try:
            logging.warning('Connection found')
            return True
        else:
            return True
    else:  # no break; really no internet connection
        return False
