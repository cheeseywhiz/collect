"""Provides functions for downloading images"""
import functools
import random

import requests

from . import config
from .logger import Logger
from . import path as _path
from .flags import *
from .flags import __all__ as _flags_all

__all__ = ['Collect']
__all__.extend(_flags_all)

_get = functools.partial(requests.get, headers={
    'User-Agent': 'collect/%s' % config.VERSION
})


def _randomized(list_):
    """Yield values of a sequence in random order."""
    yield from random.sample(list_, len(list_))


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
                 'path (%s)') % self)

    @_path.Path.CastCls
    def url_fname(self, url):
        return super().url_fname(url)

    def download(self, url):
        """Save a picture to this path. Raises ValueError if the HTTP response
        indicates that we did not receive an image."""
        error_msg = None
        res = _get(url)
        content_type = res.headers['content-type']

        if 'removed' in res.url:
            error_msg = 'Appears to be removed (%s)' % res.url
        if 'image' not in content_type:
            error_msg = 'Not an image (%s)' % content_type
        if 'gif' in content_type:
            error_msg = 'Is a .gif (%s)' % content_type

        if error_msg is not None:
            raise ValueError('%s: %s' % (error_msg, url))

        with open(self, 'wb') as file:
            file.write(res.content)

        return self

    def reddit(self, json_url, flags=FAIL):
        """Download a random image from a Reddit json url. Returns Path object
        of new image. Raises RuntimeError if it failed with no failsafe.
        Inherits FileNotFoundError behavior from self.random."""
        data = None
        image_url = None
        image_path = None

        existing_paths = {}

        for post in _randomized(_get(json_url).json()['data']['children']):
            data = post['data']
            image_url = data['url']
            image_path = self.url_fname(image_url)

            if self == image_path:
                pass
            elif image_path.exists():
                Logger.debug('Already downloaded: %s' % image_url)
                existing_paths[image_path] = data
                if not flags & NO_REPEAT:
                    break
            else:
                try:
                    image_path.download(image_url)
                except ValueError as error:
                    Logger.debug(str(error))
                else:
                    Logger.debug('Collected new image: %s', image_url)
                    break

            data = None
            image_url = None
            image_path = None
        else:
            failed = False

            if flags & ALL:
                Logger.debug('Falling back on image from all')
                image_path = self.random()
                data = existing_paths.get(image_path)
            elif flags & NEW:
                Logger.debug('Falling back on image from new')
                try:
                    image_path, data = next(
                        _randomized(existing_paths.items())
                    )
                except StopIteration:
                    failed = True
            else:
                failed = True

            if failed:
                raise RuntimeError(
                    'Collection failed: %s' % json_url)

        if data is not None:
            Logger.info('Title: %s', data['title'])
            Logger.info('Post: %s', data['permalink'])
            Logger.info('URL: %s', data['url'])

        Logger.info('File: %s', image_path)
        return image_path

    def random(self):
        """Return a random file within this directory. Raises FileNotFoundError
        if no suitable file was found."""
        for path in _randomized(list(self)):
            if path.is_file():
                return path
        else:
            raise FileNotFoundError('No suitable files: %s' % self)
