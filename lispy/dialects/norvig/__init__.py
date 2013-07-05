############### Scheme Interpreter in Python

## (c) Peter Norvig, 2010; See http://norvig.com/lispy2.html

################ Symbol, Procedure, classes

from __future__ import division
import re
import sys
from io import StringIO

from .scope import Scope, add_globals
from .symbols import Symbol, SYMBOLS, EOF_OBJECT
from .special_forms import is_pair, read, cons
from .parse import to_string

TOKEN_REGEX = r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)"""


class Procedure(object):
    "A user-defined Scheme procedure."

    def __init__(self, parms, exp, env):
        self.parms, self.exp, self.env = parms, exp, env

    def __call__(self, *args):
        return eval(self.exp, Scope(self.parms, args, self.env))

################ parse, read, and user interaction


def parse(inport):
    "Parse a program: read and expand/error-check it."
    # Backwards compatibility: given a str, convert it to an InPort
    if isinstance(inport, str):
        if sys.version_info[0] < 3:
            inport = unicode(inport)

        inport = InPort(StringIO(inport))

    return expand(read(inport), toplevel=True)


class InPort(object):
    "An input port. Retains a line of chars."
    tokenizer = TOKEN_REGEX

    def __init__(self, file):
        self.file = file
        self.line = ''

    def next_token(self):
        "Return the next token, reading new text into line buffer if needed."
        while True:
            if self.line == '':
                self.line = self.file.readline()
            if self.line == '':
                return EOF_OBJECT
            token, self.line = re.match(InPort.tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                return token


################ Environment class

global_env = add_globals(Scope())

################ eval (tail recursive)


def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    while True:
        if isinstance(x, Symbol):       # variable reference
            return env.find(x)[x]
        elif not isinstance(x, list):   # constant literal
            return x
        elif x[0] is SYMBOLS["QUOTE"]:     # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] is SYMBOLS["IF"]:        # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = (conseq if eval(test, env) else alt)
        elif x[0] is SYMBOLS["SET!"]:       # (set! var exp)
            (_, var, exp) = x
            env.find(var)[var] = eval(exp, env)
            return None
        elif x[0] is SYMBOLS["DEFINE"]:    # (define var exp)
            (_, var, exp) = x
            env[var] = eval(exp, env)
            return None
        elif x[0] is SYMBOLS["LAMBDA"]:    # (lambda (var*) exp)
            (_, vars, exp) = x
            return Procedure(vars, exp, env)
        elif x[0] is SYMBOLS["BEGIN"]:     # (begin exp+)
            for exp in x[1:-1]:
                eval(exp, env)
            x = x[-1]
        else:                    # (proc exp*)
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            if isinstance(proc, Procedure):
                x = proc.exp
                env = Scope(proc.parms, exps, proc.env)
            else:
                return proc(*exps)

################ expand


def expand(x, toplevel=False):
    "Walk tree of x, making optimizations/fixes, and signaling SyntaxError."
    require(x, x != [])                    # () => Error
    if not isinstance(x, list):                 # constant => unchanged
        return x
    elif x[0] is SYMBOLS["QUOTE"]:                 # (quote exp)
        require(x, len(x) == 2)
        return x
    elif x[0] is SYMBOLS["IF"]:
        if len(x) == 3:
            x = x + [None]     # (if t c) => (if t c None)
        require(x, len(x) == 4)
        return list(map(expand, x))
    elif x[0] is SYMBOLS["SET!"]:
        require(x, len(x) == 3)
        var = x[1]                       # (set! non-var exp) => Error
        require(x, isinstance(var, Symbol), "can set! only a symbol")
        return [SYMBOLS["SET!"], var, expand(x[2])]
    elif x[0] is SYMBOLS["DEFINE"] or x[0] is SYMBOLS["DEFINE-MACRO"]:
        require(x, len(x) >= 3)
        _def, v, body = x[0], x[1], x[2:]
        if isinstance(v, list) and v:           # (define (f args) body)
            f, args = v[0], v[1:]        # => (define f (lambda (args) body))
            return expand([_def, f, [SYMBOLS["LAMBDA"], args]+body])
        else:
            require(x, len(x) == 3)        # (define non-var/list exp) => Error
            require(x, isinstance(v, Symbol), "can define only a symbol")
            exp = expand(x[2])
            if _def is SYMBOLS["DEFINE-MACRO"]:
                require(x, toplevel, "define-macro only allowed at top level")
                proc = eval(exp)
                require(x, callable(proc), "macro must be a procedure")
                macro_table[v] = proc    # (define-macro v proc)
                return None              # => None; add v:proc to macro_table
            return [SYMBOLS["DEFINE"], v, exp]
    elif x[0] is SYMBOLS["BEGIN"]:
        if len(x) == 1:
            return None        # (begin) => None
        else:
            return [expand(xi, toplevel) for xi in x]
    elif x[0] is SYMBOLS["LAMBDA"]:                # (lambda (x) e1 e2)
        require(x, len(x) >= 3)            # => (lambda (x) (begin e1 e2))
        vars, body = x[1], x[2:]
        require(x,
                (isinstance(vars, list)
                 and all(isinstance(v, Symbol) for v in vars))
                or isinstance(vars, Symbol), "illegal lambda argument list")
        exp = body[0] if len(body) == 1 else [SYMBOLS["BEGIN"]] + body
        return [SYMBOLS["LAMBDA"], vars, expand(exp)]
    elif x[0] is SYMBOLS["QUASIQUOTE"]:            # `x => expand_quasiquote(x)
        require(x, len(x) == 2)
        return expand_quasiquote(x[1])
    elif isinstance(x[0], Symbol) and x[0] in macro_table:
        return expand(macro_table[x[0]](*x[1:]), toplevel)  # (m arg...)
    else:                                # => macroexpand if m isinstance macro
        return list(map(expand, x))            # (f arg...) => expand each


def require(x, predicate, msg="wrong length"):
    "Signal a syntax error if predicate is false."
    if not predicate:
        raise SyntaxError(to_string(x)+': '+msg)


def expand_quasiquote(x):
    """Expand `x => 'x; `,x => x; `(,@x y) => (append x y) """
    if not is_pair(x):
        return [SYMBOLS["QUOTE"], x]
    require(x, x[0] is not SYMBOLS["UNQUOTE-SPLICING"], "can't splice here")
    if x[0] is SYMBOLS["UNQUOTE"]:
        require(x, len(x) == 2)
        return x[1]
    elif is_pair(x[0]) and x[0][0] is SYMBOLS["UNQUOTE-SPLICING"]:
        require(x[0], len(x[0]) == 2)
        return [SYMBOLS["APPEND"], x[0][1], expand_quasiquote(x[1:])]
    else:
        return [
            SYMBOLS["CONS"],
            expand_quasiquote(x[0]),
            expand_quasiquote(x[1:])
        ]


def let(*args):
    args = list(args)
    x = cons(SYMBOLS["LET"], args)
    require(x, len(args) > 1)
    bindings, body = args[0], args[1:]
    require(x, all(
            isinstance(b, list) and len(b) == 2 and isinstance(b[0], Symbol)
            for b in bindings), "illegal binding list")
    vars, vals = zip(*bindings)
    return [
        [SYMBOLS["LAMBDA"],
         list(vars)]+ list(map(expand, body))] + list(map(expand, vals))

macro_table = {SYMBOLS["LET"]: let}  # More macros can go here

eval(parse("""(begin
(define-macro and (lambda args
   (if (null? args) #t
       (if (= (length args) 1) (car args)
           `(if ,(car args) (and ,@(cdr args)) #f)))))

;; More macros can also go here

)"""))
