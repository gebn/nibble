# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from collections import OrderedDict
from decimal import Decimal
import datetime
import math
import six

from nibble import util, decorators


@decorators.python_2_div_compatible
@decorators.python_2_nonzero_compatible
@six.python_2_unicode_compatible
class Duration(object):
    """
    Represents a positive period of time as an integral number of nanoseconds.
    Equivalent to `datetime.timedelta`, but with nanosecond precision and the
    addition of month and year units.
    """

    NANOSECONDS = 1
    MICROSECONDS = 10 ** 3
    MILLISECONDS = 10 ** 6
    SECONDS = 10 ** 9
    MINUTES = SECONDS * 60
    HOURS = MINUTES * 60
    DAYS = HOURS * 24
    WEEKS = DAYS * 7
    MONTHS = HOURS * 730
    YEARS = MONTHS * 12

    _SYMBOLS = {
        'ns': NANOSECONDS,
        'nanosecond': NANOSECONDS,
        'nanoseconds': NANOSECONDS,
        'us': MICROSECONDS,  # because who's going to type μ
        'microsecond': MICROSECONDS,
        'microseconds': MICROSECONDS,
        'ms': MILLISECONDS,
        'millisecond': MILLISECONDS,
        'milliseconds': MILLISECONDS,
        's': SECONDS,
        'sec': SECONDS,
        'secs': SECONDS,
        'second': SECONDS,
        'seconds': SECONDS,
        'm': MINUTES,
        'min': MINUTES,
        'mins': MINUTES,
        'minute': MINUTES,
        'minutes': MINUTES,
        'h': HOURS,
        'hr': HOURS,
        'hrs': HOURS,
        'hour': HOURS,
        'hours': HOURS,
        'd': DAYS,
        'day': DAYS,
        'days': DAYS,
        'w': WEEKS,
        'wk': WEEKS,
        'wks': WEEKS,
        'week': WEEKS,
        'weeks': WEEKS,
        'mo': MONTHS,
        'mos': MONTHS,
        'month': MONTHS,
        'months': MONTHS,
        'y': YEARS,
        'yr': YEARS,
        'yrs': YEARS,
        'year': YEARS,
        'years': YEARS
    }

    def __init__(self, nanoseconds=0, microseconds=0, milliseconds=0, seconds=0,
                 minutes=0, hours=0, days=0, weeks=0, months=0, years=0):
        """
        Initialise a new Duration instance. The instance will be made to
        represent the closest nanosecond to the sum of all of the arguments.

        :param nanoseconds: The number of nanoseconds to represent.
        :param microseconds: The number of microseconds to represent.
        :param milliseconds: The number of milliseconds to represent.
        :param seconds: The number of seconds to represent.
        :param minutes: The number of minutes to represent.
        :param hours: The number of hours to represent.
        :param days: The number of days to represent.
        :param weeks: The number of weeks to represent.
        :param months: The number of months to represent.
        :param years: The number of years to represent.
        """
        self.nanoseconds = int(round(nanoseconds +  # Py2 round() returns float
                                     microseconds * self.MICROSECONDS +
                                     milliseconds * self.MILLISECONDS +
                                     seconds * self.SECONDS +
                                     minutes * self.MINUTES +
                                     hours * self.HOURS +
                                     days * self.DAYS +
                                     weeks * self.WEEKS +
                                     months * self.MONTHS +
                                     years * self.YEARS))

    @classmethod
    def from_quantity_unit(cls, quantity, unit):
        """
        Initialise a new duration object from a quantity and unit string.

        :param quantity: The number of the unit.
        :param unit: The unit as a string, e.g. 'm' or 'minutes'.
        :return: A `Duration` object representing the quantity and unit.
        """
        return Duration(nanoseconds=quantity * cls._SYMBOLS[unit])

    @classmethod
    def is_valid_symbol(cls, symbol):
        """
        Find whether a symbol is a valid unit of time.

        :param symbol: The symbol to check.
        :return: True if the symbol is a valid unit, false otherwise.
        """
        return symbol in cls._SYMBOLS

    @property
    def timedelta(self):
        """
        Get a `datetime.timedelta` representing this instance.

        :return: A timedelta equivalent to this instance. Some accuracy is lost,
                 as timedelta only goes down to the microsecond level.
        """
        return datetime.timedelta(microseconds=self.nanoseconds / 1000)

    def total_seconds(self):
        """
        Retrieve the number of seconds equivalent to this duration. This is
        compatible with `datetime.timedelta`'s identically named method.

        :return: The number of seconds represented by this duration, as a float.
        """
        return self.nanoseconds / 10 ** 9

    def human_readable(self):
        """
        Format this duration as a human-readable string of units, e.g.
        "1y 2mo", or "3w 6d 45m 20s". This is the default when no specification
        is supplied when `.format()`ing this object. This is not a property as
        there is a non-trivial amount of computation involved.

        :return: A human-readable representation of this object.
        """
        remaining = self.nanoseconds
        chunks = []
        for unit, nanos in six.iteritems(self._HUMAN_MAGNITUDES):
            quantity = int(math.floor(remaining / nanos))
            if quantity < 1:
                # skip
                continue

            suffix = '' if quantity == 1 else 's'
            chunks.append('{0} {1}{2}'.format(quantity, unit, suffix))

            remaining -= quantity * nanos
            if not remaining:  # simple optimisation
                break

        if not chunks:
            # only the case if representing Duration.ZERO
            return '0 nanoseconds'

        return ' '.join(chunks)

    @classmethod
    def from_timedelta(cls, timedelta):
        """
        Create a duration from a timedelta instance.

        :param timedelta: The `datetime.timedelta` to parse.
        :return: A `Duration` representing the same duration.
        """
        return Duration(seconds=timedelta.total_seconds())

    @classmethod
    def unit_nanoseconds(cls, unit):
        """
        Retrieve the number of nanoseconds represented by a unit.
        This allows other classes, e.g. `Speed`, to work with units of time.

        :param unit: The unit of time, e.g. 'm'.
        :return: The number of nanoseconds in one of that unit.
        :raises ValueError: If `unit` is not recognised.
        """
        if unit not in cls._SYMBOLS:
            raise ValueError('Unrecognised time unit \'{0}\''.format(unit))
        return cls._SYMBOLS[unit]

    @decorators.operator_same_class
    def __lt__(self, other):
        return self.nanoseconds < other.nanoseconds

    def __le__(self, other):
        return self < other or self == other

    @decorators.operator_same_class
    def __eq__(self, other):
        return self.nanoseconds == other.nanoseconds

    def __ne__(self, other):
        return not other == self

    def __ge__(self, other):
        return self == other or self > other

    @decorators.operator_same_class
    def __gt__(self, other):
        return self.nanoseconds > other.nanoseconds

    @decorators.operator_same_class
    def __add__(self, other):
        return Duration(nanoseconds=self.nanoseconds + other.nanoseconds)

    @decorators.operator_same_class
    def __sub__(self, other):
        if self.nanoseconds - other.nanoseconds < 0:
            raise ArithmeticError(
                'Cannot have a negative duration')
        return Duration(nanoseconds=self.nanoseconds - other.nanoseconds)

    @decorators.operator_numeric_type
    def __mul__(self, other):
        return Duration(nanoseconds=self.nanoseconds * other)

    @decorators.operator_numeric_type
    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError('Cannot divide {0} by zero'.format(self))
        return Duration(nanoseconds=round(self.nanoseconds / other))

    @decorators.operator_numeric_type
    def __floordiv__(self, other):
        if other == 0:
            raise ZeroDivisionError('Cannot divide {0} by zero'.format(self))
        return Duration(nanoseconds=self.nanoseconds // other)

    def __repr__(self):
        return '<Duration({0})>'.format(repr(self.nanoseconds))

    def __bool__(self):
        return self > Duration.ZERO

    @decorators.python_2_format_compatible
    def __format__(self, format_spec):

        # [number format|][ ][unit symbol]

        if not format_spec:
            return self.human_readable()

        num_fmt, _, unit = format_spec.rpartition('|')

        # we want to be able to support unit = ' ' so the user can choose
        # whether to have a separator without forcing the unit

        # find whether the user wants a space before the unit
        separator = ''
        if unit and unit[0] == ' ':
            separator = ' '
            unit = unit[1:]

        # if we have a unit, ensure it's valid
        if not unit:
            # attempt to find the largest unit where the quantity is >= 1 of
            # that unit
            for symbol, nanos in six.iteritems(self._MAGNITUDES):
                if self.nanoseconds >= nanos:
                    unit = symbol
                    break

            # we should only get here if this object represents 0 nanoseconds
            if not unit:
                unit = 'ns'
        elif unit not in self._SYMBOLS:
            raise TypeError('Unrecognised time unit: {0}'.format(unit))

        quantity = self.nanoseconds / self._SYMBOLS[unit]

        if not num_fmt:
            quantity = util.round_two_non_zero_dp(Decimal(quantity))
            num_fmt = ',f'

        return '{0:{1}}{2}{3}'.format(quantity, num_fmt, separator, unit)

    def __str__(self):
        return '{0}'.format(self)


# https://stackoverflow.com/a/13913933
# noinspection PyProtectedMember
Duration._MAGNITUDES = OrderedDict(
    [(symbol, Duration._SYMBOLS[symbol])
     for symbol in ['y', 'mo', 'w', 'd', 'h', 'm', 's', 'ms', 'us', 'ns']])
# noinspection PyProtectedMember
Duration._HUMAN_MAGNITUDES = OrderedDict(
    [(symbol, Duration._SYMBOLS[symbol])
     for symbol in ['year', 'month', 'week', 'day', 'hour', 'minute', 'second',
                    'millisecond', 'microsecond', 'nanosecond']])

Duration.ZERO = Duration(nanoseconds=0)
Duration.SECOND = Duration(seconds=1)
