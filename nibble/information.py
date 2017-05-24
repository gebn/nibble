# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import math
import six


@six.python_2_unicode_compatible
class Information(object):
    """
    Represents a quantity of digital information.
    """

    PARSE_REGEX = re.compile(r'(\d+(?:\.\d+)?|\.\d+)(?: +)?(\w+)')

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
        'B': BYTES,
        'N': NIBBLES,
        'n': NIBBLES,

        'K': KIBIBYTES,
        'KiB': KIBIBYTES,
        'kiB': KIBIBYTES,
        'M': MEBIBYTES,
        'MiB': MEBIBYTES,
        'miB': MEBIBYTES,
        'G': GIBIBYTES,
        'GiB': GIBIBYTES,
        'giB': GIBIBYTES,
        'T': TEBIBYTES,
        'TiB': TEBIBYTES,
        'tiB': TEBIBYTES,
        'P': PEBIBYTES,
        'PiB': PEBIBYTES,
        'piB': PEBIBYTES,
        'E': EXBIBYTES,
        'EiB': EXBIBYTES,
        'eiB': EXBIBYTES,
        'Z': ZEBIBYTES,
        'ZiB': ZEBIBYTES,
        'ziB': ZEBIBYTES,
        'Y': YOBIBYTES,
        'YiB': YOBIBYTES,
        'yiB': YOBIBYTES,

        'KB': KILOBYTES,
        'kB': KILOBYTES,
        'MB': MEGABYTES,
        'mB': MEGABYTES,
        'GB': GIGABYTES,
        'gB': GIGABYTES,
        'TB': TERABYTES,
        'tB': TERABYTES,
        'PB': PETABYTES,
        'pB': PETABYTES,
        'EB': EXABYTES,
        'eB': EXABYTES,
        'ZB': ZETTABYTES,
        'zB': ZETTABYTES,
        'YB': YOTTABYTES,
        'yB': YOTTABYTES,

        'Kib': KIBIBITS,
        'kib': KIBIBITS,
        'Mib': MEBIBITS,
        'mib': MEBIBITS,
        'Gib': GIBIBITS,
        'gib': GIBIBITS,
        'Tib': TEBIBITS,
        'tib': TEBIBITS,
        'Pib': PEBIBITS,
        'pib': PEBIBITS,
        'Eib': EXBIBITS,
        'eib': EXBIBITS,
        'Zib': ZEBIBITS,
        'zib': ZEBIBITS,
        'Yib': YOBIBITS,
        'yib': YOBIBITS,

        'Kb': KILOBITS,
        'kb': KILOBITS,
        'Mb': MEGABITS,
        'mb': MEGABITS,
        'Gb': GIGABITS,
        'gb': GIGABITS,
        'Tb': TERABITS,
        'tb': TERABITS,
        'Pb': PETABITS,
        'pb': PETABITS,
        'Eb': EXABITS,
        'eb': EXABITS,
        'Zb': ZETTABITS,
        'zb': ZETTABITS,
        'Yb': YOTTABITS,
        'yb': YOTTABITS
    }

    def __init__(self, quantity, unit=BITS):
        """
        Initialise a new information object.
        
        :param quantity: The number of the unit.
        :param unit: The size of the unit in bits, e.g. MiB = 8388608 bits.
                     Defaults to bits.
        """
        self.bits = math.ceil(quantity * unit)

    @classmethod
    def parse(cls, string):
        """
        Get an object representing an information string, e.g. "12TiB" or "9 n".
        
        :param string: The information string.
        :return: The parsed quantity of information.
        :raises ValueError: If the string could not be parsed. Check the message
                            for the reason why.
        """
        result = cls.PARSE_REGEX.match(string.strip())
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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return other.bits == self.bits

    def __repr__(self):
        return '<Information({0})>'.format(self.bits)

    def __str__(self):
        return '{0:,} bits'.format(self.bits)
