"""Provides functions for downloading images"""
from urllib.parse import urlparse

from . import util
from . import logging
from . import path

__all__ = ['Collect']


class Collect(path.Path):
    """Perform image collection operations on a path."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if super().exists() and not super().is_dir():
            raise NotADirectoryError(
                ('Attempted to instantiate Collect without a directory '
                 f'path. Path: {self}'))

    def download(self, url):
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
            logging.debug('Already downloaded')
            return url, image_path

        error_msg = None
        req = util.get(url)
        content_type = req.headers['content-type']

        if 'removed' in req.url:
            error_msg = 'Appears to be removed'
        if not content_type.startswith('image'):
            error_msg = 'Not an image'
        if content_type.endswith('gif'):
            error_msg = 'Is a .gif'

        if error_msg is not None:
            logging.debug('%s: %s', error_msg, url)
            return None

        logging.debug('Collected new image.')

        with image_path.open('wb') as file:
            file.write(req.content)

        return url, image_path

    def reddit(self, url):
        """Download a random image from a Reddit json url. Returns the
        destination path or raises RuntimeError if not successful."""
        urls = {
            post['data']['url']: post['data']
            for post in util.get(url).json()['data']['children']}

        try:
            url, image_path = next(filter(None, util.random_map(
                self.download, urls.keys()
            )))
        except StopIteration:
            raise RuntimeError('Could not find image')

        post = urls[url]
        logging.info('Post: %s', post['permalink'])
        logging.info('Title: %s', post['title'])
        logging.info('Image: %s', url)
        logging.info('File: %s', image_path)

        return image_path

    def empty(self):
        """Remove each file in this directory."""
        super().rmtree()
        super().mkdir()

    def random(self):
        try:
            return next(util.randomized(list(self)))
        except StopIteration:
            return ''
