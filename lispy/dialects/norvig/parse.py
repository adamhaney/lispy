from .symbols import Symbol


def to_string(x):
    "Convert a Python object back into a Lisp-readable string."
    if x is True:
        return "#t"
    elif x is False:
        return "#f"
    elif isinstance(x, Symbol):
        return x
    elif isinstance(x, str):
        return '"%s"' % x.encode('string_escape').replace('"', r'\"')
    elif isinstance(x, list):
        return '('+' '.join(list(map(to_string, x)))+')'
    elif isinstance(x, complex):
        return str(x).replace('j', 'i')
    else:
        return str(x)
