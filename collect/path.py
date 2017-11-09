import functools
import mimetypes
import os
import shutil

try:
    from magic import from_file as magic_from_file
except ImportError:
    magic_from_file = None

from . import config

__all__ = ['PathBase', 'PathMeta', 'Path']


class _ApplyDecorators(type):
    """Metaclass that applies decorators to methods as specified by _Decorate
    instances."""
    def __new__(cls, name, bases, namespace):
        self = type.__new__(cls, name, bases, namespace)

        for name_, value in namespace.items():
            if isinstance(type(value), _Decorate):
                setattr(self, name_, value.decorator(self, value.method))

        return self


class _Decorate(type):
    """Indicate to the _ApplyDecorators metaclass to apply the given decorator
    by calling the decorator with the new class as the first agument."""
    def __new__(cls, decorator):
        name = 'Decorate_%s_At_Class_Creation' % decorator.__name__
        bases = (_Decorate.Base, )
        namespace = {
            'decorator': staticmethod(decorator),
            '__doc__': _Decorate.Base.__doc__ % decorator,
        }
        return type.__new__(cls, name, bases, namespace)

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        return '%s.%s(%r)' % (module, name, self.decorator)

    class Base:
        """Apply %r on new class instances."""

        def __init__(self, method):
            self.method = method


class PathMeta(_ApplyDecorators):
    """Provides the numerous class methods for all Path types."""

    def home(self):
        """Return the user's home directory."""
        return self(path=os.path.expanduser('~'))

    def cwd(self):
        """Return the current working directory."""
        return self(path=os.getcwd())

    def from_str(self, func):
        """Wrap a function such that the result is passed to a new instance of
        this class."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.__new__(self, func(*args, **kwargs))

        return wrapper

    MakeStr = _Decorate(from_str)


class PathBase(metaclass=PathMeta):
    """Provides general functionality for all Path types."""
    def __new__(cls, path=None):
        self = object.__new__(cls)
        if path is None:
            path = '.'

        self.__path = os.path.normpath(os.path.expanduser(path))
        parts = self.__path.split(os.sep)

        if os.path.isabs(self.__path):
            if config.WINDOWS:
                if not parts[0]:
                    parts[0] = os.getenv('HOMEDRIVE')

                parts.insert(0, os.sep)
            else:
                parts[0] = os.sep

        if not parts[-1]:
            parts.pop()

        self.__parts = tuple(parts)
        return self

    def __init__(self, path=None):
        pass

    @property
    def parts(self):
        """Split the path by the OS path slash separator."""
        return self.__parts

    @property
    def basename(self):
        """The final element in the path."""
        return self.__parts[-1]

    @property
    def split(self):
        """Split the path's basename by filename and extension."""
        res = self.basename.split('.', maxsplit=1)

        if len(res) == 1:
            res.append('')

        return tuple(res)

    def _first_diff_part(self, other):
        """Return the first index where a path difference occurs, or -1 if no
        difference occurs."""
        if self == other:
            return len(self.parts) - 1
        elif len(other.parts) < len(self.parts):
            return len(other.parts) - 1

        for i, (self_part, other_part) in enumerate(
            zip(self.parts, other.parts)
        ):
            if self_part != other_part:
                return i
        else:
            return -1

    def __fspath__(self):
        """Return the file system representation of the path."""
        return self.__path

    def __eq__(self, other):
        try:
            return os.fspath(self) == os.fspath(other)
        except TypeError:
            return NotImplemented

    def __str__(self):
        return os.fspath(self)

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        return '%s.%s(%r)' % (module, name, str(self))

    def __hash__(self):
        return hash(str(self))


class Path(PathBase):
    """Provides high level and cross platform file system manipulations on
    paths."""
    @PathBase.MakeStr
    def join(self, *others):
        """Connect one or more file names onto this path."""
        return os.path.join(self, *others)

    @PathBase.MakeStr
    def realpath(self):
        """Return the absolute path and eliminate symbolic links."""
        return os.path.realpath(self)

    @PathBase.MakeStr
    def relpath(self, start=None):
        """Return the abbreviated form of self relative to start. Default for
        start is the current working directory."""
        if start is None:
            start = self.__class__.cwd()

        return os.path.relpath(self, start)

    @PathBase.MakeStr
    def abspath(self):
        """Return the absolute path."""
        return os.path.abspath(self)

    def __truediv__(self, other):
        """Perform self / other to join paths."""
        return self.join(other)

    def open(self, mode='r', buffering=-1, encoding=None, errors=None,
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

    def is_abs(self):
        """Check if the path is absolute."""
        return os.path.isabs(self)

    def __contains__(self, other):
        """Check recursively if other is inside self (a directory)."""
        self = self.abspath()
        other = Path(other).abspath()
        return self._first_diff_part(other) < 0

    def contains_toplevel(self, other):
        """Check if other is at the top level of self (a directory)."""
        self = self.abspath()
        other = other.abspath()
        return other in self and len(other.parts) - len(self.parts) == 1

    def is_toplevel(self, other):
        """Check if self is in the top level of other (a directory)."""
        return Path(other).contains_toplevel(self)

    def is_in_dir(self, other):
        """return self in other
        Check if self is inside other (a directory)."""
        return self in Path(other)

    def rmtree(self, ignore_errors=False, onerror=None):
        """Delete every file inside a directory file."""
        shutil.rmtree(self, ignore_errors=ignore_errors, onerror=onerror)

    def remove(self):
        """Remove a file or a directory (if empty)."""
        if self.is_file():
            os.remove(self)
        elif self.is_dir():
            os.rmdir(self)
        else:
            raise ValueError('%r is not a file or directory' % self)

    def remove_contents(self):
        """Remove each file within a directory."""
        for file in self:
            file.remove()

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
    def type(self):
        """Return the MIME type of this file."""
        if self.is_dir():
            # mimic file(1) behavior
            return 'inode/directory'

        self_path = os.fspath(self)
        mime_type, encoding = mimetypes.guess_type(self_path, strict=False)

        if mime_type is None and magic_from_file is not None:
            mime_type = magic_from_file(self_path, mime=True)

        return mime_type

    @property
    def tree(self):
        """Generate all of the paths in this directory path."""
        yield self

        for item in self:
            if item.is_dir() and not item.is_link():
                try:
                    yield from item.tree
                except PermissionError:
                    pass
            else:
                yield item

    def __iter__(self):
        """Iterate over the paths within this path."""
        yield from map(self.join, os.listdir(self))
