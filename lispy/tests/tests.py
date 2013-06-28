from unittest import TestCase

from sh import lispy

from lispy.runtime import Runtime


class SimpleEvaluationTest(TestCase):
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


class PythonBuiltinsTest(TestCase):

    def setUp(self):
        self.runtime = Runtime()

    def test_py_builtin_abs(self):
        self.assertEquals(
            self.runtime.eval("(py:abs -7)"), 7
        )

class CommandlineTest(TestCase):
    """
    Test the options provided by lispy's cli using python's sh module
    """
    def test_passed_as_string(self):
        """
        Tests that code passed in as a string with the -c flag is
        being evaluated properly
        """
        self.assertEquals(lispy("-c (+ 2 2)"), "4\n")
