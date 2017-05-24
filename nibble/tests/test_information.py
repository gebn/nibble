# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from nibble.information import Information


class TestInformation(unittest.TestCase):

    def test_parse_garbage(self):
        with self.assertRaises(ValueError):
            Information.parse('no quantity at all')

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
        with self.assertRaises(NotImplementedError):
            _ = Information(1) < 1

    def test_lt_false(self):
        self.assertFalse(Information(10) < Information(1))

    def test_lt_true(self):
        self.assertLess(Information(1), Information(10))

    def test_le_bad_class(self):
        with self.assertRaises(NotImplementedError):
            _ = Information(1) <= 1

    def test_le_false(self):
        self.assertFalse(Information(10) <= Information(1))

    def test_le_true_less(self):
        self.assertLessEqual(Information(1), Information(10))

    def test_le_true_equal(self):
        self.assertLessEqual(Information(10), Information(10))

    def test_eq_bad_class(self):
        with self.assertRaises(NotImplementedError):
            _ = Information(1) == 1

    def test_eq_false(self):
        self.assertFalse(Information(22, Information.MEBIBYTES) ==
                         Information(2528, Information.KIBIBYTES))

    def test_eq_true(self):
        self.assertEqual(Information(22, Information.MEBIBYTES),
                         Information(22528, Information.KIBIBYTES))

    def test_ne_bad_class(self):
        with self.assertRaises(NotImplementedError):
            _ = Information(1) != 1

    def test_ne_false(self):
        self.assertFalse(Information(22, Information.MEBIBYTES) !=
                         Information(22528, Information.KIBIBYTES))

    def test_ne_true(self):
        self.assertNotEqual(Information(22, Information.MEBIBYTES),
                            Information(2528, Information.KIBIBYTES))

    def test_ge_bad_class(self):
        with self.assertRaises(NotImplementedError):
            _ = Information(1) >= 1

    def test_ge_false(self):
        self.assertFalse(Information(1) >= Information(10))

    def test_ge_true_less(self):
        self.assertGreaterEqual(Information(10), Information(1))

    def test_ge_true_equal(self):
        self.assertGreaterEqual(Information(10), Information(10))

    def test_gt_bad_class(self):
        with self.assertRaises(NotImplementedError):
            _ = Information(1) > 1

    def test_gt_false(self):
        self.assertFalse(Information(1) > Information(10))

    def test_gt_true(self):
        self.assertGreater(Information(10), Information(1))

    def test_add_bad_class(self):
        with self.assertRaises(NotImplementedError):
            Information(1) + 1

    def test_add(self):
        self.assertEqual(Information(10) + Information(10), Information(20))

    def test_sub_bad_class(self):
        with self.assertRaises(NotImplementedError):
            Information(1) - 1

    def test_sub_negative(self):
        with self.assertRaises(ArithmeticError):
            Information(7) - Information(10)

    def test_sub(self):
        self.assertEqual(Information(7) - Information(4), Information(3))

    def test_mul_bad_class(self):
        with self.assertRaises(NotImplementedError):
            Information(1) * 1

    def test_mul(self):
        self.assertEqual(Information(7) * Information(4), Information(28))

    def test_truediv_bad_class(self):
        with self.assertRaises(NotImplementedError):
            Information(1) / 1

    def test_truediv(self):
        self.assertEqual(Information(3) / Information(2), Information(2))

    def test_repr(self):
        self.assertEqual(repr(Information(12345)), '<Information(12345)>')

    def test_str(self):
        self.assertEqual(str(Information(12345)), '12,345 bits')
