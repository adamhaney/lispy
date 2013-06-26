"""
Lispy: Scheme Interpreter in Python

(c) Peter Norvig, 2010; See http://norvig.com/lispy.html

"""

from __future__ import division

import importlib

from .special_forms import NORVIG_FORMS, PYTHON_BUILTIN_FORMS


Symbol = str

SPECIAL_FORMS = NORVIG_FORMS
SPECIAL_FORMS.update(PYTHON_BUILTIN_FORMS)

class Scope(dict):
    "A scope: a dict of {'var':val} pairs, with an outer Scope."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Scope where var appears."

        # If ':' in var add module to environment
        if ":" in var:
            namespace, attribute = var.split(":")
            module = importlib.import_module(namespace)

            module_funcs = {
                "{}:{}".format(namespace, k): attr
                for k, attr
                in vars(module).items()
            }
            self.update(module_funcs)
        try:
            return self if var in self else self.outer.find(var)
        except AttributeError:
            raise NameError("name '{}' is not defined".format(var))

def add_globals(env):
    "Add some Scheme standard procedures to an environment."
    env.update(SPECIAL_FORMS)
    return env

global_env = add_globals(Scope())


################ eval

def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):             # variable reference
        return env.find(x)[x]
    elif not isinstance(x, list):         # constant literal
        return x                
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        return eval((conseq if eval(test, env) else alt), env)
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var*) exp)
        (_, vars, exp) = x
        return lambda *args: eval(exp, Scope(vars, args, env))
    elif x[0] == 'begin':          # (begin exp*)
        for exp in x[1:]:
            val = eval(exp, env)
        return val
    else:                          # (proc exp*)
        exps = [eval(exp, env) for exp in x]
        proc = exps.pop(0)
        return proc(*exps)

################ parse, read, and user interaction

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
