from __future__ import print_function

NORVIG_FORMS = {
    '+':operator.add,
    '-':operator.sub,
    '*':operator.mul,
    '/':operator.div,
    'not':operator.not_,
    '>':operator.gt,
    '<':operator.lt,
    '>=':operator.ge,
    '<=':operator.le,
    '=':operator.eq, 
    'equal?':operator.eq,
    'eq?':operator.is_,
    'length':len,
    'cons':lambda x,y:[x]+y,
    'car':lambda x:x[0],
    'cdr':lambda x:x[1:],
    'append':operator.add,  
    'list':lambda *x:list(x),
    'list?': lambda x:isa(x,list), 
    'null?':lambda x:x==[],
    'symbol?':lambda x: isa(x, Symbol),
}

# Grabbing python builtins into lispy, intentionally excluding some of the builtins for now
PYTHON_BUILTIN_FORMS = {
    'exit': exit,
    'abs': lambda x: abs(x),
    'all': lambda x: all(x),
    'any': lambda x: any(x),
    'bin': lambda x: bin(x),
    'bool': lambda x: bool(x),
    'bytearray': lambda x: bytearray(x),
    'callable': lambda x: callable(x),
    'chr': lambda x: chr(x),
    'classmethod': lambda x: classmethod(x),
    'cmp': lambda x, y: cmp(x, y),
    'compile': lambda source, filename, mode, *args, **kwargs: compile(source, filename, mode, *args, **kwargs),
    'complex': lambda *args, **kwargs: complex(*args, **kwargs),
    'delattr': lambda obj, name: delattr(obj, name),
    'dict': lambda *args, **kwargs: dict(*args, **kwargs),
    'dir': lambda *args: dir(*args),
    'divmod': lambda a, b: divmod(a, b),
    'enumerate': lambda sequence, *args, **kwargs: enumerate(sequence, *args, **kwargs),
    # intentionally excluding eval for now
    # intentionally excluding execfile for now
    'file': lambda name, *args, **kwargs: file(name, *args, **kwargs),
    # intentionally excluding filter right now as we may want it built into lispy
    'float': lambda x: float(x),
    'format': lambda value, *args, **kwargs: format(value, *args, **kwargs),
    'frozenset': lambda x: frozenset(x),
    'getattr': lambda x: obj, name, *args, **kwargs: getattr(obj, name, *args, **kwargs),
    'globals': globals,
    'hasattr': lambda obj, name: hasattr(obj, name),
    'hash': lambda x: hash(x),
    'help': lambda *args, **kwargs: help(*args, **kwargs),
    'hex': lambda x: hex(x),
    'id': lambda x: id(x),
    'int': lambda x, *args, **kwargs: int(x, *args, **kwargs),
    'isinstance': lambda obj, classinfo: isinstance(obj, classinfo),
    'issubclass': lambda class, classinfo: issubclass(class, classinfo),
    'iter': lambda o, *args, **kwargs: iter(o, *args, **kwargs),
    # length is included in norvig scheme
    # list is included in norvig scheme
    'locals': locals,
    'long': lambda x, *args, **kwargs: long(x, *args, **kwargs),
    # intentionally excluding map until we determine how maps will work in lispy
    'max': lambda *args, **kwargs: max(*args, **kwargs),
    'memoryview': lambda x: memoryview(x),
    'min': lambda *args, **kwargs: min(*args, **kwargs),
    'next': lambda iterator, *args, **kwargs: next(iterator, *args, **kwargs),
    'object': object,
    'oct': lambda x: oct(x),
    'open': lambda name, *args, **kwargs: open(name, *args, **kwargs),
    'ord': lambda c: ord(c),
    'pow': lambda x, y, *args, **kwargs: pow(x, y, *args, **kwargs),
    'print': lambda x: print(x),
    'range': lambda *args, **kwargs: range(*args, **kwargs),
    'raw_input': lambda *args, **kwargs: raw_input(*args, **kwargs),
    # intentionally excluding reduce until we decide how to include it in the language
    'repr': lambda x: repr(x),
    'reversed': lambda sequence: reveresed(sequence),
    'round': lambda number, *args, **kwargs: round(number, *args, **kwargs),
    'set': lambda iterable: set(iterable),
    'setattr': lambda obj, name, value: setattr(obj, name, value),
    'slice': lambda *args, **kwargs: slice(*args, **kwargs),
    'sorted': lambda iterable, *args, **kwargs: sorted(iterable, *args, **kwargs),
    'str': lambda object: str(object),
    'sum': lambda iterable, *args, **kwargs: sum(iterable, *args, **kwargs),
    'super': lambda type, *args, **kwargs: super(type, *args, **kwargs),
    'tuple': lambda iterable: tuple(iterable),
    'type': lambda *args, **kwargs: type(*args, **kwargs),
    'unichr': lambda i: unichr(i),
    'unicode': lambda *args, **kwargs: unicode(*args, **kwargs),
    'vars': lambda object: vargs(object),
    'xrange': lambda *args, **kwargs: xrange(*args, **kwargs),
    'zip': lambda *args, **kwargs: zip(*args, **kwargs)
}
