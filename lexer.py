# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import logging

from nibble.expression.lexer import Lexer, LexingError
from nibble.expression.parser import Parser, ParsingError


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
print('Input: {0}'.format(INPUT))

try:
    print(Parser().parse(INPUT))
except (LexingError, ParsingError) as e:
    print(e, file=sys.stderr)


# for token in lexer.lex(INPUT):
#     # token : LexToken
#     logger.debug(
#         'Token(type: {0.type}, value: \'{0.value}\', line: {0.lineno}, '
#         'pos: {0.lexpos})'.format(token))
# print(parser.parse(INPUT, lexer=lexer.lexer))
