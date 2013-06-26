"""
Lispy

The main point of entry for lis.py, this file includes code to
bootstrap the scripting language. It should not include implementation
details for parsing, scoping, special forms or types
"""
import sys
import traceback
import argparse

from lispy.dialects.norvig import read_from, tokenize, eval
from lispy.dialects.norvig.scope import Scope, add_globals
from lispy.dialects.norvig.special_forms import SPECIAL_FORMS as NORVIG_FORMS
from lispy.dialects.pybuiltins.special_forms import SPECIAL_FORMS as PYBUILTIN_FORMS


def read(s):
    "Read a Scheme expression from a string."
    return read_from(tokenize(s))


def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return '('+' '.join(map(to_string, exp))+')' if isinstance(exp, list) else str(exp)


def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop"

    special_forms = NORVIG_FORMS
    special_forms.update(PYBUILTIN_FORMS)

    global_env = add_globals(Scope(), special_forms=special_forms)

    while True:
        try:
            val = eval(read(raw_input(prompt)), env=global_env)
            if val is not None: print(to_string(val))
        except Exception, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

if "__main__" == __name__:
    

    repl()
