# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ply import lex

from nibble.information import Information
from nibble.duration import Duration


class LexingError(Exception):
    """
    Raised if an error occurs during lexing. See the message for details.
    """
    pass


# noinspection PyPep8Naming,PyMethodMayBeStatic,PySingleQuotedDocstring
class Lexer(object):
    """
    Produces a stream of tokens from a calculation expression.
    """

    # reserved words
    _RESERVED = {
        'at': 'AT',
        'in': 'IN',
        'for': 'FOR',
        'per': 'PER'
    }

    _INFORMATION_UNIT = 'INFORMATION_UNIT'
    _DURATION_UNIT = 'DURATION_UNIT'

    # all possible tokens
    tokens = ['NUMBER', _INFORMATION_UNIT, _DURATION_UNIT] + \
        list(_RESERVED.values())

    # PER represents both "per" and "/", always context of speed
    t_PER = r'/'

    # all whitespace is ignored
    t_ignore = ' \t'

    def t_NUMBER(self, t):
        r'[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)'
        t.value = float(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z]+'
        if t.value in self._RESERVED.keys():
            t.type = self._RESERVED[t.value]
            return t

        if Information.is_valid_symbol(t.value) or \
                Information.is_valid_category(t.value):
            t.type = self._INFORMATION_UNIT
            return t

        if Duration.is_valid_symbol(t.value):
            t.type = self._DURATION_UNIT
            return t

        raise LexingError('Unrecognised token or unit \'{0.value}\' at '
                          'position {0.lexpos}'.format(t))

    def t_error(self, t):
        """
        The error handling rule.
        
        :param t: The erroneous token. 
        :raises LexingError: With a description of the problem and its position.
        """
        raise LexingError('Illegal sequence \'{0.value}\' at position '
                          '{0.lexpos}'.format(t))

    def __init__(self):
        """
        Initialise a new lexer.
        """
        # TODO look into optimized mode with a lextab.py file
        #      http://www.dabeaz.com/ply/ply.html#ply_nn15
        self.lexer = lex.lex(module=self)

    def lex(self, string):
        """
        Lex a string.
        
        :param string: The input to lex. 
        :return: A generator which will continue yielding tokens until the end
                 of the input is reached.
        """
        self.lexer.input(string)
        for token in self.lexer:
            yield token
