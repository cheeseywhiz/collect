import functools
import os
import shutil

from . import config

__all__ = ['PathBase', 'Path']


def from_str(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        return Path(method(*args, **kwargs))

    return wrapper


def from_iterable(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        yield from map(Path, method(*args, **kwargs))

    return wrapper


class PathBase(os.PathLike):
    __slots__ = '__path', '_parts'

    def __init__(self, path=None):
        if path is None:
            path = os.getcwd()

        parts = os.path.abspath(os.path.expanduser(path)).split(os.sep)
        self.__path = os.sep.join(parts)

        if not config.WINDOWS:
            parts[0] = os.sep

        self._parts = tuple(parts)

    @property
    def parts(self):
        """Split the path by the OS path slash separator."""
        return self._parts

    @parts.setter
    def parts(self, value):
        self._parts = value

    @parts.deleter
    def parts(self):
        # TODO: check if proper
        del self._parts

    def __fspath__(self):
        return str(self)

    def __str__(self):
        return self.__path

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        return f'{module}.{name}({self.__path !r})'


class Path(PathBase):
    """High level and cross platform operations on paths."""
    @from_str
    def join(self, *others):
        """Connect more file names onto this path."""
        return os.path.join(self, *others)

    @from_str
    def realpath(self):
        """Eliminate symbolic links."""
        return os.path.realpath(self)

    def __truediv__(self, other):
        """Perform self / other to join paths."""
        return self.join(other)

    def open(
            self, mode='r', buffering=-1, encoding=None, errors=None,
            newline=None, closefd=True, opener=None):
        """Open the file for changing."""
        return open(
            self, mode=mode, buffering=buffering, encoding=encoding,
            errors=errors, newline=newline, closefd=closefd, opener=opener)

    def exists(self):
        """Check if the path exists."""
        return os.path.exists(self)

    def is_dir(self):
        """Check if the path is a directory."""
        return os.path.isdir(self)

    def is_file(self):
        """Check if the path is a file."""
        return os.path.isfile(self)

    def rmtree(self, ignore_errors=False, onerror=None):
        """Delete every file inside a directory file."""
        shutil.rmtree(self, ignore_errors=ignore_errors, onerror=onerror)

    def mkdir(self, mode=0o777, *, exist_ok=False, dir_fd=None):
        """Make a directory exist under this path."""
        try:
            os.mkdir(self, mode=mode, dir_fd=dir_fd)
        except FileExistsError:
            if not exist_ok:
                raise

    @classmethod
    def home(cls):
        """Return the user's home directory."""
        path = os.path.expanduser('~')
        return cls(path)

    @classmethod
    def cwd(cls):
        """Return the current working directory."""
        return cls(os.getcwd())

    @from_iterable
    def __iter__(self):
        """Iterate over the paths within this path."""
        yield from map(self.join, os.listdir(self))
