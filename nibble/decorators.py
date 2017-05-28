# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six


_NUMERIC_TYPES = six.integer_types + (float,)


def operator_same_class(method):
    """
    Intended to wrap operator methods, this decorator ensures the `other`
    parameter is of the same type as the `self` parameter.
    
    :param method: The method being decorated.
    :return: The wrapper to replace the method with.
    """
    def wrapper(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                'unsupported operand types: \'{0}\' and \'{1}\''.format(
                    self.__class__.__name__, other.__class__.__name__))
        return method(self, other)
    return wrapper


def operator_numeric_type(method):
    """
    Intended to wrap operator methods, this decorator ensures a numeric type
    was passed.
    
    :param method: The method being decorated.
    :return: The wrapper to replace the method with.
    """
    def wrapper(self, other):
        if not isinstance(other, _NUMERIC_TYPES):
            raise TypeError(
                'unsupported operand types: \'{0}\' and \'{1}\''.format(
                    self.__class__.__name__, other.__class__.__name__))
        return method(self, other)
    return wrapper


def python_2_format_compatible(method):
    """
    Handles bytestring and unicode inputs for the `__format__()` method in
    Python 2. This function has no effect in Python 3.

    :param method: The `__format__()` method to wrap.
    :return: The wrapped method.
    """
    if six.PY3:
        return method

    def wrapper(self, format_spec):
        formatted = method(self, format_spec)
        if isinstance(format_spec, str):
            # bytestring
            return formatted.encode('utf-8')

        # unicode
        return formatted
    return wrapper


def python_2_nonzero_compatible(klass):
    """
    Adds a `__nonzero__()` method to classes that define a `__bool__()` method,
    so boolean conversion works in Python 2. Has no effect in Python 3.

    :param klass: The class to modify. Must define `__bool__()`.
    :return: The possibly patched class.
    """
    if six.PY2:
        if '__bool__' not in klass.__dict__:
            raise ValueError(
                '@python_2_nonzero_compatible cannot be applied to {0} because '
                'it doesn\'t define __bool__().'.format(klass.__name__))
        klass.__nonzero__ = klass.__bool__
    return klass


def python_2_div_compatible(klass):
    """
    Adds a `__div__()` method to classes that define a `__floordiv__()` method,
    so division works in Python 2. Has no effect in Python 3.

    :param klass: The class to modify. Must define `__floordiv__()`.
    :return: The possibly patched class.
    """
    if six.PY2:
        if '__floordiv__' not in klass.__dict__:
            raise ValueError(
                '@python_2_div_compatible cannot be applied to {0} because it '
                'doesn\'t define __floordiv__().'.format(klass.__name__))
        klass.__div__ = klass.__floordiv__
    return klass
