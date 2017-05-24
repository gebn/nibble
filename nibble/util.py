# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def operator_same_class(method):
    """
    Intended to wrap operator functions, this decorator ensures the `other`
    parameter is of the same type as the `self` parameter.
    
    :param method: The method being decorated.
    :return: The wrapper to replace the method with.
    """
    def wrapper(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return method(self, other)
    return wrapper
