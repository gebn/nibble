# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest

from nibble.information import Information
from nibble.duration import Duration
from nibble.speed import Speed


class TestSpeed(unittest.TestCase):

    _INFORMATION = Information(10)
    _DURATION = Duration.SECOND
    _SPEED = Speed(_INFORMATION, _DURATION)

    def test_init_instant(self):
        with self.assertRaises(ValueError):
            Speed(Information(1), Duration.ZERO)

    def test_per_second(self):
        self.assertEqual(Speed.FORTY_GIGABIT._per_second,
                         Information(40000, Information.MEGABITS))

    def test_for_duration(self):
        self.assertEqual(self._SPEED.for_duration(Duration(minutes=1)),
                         self._INFORMATION * 60)
    
    def test_lt_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.TEN_GIGABIT < 1

    def test_lt_false(self):
        self.assertFalse(Speed.TEN_GIGABIT < Speed.GIGABIT)

    def test_lt_true(self):
        self.assertLess(Speed.GIGABIT, Speed.TEN_GIGABIT)

    def test_le_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT <= 1

    def test_le_false(self):
        self.assertFalse(Speed.TEN_GIGABIT <= Speed.GIGABIT)

    def test_le_true_less(self):
        self.assertLessEqual(Speed.GIGABIT, Speed.TEN_GIGABIT)

    def test_le_true_equal(self):
        self.assertLessEqual(Speed.TEN_GIGABIT, Speed.TEN_GIGABIT)

    def test_eq_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT == 1

    def test_eq_false(self):
        self.assertFalse(Speed.GIGABIT == Speed.TEN_GIGABIT)

    def test_eq_true(self):
        self.assertEqual(Speed.GIGABIT,
                         Speed(Information(10, Information.GIGABITS),
                               Duration(seconds=10)))

    def test_ne_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT != 1

    def test_ne_false(self):
        self.assertFalse(Speed.FORTY_GIGABIT !=
                         Speed(Information(80, Information.GIGABITS),
                               Duration(seconds=2)))

    def test_ne_true(self):
        self.assertNotEqual(Speed.FORTY_GIGABIT, Speed.HUNDRED_GIGABIT)

    def test_ge_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT >= 1

    def test_ge_false(self):
        self.assertFalse(Speed.GIGABIT >= Speed.TEN_GIGABIT)

    def test_ge_true_less(self):
        self.assertGreaterEqual(Speed.TEN_GIGABIT, Speed.GIGABIT)

    def test_ge_true_equal(self):
        self.assertGreaterEqual(Speed.TEN_GIGABIT, Speed.TEN_GIGABIT)

    def test_gt_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT > 1

    def test_gt_false(self):
        self.assertFalse(Speed.GIGABIT > Speed.TEN_GIGABIT)

    def test_gt_true(self):
        self.assertGreater(Speed.TEN_GIGABIT, Speed.GIGABIT)

    def test_add_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT + 1

    def test_add(self):
        self.assertEqual(Speed(Information(500, Information.MEGABITS),
                               Duration(seconds=1)) +
                         Speed(Information(2.5, Information.GIGABITS),
                               Duration(seconds=5)),
                         Speed.GIGABIT)

    def test_sub_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT - 1

    def test_sub_zero(self):
        with self.assertRaises(ArithmeticError):
            _ = Speed.GIGABIT * 10 - Speed.TEN_GIGABIT

    def test_sub_negative(self):
        with self.assertRaises(ArithmeticError):
            _ = Speed.GIGABIT - Speed.TEN_GIGABIT

    def test_sub(self):
        self.assertEqual(Speed.TEN_GIGABIT - Speed.GIGABIT,
                         Speed(Information(90, Information.GIGABITS),
                               Duration(seconds=10)))

    def test_mul_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT * ''

    def test_mul(self):
        self.assertEqual(Speed.TEN_GIGABIT * 4, Speed.FORTY_GIGABIT)

    def test_truediv_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT / ''

    def test_truediv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = Speed.GIGABIT / 0

    def test_truediv_low(self):  # 1.33 should go down
        self.assertEqual(Speed(Information(4), Duration(1)) / 3,
                         Speed(Information(1), Duration(1)))

    def test_truediv_high(self):  # 1.66 should go up
        self.assertEqual(Speed(Information(10), Duration(1)) / 6,
                         Speed(Information(20), Duration(10)))

    def test_floordiv_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Speed.GIGABIT // ''

    def test_floordiv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = Speed.GIGABIT // 0

    def test_floordiv_low(self):  # 1.33 should go down
        self.assertEqual(Speed(Information(4), Duration(1)) // 3,
                         Speed(Information(1), Duration(1)))

    def test_floordiv_high(self):  # 1.66 should go down
        self.assertEqual(Speed(Information(10), Duration(1)) // 6,
                         Speed(Information(1), Duration(1)))

    def test_bool_true(self):
        self.assertTrue(Speed.HUNDRED_MEGABIT)

    def test_bool_false(self):
        self.assertFalse(Speed.ZERO)

    def test_format_default(self):
        self.assertEqual('{0}'.format(Speed.GIGABIT), '119.21 MiB/s')

    def test_format_zero(self):
        self.assertEqual('{0}'.format(Speed.ZERO), '0 b/s')

    def test_format_info_unit(self):
        # force Gb
        self.assertEqual('{0:Gb}'.format(Speed.GIGABIT), '1Gb/s')

    def test_format_invalid_time_unit(self):
        with self.assertRaises(TypeError):
            '{0:/z}'.format(self._SPEED)

    def test_format_invalid_info_unit(self):
        with self.assertRaises(TypeError):
            '{0:foo}'.format(self._DURATION)

    def test_format_separator_info_unit(self):
        speed = Speed(Information(1, Information.TERABITS), Duration.SECOND)
        self.assertEqual('{0: Gb}'.format(speed), '1,000 Gb/s')

    def test_format_time_unit(self):
        # use per minute instead of seconds, and work out the quantity in binary
        # bytes
        self.assertEqual('{0:/m}'.format(Speed.GIGABIT), '6.98GiB/m')

    def test_format_separator_time_unit(self):
        self.assertEqual('{0: /m}'.format(Speed.GIGABIT), '6.98 GiB/m')

    def test_format_info_category_time_unit(self):
        # work out the quantity in binary bit units per hour, putting a space
        # between the quantity and unit, and using default formatting for the
        # quantity,
        self.assertEqual('{0: bb/h}'.format(Speed.GIGABIT), '3.27 Tib/h')

    def test_format_info_unit_time_unit(self):
        # use per minute instead of seconds, and work out the quantity in MiB
        self.assertEqual('{0: MiB/m}'.format(Speed.HUNDRED_MEGABIT),
                         '715.26 MiB/m')

    def test_format(self):
        # show the quantity of information processed per month to 2dp with comma
        # separated thousands, with a space after, then a decimal bytes unit
        self.assertEqual('{0:,.2f|dB/mo}'.format(Speed.GIGABIT), '328.50TB/mo')

    def test_repr(self):
        self.assertEqual(repr(self._SPEED),
                         '<Speed(<Information(10)>, <Duration(1000000000)>)>')

    def test_str(self):
        self.assertEqual(str(self._SPEED), '1.25 B/s')
