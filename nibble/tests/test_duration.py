# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest
import datetime

from nibble.duration import Duration


class TestDuration(unittest.TestCase):

    def test_init_microseconds(self):
        self.assertEqual(Duration(microseconds=1),
                         Duration(nanoseconds=10 ** 3))

    def test_init_milliseconds(self):
        self.assertEqual(Duration(milliseconds=1),
                         Duration(nanoseconds=10 ** 6))

    def test_init_seconds(self):
        self.assertEqual(Duration(seconds=1),
                         Duration(nanoseconds=10 ** 9))

    def test_init_minutes(self):
        self.assertEqual(Duration(minutes=1),
                         Duration(nanoseconds=10 ** 9 * 60))

    def test_init_hours(self):
        self.assertEqual(Duration(hours=1),
                         Duration(nanoseconds=10 ** 9 * 60 * 60))

    def test_init_days(self):
        self.assertEqual(Duration(days=1),
                         Duration(nanoseconds=10 ** 9 * 60 * 60 * 24))

    def test_init_weeks(self):
        self.assertEqual(Duration(weeks=1),
                         Duration(nanoseconds=10 ** 9 * 60 * 60 * 24 * 7))

    def test_init_months(self):
        self.assertEqual(Duration(months=1),
                         Duration(nanoseconds=10 ** 9 * 60 * 60 * 730))

    def test_init_years(self):
        self.assertEqual(Duration(years=1),
                         Duration(nanoseconds=10 ** 9 * 60 * 60 * 730 * 12))

    def test_total_seconds(self):
        self.assertEqual(Duration(seconds=1.5).total_seconds(),
                         datetime.timedelta(seconds=1.5).total_seconds())

    def test_from_timedelta(self):
        self.assertEqual(
            Duration.from_timedelta(datetime.timedelta(milliseconds=3500)),
            Duration(seconds=3.5))

    def test_timedelta(self):
        self.assertEqual(Duration(minutes=91.5).timedelta,
                         datetime.timedelta(seconds=5490))

    def test_lt_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Duration(1) < 1

    def test_lt_false(self):
        self.assertFalse(Duration(10) < Duration(1))

    def test_lt_true(self):
        self.assertLess(Duration(1), Duration(10))

    def test_le_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Duration(1) <= 1

    def test_le_false(self):
        self.assertFalse(Duration(10) <= Duration(1))

    def test_le_true_less(self):
        self.assertLessEqual(Duration(1), Duration(10))

    def test_le_true_equal(self):
        self.assertLessEqual(Duration(10), Duration(10))

    def test_eq_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Duration(1) == 1

    def test_eq_false(self):
        self.assertFalse(Duration(seconds=2) == Duration(milliseconds=22))

    def test_eq_true(self):
        self.assertEqual(Duration(seconds=1.5), Duration(milliseconds=1500))

    def test_ne_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Duration(1) != 1

    def test_ne_false(self):
        self.assertFalse(Duration(hours=2) != Duration(minutes=120))

    def test_ne_true(self):
        self.assertNotEqual(Duration(days=1), Duration(hours=23.999))

    def test_ge_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Duration(1) >= 1

    def test_ge_false(self):
        self.assertFalse(Duration(1) >= Duration(10))

    def test_ge_true_less(self):
        self.assertGreaterEqual(Duration(10), Duration(1))

    def test_ge_true_equal(self):
        self.assertGreaterEqual(Duration(10), Duration(10))

    def test_gt_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Duration(1) > 1

    def test_gt_false(self):
        self.assertFalse(Duration(1) > Duration(10))

    def test_gt_true(self):
        self.assertGreater(Duration(10), Duration(1))

    def test_add_bad_class(self):
        with self.assertRaises(TypeError):
            Duration(1) + 1

    def test_add(self):
        self.assertEqual(Duration(seconds=30) + Duration(minutes=1),
                         Duration(seconds=90))

    def test_sub_bad_class(self):
        with self.assertRaises(TypeError):
            Duration(1) - 1

    def test_sub_negative(self):
        with self.assertRaises(ArithmeticError):
            Duration(7) - Duration(10)

    def test_sub(self):
        self.assertEqual(Duration(7) - Duration(4), Duration(3))

    def test_mul_bad_class(self):
        with self.assertRaises(TypeError):
            Duration(1) * ''

    def test_mul(self):
        self.assertEqual(Duration(7) * 4, Duration(28))

    def test_truediv_bad_class(self):
        with self.assertRaises(TypeError):
            Duration(1) / ''

    def test_truediv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = Duration(1) / 0

    def test_truediv_low(self):  # 1.33 should go down
        self.assertEqual(Duration(4) / 3, Duration(1))

    def test_truediv_high(self):  # 1.66 should go up
        self.assertEqual(Duration(5) / 3, Duration(2))

    def test_floordiv_bad_class(self):
        with self.assertRaises(TypeError):
            Duration(1) // ''

    def test_floordiv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = Duration(1) // 0

    def test_floordiv_low(self):  # 1.33 should go down
        self.assertEqual(Duration(4) // 3, Duration(1))

    def test_floordiv_high(self):  # 1.66 should go down
        self.assertEqual(Duration(5) // 3, Duration(1))

    def test_bool_true(self):
        self.assertTrue(Duration(1))

    def test_bool_false(self):
        self.assertFalse(Duration.ZERO)

    def test_format_num_fmt_comma(self):
        self.assertEqual('{0:,.0f|}'.format(Duration(years=1000)), '1,000y')

    def test_format_num_fmt_decimal_places(self):
        self.assertEqual('{0:.2f|}'.format(Duration(days=1.1)), '1.10d')

    def test_format_separator(self):
        self.assertEqual('{0: }'.format(Duration(days=1)), '1 d')

    def test_format_force_unit_separator(self):
        self.assertEqual('{0: m}'.format(Duration(seconds=90)), '1.50 m')

    def test_format_force_unit_no_separator(self):
        self.assertEqual('{0:s}'.format(Duration(minutes=1.5)), '90s')

    def test_format_invalid_unit(self):
        with self.assertRaises(TypeError):
            '{0:foo}'.format(Duration(minutes=1.5))

    def test_format_2dp(self):
        self.assertEqual('{0:y}'.format(Duration(days=3.65)), '0.01y')

    # FIXME
    @unittest.skip('Issue #1')
    def test_format_3dp(self):
        self.assertEqual('{0:y}'.format(Duration(hours=8.76581277)), '0.001y')

    # FIXME
    @unittest.skip('Issue #1')
    def test_format_8dp(self):
        self.assertEqual('{0:y}'.format(Duration(seconds=1)), '0.000000032y')

    def test_format_default(self):
        self.assertEqual('{0}'.format(Duration(hours=2)), '2h')

    def test_format_zero(self):
        self.assertEqual('{0}'.format(Duration.ZERO), '0ns')

    def test_repr(self):
        self.assertEqual(repr(Duration(minutes=1, seconds=0.1)),
                         '<Duration(60100000000)>')

    def test_str_nanoseconds(self):
        self.assertEqual(str(Duration(microseconds=0.015)), '15ns')

    def test_str_microseconds(self):
        self.assertEqual(str(Duration(milliseconds=0.039)), '39us')

    def test_str_milliseconds(self):
        self.assertEqual(str(Duration(microseconds=13000)), '13ms')

    def test_str_s(self):
        self.assertEqual(str(Duration(minutes=0.5)), '30s')

    def test_str_m(self):
        self.assertEqual(str(Duration(hours=0.25)), '15m')

    def test_str_h(self):
        self.assertEqual(str(Duration(minutes=120)), '2h')

    def test_str_d(self):
        self.assertEqual(str(Duration(hours=48)), '2d')

    def test_str_w(self):
        self.assertEqual(str(Duration(days=14)), '2w')

    def test_str_mo(self):
        self.assertEqual(str(Duration(years=1) / 12), '1mo')

    def test_str_y(self):
        self.assertEqual(str(Duration(months=24)), '2y')
