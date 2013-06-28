import re
import os
import doctest
from unittest import TestCase

import sh
from sh import lispy, grep

from lispy.runtime import Runtime

class RuntimeTest(TestCase):
    def setUp(self):
        self.runtime = Runtime()
        self.test_directory = os.path.dirname(os.path.realpath(__file__))


class SimpleEvaluationTest(RuntimeTest):

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


class PythonBuiltinsTest(RuntimeTest):

    def test_py_builtin_abs(self):
        self.assertEquals(
            self.runtime.eval("(py:abs -7)"), 7
        )

class CommandlineTest(RuntimeTest):
    """
    Test the options provided by lispy's cli using python's sh module
    """
    def test_passed_as_string(self):
        """
        Tests that code passed in as a string with the -c flag is
        being evaluated properly
        """
        self.assertEquals(lispy("-c (+ 2 2)"), "4\n")

class SICPTest(RuntimeTest):
    def test_sicp_examples(self):
        """
        Test all the files in the SICP code directory
        """

        chapters_dir = "{}/code/sicp/chapters".format(self.test_directory)

        for lispy_file in os.listdir(chapters_dir):
            abs_script_path = "{}/{}".format(chapters_dir, lispy_file)
            output = lispy("{}".format(abs_script_path))
            comments = re.findall(";;.*", open(abs_script_path).read())
            expected = map(lambda line: line.replace(";;", ""), comments)

            for output, expected in zip(output.split('\n'), expected):
                self.assertEquals(expected.strip(), output)
