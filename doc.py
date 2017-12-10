import types as _types
import builtins as _builtins
import functools as _functools


def trim_first_n_spaces(string, n_spaces):
    for j, char in enumerate(string):
        if j >= n_spaces or char != ' ':
            return string[j:]
    else:
        return ''


def trim_tabs(doc_string):
    """Trim the extra space indentation off of a docstring."""
    doc_lines = doc_string.splitlines()

    try:
        index = next(i for i, line in enumerate(doc_lines[1:], 1) if line)
    except StopIteration:
        return doc_string

    try:
        num_spaces = next(
            j
            for j, char in enumerate(doc_lines[index])
            if char != ' '
        )
    except StopIteration:
        num_spaces = 0

    return '\n'.join(
        trim_first_n_spaces(line, num_spaces)
        for line in doc_lines
    )


class DocObject:
    """Python object to markdown helper. The initial name is inferred if not
    provided."""
    template_lines = [
        '{header} {name}',
        '*{type}*',
    ]
    header_level = 1
    _type = None

    def __new__(cls, object_, names=None, parent=None):
        if cls is DocObject:
            cls = cls.child_type(object_)

        return super().__new__(cls)

    def __init__(self, object_, names=None):
        if names is None:
            names = getattr(object_, '__name__', None)
            if names is None:
                raise TypeError('Missing keyword argument \'names\'')

        if isinstance(names, str):
            names = [names]

        self.members = {}
        self.object = object_
        self.names = names

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, value):
        self._names = value
        self.name = '.'.join(value)
        self.header_link = '#' + ''.join(value).lower()
        self.link = '[%s](%s)' % (self.name, self.header_link)
        self.link_chain = '.'.join(
            '[%s](#%s)' % (name, ''.join(value[:i]).lower())
            for i, name in enumerate(value, 1)
        )

    @property
    def format_data(self):
        return {
            'name': self.link_chain,
            'type': self.type,
            'doc': self.doc,
            'header': '#' * self.header_level,
        }

    @property
    def doc(self):
        doc = getattr(self.object, '__doc__', None) or ''

        if doc:
            doc = trim_tabs(doc)

        return doc

    @property
    def type(self):
        return self._type or self.__class__.__name__

    @type.setter
    def type(self, value):
        self._type = value

    @classmethod
    def child_type(cls, object_):
        """Return the corresponding documentation helper type of the given
        object."""
        # Fix isinstance signature and make abstraction for object_
        is_inst = _functools.partial(lambda o, *t: isinstance(o, (t)), object_)
        if is_inst(_types.FunctionType, _types.BuiltinFunctionType):
            return Function
        elif is_inst(_types.ModuleType):
            return Module
        elif is_inst(type):
            return (
                Exception
                if issubclass(object_, _builtins.Exception)
                else Class
            )
        elif is_inst(staticmethod):
            return StaticMethod
        elif is_inst(classmethod):
            return ClassMethod
        else:
            return DocObject

    def new_child(self, name, object_):
        return DocObject(object_, self.names + [name])

    def __iter__(self):
        yield self

        for name, child_obj in self.members.items():
            child_type = self.child_type(child_obj)

            if child_type is not DocObject:
                yield from self.new_child(name, child_obj)

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        return '%s.%s(%r, names=%r)' % (module, name, self.object, self.names)

    def __str__(self):
        return '\n\n'.join(
            '\n\n'.join(
                line.format(**obj.format_data)
                for line in obj.template_lines
            )
            for obj in self
        )


class Function(DocObject):
    """Python function documentation helper"""
    header_level = 3
    template_lines = DocObject.template_lines + [
        '```python\n{signature}\n```',
        '{doc}',
    ]

    @property
    def signature(self):
        return 'f()'

    @property
    def format_data(self):
        data = super().format_data
        data.update({
            'signature': self.signature,
        })
        return data


class Method(Function):
    """Method function documentation helper"""

    def __init__(self, object_, names=None, parent=None):
        super().__init__(object_, names=names)
        self.parent = parent

        if self.parent is not None:
            self.type += ' of class %s' % self.parent.link

    @property
    def doc_data(self):
        return {
            'self': '[`self`](%s)' % self.parent.header_link,
        }

    @property
    def doc(self):
        return super().doc.format(**self.doc_data)


class StaticMethod(Method):
    _type = 'Static Method'

    def __new__(cls, static_method, names=None, parent=None):
        return super().__new__(
            cls, static_method.__func__, names=names, parent=parent
        )

    def __init__(self, static_method, names=None, parent=None):
        super().__init__(static_method.__func__, names=names, parent=parent)


class ClassMethod(StaticMethod):
    _type = 'Class Method'


class Module(DocObject):
    header_level = 1
    template_lines = DocObject.template_lines + ['{doc}']

    def __init__(self, module, names=None):
        super().__init__(module, names=names)
        all_ = getattr(module, '__all__', None)

        if all_ is None:
            all_ = [
                name
                for name in vars(module).keys()
                if not name.startswith('_')
            ]

        self.members = {
            name: getattr(module, name, None)
            for name in all_
        }


class Class(DocObject):
    """Class doc helper"""
    header_level = 2
    template_lines = DocObject.template_lines + ['{doc}']

    def __init__(self, class_, names=None):
        super().__init__(class_, names=names)
        self.members = {
            name: obj
            for name, obj in vars(class_).items()
            if not name.startswith('_')
        }

    @classmethod
    def child_type(cls, object_):
        child_type = super().child_type(object_)

        if child_type is Function:
            return Method
        else:
            return child_type

    def new_child(self, name, object_):
        args = object_, self.names + [name]
        child_type = self.child_type(object_)

        if issubclass(child_type, Method):
            return child_type(*args, self)
        else:
            return child_type(*args)


class Exception(Class):
    pass


def main():
    import importlib
    import sys
    module = importlib.import_module(sys.argv[1])
    print(DocObject(module))


if __name__ == '__main__':
    main()
