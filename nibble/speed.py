# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
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

    def __init__(self, information, duration):
        """
        Initialise a new speed measurement.
        
        :param information: The information processed.
        :param duration: The time taken to process the information.
        """

        if duration == Duration.ZERO:
            raise ValueError('Speed cannot be infinite')

        self.information = information
        self.duration = duration

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
        return Speed(self._per_second + other._per_second, Duration(seconds=1))

    @decorators.operator_same_class
    def __sub__(self, other):
        try:
            difference = self._per_second - other._per_second
            if difference == Information.ZERO:
                raise ArithmeticError('Cannot have an infinite speed')
            return Speed(difference, Duration(seconds=1))
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
        # [number format|][ ][unit symbol or category][/time unit]

        lhs, _, time_unit = format_spec.partition('/')

        data_passed = time_unit != ''

        if not time_unit:
            time_unit = 's'
        # TODO extract to method so don't have to access UNITS directly
        elif time_unit not in Duration.UNITS:
            raise TypeError('Unrecognised time unit: {0}'.format(time_unit))

        nanos = Duration.UNITS[time_unit]
        information = self.information * nanos / self.duration.nanoseconds

        if data_passed and not lhs:
            # this is a workaround to maintain the separator '/m' should result
            # in a separator not being printed, but '' is passed to Information
            # as the lhs, so it goes to default formatting
            lhs = 'bB'

        return '{0:{1}}/{2}'.format(information, lhs, time_unit)

    def __str__(self):
        return '{0}'.format(self)


Speed.ZERO = Speed(Information.ZERO, Duration.SECOND)
Speed.TEN_MEGABIT = Speed(Information(10, Information.MEGABITS),
                          Duration.SECOND)
Speed.HUNDRED_MEGABIT = Speed.TEN_MEGABIT * 10
Speed.GIGABIT = Speed.HUNDRED_MEGABIT * 10
Speed.TEN_GIGABIT = Speed.GIGABIT * 10
Speed.FORTY_GIGABIT = Speed.TEN_GIGABIT * 4
Speed.HUNDRED_GIGABIT = Speed.TEN_GIGABIT * 10
