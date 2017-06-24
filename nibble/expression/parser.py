# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from ply import yacc

from nibble.information import Information
from nibble.duration import Duration
from nibble.expression.lexer import Lexer


logger = logging.getLogger(__name__)


class ParsingError(Exception):
    """
    Raised if an error occurs during parsing. See the message for details.
    """
    pass


# noinspection PyMethodMayBeStatic,PySingleQuotedDocstring
class Parser(object):
    """
    Turns a stream of tokens into a single object representing a calculation
    expression.
    """

    # otherwise the parser cannot find the list of tokens
    tokens = Lexer.tokens

    precedence = (
        # lowest
        ('left', 'IN'),  # only do conversions at the end
        ('left', 'AT', 'FOR'),  # do calculations
        ('nonassoc', 'PER'),  # 10Gb/3 h 3 m
        ('left', 'DURATION_UNIT')  # 3 h 3 m is a single quantity
        # highest
    )

    # expression : information
    #            | duration
    #            | speed

    def p_expression_information(self, p):
        'expression : information'
        logger.debug('expression = information %s', p[1])
        p[0] = p[1]

    def p_expression_duration(self, p):
        'expression : duration'
        logger.debug('expression = duration %s', p[1])
        p[0] = p[1]

    def p_expression_speed(self, p):
        'expression : speed'
        logger.debug('expression = speed %s', p[1])
        p[0] = p[1]

    # information : NUMBER INFORMATION_UNIT
    #             | duration AT speed
    #             | speed FOR duration
    #             | information IN INFORMATION_UNIT

    def p_information_constructor(self, p):
        'information : NUMBER INFORMATION_UNIT'
        logger.debug('information = number %s, information unit %s', p[1], p[2])
        p[0] = Information.from_quantity_unit(p[1], p[2])

    def p_information_duration_speed(self, p):
        'information : duration AT speed'
        logger.debug('information = duration %s at speed %s', p[1], p[3])
        p[0] = p[3].for_duration(p[1])

    def p_information_speed_duration(self, p):
        'information : speed FOR duration'
        logger.debug('information = speed %s for duration %s', p[1], p[3])
        p[0] = p[1].for_duration(p[3])

    def p_information_conversion(self, p):
        'information : information IN INFORMATION_UNIT'
        logger.debug(
            'information = information %s in information unit %s', p[1], p[3])
        p[0] = '{0: {1}}'.format(p[1], p[3])

    # duration : DURATION_UNIT
    #          | NUMBER DURATION_UNIT
    #          | NUMBER DURATION_UNIT duration
    #          | information AT speed
    #          | duration IN DURATION_UNIT

    def p_duration_duration_unit(self, p):
        'duration : DURATION_UNIT'
        logger.debug('duration = 1 of duration unit %s', p[1])
        p[0] = Duration.from_quantity_unit(1, p[1])

    def p_duration_number_duration_unit(self, p):
        'duration : NUMBER DURATION_UNIT'
        logger.debug('duration = number %s, duration unit %s', p[1], p[2])
        p[0] = Duration.from_quantity_unit(p[1], p[2])

    def p_duration_number_duration_unit_duration(self, p):
        'duration : NUMBER DURATION_UNIT duration'
        logger.debug(
            'duration = number %s, duration unit %s, duration %s', p[1], p[2],
            p[3])
        duration = Duration.from_quantity_unit(p[1], p[2])
        p[0] = duration + p[3]

    def p_duration_information_speed(self, p):
        'duration : information AT speed'
        logger.debug('duration = information %s at speed %s', p[1], p[3])
        p[0] = p[1].at_speed(p[3])

    def p_duration_conversion(self, p):
        'duration : duration IN DURATION_UNIT'
        logger.debug('duration = duration %s in duration unit %s', p[1], p[3])
        p[0] = '{0: {1}}'.format(p[1], p[3])

    # speed : NUMBER speed_unit
    #       | information IN duration
    #       | speed IN speed_unit

    def p_speed_constructor(self, p):
        'speed : NUMBER speed_unit'
        logger.debug('speed = number %s, speed unit %s', p[1], p[2])
        information_unit, duration = p[2]
        information = Information.from_quantity_unit(p[1], information_unit)
        p[0] = information.in_duration(duration)

    def p_speed_information_duration(self, p):
        'speed : information IN duration'
        logger.debug('speed = information %s in duration %s', p[1], p[3])
        p[0] = p[1].in_duration(p[3])

    def p_speed_conversion(self, p):
        'speed : speed IN speed_unit'
        logger.debug('speed = speed %s in speed unit %s', p[1], p[3])
        information_unit, duration = p[3]
        p[0] = '{0: {1}}'.format(p[1],
                                 '{0}/{1}'.format(information_unit, duration))

    # speed_unit : INFORMATION_UNIT PER duration

    def p_speed_unit(self, p):
        'speed_unit : INFORMATION_UNIT PER duration'
        logger.debug(
            'speed unit = information unit %s per duration %s', p[1], p[3])
        p[0] = (p[1], p[3])

    def p_error(self, p):
        """
        Parsing error handler.
        
        :param p: The token causing the problem, if identifiable. 
        :raises ParsingError: With our best description of the problem.
        """
        if not p:
            raise ParsingError('Expression is senseless')
        raise ParsingError(
            'Unable to parse expression: unexpected {0.type} token with value '
            '\'{0.value}\' after character {0.lexpos}'.format(p))

    def __init__(self):
        """
        Initialise a new parser.
        """
        self._build()

    def _build(self):
        """
        Build the parser.
        """
        # TODO how can you print the list of tokens when debugging?
        # TODO look into optimize and picklefile options
        self.parser = yacc.yacc(module=self)

    def parse(self, string, lexer=None):
        """
        Interpret a string.
        
        :param string: The input to lex and parse.
        :param lexer: The lexer to use. A new one will be created if not
                      provided.
        :return: An object representation of the input.
        """
        if not lexer:
            lexer = Lexer().lexer

        return self.parser.parse(string, lexer=lexer)
