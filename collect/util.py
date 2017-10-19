"""Provides general utility functions"""
import random
import shlex
import subprocess
import time

from .logger import Logger
from . import config

__all__ = [
    'disown', 'randomized', 'random_map', 'wait_for_connection']


# inspired by pywal.util.disown
def disown(cmd: str):
    """Hide a command's output."""
    process = subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    return process


def randomized(list_):
    """Shuffle the order of a sequence in place."""
    yield from random.choices(list_, k=len(list_))


def random_map(func, *iterables):
    """Implement map() by sending in arguments in a random order"""
    return map(func, *zip(*randomized(list(zip(*iterables)))))


def wait_for_connection(max_seconds=60, seconds_wait=5, ip_address='8.8.8.8'):
    """Execute a test ping repeatedly, if necessary, returning whether or not
    it succeeded."""
    count_flag = '-n' if config.WINDOWS else '-c'

    for n_try in range(max_seconds // seconds_wait):
        if disown(f'ping {count_flag} 1 -w 1 {ip_address}').wait():
            Logger.warning('Connection not found')
            time.sleep(seconds_wait)
        elif n_try:
            Logger.warning('Connection found')
            return True
        else:
            return True
    else:  # no break; really no internet connection
        return False
