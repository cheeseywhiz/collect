"""Automate downloading an image from the Reddit json API."""
from . import collect
from .logger import Logger
from . import path

__all__ = ['collect', 'path']

Logger.name = __name__
