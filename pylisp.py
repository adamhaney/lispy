#!/usr/bin/python

import sys

def echo(str):
    print str

def str2primative(primative_str):
    """
    Takes a python primative presented as a string and returns the
    appropriate python object
    """
    return eval(primative_str)


def str2function(func_str):
    """
    Searches code defined in the file and python code to find the
    function referenced by this name
    """
    return eval(func_str)

def pylisp_eval(code):
    """
    Expects a code snipet wrapped in parens (arbitrarily nested)
    """
    pieces = code[1:-1].split(" ")

    func_str = pieces[0]

    func = str2function(func_str)


    values = []
    for evaluatable_piece in pieces[1:]:
        if evaluatable_piece[0] == "(":
            value = pylisp_eval(evaluatable_piece)
        else:
            value = str2primative(evaluatable_piece)
        values.append(value)

    return func(*values)
    

if "__main__" == __name__:
    pylisp_eval(sys.stdin.read())
