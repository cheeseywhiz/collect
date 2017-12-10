import builtins as _builtins
import collections as _collections
import functools as _functools
import inspect as _inspect
import types as _types


class DocObject:
    """Python object to markdown helper. The initial name is inferred if not
    provided."""
    header_level = 1
    _type = None

    def __new__(cls, object_, *args, names=None, **kwargs):
        if cls is DocObject:
            cls = cls.child_type(object_)

        return super().__new__(cls)

    def __init__(self, object_, *args, names=None, **kwargs):
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
    def template_lines(self):
        """The template of each object."""
        return _collections.OrderedDict([
            ('header', '{header} {name}'),
            ('type', '*{type}*'),
        ])

    @property
    def names(self):
        """The list of names up to this object in the hierarchy."""
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
        """The dict of information sent to the template."""
        return {
            'name': self.link_chain,
            'type': self.type,
            'header': '#' * self.header_level,
        }

    @property
    def type(self):
        """The subtitle of the object indicating what is is."""
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

    def new_child(self, object_, name):
        """Return a new doc helper object that is a child of {self} within the
        hierarchy."""
        return DocObject(object_, names=self.names + [name])

    def __iter__(self):
        yield self

        for name, child_obj in self.members.items():
            child_type = self.child_type(child_obj)

            if child_type is not DocObject:
                yield from self.new_child(child_obj, name)

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        return '%s.%s(%r, names=%r)' % (module, name, self.object, self.names)

    def __str__(self):
        return '\n\n'.join(
            line.format(**self.format_data)
            for line in self.template_lines.values()
        )

    def str_all(self):
        return '\n\n'.join(
            str(obj)
            for obj in self
        )


class ClassMemberMix(DocObject):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.type += ' of class %s' % self.parent.link

    @property
    def doc_data(self):
        data = super().doc_data
        data.update(self='[`self`](%s)' % self.parent.header_link)
        return data


class DocStringMix(DocObject):
    @staticmethod
    def trim_first_n_spaces(string, n_spaces):
        for j, char in enumerate(string):
            if j >= n_spaces or char != ' ':
                return string[j:]
        else:
            return ''

    @staticmethod
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
            return doc_string

        return '\n'.join(
            DocStringMix.trim_first_n_spaces(line, num_spaces)
            for line in doc_lines
        )

    @property
    def template_lines(self):
        lines = super().template_lines

        if self.doc:
            lines = lines.copy()
            lines.update(doc='{doc}')

        return lines

    @property
    def format_data(self):
        data = super().format_data.copy()
        data.update(doc=self.doc)
        return data

    @property
    def doc_data(self):
        """The dict of information available to user docstrings."""
        return {}

    @property
    def doc(self):
        """The object's docstring with removed indentation and formatted with
        doc_data."""
        doc = getattr(self.object, '__doc__', None) or ''

        if doc:
            doc = DocStringMix.trim_tabs(doc)

        return doc.format(**self.doc_data)


class CallableMix(DocObject):
    @property
    def template_lines(self):
        lines = super().template_lines.copy()
        lines.update(signature='```python\n{signature}\n```')
        return lines

    @property
    def signature(self):
        """The call signature of the object."""
        try:
            sig = str(_inspect.signature(self.object))
        except ValueError:
            sig = '(...)'

        return '{name}{sig}'.format(sig=sig, name=self.name)

    @property
    def format_data(self):
        data = super().format_data.copy()
        data.update(signature=self.signature)
        return data


class DocCallableMix(DocStringMix, CallableMix):
    # because order is significant
    pass


class Function(DocCallableMix):
    header_level = 3


class Method(ClassMemberMix, Function):
    pass


class InitDunderFunc(DocObject):
    def __new__(cls, object_, *args, **kwargs):
        return super().__new__(cls, object_.__func__, *args, **kwargs)

    def __init__(self, object_, *args, **kwargs):
        super().__init__(object_.__func__, *args, **kwargs)


class StaticMethod(InitDunderFunc, Method):
    _type = 'Static Method'


class ClassMethod(InitDunderFunc, Method):
    _type = 'Class Method'


class Module(DocStringMix):
    header_level = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_ = getattr(self.object, '__all__', None)

        if all_ is None:
            all_ = [
                name
                for name in vars(self.object).keys()
                if not name.startswith('_')
            ]

        self.members = {
            name: getattr(self.object, name, None)
            for name in all_
        }


class Class(DocCallableMix):
    header_level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.members = {
            name: obj
            for name, obj in vars(self.object).items()
            if not name.startswith('_')
        }

    @classmethod
    def child_type(cls, object_):
        if _inspect.isdatadescriptor(object_):
            return DataDescriptor

        child_type = super().child_type(object_)

        if child_type is Function:
            return Method
        else:
            return child_type

    def new_child(self, object_, name):
        args = object_,
        kwargs = dict(names=super().names + [name])
        child_type = self.child_type(object_)

        if issubclass(child_type, ClassMemberMix):
            return child_type(*args, **kwargs, parent=self)
        else:
            return child_type(*args, **kwargs)


class Exception(Class):
    pass


class DataDescriptor(ClassMemberMix, DocStringMix):
    _type = 'Data Descriptor'
    header_level = 4


def main():
    import importlib
    import sys
    module = importlib.import_module(sys.argv[1])
    print(DocObject(module).str_all())


if __name__ == '__main__':
    main()
