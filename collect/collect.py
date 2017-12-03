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


def _verify_image_response(res):
    error_msg = None
    content_type = res.headers['content-type']

    if 'removed' in res.url:
        error_msg = 'Appears to be removed (%s)' % res.url
    if 'image' not in content_type:
        error_msg = 'Not an image (%s)' % content_type
    if 'gif' in content_type:
        error_msg = 'Is a .gif (%s)' % content_type

    if error_msg is not None:
        strerr = '%s: %s' % (error_msg, res.url)
        Logger.debug(strerr)
        raise ValueError(strerr)


def _get_image(url):
    res = _get(url)
    _verify_image_response(res)
    return res


class _RedditPost:
    def __init__(self, parent_path, data):
        self.data = data
        self.url = self.data['url']
        self.path = parent_path.url_fname(self.url)

    def download(self):
        """Save a picture to this path. Raises ValueError if the HTTP response
        indicates that we did not receive an image."""
        res = _get_image(self.url)

        with open(self.path, 'wb') as file:
            file.write(res.content)

        Logger.debug('Collected new image: %s', self.url)
        return self

    def log(self):
        Logger.info('Title: %s', self.data['title'])
        Logger.info('Post: %s', self.data['permalink'])
        Logger.info('URL: %s', self.data['url'])


class _RedditJsonAPI:
    def __init__(self, path, api_url):
        self.path = path
        self.url = api_url
        self.posts = _randomized(_get(api_url).json()['data']['children'])
        self.existing_paths = {}

    def __next__(self):
        post = _RedditPost(self.path, next(self.posts)['data'])

        if self.path == post.path:
            return next(self)

        if post.path.exists():
            Logger.debug('Already downloaded: %s' % post.url)
            self.existing_paths[post.path] = post
            return post

        try:
            post.download()
        except ValueError as error:
            return next(self)
        else:
            return post

    def next_no_repeat(self):
        post = next(self)

        if post.path in self.existing_paths:
            return self.next_no_repeat()
        else:
            return post

    def recover_all(self):
        image_path = self.path.random()
        post = self.existing_paths.get(image_path)
        return image_path, post

    def recover_new(self):
        return next(_randomized(
            self.existing_paths.items()
        ))


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

    def _api(self, api_url):
        return _RedditJsonAPI(self, api_url)

    def _api_next(self, api, flags):
        if flags & NO_REPEAT:
            return api.next_no_repeat()
        else:
            return next(api)

    def _handle_fail(self, api, flags):
        if flags & NEW:
            Logger.debug('Falling back on image from new')
            try:
                return api.recover_new()
            except StopIteration:
                pass

        if flags & ALL:
            Logger.debug('Falling back on image from all')
            return api.recover_all()

        raise RuntimeError('Collection failed: %s' % api.url)

    def reddit(self, json_url, flags=FAIL):
        """Download a random image from a Reddit json url. Returns Path object
        of new image. Raises RuntimeError if it failed with no failsafe.
        Inherits FileNotFoundError behavior from self.random."""
        api = self._api(json_url)

        try:
            post = self._api_next(api, flags)
        except StopIteration:
            image_path, post = self._handle_fail(api, flags)

        if post is not None:
            post.log()
            image_path = post.path

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
