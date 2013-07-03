"""
Lispy

The main point of entry for lis.py, this file includes code to
start the runtime. It should not include implementation
details for parsing, scoping, special forms or types
"""

from __future__ import print_function

import argparse

from .runtime import Runtime


def cli():
    """
    The function that console_scripts points to for command line
    evaluation
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'infile',
        help="A lispy program to read from a script file",
        nargs='?',
        type=argparse.FileType('r'),
        default=None
    )
    parser.add_argument('-c', help="lispy program passed in as a string")

    args = parser.parse_args()

    if args.infile:
        Runtime().read_file(args.infile)
    elif args.c:
        print(Runtime().eval(args.c))
    else:
        Runtime().repl()

if "__main__" == __name__:
    cli()
