"""Entry point for command line script."""
import argparse
import contextlib
import shlex
import sys

from . import collect
from .config import DIRECTORY, REDDIT_URL
from .logger import Logger
from . import util
from . import __doc__

__all__ = ['CollectParser', 'main']


@contextlib.contextmanager
def log_exceptions(args, *exc_types):
    """Context manager setting args.exit to 1 and logging the value of any
    matching Exception raised within."""
    try:
        yield
    except Exception as error:
        for exc_type in exc_types:
            if isinstance(error, exc_type):
                Logger.debug(str(error))
                args.exit = 1
                break


class CollectParser(argparse.ArgumentParser):
    def __init__(self, *args, description=__doc__, **kwargs):
        super().__init__(*args, description=description, **kwargs)
        self.subcommands = {
            'reddit': self.reddit,
            'random': self.random,
            'clear': self.clear}
        commands = super().add_subparsers(
            title='Subcommands', dest='subcommand',
            parser_class=argparse.ArgumentParser)

        reddit = commands.add_parser(
            'reddit',
            description='Carry out the collection.')
        reddit.add_argument(
            '--fail', default='fail', choices=[
                name.lower()
                for name in collect.Failsafe.__members__.keys()
                if name != 'FAIL'],
            help='Print random file path if collection fails. all: pull '
                 'random path from collection directory. new: pull random '
                 'path from provided URL.')
        reddit.add_argument(
            '-n', action='store_true', dest='no_repeat_flag',
            help='Collect a new image each time.')
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
            args.exit = 1
            return

        with log_exceptions(args, FileNotFoundError, RuntimeError):
            return args.collector.reddit(
                args.reddit_url, args.no_repeat_flag,
                getattr(collect.Failsafe, args.fail.upper())
            )

    def random(self, args):
        with log_exceptions(args, FileNotFoundError):
            return args.collector.random()

    def clear(self, args):
        args.collector.remove_contents()


def main(argv=None):
    try:
        exit = CollectParser().parse_args(argv).exit
    except Exception as error:
        Logger.critical('%s: %s', error.__class__.__name__, error)
        raise
    else:
        if exit:
            sys.exit(exit)


if __name__ == '__main__':
    main()
