from unittest2 import TestCase


class SimpleTest(TestCase):
    def setUp(self):
        self.runtime = Runtime()

    def test_simple_addition(self):
        self.assertEquals(
            self.runtime.eval("(+ 2 2)"),
            2
        )
