"""Automate downloading an image from the Reddit json API."""
from . import collect
from .logger import Logger
from . import path
from . import util

__all__ = ['collect', 'path', 'util']

Logger.name = __name__
