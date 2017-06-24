# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import logging
from ply import yacc

from nibble.information import Information
from nibble.duration import Duration
from nibble.expression.lexer import Lexer, LexingError


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# Need 1 test per input - info in duration, speed for duration etc. both with and without conversion
# INPUT = '17.3GB at 688.3kB/s'  # printing durations in verbose form (years, months, weeks etc.)
# INPUT = '1Gb/s in TiB/day'  # bare conversion
# INPUT = '22 MiB in 3h in GiB/h'  # calculation and conversion
# INPUT = '22 MiB in 3h 30m in GiB/h'  # compound duration
# INPUT = '10 gigabits/s in tebibytes/hour'  # type aliases
# INPUT = '10.842Gib in bB'  # categories
# INPUT = '10Gb per second in TiB per hour'  # 'per' and '/' as PER terminals
# INPUT = '10Gb/s for 11 minutes'  # information : speed FOR duration
# INPUT = '11 minutes at 10Gb/s'  # information : duration AT speed
# INPUT = '10Gb/s for 11 minutes at 5Gb/s'  # nesting
# INPUT = '481MB at 15Mb/s in s'  # nesting
# INPUT = '50Gb/5s'  # non-one speed duration
# INPUT = '50Gb/s for minute'  # 1 is implicit
# INPUT = '10Gb/s in MiB/2m'  # valued duration time for speed_unit

# INPUT = '10Gb/s in GiB/s in KiB/s in MiB/s'  # FIXME - a conversion should produce a FormattedQuantity, which can be reformatted by subsequent conversions
# TODO parser.parse(INPUT) should return a non-string that is converted into a string; this allows easier chaining internally, e.g. multiple conversions

# INPUT = '10Gb/s in /w'  # PONDERING (grammar too strict - look back at valid `format_spec`s)
# INPUT = '10Gb/s in MiB'  # PONDERING (same reason as above)

INPUT = ' '.join(sys.argv[1:])

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


"""
expression : information
           | duration
           | speed
"""


def p_expression_information(p):
    'expression : information'
    logger.debug('expression = information %s', p[1])
    p[0] = p[1]


def p_expression_duration(p):
    'expression : duration'
    logger.debug('expression = duration %s', p[1])
    p[0] = p[1]


def p_expression_speed(p):
    'expression : speed'
    logger.debug('expression = speed %s', p[1])
    p[0] = p[1]


"""
information : NUMBER INFORMATION_UNIT
            | duration AT speed
            | speed FOR duration
            | information IN INFORMATION_UNIT
"""


def p_information_constructor(p):
    'information : NUMBER INFORMATION_UNIT'
    logger.debug('information = number %s, information unit %s', p[1], p[2])
    p[0] = Information.from_quantity_unit(p[1], p[2])


def p_information_duration_speed(p):
    'information : duration AT speed'
    logger.debug('information = duration %s at speed %s', p[1], p[3])
    p[0] = p[3].for_duration(p[1])


def p_information_speed_duration(p):
    'information : speed FOR duration'
    logger.debug('information = speed %s for duration %s', p[1], p[3])
    p[0] = p[1].for_duration(p[3])


def p_information_conversion(p):
    'information : information IN INFORMATION_UNIT'
    logger.debug(
        'information = information %s in information unit %s', p[1], p[3])
    p[0] = '{0: {1}}'.format(p[1], p[3])


"""
duration : DURATION_UNIT
         | NUMBER DURATION_UNIT
         | NUMBER DURATION_UNIT duration
         | information AT speed
         | duration IN DURATION_UNIT
"""


def p_duration_duration_unit(p):
    'duration : DURATION_UNIT'
    logger.debug('duration = 1 of duration unit %s', p[1])
    p[0] = Duration.from_quantity_unit(1, p[1])


def p_duration_number_duration_unit(p):
    'duration : NUMBER DURATION_UNIT'
    logger.debug('duration = number %s, duration unit %s', p[1], p[2])
    p[0] = Duration.from_quantity_unit(p[1], p[2])


def p_duration_number_duration_unit_duration(p):
    'duration : NUMBER DURATION_UNIT duration'
    logger.debug(
        'duration = number %s, duration unit %s, duration %s', p[1], p[2], p[3])
    duration = Duration.from_quantity_unit(p[1], p[2])
    p[0] = duration + p[3]


def p_duration_information_speed(p):
    'duration : information AT speed'
    logger.debug('duration = information %s at speed %s', p[1], p[3])
    p[0] = p[1].at_speed(p[3])


def p_duration_conversion(p):
    'duration : duration IN DURATION_UNIT'
    logger.debug('duration = duration %s in duration unit %s', p[1], p[3])
    p[0] = '{0: {1}}'.format(p[1], p[3])


"""
speed : NUMBER speed_unit
      | information IN duration
      | speed IN speed_unit
"""


def p_speed_constructor(p):
    'speed : NUMBER speed_unit'
    logger.debug('speed = number %s, speed unit %s', p[1], p[2])
    information_unit, duration = p[2]
    information = Information.from_quantity_unit(p[1], information_unit)
    p[0] = information.in_duration(duration)


def p_speed_information_duration(p):
    'speed : information IN duration'
    logger.debug('speed = information %s in duration %s', p[1], p[3])
    p[0] = p[1].in_duration(p[3])


def p_speed_conversion(p):
    'speed : speed IN speed_unit'
    logger.debug('speed = speed %s in speed unit %s', p[1], p[3])
    information_unit, duration = p[3]
    p[0] = '{0: {1}}'.format(p[1],
                             '{0}/{1}'.format(information_unit, duration))


"""
speed_unit : INFORMATION_UNIT PER duration
"""


def p_speed_unit(p):
    'speed_unit : INFORMATION_UNIT PER duration'
    logger.debug(
        'speed unit = information unit %s per duration %s', p[1], p[3])
    p[0] = (p[1], p[3])


# Error rule for syntax errors
def p_error(p):
    if not p:
        raise ValueError('Unable to parse expression')
    raise ValueError(
        'Unable to parse expression: unexpected {0.type} token with value '
        '\'{0.value}\' after character {0.lexpos}'.format(p))

lexer = Lexer()

# Build the parser
parser = yacc.yacc()

print('Input: {0}'.format(INPUT))

try:
    # for token in lexer.lex(INPUT):
    #     # token : LexToken
    #     logger.debug(
    #         'Token(type: {0.type}, value: \'{0.value}\', line: {0.lineno}, '
    #         'pos: {0.lexpos})'.format(token))
    print(parser.parse(INPUT, lexer=lexer.lexer))
except LexingError as e:
    print(e, file=sys.stderr)
