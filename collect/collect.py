"""Provides functions for downloading images"""
import pathlib
import time

from . import cache
from . import config
from . import util
from . import logging

__all__ = ['collect', 'download', 'ensure_download']


@cache.cache(path=config.PICKLE_PATH)
def download(url):
    """Download an image and return cache.DownloadResult with relevant info."""
    # cache.DownloadResult(url: str, invalid: bool, message: str, path: str)
    error_msg = None
    path = util.url_make_path(url)
    result = cache.DownloadResult(url, False, None, str(path))

    if path.exists():
        return result

    req = util.get(url)
    content_type = req.headers['content-type']

    if 'removed' in req.url:
        error_msg = 'Appears to be removed'
    if not content_type.startswith('image'):
        error_msg = 'Not an image'
    if content_type.endswith('gif'):
        error_msg = 'Is a .gif'

    if error_msg:
        return cache.DownloadResult(url, True, error_msg, None)

    with path.open('wb') as file:
        file.write(req.content)

    return result


def ensure_download(url):
    """Ensure that the image is downloaded if it is still cached."""
    path_guess = util.url_make_path(url)
    key_guess = download.key(url)

    if path_guess.is_file():
        on_disk_before = True
    else:
        on_disk_before = False

    if key_guess in download.cache.keys():
        cached_before = True
    else:
        cached_before = False

    with download.saving():
        result = download(url)
        if result.invalid:
            return result
        elif on_disk_before:
            return result._replace(message='Already downloaded')
        elif cached_before:
            download.remove(url)
            result = download(url)
        return result._replace(message='Collected new image')


def collect(url=None):
    """Download a random image from a Reddit json url."""
    if url is None:
        url = config.REDDIT_LINK

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

    urls = {
        post['data']['url']: post['data']
        for post in util.get(url).json()['data']['children']}

    for res in util.random_map(ensure_download, urls.keys()):
        if res.invalid:
            logging.debug('%s: %s', res.message, res.url)
            continue
        post = urls[res.url]
        path = pathlib.Path(res.path)
        logging.debug(res.message)
        logging.info('Post: %s', post['permalink'])
        logging.info('Title: %s', post['title'])
        logging.info('Image: %s', res.url)
        logging.info('File: %s', path)
        print(path)
        return
    else:  # no break; did not succeed
        raise RuntimeError('Could not find image')
