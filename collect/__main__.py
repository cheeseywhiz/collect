"""Entry point for command line script."""
import argparse
import sys

from . import collect
from .config import DIRECTORY, REDDIT_URL
from . import logging
from . import util
from . import __doc__ as description

__all__ = ['CollectParser', 'main']


class CollectParser(argparse.ArgumentParser):
    """Configured Argument Parser for collect script."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().add_argument(
            '--clear', action='store_true',
            help='Clear the cache file and the image directory.')
        super().add_argument(
            '--collect', action='store_true',
            help='Carry out the collection with current settings.')
        super().add_argument(
            'collector', metavar='PATH', default=DIRECTORY, nargs='?',
            type=collect.Collect,
            help='Set where images are downloaded to. Default {DIRECTORY}')
        super().add_argument(
            '--random', action='store_true',
            help='Print out a random image path in the collection folder.')
        super().add_argument(
            '-u', metavar='URL', dest='reddit_url', default=REDDIT_URL,
            help='Set the URL for the Reddit json API. Default {REDDIT_URL}')
        super().add_argument(
            '-v', action='count',
            help='Output post information or -vv for debug information.')

    def parse_args(self, *args, **kwargs):
        """Parse args and launch the proper programs."""
        args = super().parse_args(*args, **kwargs)

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

        if False not in (args.random, args.collect):
            self.show_help(args)
            logging.error('Both --random and --collect present.')
            sys.exit(1)

        if True not in (args.random, args.clear, args.collect):
            self.show_help(args)
            sys.exit(1)

        self.using(args)
        args.collector.mkdir(exist_ok=True)

        if args.random:
            path = args.collector.random()
            if path is not None:
                print(path)

        if args.clear:
            args.collector.empty()

        if args.collect:
            if not util.wait_for_connection():
                raise RuntimeError('Could not connect to the internet')
            path = args.collector.reddit(args.reddit_url)
            print(path)

        self.args = args
        return args

    def show_help(self, args):
        """Show usage if not verbose or full help otherwise."""
        if args.v:
            super().print_help(file=sys.stderr)
        else:
            super().print_usage(file=sys.stderr)

    def using(self, args):
        """Log parsed information."""
        usages = []
        parts = ['Using ']

        if args.random:
            usages.append('random path output option')
        elif args.clear:
            usages.append('directory clear option')
        elif args.collect:
            usages.append('collect image option')

        usages.extend(filter(None, (
            (f'image directory {args.collector}'
             if str(args.collector) != DIRECTORY
             else None),
            (f'URL {args.reddit_url}'
             if str(args.reddit_url) != REDDIT_URL
             else None),
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

    try:
        CollectParser(description=description).parse_args(argv)
    except Exception as error:
        logging.critical('%s: %s', error.__class__.__name__, str(error))
        raise
