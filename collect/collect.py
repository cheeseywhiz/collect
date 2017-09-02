"""Provides functions for downloading images"""
import functools
import pathlib
import time

import requests

from . import cache
from . import util
from . import logging
from .config import PICKLE_PATH, REDDIT_LINK, IMG_DIR

__all__ = ['get', 'download', 'ensure_download', 'collect']


@util.partial(requests.get, headers={'User-Agent': 'u/cheeseywhiz'})
def get(url, *args, **kwargs):
    yield
    yield lambda req: logging.debug('Reason: %s', req.reason)


@cache.cache(path=PICKLE_PATH)
def download(url, img_dir):
    """Download an image and return cache.DownloadResult with relevant info."""
    # cache.DownloadResult(
    #   url: str, time: int, invalid: bool, message: str, path: pathlib.Path)
    req = get(url)
    time_ = int(time.time())

    error_msg = None
    content_type = req.headers['content-type']
    if not content_type.startswith('image'):
        error_msg = 'Not an image'
    if content_type.endswith('gif'):
        error_msg = 'Is a .gif'
    if 'removed' in req.url:
        error_msg = 'Appears to be removed'
    if error_msg:
        return cache.DownloadResult(url, time_, True, error_msg, None)

    path = util.url_make_path(url, img_dir)
    result = cache.DownloadResult(
        url, time_, False, 'Collected new image', path)

    with path.open('wb') as file:
        file.write(req.content)

    return result


def ensure_download(url, img_dir=None):
    """Ensure that the image is downloaded if it is still cached."""
    download_args = url, img_dir
    path_guess = util.url_make_path(*download_args)
    key_guess = download.key(*download_args)

    if path_guess.is_file():
        on_disk_before = True
    else:
        on_disk_before = False

    if key_guess in download.cache.keys():
        cached_before = True
    else:
        cached_before = False

    with download.saving():
        result = download(*download_args)
        if result.invalid or not cached_before:
            return result
        elif on_disk_before:
            return result._replace(message='Already downloaded')
        else:
            download.cache.pop(key_guess)
            return download(*download_args)


def collect(img_dir=None, url=None):
    """Download a random image from a Reddit .json url and save it in the given
    folder path."""
    if img_dir is None:
        img_dir = IMG_DIR
    if url is None:
        url = REDDIT_LINK

    max_seconds = 60
    seconds_wait = 5

    for n_try in range(max_seconds // seconds_wait):
        if not util.ping():
            logging.warning('Connection not found')
            time.sleep(seconds_wait)
        elif n_try:
            logging.info('Connection found')
            break
        else:
            break
    else:  # no break; really no internet connection
        raise RuntimeError('Could not connect to the internet')

    img_dir = pathlib.Path(img_dir)
    img_dir.mkdir(exist_ok=True)
    ensure_download_ = functools.partial(ensure_download, img_dir=str(img_dir))

    urls = {
        post['data']['url']: post['data']
        for post in get(url).json()['data']['children']}

    for res in util.random_map(ensure_download_, urls.keys()):
        if res.invalid:
            logging.debug('%s: %s', res.message, res.url)
            continue
        post = urls[res.url]
        logging.debug(res.message)
        logging.info('Post: %s', post['permalink'])
        logging.info('Title: %s', post['title'])
        logging.info('Image: %s', res.url)
        logging.info('File: %s', res.path)
        print(res.path)
        return
    else:  # no break; did not succeed
        raise RuntimeError('Could not find image')
