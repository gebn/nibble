# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest
import six

from nibble import decorators


class TestOperatorSameClass(unittest.TestCase):

    # noinspection PyUnusedLocal
    @decorators.operator_same_class
    def wrapped(self, other):
        return True

    def test_same_class(self):
        self.assertTrue(self.wrapped(self))

    def test_different_class(self):
        with self.assertRaises(TypeError):
            self.wrapped('')


class TestOperatorNumericType(unittest.TestCase):

    # noinspection PyUnusedLocal
    @decorators.operator_numeric_type
    def wrapped(self, other):
        return True

    def test_int(self):
        self.assertTrue(self.wrapped(1))

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_long(self):
        # noinspection PyUnresolvedReferences
        self.assertTrue(self.wrapped(long(1)))

    def test_float(self):
        self.assertTrue(self.wrapped(1.0))

    def test_string(self):
        with self.assertRaises(TypeError):
            self.wrapped('')


class TestPython2FormatCompatible(unittest.TestCase):

    # noinspection PyUnusedLocal
    @decorators.python_2_format_compatible
    def __format__(self, format_spec):
        return ''

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_py2_str(self):
        bytestring = 'abc'.encode('utf-8')
        self.assertIsInstance(format(self, bytestring), type(bytestring))

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_py2_unicode(self):
        unicode_ = 'abc'
        self.assertIsInstance(format(self, unicode_), type(unicode_))

    @unittest.skipUnless(six.PY3, 'Only applies to Python 3')
    def test_py3_str(self):
        self.assertIsInstance(format(self, 'abc'), str)


class TestPython2NonzeroCompatible(unittest.TestCase):

    @decorators.python_2_nonzero_compatible
    class Inner(object):

        def __init__(self, val):
            self.val = val

        def __bool__(self):
            return self.val

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_py2_true(self):
        self.assertTrue(self.Inner(True))

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_py2_false(self):
        self.assertFalse(self.Inner(False))

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_no_bool_method(self):
        with self.assertRaises(ValueError):
            # noinspection PyUnusedLocal
            @decorators.python_2_nonzero_compatible
            class NoBool(object):
                pass

    @unittest.skipUnless(six.PY3, 'Only applies to Python 3')
    def test_py3(self):
        self.assertFalse(hasattr(self.Inner(True), '__nonzero__'))


class TestPython2DivCompatible(unittest.TestCase):

    @decorators.python_2_div_compatible
    class Inner(object):

        def __init__(self, val):
            self.val = val

        def __floordiv__(self, other):
            return self.val // other

        def __truediv__(self, other):
            return self.val / other

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_py2_div(self):
        self.assertEqual(self.Inner(5).__div__(3), 1)

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_py2_floordiv(self):
        self.assertEqual(self.Inner(5) // 3, 1)

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_py2_truediv(self):
        self.assertAlmostEqual(self.Inner(5) / 3, 1.66666666)

    @unittest.skipUnless(six.PY2, 'Only applies to Python 2')
    def test_no_floordiv_method(self):
        with self.assertRaises(ValueError):
            # noinspection PyUnusedLocal
            @decorators.python_2_div_compatible
            class NoFloordiv(object):
                pass

    @unittest.skipUnless(six.PY3, 'Only applies to Python 3')
    def test_py3(self):
        self.assertFalse(hasattr(self.Inner(None), '__div__'))
