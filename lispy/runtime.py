"""
The runtime functions like an air traffic controller, knitting
together the various language modules to create a context for running
some code
"""

from __future__ import print_function

import os
import sys
import cmd
import traceback
from io import StringIO

from .dialects.norvig.scope import Scope, add_globals
from .dialects.norvig import eval, InPort, parse
from .dialects.norvig import EOF_OBJECT
from .dialects.norvig.parse import to_string


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

        special_forms: should be a class that inherits from the dict
        module (or just be a dict)

        """

        # spcial forms may be passed in, or read from the environment,
        # by default they're the norvig combination of default dialects
        if special_forms is None:
            special_forms = os.environ.get("LISPY_SPECIAL_FORMS_CLASS")
            if special_forms is None:
                from .dialects.norvig.special_forms import SPECIAL_FORMS
                special_forms = SPECIAL_FORMS

        self.special_forms = special_forms

        self.global_env = add_globals(Scope(), special_forms=special_forms)

    def repl(
        self,
        prompt='lispy> ',
        inport=InPort(sys.stdin),
        out=sys.stdout,
        err=sys.stderr,
        return_value=False
    ):
        "A prompt-read-eval-print loop."
        if out is None:
            out = StringIO()

        if err is None:
            err = StringIO()

        while True:
            try:
                if prompt:
                    sys.stderr.write(prompt)
                x = parse(inport)
                if x is EOF_OBJECT:
                    return
                val = eval(x)
                if val is not None and out and return_value is False:
                    err.write(to_string(val) + "\n")
                    err.flush()
                elif return_value:
                    return val
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)

    def read_file(self, file):
        """
        grab the individual pieces of code from a file (the complete
        s-expressions) and evaluate them syncronously
        """
        self.repl(None, InPort(file), None)

    def eval(self, expression, out=None, err=None):
        """
        Evaluate a string as a lispy program and return its value
        """
        return self.repl(
            None,
            InPort(StringIO(unicode(expression))),
            out,
            err,
            return_value=True
        )
