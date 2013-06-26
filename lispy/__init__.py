"""
Lispy

The main point of entry for lis.py, this file includes code to
start the runtime. It should not include implementation
details for parsing, scoping, special forms or types
"""

from runtime import Runtime

def repl():
    Runtime().repl()

if "__main__" == __name__:
    Runtime().repl()
