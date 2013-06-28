lispy
=====

An extension of Peter Norvig's lispy (http://norvig.com/lispy.html)
which includes the ability to access symbols from python packages as
if they were written in lispy. 

This experiment was initially intended to let me play with scheme while
still having access to python's batteries.

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

Goals
-----

This is currently a pet project to facilitate learning the LISP and
scheme ecosystems and to bring about a better understanding of the
theory and complexity of language design. My roadmap includes several
additions to lispy to make it a toolkit for python developers who
might be interested in dipping their toe in LISP. For functionality
that's left to be implemented please check the issue tracker for the
project at https://github.com/adamhaney/lispy/issues

  - Implement reader macros
