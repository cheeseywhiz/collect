"""Provides functions for downloading images"""
import pathlib
import random
import time
from urllib.parse import urlparse

import requests

from . import cache
from . import util
from . import logging
from . import CACHE_PATH, REDDIT_LINK, SAVE_DIR


def random_map(func, *iterables):
    """Implement map() by sending in arguments in a random order"""
    args = list(zip(*iterables))
    random.shuffle(args)
    return map(func, *zip(*args))


@util.partial(requests.get, headers={'User-Agent': 'u/cheeseywhiz'})
def get(url, *args, **kwargs):
    yield
    yield lambda req: logging.debug('Reason: %s', req.reason)


@cache.cache(path=CACHE_PATH)
def download(url):
    """Download an image and return cache.DownloadResult with relevant info"""
    req = get(url)
    time_ = int(time.time())

    error_msg = None
    type_ = req.headers['content-type']
    if not type_.startswith('image'):
        error_msg = 'Not an image'
    if type_.endswith('gif'):
        error_msg = 'Is a .gif'
    if 'removed' in req.url:
        error_msg = 'Appears to be removed'
    if error_msg:
        return cache.DownloadResult(url, time_, False, error_msg, None, None)

    fname = urlparse(req.url).path.split('/')[-1]
    return cache.DownloadResult(
        url, time_, True, 'Collected new image', fname, req.content)


def write_image(download_result, path):
    """Write an image to disk given a download() response and a full path"""
    path = pathlib.Path(path)

    if path.exists():
        return download_result._replace(
            status='Already downloaded; not re-writing')

    with path.open('wb') as file:
        file.write(download_result.content)

    return download_result


def collect(save_dir=None, url=None):
    """Download a random image from a Reddit .json url and save it in the given
    folder path."""
    if save_dir is None:
        save_dir = SAVE_DIR
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
        logging.warning('Too many tries')
        return 1

    save_dir = pathlib.Path(save_dir)
    save_dir.mkdir(exist_ok=True)

    urls = {
        post['data']['url']: post['data']
        for post in get(url).json()['data']['children']}

    with download.saving():
        for res in random_map(download, urls.keys()):
            if not res.succeeded:
                logging.debug('%s: %s', res.status, res.url)
                continue
            post = urls[res.url]
            path = save_dir / res.fname
            res = write_image(res, path)
            logging.debug(res.status)
            logging.info('Post: %s', post['permalink'])
            logging.info('Title: %s', post['title'])
            logging.info('Image: %s', res.url)
            logging.info('File: %s', path)
            print(path)
            return 0
        else:  # no break; did not succeed
            logging.error('Could not find image')
            return 1
