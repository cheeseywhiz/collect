"""Provides general utility functions"""
import random
import subprocess
import time

from .logger import Logger
from . import config

__all__ = ['randomized', 'wait_for_connection']


def randomized(list_):
    """Yield values of a sequence in random order."""
    yield from random.choices(list_, k=len(list_))


def wait_for_connection(n_tries=10, seconds_wait=5, ip_address='8.8.8.8'):
    """Return whether or not a test ping was successful."""
    count_flag = '-n' if config.WINDOWS else '-c'

    for n_try in range(n_tries):
        ping = subprocess.Popen(
            ['ping', count_flag, str(1), '-w', str(1), ip_address],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        ping.communicate()
        if ping.wait():
            Logger.warning('Connection not found')
            time.sleep(seconds_wait)
        elif n_try:
            Logger.warning('Connection found')
            return True
        else:
            return True
    else:  # no break; really no internet connection
        return False
