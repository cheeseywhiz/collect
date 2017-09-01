"""Entry point for command line script."""
import argparse
import os
import sys
import logging
from . import CACHE_PATH, REDDIT_LINK, SAVE_DIR, __doc__ as description
from . import collect


def parse_v_flag(value):
    if isinstance(value, int):
        if value > 2:
            value = 2
        elif value < 1:
            value = None

    log_level = {
        None: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
    }[value]

    collect.logging.root.setLevel(log_level)


def path_type(path):
    return os.path.abspath(os.path.expanduser(path))


def get_args(argv):
    arg = argparse.ArgumentParser(description=description)
    arg.add_argument(
        '-c', default=CACHE_PATH, metavar='PATH', type=path_type,
        help=f'Set the pickle cache path. Default {CACHE_PATH}')
    arg.add_argument(
        '-d', action='store_true',
        help='Verify using all defaults')
    arg.add_argument(
        '-s', default=SAVE_DIR, metavar='PATH', type=path_type,
        help=f'Set the image save path. Default {SAVE_DIR}')
    arg.add_argument(
        '-u', default=REDDIT_LINK, metavar='URL',
        help=(
            'Set the URL for the Reddit json API. '
            f'Default {REDDIT_LINK}'))
    arg.add_argument(
        '-v', action='count',
        help='Output more information. -vv for even more.')
    args = arg.parse_args(argv)

    options = args.c, args.s, args.u
    defaults = CACHE_PATH, SAVE_DIR, REDDIT_LINK

    if options == defaults and not args.d:
        arg.print_usage(file=sys.stderr)
        sys.exit(1)
    else:
        return args


def process_args(args):
    parse_v_flag(args.v)
    collect.download.load_cache(path=args.c)
    return collect.collect(args.s, args.u)


def main(argv=None):
    """Launch the main functions with the given sys.argv or imported sys.argv
    by default."""
    if argv is None:
        argv = sys.argv[1:]

    args = get_args(argv)
    sys.exit(process_args(args))
