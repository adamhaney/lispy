lispy
=====

An extension of Peter Norvig's lispy (http://norvig.com/lispy.html)
which includes the ability to access symbols from python packages as
if they were written in lispy.

This experiment was initially intended to let me play with scheme while
still having access to python's batteries.

Getting Started
---------------

To start hacking with the latest "stable" (we're being very liberal
with english here) version of lispy you simply need to

    $ pip install lispy
    $ lispy

This will open a lispy repl, for more commandline options run

    $ lispy --help


By default Lispy uses a scheme dialect as described by Peter Norvig in
his minimalist implementation of scheme (http://norvig.com/lispy.html)
once you've familiarized yourself with this implementation you're
ready for some of the "cool" stuff we've layered on top of Norvig's
implementation.

Lispy can access any python module in python environment it's run from
(note that lispy can also be run from inside a virtual environment,
though that's not well documented yet, you can reach out to me or open
an issue if you'd like help with this). In order to access a function
or library from a python module simply call it using the colon symbol
notation.

    > (print os:environ)

Also in order to eval a bit of python code (to for example access the
builtin python functions) simply namespace the function name with py:

    > (py:getattr datetime:datetime "now")

is equivalent to

    >>> import datetime
    >>> datetime.datetime.now()



Motivation
----------

I've been writing a lot of python code, and I love the python
ecosystem. It has wonderful tools for web application development
(Django, Flask, Pyramid), data munging (Beautiful Soup, requests) and
data analysis (NumPy, SciPy, Pandas, IPython). I'd like to learn more
about the internal implementation of python, its introspection
abilities and its design decisions. I'd also like to better understand
the LISP ecosystem, what better way than implementing a LISP in
python.

Current Features
----------------

  - A minimal scheme implementation in Python (based on Peter Norvig's lispy)
  - A scheme implementation which can call python functions within the same process
  - The begining of a "dialect framework" which will allow customized
    lisp dialects with changes to the lanage implemented in either
    python or a lispy dialect


Architecture
------------

I'm doing my very best to keep this language rather sparse, but
configurable. There are many LISP dialiects and rather than start
bikeshedding wars about the way that this LISP on python should be
implemented I'd like to make language decisions configurable with
reasonable defaults. Because of this I've created the concept of
"dialects" currently there are two dialects the 'norvig' dialect which
tries to stay true to Peter Norvig's original implementation of LISP
in python and the "haney" dialiect which includes language additions
that I think are interesting.

As we add features to the language or pieces from other languages I
intend to also implement them as seperate dialects so that the
mechanics of parsing, scoping, and evaluation can be snapped together
to form a lisp that solves the problem at hand for a given
developer. This also has the added benefit of (potnentially) being
able to knit together lisp code written in many dialects together into
python (and Java using Jython).

A dialect is currently not very well defined, but it will include a
Scope object that determines scoping rules, an eval function or
object, and a SpecialForms object. It will also include a settings
variable that will list the class paths for the definitions of these
various components so a dialect that only needs to change a particular
aspect of the language can inherit from other dialects.

When a new language feature is added by me it wil attempt to follow
this loosely coupled pattern. This will, hopefully allow us to make
the language modular, and well tested enough that we can add language
features to solve domain specific problems better than other languages
(there are plans for work that would enable easier distributed systems
and parallel computing problem solving)

Goals
-----

This is currently a pet project to facilitate learning the LISP and
scheme ecosystems and to bring about a better understanding of the
theory and complexity of language design. My roadmap includes several
additions to lispy to make it a toolkit for python developers who
might be interested in dipping their toe in LISP. For functionality
that's left to be implemented please check the issue tracker for the
project at https://github.com/adamhaney/lispy/issues

Anti-Goals
----------

There are a few things this project is not aiming to achieve. While I
do want lispy to be able to run in python 2.x and 3.x I do not intend
to mask some of the differences between 2.x and 3.x namely the
different ways the two python branches handle math (in 2.x integer
division returns a truncated value, in 3.x it returns a float). Trying
to translate between these two design decisions is outside the scope
of this project.
