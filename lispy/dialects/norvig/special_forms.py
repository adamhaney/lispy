import sys
import operator

from .symbols import *
from .parse import to_string


def readchar(inport):
    "Read the next character from an input port."
    if inport.line != '':
        ch, inport.line = inport.line[0], inport.line[1:]
        return ch
    else:
        return inport.file.read(1) or EOF_OBJECT


def cons(x, y):
    return [x]+y


def is_pair(x):
    return x != [] and isinstance(x, list)


def callcc(proc):
    "Call proc with current continuation; escape only"
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer")

    def throw(retval):
        ball.retval = retval
        raise ball

    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball:
            return ball.retval
        else:
            raise w


def read(inport):
    "Read a Scheme expression from an input port."
    def read_ahead(token):
        if '(' == token:
            L = []
            while True:
                token = inport.next_token()
                if token == ')':
                    return L
                else:
                    L.append(read_ahead(token))
        elif ')' == token:
            raise SyntaxError('unexpected )')
        elif token in QUOTES:
            return [QUOTES[token], read(inport)]
        elif token is EOF_OBJECT:
            raise SyntaxError('unexpected EOF in list')
        else:
            return atom(token)
    # body of read:
    token1 = inport.next_token()
    return EOF_OBJECT if token1 is EOF_OBJECT else read_ahead(token1)


def display(x, port=sys.stdout):
    return port.write(x if isinstance(x, str) else to_string(x) + "\n")

SPECIAL_FORMS = {
    '+': lambda *args: reduce(operator.add, args),
    '+': operator.add,
    '-': operator.sub,
    '*': lambda *args: reduce(operator.mul, args),
    '/': operator.div,
    'not': operator.not_,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '=': operator.eq,
    'equal?': operator.eq,
    'eq?': operator.is_,
    'length': len,
    'cons': cons,
    'car': lambda x: x[0],
    'cdr': lambda x: x[1:],
    'append': operator.add,
    'list': lambda *x: list(x),
    'list?': lambda x: isinstance(x, list),
    'null?': lambda x: x == [],
    'symbol?': lambda x: isinstance(x, Symbol),
    'boolean?': lambda x: isinstance(x, bool),
    'pair?': is_pair,
    'port?': lambda x: isinstance(x, file),
    'apply': lambda proc, l: proc(*l),
    'eval': lambda x: eval(expand(x)),
    'load': lambda fn: load(fn),
    'call/cc': callcc,
    'open-input-file': open,
    'close-input-port': lambda p:  p.file.close(),
    'open-output-file': lambda f: open(f, 'w'),
    'close-output-port': lambda p:  p.close(),
    'eof-object?': lambda x: x is EOF_OBJECT,
    'read-char': readchar,
    'read': read,
    'write': lambda x, port=sys.stdout: port.write(to_string(x)),
    'display': display,
    'exit':  exit
}
