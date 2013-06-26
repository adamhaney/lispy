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

Goals
-----

This is currently a pet project to facilitate learning the LISP and
scheme ecosystems and to bring about a better understanding of the
theory and complexity of language design. My roadmap includes several
additions to lispy to make it a toolkit for python developers who
might be interested in dipping their toe in LISP.

  - [x] Implement a scheme which allows the calling of python functions using s-expressions
  - [ ] Implement a shebang system
  - [ ] Implement a better REPL
  - [ ] Implement pluggable language options for different lisp dialect plugins, allow language rules to be overridden to emulate other languages either in lisp, macros or in the python code that implements the language
  - [ ] Implement reader macros
