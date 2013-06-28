"""
The runtime functions like an air traffic controller, knitting
together the various language modules to create a context for running
some code
"""

from __future__ import print_function

import re
import os
import sys
import cmd
import traceback
import argparse

import lispy.dialects.haney.special_forms
from lispy.dialects.norvig import read_from, tokenize, eval
from lispy.dialects.norvig.scope import Scope, add_globals


def read(s):
    "Read a Scheme expression from a string."
    return read_from(tokenize(s))


def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return '('+' '.join(map(to_string, exp))+')' if isinstance(exp, list) else str(exp)


class Repl(cmd.Cmd):
    prompt = "lispy> "

    def __init__(self, runtime=None, *args, **kwargs):
        self.runtime = runtime
        cmd.Cmd.__init__(self, *args, **kwargs)

    def default(self, line):
        print(self.runtime.eval(line))


class Runtime(object):
    """
    Lispy requires a bit of bootstrapping to get going, setting up
    special forms from multiple dialects, creating a global scope to
    run in, and then calling eval on statements either interactively
    or as a part of a script. This class takes care of the creation of
    a Runtime
    """

    def __init__(self, special_forms=None):
        """
        Initialize a runtime context.

        special_forms: should be a class that inherits from the dict module (or just be a dict)

        """

        # spcial forms may be passed in, or read from the environment,
        # by default they're the Haney combination of default dialects
        if special_forms is None:
            special_forms = os.environ.get("LISPY_SPECIAL_FORMS_CLASS")
            if special_forms is None:
                special_forms = lispy.dialects.haney.special_forms.SPECIAL_FORMS

        self.special_forms = special_forms

        self.global_env = add_globals(Scope(), special_forms=special_forms)

    def repl(self, prompt='lis.py> '):
        "A prompt-read-eval-print loop"
        Repl(runtime=self).cmdloop()

    def read_file(self, file):
        """
        grab the individual pieces of code from a file (the complete
        s-expressions) and evaluate them syncronously
        """
        return self.eval(file.read())

    def eval(self, str_):
        ## preprocess

        # Remove hash comments so we can support hashbangs
        str_ = re.sub("\#.*", "\n", str_)

        # Remove lisp style comments
        str_ = re.sub(";.*", "\n", str_)

        # wrap everything in an implicit begin statement
        str_ = "(begin {})".format(str_)


        try:
            return eval(read(str_), env=self.global_env)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
