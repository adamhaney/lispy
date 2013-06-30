Dialects
========

Dialects are one of the most powerful features of lispy. They allow
for the language implementation to be modified in a object oriented
way. Dialects are made up of objects that implement certain language
features, and these language features can inherit from other dialects.

Included Dialects
-----------------

As of 0.0.2 The included dialects are the `norvig` dialect, which
attempts to faithfully reproduce Peter Norvig's lispy2 implementation,
and the `haney` dialect which inherits from the norvig dialect and
adds some additional features that allow the accessing of python
modules. Good dialects should have appropriate hooks that allow other
dialects to inherit from them and override specific features of that
dialect without having to fully re-implement the dialect itself. For
example, there is a plan to work on language level memoization. This
will likely be implemented in a memoized dialect which inherits from
the haney dialect (as we can see already this would give us access to
features from the norvig dialect and the haney dialect), this
overridden code would handle the memoization of evaluated procedures,
and should include hooks to override features specific to memoization
so another dialect implementer could experiment with other memoization
features (such as a storage backend for memoized values) without
having to fully re-implement the eval function.

Dialect Pieces
--------------
Dialects only have to implement the language features they're
interested in modifying, and if they simply wish to be a configuration
of other dialect features composed together all they have to implement
is a DIALECT_SPECIFICATION in the settings.py file of the dialect. The
Runtime object, which is a part of core lispy (though it too is simply
an object that could be modified to suite needs) uses this
specification to assemble the language together in a way that can be
used to evaluate code.

Scope
^^^^^


Symbol
------

Atom
----

Eval
----

Special Forms
-------------
