"""Provides functions for downloading images"""
import enum
import functools
import random
from urllib.parse import urlparse

import requests

from . import config
from .logger import Logger
from . import path as _path

__all__ = ['Collect', 'Failsafe']
_get = functools.partial(requests.get, headers={
    'User-Agent': 'collect/%s' % config.VERSION
})


def randomized(list_):
    """Yield values of a sequence in random order."""
    yield from random.sample(list_, len(list_))


class Failsafe(enum.Enum):
    """Specify location for a new random path if Reddit collection fails.
    FAIL: do nothing
    ALL: from specified directory
    NEW: from specified URL"""
    FAIL = 0b00
    ALL = 0b01
    NEW = 0b10


class Collect(_path.Path):
    """Perform image collection operations on a path."""
    def __new__(cls, path=None):
        self = super(_path.Path, cls).__new__(cls, path=path)
        super(_path.Path, self).__init__(path=path)
        return self

    def __init__(self, path=None):
        if super().exists() and not super().is_dir():
            raise NotADirectoryError(
                ('Attempted to instantiate Collect without a directory '
                 'path (%s)' % self))

    def download(self, url, no_repeat=False):
        """Save a picture to the path. Returns Path object of new image. Can
        raise FileExistsError if no_repeat is False. Raises ValueError if
        something isn't right about the HTTP response."""
        url_parts = urlparse(url).path.split('/')

        if not url_parts[-1]:
            # url path ends in literal /
            url_parts.pop()

        image_path = self / url_parts[-1]

        if image_path.exists():
            if no_repeat:
                raise FileExistsError('Already downloaded: %s' % url)
            else:
                return image_path

        error_msg = None
        res = _get(url)
        content_type = res.headers['content-type']

        if 'removed' in res.url:
            error_msg = 'Appears to be removed'
        if 'image' not in content_type:
            error_msg = 'Not an image (%s)' % content_type
        if 'gif' in content_type:
            error_msg = 'Is a .gif'

        if error_msg is not None:
            raise ValueError('%s: %s' % (error_msg, url))

        Logger.debug('Collected new image: %s', url)

        with open(image_path, 'wb') as file:
            file.write(res.content)

        return image_path

    def reddit(self, url, no_repeat=False, failsafe=Failsafe.FAIL):
        """Download a random image from a Reddit json url. Returns Path object
        of new image. Raises RuntimeError if it failed with no failsafe.
        Inherits FileNotFoundError behavior from self.random."""
        failsafe = Failsafe(failsafe)
        existing_paths = []

        for post in randomized(_get(url).json()['data']['children']):
            data = post['data']
            url = data['url']

            try:
                image_path = self.download(url, no_repeat)
            except FileExistsError as error:
                existing_paths.append(self.download(url))
                Logger.debug(str(error))
            except ValueError as error:
                Logger.debug(str(error))
            else:
                Logger.info('Title: %s', data['title'])
                Logger.info('Post: %s', data['permalink'])
                break
        else:
            if failsafe is Failsafe.FAIL:
                raise RuntimeError('Collection failed: %s to %s' % (url, self))
            else:
                Logger.debug(
                    'Falling back on image from %s', failsafe.name.lower())

            try:
                if failsafe is Failsafe.ALL:
                    image_path = self.random()
                elif failsafe is Failsafe.NEW:
                    image_path = next(randomized(existing_paths))
            except StopIteration:
                pass

        Logger.info('URL: %s', url)
        Logger.info('File: %s', image_path)
        return image_path

    def random(self):
        """Return a random file within this directory. Raises FileNotFoundError
        if no suitable file was found."""
        for path in randomized(list(self)):
            if path.is_file():
                Logger.info('File: %s', path)
                return path
        else:
            raise FileNotFoundError('No suitable files: %s' % self)
