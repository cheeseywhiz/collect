"""Entry point for command line script."""
import argparse
import shlex
import sys

from . import collect
from .config import DIRECTORY, REDDIT_URL
from .logger import Logger
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
            help='Carry out the collection. Usable in conjunction with '
                 '--random if collection failed.')
        super().add_argument(
            'collector', metavar='PATH', default=DIRECTORY, nargs='?',
            type=collect.Collect,
            help=f'Set where images are downloaded to. Default {DIRECTORY}')
        super().add_argument(
            '--no-repeat', action='store_true',
            help='Collect a new image each time.')
        super().add_argument(
            '--random', action='store_true',
            help='Print out a random image path in the collection folder.')
        super().add_argument(
            '-u', metavar='URL', dest='reddit_url', default=REDDIT_URL,
            help=f'Set the URL for the Reddit json API. Default {REDDIT_URL}')
        super().add_argument(
            '-v', action='count',
            help='Output post information or -vv for debug information.')

    def parse_args(self, argv=None, *args, **kwargs):
        """Parse args and launch the proper programs. Default for argv is to
        use sys.argv. argv accepts str or list of arguments."""
        if argv is None:
            argv = sys.argv[1:]
        elif isinstance(argv, str):
            argv = shlex.split(argv)

        args = super().parse_args(argv, *args, **kwargs)

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

        Logger.setLevel(log_level)

        if not any((args.random, args.clear, args.collect)):
            self.show_help(args)
            sys.exit(1)

        self.using(args)
        args.collector.mkdir(exist_ok=True)

        if args.clear:
            args.collector.empty()

        if args.collect:
            if not util.wait_for_connection():
                Logger.exit('Could not connect to the internet')

            path = args.collector.reddit(args.reddit_url, args.no_repeat)

            if path is None:
                Logger.debug('Could not find new image')
                if args.random:
                    Logger.debug('Falling back on random image')
                    self._print_random(args)
                else:
                    sys.exit(1)
            else:
                print(path)
        elif args.random:
            self._print_random(args)

        self.args = args
        return args

    def _print_random(self, args):
        path = args.collector.random()

        if path is not None:
            print(path)
        else:
            Logger.debug('Random image not found')

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

        if args.clear:
            usages.append('directory clear option')
        if args.collect:
            usages.append('collect image option')
            if args.no_repeat:
                usages.append('no repeat option')
        if args.random:
            usages.append('random path output option')

        usages.extend(filter(None, (
            (f'image directory {args.collector}'
             if args.collector != DIRECTORY
             else None),
            (f'URL {args.reddit_url}'
             if args.reddit_url != REDDIT_URL
             else None),
        )))

        for i, item in enumerate(usages, 1):
            parts.append(item)
            if len(usages) == i:
                break
            elif len(usages) != 2:
                parts.append(',')
            parts.append(' ')
            if len(usages) - 1 == i:
                parts.append('and ')

        if usages:
            Logger.debug(''.join(parts))


def main(argv=None):
    try:
        CollectParser(description=description).parse_args(argv)
    except Exception as error:
        Logger.critical('%s: %s', error.__class__.__name__, error)
        raise


if __name__ == '__main__':
    main()
