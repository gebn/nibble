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

    def test_eq_bad_class(self):
        with self.assertRaises(NotImplementedError):
            _ = Information(1) == 1

    def test_eq_false(self):
        self.assertTrue(Information(22, Information.MEBIBYTES),
                        Information(2528, Information.KIBIBYTES))

    def test_eq_true(self):
        self.assertTrue(Information(22, Information.MEBIBYTES),
                        Information(22528, Information.KIBIBYTES))

    def test_repr(self):
        self.assertEqual(repr(Information(12345)), '<Information(12345)>')

    def test_str(self):
        self.assertEqual(str(Information(12345)), '12,345 bits')
