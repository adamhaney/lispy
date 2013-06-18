#!/usr/bin/python

import re
import sys

__global_scope__ = {}


def echo(str):
    """
    Creates a print like function for testing. Temporary until I write
    better parsing.
    """
    print str

def add(lhs, rhs):
    return lhs + rhs

def subtract(lhs, rhs):
    return lhs - rhs

def multiply(lhs, rhs):
    return lhs * rhs

def divide(lhs, rhs):
    return lhs / rhs

def pow(lhs, rhs):
    return lhs**rhs

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


def lispy_eval(statement):
    """
    Expects a statement wrapped in parens (arbitrarily nested)
    """
    symbol, arguments = statement[1:].split(' ')

    for char in ''.join(arguments):
        
        

if "__main__" == __name__:
    for statement in sys.stdin.read().split("\n"):
        print pylisp_eval(statement)
