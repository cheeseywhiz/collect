"""Provides functions for downloading images"""
import functools
from urllib.parse import urlparse
import sys

from . import util
from .logger import Logger
from . import path as _path

__all__ = ['Collect']


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
        """Save a picture to the path. Returns (url, destination_path) if
        successful or None otherwise."""
        url_parts = urlparse(url).path.split('/')

        if url_parts[-1]:
            file_name = url_parts[-1]
        else:
            # url path ends in literal /
            file_name = url_parts[-2]

        image_path = self / file_name

        if image_path.exists():
            Logger.debug('Already downloaded: %s', url)
            return None if no_repeat else (url, image_path)

        error_msg = None
        res = util.get(url)
        content_type = res.headers['content-type']

        if 'removed' in res.url:
            error_msg = 'Appears to be removed'
        if 'image' not in content_type:
            error_msg = 'Not an image'
        if 'gif' in content_type:
            error_msg = 'Is a .gif'

        if error_msg is not None:
            Logger.debug('%s: %s', error_msg, url)
            return None

        Logger.debug('Collected new image: %s', url)

        with image_path.open('wb') as file:
            file.write(res.content)

        return url, image_path

    def reddit(self, url, no_repeat=False):
        """Download a random image from a Reddit json url. Returns the
        destination path or raises RuntimeError if not successful."""
        download = functools.partial(self.download, no_repeat=no_repeat)
        urls = {
            post['data']['url']: post['data']
            for post in util.get(url).json()['data']['children']}

        try:
            url, image_path = next(filter(None, util.random_map(
                download, urls.keys()
            )))
        except StopIteration:
            Logger.error('Could not find new image')
            sys.exit(1)

        post = urls[url]
        Logger.info('Post: %s', post['permalink'])
        Logger.info('Title: %s', post['title'])
        Logger.info('Image: %s', url)
        Logger.info('File: %s', image_path)

        return image_path

    def empty(self):
        """Remove each file in this directory."""
        super().rmtree()
        super().mkdir()

    def random(self):
        try:
            return next(util.randomized(list(self)))
        except StopIteration:
            return None
