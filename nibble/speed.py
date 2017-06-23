# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import re
import six

from nibble.information import Information
from nibble.duration import Duration
from nibble import decorators


@decorators.python_2_div_compatible
@decorators.python_2_nonzero_compatible
@six.python_2_unicode_compatible
class Speed(object):
    """
    Represents a quantity of information processed over a period of time.
    """

    # matches a duration with a unit
    DURATION_REGEX = re.compile(r'^(\d+\.?\d*)\s*(\w+)')

    def __init__(self, information, duration=Duration.SECOND):
        """
        Initialise a new speed measurement.
        
        :param information: The information processed.
        :param duration: The time taken to process the information. Defaults to
                         one second.
        """

        if duration == Duration.ZERO:
            raise ValueError('Speed cannot be infinite')

        self.information = information
        self.duration = duration

    @classmethod
    def from_quantity_units(cls, quantity, information_unit, duration_unit):
        """
        Initialise a new speed object from a quantity and unit string.

        :param quantity: The number of the unit.
        :param information_unit: The information part of the unit, e.g. 'GiB'.
        :param duration_unit: The duration part of the unit, e.g. 'week'.
        :return: A `Speed` object representing the quantity and unit.
        """
        information = Information.from_quantity_unit(quantity, information_unit)
        duration = Duration.from_quantity_unit(1, duration_unit)
        return Speed(information, duration)

    @property
    def _per_second(self):
        """
        The amount of information processed per second at this speed. This
        normalised value is used for comparing speeds.
        
        :return: The amount of information processed per second at this speed.
        """
        return self.information / self.duration.total_seconds()

    def for_duration(self, duration):
        """
        Find the quantity of information processed if this speed is maintained
        for a certain amount of time.
        
        :param duration: The amount of time this speed is maintained for.
        :return: The resulting amount of information processed.
        """
        scale = duration.nanoseconds / self.duration.nanoseconds
        return self.information * scale

    @decorators.operator_same_class
    def __lt__(self, other):
        return self._per_second < other._per_second

    def __le__(self, other):
        return self < other or self == other

    @decorators.operator_same_class
    def __eq__(self, other):
        return self._per_second == other._per_second

    def __ne__(self, other):
        return not other == self

    def __ge__(self, other):
        return self == other or self > other

    @decorators.operator_same_class
    def __gt__(self, other):
        return self._per_second > other._per_second

    @decorators.operator_same_class
    def __add__(self, other):
        return Speed(self._per_second + other._per_second)

    @decorators.operator_same_class
    def __sub__(self, other):
        try:
            difference = self._per_second - other._per_second
            if difference == Information.ZERO:
                raise ArithmeticError('Cannot have an infinite speed')
            return Speed(difference)
        except ArithmeticError:
            # negative result
            raise ArithmeticError('Cannot have a negative speed')

    @decorators.operator_numeric_type
    def __mul__(self, other):
        return Speed(self.information * other, self.duration)

    @decorators.operator_numeric_type
    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError('Cannot divide {0} by zero'.format(self))
        return Speed(self.information / other, self.duration)

    @decorators.operator_numeric_type
    def __floordiv__(self, other):
        if other == 0:
            raise ZeroDivisionError('Cannot divide {0} by zero'.format(self))
        return Speed(self.information // other, self.duration)

    def __repr__(self):
        return '<Speed({0}, {1})>'.format(repr(self.information),
                                          repr(self.duration))

    def __bool__(self):
        return self._per_second > Information.ZERO

    @decorators.python_2_format_compatible
    def __format__(self, format_spec):
        # Defaults to <the most appropriate binary bytes unit> per second
        # [number format|][ ][unit symbol or category][/[quantity][ ]time unit]

        lhs, _, time = format_spec.partition('/')

        if time:
            match = self.DURATION_REGEX.match(time)
            if match:
                # quantity provided
                quantity = float(match.group(1))
                if quantity.is_integer():
                    quantity = int(quantity)
                unit = match.group(2)
            else:
                # no quantity
                quantity = 1
                unit = time

            if not lhs:
                # this is a workaround to maintain the separator '/m' should
                # result in a separator not being printed, but '' is passed to
                # Information as the lhs, so it goes to default formatting
                lhs = 'bB'
        else:
            quantity = 1
            unit = 's'

        try:
            nanos = quantity * Duration.unit_nanoseconds(unit)
        except ValueError as e:
            raise TypeError(e)

        information = self.information * nanos / self.duration.nanoseconds

        time_fmt = unit if quantity == 1 else '{0}{1}'.format(quantity, unit)
        return '{0:{1}}/{2}'.format(information, lhs, time_fmt)

    def __str__(self):
        return '{0}'.format(self)


Speed.ZERO = Speed(Information.ZERO)

# Ethernet
Speed.TEN_MEGABIT = Speed(Information(10, Information.MEGABITS))
Speed.HUNDRED_MEGABIT = Speed.TEN_MEGABIT * 10
Speed.GIGABIT = Speed.HUNDRED_MEGABIT * 10
Speed.TEN_GIGABIT = Speed.GIGABIT * 10
Speed.FORTY_GIGABIT = Speed.TEN_GIGABIT * 4
Speed.HUNDRED_GIGABIT = Speed.TEN_GIGABIT * 10

# E-carrier
Speed.E0 = Speed(Information(64, Information.KILOBITS))
Speed.E1 = Speed(Information(2.048, Information.MEGABITS))
Speed.E2 = Speed(Information(8.448, Information.MEGABITS))
Speed.E3 = Speed(Information(34.368, Information.MEGABITS))
Speed.E4 = Speed(Information(139.264, Information.MEGABITS))
Speed.E5 = Speed(Information(565.148, Information.MEGABITS))

# T-carrier signaling
Speed.DS0 = Speed.E0
Speed.DS1 = Speed(Information(1.544, Information.MEGABITS))
Speed.DS1C = Speed(Information(3.152, Information.MEGABITS))
Speed.DS2 = Speed(Information(6.312, Information.MEGABITS))
Speed.DS3 = Speed(Information(44.736, Information.MEGABITS))
Speed.DS4 = Speed(Information(274.176, Information.MEGABITS))
Speed.DS5 = Speed(Information(400.352, Information.MEGABITS))

# T-carrier lines
Speed.T1 = Speed.DS1
Speed.T1C = Speed.DS1C
Speed.T2 = Speed.DS2
Speed.T3 = Speed.DS3
Speed.T4 = Speed.DS4
Speed.T5 = Speed.DS5
