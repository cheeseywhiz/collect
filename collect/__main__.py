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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcommands = {
            'reddit': self.reddit,
            'random': self.random,
            'clear': self.clear,
        }
        commands = super().add_subparsers(
            title='Subcommands', dest='subcommand',
            parser_class=argparse.ArgumentParser)

        reddit = commands.add_parser(
            'reddit',
            description='Carry out the collection.')
        reddit.add_argument(
            '-n', action='store_true', dest='no_repeat_flag',
            help='Collect a new image each time.')
        reddit.add_argument(
            '-r', action='store_true', dest='random_flag',
            help='Print random file if collection fails.'
        )
        reddit.add_argument(
            '--url', metavar='URL', dest='reddit_url', default=REDDIT_URL,
            help=f'Set the URL for the Reddit json API. Default {REDDIT_URL}')

        commands.add_parser(
            'random',
            description='Print out a random image path in the collection '
                        'folder.')

        commands.add_parser(
            'clear',
            description='Clear the image directory.')

        super().add_argument(
            '--dir', metavar='PATH', dest='collector', default=DIRECTORY,
            type=collect.Collect,
            help=f'Set the download location. Default {DIRECTORY}')

        super().add_argument(
            '-v', action='count',
            help='Set verbosity level.')
        super().set_defaults(exit=0)

    def parse_args(self, argv=None, *args, **kwargs):
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

        subcommand_func = self.subcommands.get(args.subcommand)

        if subcommand_func is None:
            args.exit = 1
            if args.v:
                super().print_help(file=sys.stderr)
            else:
                super().print_usage(file=sys.stderr)
        else:
            args.collector.mkdir(exist_ok=True)
            path = subcommand_func(args)

            if path is not None:
                print(path)
            elif args.subcommand != 'clear':
                args.exit = 1

        return args

    def reddit(self, args):
        if not util.wait_for_connection():
            Logger.error('Could not connect to the internet')
            return

        path = args.collector.reddit(args.reddit_url, args.no_repeat_flag)

        if path is None:
            Logger.debug('Failed to carry out the collection')
            if args.random_flag:
                Logger.debug('Falling back on random image')
                path = self.random(args)

        return path

    def random(self, args):
        return args.collector.random()

    def clear(self, args):
        args.collector.remove_contents()


def main(argv=None):
    try:
        exit = CollectParser(description=description).parse_args(argv).exit
    except Exception as error:
        Logger.critical('%s: %s', error.__class__.__name__, error)
        raise
    else:
        if exit:
            sys.exit(exit)


if __name__ == '__main__':
    main()
