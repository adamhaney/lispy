from unittest import TestCase

from lispy.runtime import Runtime


class SimpleTest(TestCase):
    def setUp(self):
        self.runtime = Runtime()

    def test_simple_addition(self):
        self.assertEquals(
            self.runtime.eval("(+ 2 2)"),
            4
        )

    def test_simple_module_access(self):
        import os
        self.assertEquals(
            self.runtime.eval("(list os:environ)"), [os.environ]
        )

    def test_py_builtin_abs(self):
        self.assertEquals(
            self.runtime.eval("(py:abs -7)"), 7
        )
