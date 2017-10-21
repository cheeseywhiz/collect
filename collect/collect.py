"""Provides functions for downloading images"""
import functools
from urllib.parse import urlparse

import requests

from . import util
from .logger import Logger
from . import path as _path

__all__ = ['Collect']
_get = functools.partial(requests.get, headers={'User-Agent': 'collect/1.0'})


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
                 f'path. Path: {self}'))

    def download(self, url, no_repeat=False):
        """Save a picture to the path. Returns Path object of new image if
        successful or None otherwise."""
        url_parts = urlparse(url).path.split('/')

        if not url_parts[-1]:
            # url path ends in literal /
            url_parts.pop()

        image_path = self / url_parts[-1]

        if image_path.exists():
            Logger.debug('Already downloaded: %s', url)
            return None if no_repeat else image_path

        error_msg = None
        res = _get(url)
        content_type = res.headers['content-type']

        if 'removed' in res.url:
            error_msg = 'Appears to be removed'
        if 'image' not in content_type:
            error_msg = f'Not an image ({content_type})'
        if 'gif' in content_type:
            error_msg = 'Is a .gif'

        if error_msg is not None:
            Logger.debug('%s: %s', error_msg, url)
            return None

        Logger.debug('Collected new image: %s', url)

        with image_path.open('wb') as file:
            file.write(res.content)

        return image_path

    def reddit(self, url, no_repeat=False):
        """Download a random image from a Reddit json url. Returns Path object
        of new image if successful or None otherwise."""
        for post in util.randomized(_get(url).json()['data']['children']):
            data = post['data']
            url = data['url']
            image_path = self.download(url, no_repeat)

            if image_path is not None:
                Logger.info('Post: %s', data['permalink'])
                Logger.info('Title: %s', data['title'])
                Logger.info('Image: %s', url)
                Logger.info('File: %s', image_path)
                return image_path

    def empty(self):
        """Remove each file in this directory."""
        if _path.Path.cwd() == self.abspath():
            for file in self:
                file.remove()
        else:
            super().rmtree()
            super().mkdir()

    def random(self):
        try:
            return next(util.randomized(list(self)))
        except StopIteration:
            return None
