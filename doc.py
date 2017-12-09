import types as _types
import builtins as _builtins


class DocObject:
    """Python object to markdown helper. The initial name is inferred if not
    provided."""
    template = '''\
{header} {name}

*{type}*

{doc}'''
    header_level = 1

    def __new__(cls, object_, names=None, parent=None):
        if cls is DocObject:
            obj_class = DocObject.obj_class(parent, object_)

            if obj_class is not None:
                return object.__new__(obj_class)

        return object.__new__(cls)

    def __init__(self, object_, names=None, **kwargs):
        if names is None:
            names = getattr(object_, '__name__', None)
            if names is None:
                raise TypeError('Missing keyword argument \'names\'')

        if isinstance(names, str):
            names = [names]

        self.members = {}
        self._doc = None
        self.names = names
        self.name = '.'.join(names)
        self.object = object_
        self.format_data = {
            'name': self.links(self.names),
            'type': self.__class__.__name__,
            'doc': self.doc,
            'header': '#' * self.header_level,
        }

    @property
    def doc(self):
        if self._doc is not None:
            return self._doc

        doc = getattr(self.object, '__doc__', None)

        if doc is None:
            doc = ''
        elif doc:
            doc += '\n' * 2

        self.doc = doc
        return doc

    @doc.setter
    def doc(self, value):
        self._doc = value

    def obj_class(self, object_):
        if isinstance(object_, (
            _types.FunctionType, _types.BuiltinFunctionType
        )):
            return Method if isinstance(self, Class) else Function
        elif isinstance(object_, _types.ModuleType):
            return Module
        elif isinstance(object_, type):
            return (
                Exception
                if _builtins.BaseException in object_.__bases__ else
                Class
            )
        else:
            return

    @staticmethod
    def links(names):
        parts = []

        for i, name in enumerate(names, 1):
            link = ''.join(names[:i]).lower()
            parts.append('[%s](#%s)' % (name, link))

        return '.'.join(parts)

    def __iter__(self):
        yield self

        for name, child_obj in self.members.items():
            child_doc = DocObject(child_obj, self.names + [name], parent=self)

            if type(child_doc) is DocObject:
                continue

            yield from child_doc

    def __repr__(self):
        cls = self.__class__
        module = cls.__module__
        name = cls.__name__
        return '%s.%s(%r, names=%r)' % (module, name, self.object, self.names)

    def __str__(self):
        return ''.join(
            self.template.format(**obj.format_data)
            for obj in self
        )


class Function(DocObject):
    """Python function documentation helper"""
    header_level = 3


class Method(DocObject):
    """Method function documentation helper"""
    header_level = 3


class Module(DocObject):
    header_level = 1

    def __init__(self, module, names=None, **kwargs):
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

    def __init__(self, class_, names=None, **kwargs):
        super().__init__(class_, names=names)
        self.members = {
            name: obj
            for name, obj in vars(class_).items()
            if not name.startswith('_')
        }


class Exception(Class):
    pass


def main():
    import importlib
    import sys
    module = importlib.import_module(sys.argv[1])
    print(str(DocObject(module)).strip())


if __name__ == '__main__':
    main()
