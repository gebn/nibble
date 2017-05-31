# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from collections import OrderedDict
from decimal import Decimal
import datetime
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

    UNITS = OrderedDict([
        ('y', YEARS),
        ('mo', MONTHS),
        ('w', WEEKS),
        ('d', DAYS),
        ('h', HOURS),
        ('m', MINUTES),
        ('s', SECONDS),
        ('ms', MILLISECONDS),
        ('us', MICROSECONDS),
        ('ns', NANOSECONDS),
    ])

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

    @classmethod
    def from_timedelta(cls, timedelta):
        """
        Create a duration from a timedelta instance.

        :param timedelta: The `datetime.timedelta` to parse.
        :return: A `Duration` representing the same duration.
        """
        return Duration(seconds=timedelta.total_seconds())

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
            for symbol, nanos in six.iteritems(self.UNITS):
                if self.nanoseconds >= nanos:
                    unit = symbol
                    break

            # we should only get here if this object represents 0 nanoseconds
            if not unit:
                unit = 'ns'
        elif unit not in self.UNITS:
            raise TypeError('Unrecognised time unit: {0}'.format(unit))

        quantity = self.nanoseconds / self.UNITS[unit]

        if not num_fmt:
            quantity = util.round_two_non_zero_dp(Decimal(quantity))
            num_fmt = ',f'

        return '{0:{1}}{2}{3}'.format(quantity, num_fmt, separator, unit)

    def __str__(self):
        return '{0}'.format(self)


Duration.ZERO = Duration(nanoseconds=0)
Duration.SECOND = Duration(seconds=1)
