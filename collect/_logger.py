import logging
import sys


class StdErrHandler(logging.Handler):
    def __init__(self, level=None):
        if level is None:
            level = logging.NOTSET

        super().__init__(level)
        fmt = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
        super().setFormatter(fmt)

    def flush(self):
        print(file=sys.stderr, end='', flush=True)

    def emit(self, record):
        message = super().format(record)
        print(message, file=sys.stderr)


def _instantiate(cls):
    return cls()


@_instantiate
class Logger(logging.Logger):
    def __init__(self):
        super().__init__(__name__)
        self.handler = StdErrHandler()
        super().addHandler(self.handler)

    def exit(self, *args, **kwargs):
        """Log the error and exit with status code 1."""
        super().error(*args, **kwargs)
        sys.exit(1)
