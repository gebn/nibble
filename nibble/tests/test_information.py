# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest
from collections import OrderedDict
import six

from nibble.information import Information
from nibble.duration import Duration
from nibble.speed import Speed


class TestInformation(unittest.TestCase):

    def test_init_integer(self):
        information = Information(2, Information.GIBIBYTES)
        self.assertEqual(information, Information(17179869184))

    def test_init_float(self):
        information = Information(2.4, Information.GIBIBYTES)
        self.assertIsInstance(information.bits, int)
        self.assertEqual(information, Information(20615843021))

    def test_at_speed(self):
        speed = Speed(Information(100, Information.GIBIBYTES),
                      Duration(seconds=1))
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual(information.at_speed(speed),
                         Duration(milliseconds=100))

    def test_in_duration(self):
        information = Information(10, Information.MEGABYTES)
        self.assertEqual(information.in_duration(Duration(seconds=5)),
                         Speed(Information(2, Information.MEGABYTES),
                               Duration(seconds=1)))

    def test_parse_rubbish(self):
        with self.assertRaises(ValueError):
            Information.parse('rubbish')

    def test_parse_invalid_number(self):
        with self.assertRaises(ValueError):
            Information.parse('1.2.3 TiB')

    def test_parse_invalid_unit(self):
        with self.assertRaises(ValueError):
            Information.parse('1 TiBoo')

    def test_parse_integer(self):
        self.assertEqual(Information.parse('123 YiB'),
                         Information(2 ** 80 * 123 * 8, Information.BITS))

    def test_parse_decimal(self):
        self.assertEqual(Information.parse('1.4 GB'),
                         Information(10 ** 9 * 1.4 * 8, Information.BITS))

    def test_lt_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Information(1) < 1

    def test_lt_false(self):
        self.assertFalse(Information(10) < Information(1))

    def test_lt_true(self):
        self.assertLess(Information(1), Information(10))

    def test_le_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Information(1) <= 1

    def test_le_false(self):
        self.assertFalse(Information(10) <= Information(1))

    def test_le_true_less(self):
        self.assertLessEqual(Information(1), Information(10))

    def test_le_true_equal(self):
        self.assertLessEqual(Information(10), Information(10))

    def test_eq_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Information(1) == 1

    def test_eq_false(self):
        self.assertFalse(Information(22, Information.MEBIBYTES) ==
                         Information(2528, Information.KIBIBYTES))

    def test_eq_true(self):
        self.assertEqual(Information(22, Information.MEBIBYTES),
                         Information(22528, Information.KIBIBYTES))

    def test_ne_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Information(1) != 1

    def test_ne_false(self):
        self.assertFalse(Information(22, Information.MEBIBYTES) !=
                         Information(22528, Information.KIBIBYTES))

    def test_ne_true(self):
        self.assertNotEqual(Information(22, Information.MEBIBYTES),
                            Information(2528, Information.KIBIBYTES))

    def test_ge_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Information(1) >= 1

    def test_ge_false(self):
        self.assertFalse(Information(1) >= Information(10))

    def test_ge_true_less(self):
        self.assertGreaterEqual(Information(10), Information(1))

    def test_ge_true_equal(self):
        self.assertGreaterEqual(Information(10), Information(10))

    def test_gt_bad_class(self):
        with self.assertRaises(TypeError):
            _ = Information(1) > 1

    def test_gt_false(self):
        self.assertFalse(Information(1) > Information(10))

    def test_gt_true(self):
        self.assertGreater(Information(10), Information(1))

    def test_add_bad_class(self):
        with self.assertRaises(TypeError):
            Information(1) + 1

    def test_add(self):
        self.assertEqual(Information(10) + Information(10), Information(20))

    def test_sub_bad_class(self):
        with self.assertRaises(TypeError):
            Information(1) - 1

    def test_sub_negative(self):
        with self.assertRaises(ArithmeticError):
            Information(7) - Information(10)

    def test_sub(self):
        self.assertEqual(Information(7) - Information(4), Information(3))

    def test_mul_bad_class(self):
        with self.assertRaises(TypeError):
            Information(1) * ''

    def test_mul(self):
        self.assertEqual(Information(7) * 4, Information(28))

    def test_truediv_bad_class(self):
        with self.assertRaises(TypeError):
            Information(1) / ''

    def test_truediv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            Information(1) / 0

    def test_truediv_low(self):  # 1.33 should go down
        self.assertEqual(Information(4) / 3, Information(1))

    def test_truediv_high(self):  # 1.66 should go up
        self.assertEqual(Information(5) / 3, Information(2))

    def test_floordiv_bad_class(self):
        with self.assertRaises(TypeError):
            Information(1) // ''

    def test_floordiv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            Information(1) // 0

    def test_floordiv_low(self):  # 1.33 should go down
        self.assertEqual(Information(4) // 3, Information(1))

    def test_floordiv_high(self):  # 1.66 should go down
        self.assertEqual(Information(5) // 3, Information(1))

    def test_bool_true(self):
        self.assertTrue(Information(1))

    def test_bool_false(self):
        self.assertFalse(Information.ZERO)

    def test_expand_units(self):
        units = ['TiB', 'B', 'YiB']
        self.assertEqual(Information._expand_units(units),
                         OrderedDict([(unit, Information._SYMBOLS[unit])
                                      for unit in units]))

    def test_determine_unit_symbol_quantity(self):
        for category in [Information.BINARY_BITS, Information.BINARY_BYTES,
                         Information.DECIMAL_BITS, Information.DECIMAL_BYTES]:
            expanded = Information._expand_units(category)
            for unit, bits in six.iteritems(expanded):
                # ensure this unit is used when we want to represent the exact
                # amount of data that it is equivalent to
                self.assertEqual(
                    Information._determine_unit_symbol_quantity(bits, category),
                    unit)

                # we should also use the same unit for this number of bits + 1
                # (assuming units are not close together)
                self.assertEqual(
                    Information._determine_unit_symbol_quantity(
                        bits + 1, category),
                    unit)

    def test_format_default(self):
        information = Information(1234, Information.GIBIBYTES)
        self.assertEqual('{0}'.format(information), '1.21 TiB')

    def test_format_zero(self):
        self.assertEqual('{0}'.format(Information.ZERO), '0 b')

    def test_format_invalid_unit(self):
        with self.assertRaises(TypeError):
            '{0:foo}'.format(Information.ZERO)

    def test_format_separator(self):
        information = Information(1234, Information.GIBIBYTES)
        self.assertEqual('{0: }'.format(information), '1.21 TiB')

    def test_format_separator_unit(self):
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual('{0: GB}'.format(information), '10.74 GB')

    def test_format_megabytes(self):
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual('{0:M}'.format(information), '10,240M')

    def test_format_gibibytes(self):
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual('{0:G}'.format(information), '10G')

    def test_format_comma_separator_unit(self):
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual('{0:,.0f| MiB}'.format(information), '10,240 MiB')

    def test_format_comma_2dp_unit(self):
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual('{0:,.2f|MiB}'.format(information), '10,240.00MiB')

    def test_format_2dp_separator_unit(self):
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual('{0:.2f| Gb}'.format(information), '85.90 Gb')

    def test_format_4dp_separator_unit(self):
        information = Information(10, Information.GIBIBYTES)
        self.assertEqual('{0:.4f| Gb}'.format(information), '85.8993 Gb')

    def test_repr(self):
        self.assertEqual(repr(Information(12345)), '<Information(12345)>')

    def test_str(self):
        self.assertEqual(str(Information(12345)), '1.51 KiB')
