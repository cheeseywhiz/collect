"""Provides functions for downloading images"""
import functools
import random

import praw
import requests

from . import _config
from ._logger import Logger
from . import _path
from ._flags import *
from ._flags import __all__ as _flags_all

__all__ = ['RedditSubmissionWrapper', 'RedditListingWrapper', 'Collect']
__all__.extend(_flags_all)

_reddit_inited = False


def _reddit():
    global _reddit_inst

    if not _reddit_inited:
        _reddit_inst = praw.Reddit()

    return _reddit_inst


def _reddit_init(user):
    global _reddit_inst, _reddit_inited
    _reddit_inited = True
    _reddit_inst = praw.Reddit(user)


_get = functools.partial(requests.get, headers={
    'User-Agent': 'collect/%s' % _config.VERSION
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


class RedditSubmissionWrapper:
    """Wrapper for Reddit submission objects to facilitate logging and URL
    downloading."""

    def __init__(self, parent_path, data):
        self.data = data
        self.url = self.data.url
        self.path = parent_path.url_fname(self.url)

    def download(self):
        """Save a picture to {self}. Raises `ValueError` if the HTTP
        response indicates that we did not receive an image."""
        res = _get_image(self.url)

        with self.path.open('wb') as file:
            file.write(res.content)

        Logger.debug('Collected new image: %s', self.url)
        return self

    def log(self):
        """Log the submission's title, comment URL, and link URL."""
        Logger.info('Title: %s', self.data.title)
        Logger.info('Post: %s', self.data.permalink)
        Logger.info('URL: %s', self.data.url)


class RedditListingWrapper:
    """Wrapper for Reddit listing generators to facilitate image downloading
    and handling certain behaviors."""

    def __init__(self, path, api_url):
        self.path = Collect(path)
        self.url = api_url
        self.listing = _reddit().get(api_url)
        self.posts = _randomized(list(self.listing))
        self.existing_paths = {}

    def __iter__(self):
        """Allow {self} to be used as an iterator."""
        return self

    def __next__(self):
        """Return the next submission in the listing in a random order while
        noting if the submission's corresponding download path already
        exists."""
        post = RedditSubmissionWrapper(self.path, next(self.posts))

        if self.path == post.path:
            return next(self)

        if post.path.exists():
            Logger.debug('Already downloaded: %s' % post.url)
            self.existing_paths[post.path] = post

        return post

    def next_download(self):
        """`next(`{self}`)` while downloading the submission's image."""
        post = next(self)

        if post.path.exists():
            return post

        try:
            return post.download()
        except ValueError as error:
            return self.next_download()

    def next_no_repeat(self):
        """`next(`{self}`)` while skipping submissions that have already been
        collected."""
        post = next(self)

        if post.path.exists():
            return self.next_no_repeat()
        else:
            return post

    def next_no_repeat_download(self):
        """{self}`.next_no_repeat()` while downloading the submisson's
        image."""
        try:
            return self.next_no_repeat().download()
        except ValueError as error:
            return self.next_no_repeat_download()

    def flags_next_download(self, flags):
        """Download the next submission's image according to the specified
        flags."""
        if flags & NO_REPEAT:
            return self.next_no_repeat_download()
        else:
            return self.next_download()

    def _random(self):
        image_path = self.path.random()
        post = self.existing_paths.get(image_path)
        return image_path, post

    def _flags_handle_stop(self, flags):
        if flags & NEW:
            Logger.debug('Falling back on image from new')
            try:
                return next(_randomized(
                    self.existing_paths.items()
                ))
            except StopIteration:
                pass

        if flags & ALL:
            Logger.debug('Falling back on image from all')
            return self._random()

        raise RuntimeError('Collection failed: %s' % self.url)

    def flags_next_recover(self, flags):
        """Download the next submission's image but handle collection errors
        according to the flags."""
        try:
            post = self.flags_next_download(flags)
        except StopIteration:
            image_path, post = self._flags_handle_stop(flags)

        if post is not None:
            post.log()
            image_path = post.path

        return image_path

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        args = self.path, self.url
        args_str = ', '.join(map(repr, args))
        return '%s.%s(%s)' % (module, name, args_str)


class Collect(_path.Path):
    """Perform image collection operations on a path."""

    def reddit_listing(self, api_url):
        """Helper for new `RedditListingWrapper` at {self}."""
        return RedditListingWrapper(self, api_url)

    def random(self):
        """Return a random file within {self} (a directory). Raises
        `FileNotFoundError` if no suitable file was found."""
        try:
            return next(
                path
                for path in _randomized(list(self))
                if path.is_file()
            )
        except StopIteration:
            raise FileNotFoundError('No suitable files: %s' % self)
