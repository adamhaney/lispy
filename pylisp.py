#!/usr/bin/python

import sys

__global_scope__ = {}

def echo(str):
    """
    Creates a print like function for testing. Temporary until I write
    better parsing.
    """
    print str


def let(k, v, scope=None):
    """
    Implements setting variables
    """
    if scope is None:
        scope = __global_scope__

    scope[k] = v


def get_variable(k, scope=None):
    """
    Gets a variable from the given scope, failing that it looks to the
    global scope
    """
    if scope is None:
        scope = __global_scope__

    try:

        # Check local scope
        return scope[k]

    except KeyError:
        try:

            # Check global scope
            return __global_scope__[k]
        except KeyError:
            try:
                # Check python
                return eval(k)
            except NameError:
                raise NameError(
                    "{}, not available in current scope".format(k)
                    )

def pylisp_eval(statement):
    """
    Expects a statement wrapped in parens (arbitrarily nested)
    """
    tokens = statement[1:-1].split(" ")

    func_str = tokens[0]

    func = get_variable(func_str)


    values = []
    for evaluatable_piece in tokens[1:]:
        if evaluatable_piece[0] == "(":
            value = pylisp_eval(evaluatable_piece)
        else:
            value = get_variable(evaluatable_piece)
        values.append(value)

    return func(*values)
    

if "__main__" == __name__:
    for statement in sys.stdin.read().split("\n"):
        pylisp_eval(statement)
