# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from collections import OrderedDict
from decimal import Decimal
import re
import math
import six

from nibble import util, decorators


@decorators.python_2_div_compatible
@decorators.python_2_nonzero_compatible
@six.python_2_unicode_compatible
class Information(object):
    """
    Represents a quantity of digital information as a number of bits.
    """

    # this is deliberately lax with the number to provide a more helpful error
    # message
    _PARSE_REGEX = re.compile(r'([\d\\.]+)(?: +)?(\w+)')

    BITS = 1
    NIBBLES = 4
    BYTES = 8

    # binary, bytes
    KIBIBYTES = BYTES * 1024
    MEBIBYTES = BYTES * 1024 ** 2
    GIBIBYTES = BYTES * 1024 ** 3
    TEBIBYTES = BYTES * 1024 ** 4
    PEBIBYTES = BYTES * 1024 ** 5
    EXBIBYTES = BYTES * 1024 ** 6
    ZEBIBYTES = BYTES * 1024 ** 7
    YOBIBYTES = BYTES * 1024 ** 8

    # decimal, bytes
    KILOBYTES = BYTES * 1000
    MEGABYTES = BYTES * 1000 ** 2
    GIGABYTES = BYTES * 1000 ** 3
    TERABYTES = BYTES * 1000 ** 4
    PETABYTES = BYTES * 1000 ** 5
    EXABYTES = BYTES * 1000 ** 6
    ZETTABYTES = BYTES * 1000 ** 7
    YOTTABYTES = BYTES * 1000 ** 8

    # binary, bits
    KIBIBITS = 1024
    MEBIBITS = 1024 ** 2
    GIBIBITS = 1024 ** 3
    TEBIBITS = 1024 ** 4
    PEBIBITS = 1024 ** 5
    EXBIBITS = 1024 ** 6
    ZEBIBITS = 1024 ** 7
    YOBIBITS = 1024 ** 8

    # decimal, bits
    KILOBITS = 1000
    MEGABITS = 1000 ** 2
    GIGABITS = 1000 ** 3
    TERABITS = 1000 ** 4
    PETABITS = 1000 ** 5
    EXABITS = 1000 ** 6
    ZETTABITS = 1000 ** 7
    YOTTABITS = 1000 ** 8

    _SYMBOLS = {
        'b': 1,
        'bits': 1,

        'B': BYTES,
        'bytes': BYTES,

        'N': NIBBLES,
        'n': NIBBLES,
        'nibbles': NIBBLES,

        'K': KIBIBYTES,
        'KiB': KIBIBYTES,
        'kiB': KIBIBYTES,
        'kibibytes': KIBIBYTES,
        'M': MEBIBYTES,
        'MiB': MEBIBYTES,
        'miB': MEBIBYTES,
        'mebibytes': MEBIBYTES,
        'G': GIBIBYTES,
        'GiB': GIBIBYTES,
        'giB': GIBIBYTES,
        'gibibytes': GIBIBYTES,
        'T': TEBIBYTES,
        'TiB': TEBIBYTES,
        'tiB': TEBIBYTES,
        'tebibytes': TEBIBYTES,
        'P': PEBIBYTES,
        'PiB': PEBIBYTES,
        'piB': PEBIBYTES,
        'pebibytes': PEBIBYTES,
        'E': EXBIBYTES,
        'EiB': EXBIBYTES,
        'eiB': EXBIBYTES,
        'exbibytes': EXBIBYTES,
        'Z': ZEBIBYTES,
        'ZiB': ZEBIBYTES,
        'ziB': ZEBIBYTES,
        'zebibytes': ZEBIBYTES,
        'Y': YOBIBYTES,
        'YiB': YOBIBYTES,
        'yiB': YOBIBYTES,
        'yobibytes': YOBIBYTES,

        'KB': KILOBYTES,
        'kB': KILOBYTES,
        'kilobytes': KILOBYTES,
        'MB': MEGABYTES,
        'mB': MEGABYTES,
        'megabytes': MEGABYTES,
        'GB': GIGABYTES,
        'gB': GIGABYTES,
        'gigabytes': GIGABYTES,
        'TB': TERABYTES,
        'tB': TERABYTES,
        'terabytes': TERABYTES,
        'PB': PETABYTES,
        'pB': PETABYTES,
        'petabytes': PETABYTES,
        'EB': EXABYTES,
        'eB': EXABYTES,
        'exabytes': EXABYTES,
        'ZB': ZETTABYTES,
        'zB': ZETTABYTES,
        'zettabytes': ZETTABYTES,
        'YB': YOTTABYTES,
        'yB': YOTTABYTES,
        'yottabytes': YOTTABYTES,

        'Kib': KIBIBITS,
        'kib': KIBIBITS,
        'kibibits': KIBIBITS,
        'Mib': MEBIBITS,
        'mib': MEBIBITS,
        'mebibits': MEBIBITS,
        'Gib': GIBIBITS,
        'gib': GIBIBITS,
        'gibibits': GIBIBITS,
        'Tib': TEBIBITS,
        'tib': TEBIBITS,
        'tebibits': TEBIBITS,
        'Pib': PEBIBITS,
        'pib': PEBIBITS,
        'pebibits': PEBIBITS,
        'Eib': EXBIBITS,
        'eib': EXBIBITS,
        'exbibits': EXBIBITS,
        'Zib': ZEBIBITS,
        'zib': ZEBIBITS,
        'zebibits': ZEBIBITS,
        'Yib': YOBIBITS,
        'yib': YOBIBITS,
        'yobibits': YOBIBITS,

        'Kb': KILOBITS,
        'kb': KILOBITS,
        'kilobits': KILOBITS,
        'Mb': MEGABITS,
        'mb': MEGABITS,
        'megabits': MEGABITS,
        'Gb': GIGABITS,
        'gb': GIGABITS,
        'gigabits': GIGABITS,
        'Tb': TERABITS,
        'tb': TERABITS,
        'terabits': TERABITS,
        'Pb': PETABITS,
        'pb': PETABITS,
        'petabits': PETABITS,
        'Eb': EXABITS,
        'eb': EXABITS,
        'exabits': EXABITS,
        'Zb': ZETTABITS,
        'zb': ZETTABITS,
        'zettabits': ZETTABITS,
        'Yb': YOTTABITS,
        'yb': YOTTABITS,
        'yottabits': YOTTABITS
    }

    BINARY_BITS =  ['Yib', 'Zib', 'Eib', 'Pib', 'Tib', 'Gib', 'Mib', 'Kib', 'b']
    BINARY_BYTES = ['YiB', 'ZiB', 'EiB', 'PiB', 'TiB', 'GiB', 'MiB', 'KiB', 'B']
    DECIMAL_BITS = ['Yb',  'Zb',  'Eb',  'Pb',  'Tb',  'Gb',  'Mb',  'Kb',  'b']
    DECIMAL_BYTES = ['YB', 'ZB',  'EB',  'PB',  'TB',  'GB',  'MB',  'KB',  'B']

    _CATEGORY_MAPS = {
        'bB': BINARY_BYTES,
        'dB': DECIMAL_BYTES,
        'bb': BINARY_BITS,
        'db': DECIMAL_BITS
    }

    def __init__(self, quantity, unit=BITS):
        """
        Initialise a new information object.
        
        :param quantity: The number of the unit.
        :param unit: The size of the unit in bits, e.g. MiB = 8388608 bits.
                     Defaults to bits.
        """
        bits = quantity * unit
        if isinstance(bits, float):
            bits = int(math.ceil(bits))

        self.bits = bits

    @classmethod
    def from_quantity_unit(cls, quantity, unit):
        """
        Initialise a new information object from a quantity and unit string.

        :param quantity: The number of the unit.
        :param unit: The unit as a string, e.g. 'MiB' or 'mebibytes'.
        :return: An `Information` object representing the quantity and unit.
        """
        return Information(quantity, cls._SYMBOLS[unit])

    @classmethod
    def is_valid_symbol(cls, symbol):
        """
        Find whether a symbol is a valid unit of information.

        :param symbol: The symbol to check.
        :return: True if the symbol is a valid unit, false otherwise.
        """
        return symbol in cls._SYMBOLS

    @classmethod
    def is_valid_category(cls, category):
        """
        Find whether a category is valid.

        :param category: The category to check.
        :return: True if the category is valid, false otherwise.
        """
        return category in cls._CATEGORY_MAPS

    def at_speed(self, speed):
        """
        Find how long it would take to process this amount of data at a certain
        speed.

        :param speed: The speed of processing.
        :return: The time taken as a `datetime.timedelta`.
        """
        from nibble.duration import Duration
        scale = self.bits / speed.information.bits
        return Duration(seconds=speed.duration.total_seconds() * scale)

    def in_duration(self, duration):
        """
        Find the speed of processing if this quantity of information is
        processed in a given time.

        :param duration: The time taken to process this amount of data.
        :return: The speed of the processing.
        """
        from nibble.speed import Speed
        return Speed(self, duration)

    @classmethod
    def parse(cls, string):
        """
        Get an object representing an information string, e.g. "12TiB" or "9 n".
        
        :param string: The information string.
        :return: The parsed quantity of information.
        :raises ValueError: If the string could not be parsed. Check the message
                            for the reason why.
        """
        result = cls._PARSE_REGEX.match(string.strip())
        if not result:
            raise ValueError(
                'Unable to parse information string: {0}'.format(string))

        quantity_str = result.group(1)
        try:
            quantity = float(quantity_str)
            if quantity.is_integer():
                quantity = int(quantity)
        except ValueError:
            raise ValueError(
                'Unable to parse quantity number: {0}'.format(quantity_str))

        unit_str = result.group(2)
        if unit_str not in cls._SYMBOLS:
            raise ValueError(
                'Unrecognised information unit symbol: {0}'.format(unit_str))
        unit = cls._SYMBOLS[unit_str]

        return Information(quantity, unit)

    @decorators.operator_same_class
    def __lt__(self, other):
        return self.bits < other.bits

    def __le__(self, other):
        return self < other or self == other

    @decorators.operator_same_class
    def __eq__(self, other):
        return self.bits == other.bits

    def __ne__(self, other):
        return not other == self

    def __ge__(self, other):
        return self == other or self > other

    @decorators.operator_same_class
    def __gt__(self, other):
        return self.bits > other.bits

    @decorators.operator_same_class
    def __add__(self, other):
        return Information(self.bits + other.bits)

    @decorators.operator_same_class
    def __sub__(self, other):
        if self.bits - other.bits < 0:
            raise ArithmeticError(
                'Cannot have a negative amount of information')
        return Information(self.bits - other.bits)

    @decorators.operator_numeric_type
    def __mul__(self, other):
        return Information(self.bits * other)

    @decorators.operator_numeric_type
    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError('Cannot divide {0} by zero'.format(self))
        return Information(round(self.bits / other))

    @decorators.operator_numeric_type
    def __floordiv__(self, other):
        if other == 0:
            raise ZeroDivisionError('Cannot divide {0} by zero'.format(self))
        return Information(self.bits // other)

    def __repr__(self):
        return '<Information({0})>'.format(repr(self.bits))

    def __bool__(self):
        return self > Information.ZERO

    @classmethod
    def _expand_units(cls, category):
        """
        Turn a list of units into an ordered dictionary mapping those units
        to the number of bits 1 of that unit represents, e.g. 'B' (byte) will
        map to 8.

        :param category: The list of units to map.
        :return: The resulting ordered dictionary.
        """
        return OrderedDict([(symbol, cls._SYMBOLS[symbol])
                            for symbol in category])

    @classmethod
    def _determine_unit_symbol_quantity(cls, bits, category):
        """
        Given a list of units in descending order of size, choose the one most
        appropriate to represent a number of bits.

        :param bits: The number of bits to represent.
        :param category: A list containing choices of units we can choose from.
                         This must be in descending order of size, so largest
                         unit first.
        :return: The unit that should be used to represent `bits`. An element
                 in the input `category` list.
        """

        # unit: bits
        expanded = cls._expand_units(category)

        # find the first unit smaller than or equal to `bits` in size
        for unit, bits_ in six.iteritems(expanded):
            if bits >= bits_:
                # because categories are sorted descending, the first one where
                # this is true is the unit we should use to avoid <1 of a unit
                return unit

        # default to using the smallest unit we have
        return next(reversed(expanded))

    @decorators.python_2_format_compatible
    def __format__(self, format_spec):
        # [number format|][ ][unit symbol or category]

        num_fmt, _, symbol = format_spec.rpartition('|')

        if symbol:
            # separator and/or unit and/or category passed

            # chomp off any separator
            if symbol[0] == ' ':
                separator = ' '
                symbol = symbol[1:]
            else:
                # unit provided with no space, so no separator wanted
                separator = ''
        else:
            # no symbol, so default separator
            separator = ' '

        # the user may have provided a separator but no symbol
        if not symbol:
            # default to binary bytes
            symbol = 'bB'

        # symbol now contains a unit or category - let's find out
        if symbol in self._SYMBOLS:
            # specific unit
            quantity = self.bits / self._SYMBOLS[symbol]
            unit = symbol
        elif symbol in self._CATEGORY_MAPS:
            # category of units
            unit = self._determine_unit_symbol_quantity(
                self.bits, self._CATEGORY_MAPS[symbol])
            quantity = self.bits / self._SYMBOLS[unit]
        else:
            raise TypeError(
                'Unrecognised information unit or category: {0}'.format(symbol))

        if not num_fmt:
            quantity = util.round_two_non_zero_dp(Decimal(quantity))
            num_fmt = ',f'

        return '{0:{1}}{2}{3}'.format(quantity, num_fmt, separator, unit)

    def __str__(self):
        return '{0}'.format(self)


Information.ZERO = Information(0)
