import functools
import os
import shutil

from . import config

__all__ = ['PathBase', 'Path']


def from_iterable(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        yield from map(Path, method(*args, **kwargs))

    return wrapper


class PathMeta(type, os.PathLike):
    def __new__(cls, name, bases, namespace):
        def from_str(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return self.__new__(self, func(*args, **kwargs))

            return wrapper

        def from_iter(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                yield from map(
                    lambda path: self.__new__(self, path),
                    func(*args, **kwargs))

            return wrapper

        namespace.update({
            name: from_str(value.func)
            for name, value in namespace.items()
            if type(value) is PathMeta.MakeStr
        })
        namespace.update({
            name: from_iter(value.func)
            for name, value in namespace.items()
            if type(value) is PathMeta.MakeIter
        })
        self = type.__new__(cls, name, bases, namespace)
        return self

    def __init__(self, name, bases, namespace):
        pass

    class MakeStr:
        def __init__(self, func):
            self.func = func

    class MakeIter:
        def __init__(self, func):
            self.func = func


class PathBase(metaclass=PathMeta):
    def __new__(cls, path=None):
        self = object.__new__(cls)
        if path is None:
            path = '.'

        parts = os.path.normpath(os.path.expanduser(path)).split(os.sep)
        self.__path = os.sep.join(parts)

        if not config.WINDOWS:
            if not parts[0]:
                parts[0] = os.sep

        self.__parts = tuple(parts)
        return self

    def __init__(self, path=None):
        pass

    @property
    def parts(self):
        """Split the path by the OS path slash separator."""
        return self.__parts

    @classmethod
    def home(cls):
        """Return the user's home directory."""
        return cls(path=os.path.expanduser('~'))

    @classmethod
    def cwd(cls):
        """Return the current working directory."""
        return cls(path=os.getcwd())

    def __fspath__(self):
        return str(self)

    def __eq__(self, other):
        try:
            return os.path.samefile(self, other)
        except TypeError:
            return NotImplemented

    def __str__(self):
        return self.__path

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        return f'{module}.{name}({self.__path !r})'


class Path(PathBase):
    """High level and cross platform operations on paths."""
    @PathBase.MakeStr
    def join(self, *others):
        """Connect more file names onto this path."""
        return os.path.join(self, *others)

    @PathBase.MakeStr
    def realpath(self):
        """Return the absolute path and eliminate symbolic links."""
        return os.path.realpath(self)

    @PathBase.MakeStr
    def abspath(self):
        """Return the absolute path."""
        return os.path.abspath(self)

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

    def is_link(self):
        """Check if the path is a symbolic link."""
        return os.path.islink(self)

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

    @property
    def parent(self):
        """Move up one directory."""
        return self / '..'

    @property
    def tree(self):
        """Generate all of the paths in this directory path."""
        def recur(path):
            yield path

            for subpath in path:
                if subpath.is_dir() and not subpath.is_link():
                    try:
                        yield from recur(subpath)
                    except PermissionError:
                        pass
                else:
                    yield subpath

        yield from recur(self)

    @PathBase.MakeIter
    def __iter__(self):
        """Iterate over the paths within this path."""
        yield from map(self.join, os.listdir(self))
