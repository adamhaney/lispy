from __future__ import print_function

import re
import os
from unittest import TestCase
from inspect import isclass

from nose.tools import raises

from lispy.runtime import Runtime
from lispy.dialects.norvig import to_string

from sh import lispy


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
        self.assertEquals(
            list(self.runtime.eval("(list os:environ)")),
            [os.environ]
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


def check_expected(filename, expected, actual):
    print(filename)
    assert expected == actual, "{} != {}".format(expected, actual)


def test_sicp_examples():
    """
    Test all the files in the SICP code directory
    """
    test_directory = os.path.dirname(os.path.realpath(__file__))
    chapters_dir = "{}/code/sicp/chapters".format(test_directory)

    for lispy_file in os.listdir(chapters_dir):
        abs_script_path = "{}/{}".format(chapters_dir, lispy_file)
        output = lispy("{}".format(abs_script_path))
        comments = re.findall(";;.*", open(abs_script_path).read())
        expected = map(lambda line: line.replace(";;", ""), comments)

        for output_line, expected in zip(output.split('\n'), expected):
            yield check_expected, lispy_file, expected.strip(), output_line

################ Tests for lis.py and lispy.py

lis_tests = [
    ("(+ 2 2)", 4),
    ("(+ (* 2 100) (* 1 10))", 210),
    ("(if (> 6 5) (+ 1 1) (+ 2 2))", 2),
    ("(if (< 6 5) (+ 1 1) (+ 2 2))", 4),
    ("(quote (testing 1 (2.0) -3.14e159))", ['testing', 1, [2.0], -3.14e159]),
    ("(define x 3)", None), ("x", 3), ("(+ x x)", 6),
    ("(begin (define x 1) (set! x (+ x 1)) (+ x 1))", 3),
    ("((lambda (x) (+ x x)) 5)", 10),
    ("(define twice (lambda (x) (* 2 x)))", None), ("(twice 5)", 10),
    ("(define compose (lambda (f g) (lambda (x) (f (g x)))))", None),
    ("((compose list twice) 5)", [10]),
    ("(define repeat (lambda (f) (compose f f)))", None),
    ("((repeat twice) 5)", 20), ("((repeat (repeat twice)) 5)", 80),
    ("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))", None),
    ("(fact 3)", 6),
    ("(fact 50)",
     30414093201713378043612608166064768844377641568960512000000000000),
    ("(define abs (lambda (n) ((if (> n 0) + -) 0 n)))", None),
    ("(list (abs -3) (abs 0) (abs 3))", [3, 0, 3]),
    ("""(define combine (lambda (f)
    (lambda (x y)
      (if (null? x) (quote ())
          (f (list (car x) (car y))
             ((combine f) (cdr x) (cdr y)))))))""", None),
    ("(define zip (combine cons))", None),
    ("(zip (list 1 2 3 4) (list 5 6 7 8))", [[1, 5], [2, 6], [3, 7], [4, 8]]),
    ("""(define riff-shuffle (lambda (deck) (begin
    (define take
      (lambda (n seq)
        (if (<= n 0)
          (quote ()) (cons (car seq) (take (- n 1) (cdr seq))))))
    (define drop (lambda (n seq) (if (<= n 0) seq (drop (- n 1) (cdr seq)))))
    (define mid (lambda (seq) (/ (length seq) 2)))
    ((combine append) (take (mid deck) deck) (drop (mid deck) deck)))))""",
     None),
    ("(riff-shuffle (list 1 2 3 4 5 6 7 8))", [1, 5, 2, 6, 3, 7, 4, 8]),
    ("((repeat riff-shuffle) (list 1 2 3 4 5 6 7 8))",
     [1, 3, 5, 7, 2, 4, 6, 8]),
    ("(riff-shuffle (riff-shuffle (riff-shuffle (list 1 2 3 4 5 6 7 8))))",
     [1, 2, 3, 4, 5, 6, 7, 8]),
]

lispy_tests = [
    ("(define (twice x) (* 2 x))", None),
    ("(twice 2)", 4),
    ("(define lyst (lambda items items))", None),
    ("(lyst 1 2 3 (+ 2 2))", [1, 2, 3, 4]),
    ("(if 1 2)", 2),
    ("(if (= 3 4) 2)", None),
    ("(define ((account bal) amt) (set! bal (+ bal amt)) bal)", None),
    ("(define a1 (account 100))", None),
    ("(a1 0)", 100), ("(a1 10)", 110), ("(a1 10)", 120),
    ("""(define (newton guess function derivative epsilon)
    (define guess2 (- guess (/ (function guess) (derivative guess))))
    (if (< (abs (- guess guess2)) epsilon) guess2
        (newton guess2 function derivative epsilon)))""", None),
    ("""(define (square-root a)
    (newton 1 (lambda (x) (- (* x x) a)) (lambda (x) (* 2 x)) 1e-8))""", None),
    ("(> (square-root 200.) 14.14213)", True),
    ("(< (square-root 200.) 14.14215)", True),
    ("(= (square-root 200.) (math:sqrt 200.))", True),
    ("""(define (sum-squares-range start end)
         (define (sumsq-acc start end acc)
            (if
              (> start end)
                acc
                (sumsq-acc (+ start 1) end (+ (* start start) acc))))
         (sumsq-acc start end 0))""", None),
    ("(sum-squares-range 1 3000)", 9004500500),  # Tests tail recursion
    ("(call/cc (lambda (throw) (+ 5 (* 10 (throw 1))))) ;; throw", 1),
    ("(call/cc (lambda (throw) (+ 5 (* 10 1)))) ;; do not throw", 15),
    ("""(call/cc (lambda (throw)
         (+ 5 (* 10 (call/cc
                      (lambda (escape)
                        (* 100 (escape 3)))))))) ; 1 level""", 35),
    ("""(call/cc (lambda (throw)
         (+ 5 (* 10 (call/cc
                      (lambda (escape) (* 100 (throw 3)))))))) ; 2 levels""",
     3),
    ("""(call/cc (lambda (throw)
         (+ 5 (* 10 (call/cc (lambda (escape) (* 100 1))))))) ; 0 levels""",
     1005),
    ("(* 1i 1i)", -1), ("(cmath:sqrt -1)", 1j),
    ("(let ((a 1) (b 2)) (+ a b))", 3),
    ("(and 1 2 3)", 3), ("(and (> 2 1) 2 3)", 3), ("(and)", True),
    ("(and (> 2 1) (> 2 3))", False),
    ("""(define-macro unless
          (lambda args
            `(if (not ,(car args)) (begin ,@(cdr args))))) ; test `""",
     None),
    ("(unless (= 2 (+ 1 1)) (display 2) 3 4)", None),
    (r'(unless (= 4 (+ 1 1)) (display 2) (display "\n") 3 4)', 4),
    ("(quote x)", 'x'),
    ("(quote (1 2 three))", [1, 2, 'three']),
    ("'x", 'x'),
    ("'(one 2 3)", ['one', 2, 3]),
    ("(define L (list 1 2 3))", None),
    ("`(testing ,@L testing)", ['testing', 1, 2, 3, 'testing']),
    ("`(testing ,L testing)", ['testing', [1, 2, 3], 'testing']),
    ("""'(1 ;test comments '
     ;skip this line
     2 ; more ; comments ; ) )
     3) ; final comment""", [1, 2, 3]),
]

syntax_errors = [
    ("`,@L", SyntaxError),
    ("(let ((a 1) (b 2 3)) (+ a b))", SyntaxError),
    ("()", SyntaxError),
    ("(set! x)", SyntaxError),
    ("(define 3 4)", SyntaxError),
    ("(quote 1 2)", SyntaxError),
    ("(if 1 2 3 4)", SyntaxError),
    ("(lambda 3 3)", SyntaxError),
    ("(lambda (x))", SyntaxError),
    ("""(if (= 1 2) (define-macro a 'a)
     (define-macro a 'b))""", SyntaxError),
]

type_errors = [
    ("(twice 2 2)", TypeError),
]


def check_norvig_expected(x, expected, rt):
    try:
        result = rt.eval(x)
        print(x, '=>', to_string(result))
        if isclass(expected) and not issubclass(expected, Exception):
            assert result == expected
    except Exception as e:
        assert issubclass(expected, Exception)
        assert isinstance(e, expected)


def norvig_suite_test():
    tests = lis_tests + lispy_tests

    "For each (exp, expected) test case, see if eval(parse(exp)) == expected."
    fails = 0
    rt = Runtime()

    for (x, expected) in tests:
        yield check_norvig_expected, x, expected, rt


@raises(SyntaxError)
def check_for_syntax_error(expression, rt):
    val = rt.eval(expression)


def norvig_test_syntax_errors():
    rt = Runtime()

    for syntax_error_case in syntax_errors:
        yield check_for_syntax_error, syntax_error_case[0], rt


@raises(TypeError)
def check_for_type_error(expression, rt):
    val = rt.eval(expression)


def norvig_test_type_errors():
    rt = Runtime()

    for type_error_case in type_errors:
        yield check_for_type_error, type_error_case[0], rt
