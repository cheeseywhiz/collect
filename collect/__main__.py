"""Entry point for command line script."""
import argparse
import pathlib
import sys

from . import collect
from . import config
from . import logging
from . import util
from . import __doc__ as description

__all__ = ['CollectParser', 'main']


class CollectParser(argparse.ArgumentParser):
    """Configured Argument Parser for collect script."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().add_argument(
            '-c', default=config.CACHE_ROOT, metavar='PATH', dest='cache_root',
            type=util.path_type,
            help=f'Set the cache root path. Default {config.CACHE_ROOT}')
        super().add_argument(
            '--clear', action='store_true',
            help='Clear the cache file and the image directory.')
        super().add_argument(
            '--collect', action='store_true',
            help='Carry out the collection with current settings.')
        super().add_argument(
            '--show-urls', action='store_true',
            help='List all of the successful URLs in the cache.')
        super().add_argument(
            '-u', default=config.REDDIT_LINK, metavar='URL', dest='url',
            help=(
                'Set the URL for the Reddit json API. Default'
                f'{config.REDDIT_LINK}'))
        super().add_argument(
            '-v', action='count',
            help='Output post information or -vv for debug information.')

    def parse_args(self, *args, **kwargs):
        """Parse args and launch the proper programs."""
        args = super().parse_args(*args, **kwargs)

        # record changes relative to default state
        self.cache_root_changed = args.cache_root != config.CACHE_ROOT
        self.url_changed = args.url != config.REDDIT_LINK

        # set global state
        config.set_cache_root(args.cache_root)
        collect.download.load_cache(path=config.PICKLE_PATH)

        for path in (config.CACHE_ROOT, config.IMG_DIR):
            pathlib.Path(path).mkdir(exist_ok=True)

        # act on the parse result
        self.v_flag(args)
        self.using(args)

        for value in map(lambda f: f(args), (
                self.show_urls_flag, self.clear_flag, self.collect,
                self.show_help)):
            if value:
                break

        return args

    def show_help(self, args):
        if args.v:
            super().print_help(file=sys.stderr)
        else:
            super().print_usage(file=sys.stderr)

        return True

    def v_flag(self, args):
        """Set root log level based on the amout of -v flags."""
        if isinstance(args.v, int):
            if args.v > 2:
                args.v = 2
            elif args.v < 1:
                args.v = None

        log_level = {
            None: 'WARNING',
            1: 'INFO',
            2: 'DEBUG',
        }[args.v]

        logging.root.setLevel(log_level)
        return log_level

    def show_urls_flag(self, args):
        """Output URLs in the current cache if supplied --show-urls."""
        if args.show_urls:
            for url, invalid, *_ in collect.download.cache.values():
                if not invalid:
                    print(url)

        return args.show_urls

    def clear_flag(self, args):
        """Clear the cache file if supplied --clear."""
        if args.clear:
            collect.download.re_init_cache()
            for file in pathlib.Path(config.IMG_DIR).iterdir():
                util.disown('rm', '-f', file)

        return args.clear

    def collect(self, args):
        """Collect the image from Reddit if supplied --collect."""
        if args.collect:
            collect.collect(args.url)
            return True
        else:
            return False

    def using(self, args):
        """Log parsed information."""
        usages = []
        parts = ['Using ']

        if args.show_urls:
            usages.append('URLs output option')
        elif args.clear:
            usages.append('cache clear option')
        elif args.collect:
            usages.append('collect image option')

        usages.extend(filter(None, (
            (
                f'cache root {args.cache_root}'
                if self.cache_root_changed
                else None
            ),
            (
                f'URL {args.url}'
                if self.url_changed
                else None
            ),
        )))

        for i, item in enumerate(usages, 1):
            parts.append(item)
            if len(usages) == i:
                parts.append('.')
                break
            elif len(usages) != 2:
                parts.append(',')
            parts.append(' ')
            if len(usages) - 1 == i:
                parts.append('and ')

        if usages:
            logging.debug(''.join(parts))


def main(argv=None):
    """Launch the main functions with the given argv or imported sys.argv by
    default."""
    if argv is None:
        argv = sys.argv[1:]

    CollectParser(description=description).parse_args(argv)
