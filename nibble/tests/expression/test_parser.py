# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from nibble.information import Information
from nibble.duration import Duration
from nibble.speed import Speed
from nibble.expression.parser import Parser, ParsingError


class TestParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = Parser()

    def test_empty(self):
        with self.assertRaises(ParsingError):
            self.parser.parse('')

    def test_invalid_semantics(self):
        with self.assertRaises(ParsingError):
            self.parser.parse('10Gb/s at 1 minute')

    def test_expression_information(self):
        self.assertEqual(self.parser.parse('10Gb'),
                         Information(10, Information.GIGABITS))

    def test_expression_duration(self):
        self.assertEqual(self.parser.parse('12.5 minutes'),
                         Duration(minutes=12.5))

    def test_expression_speed(self):
        self.assertEqual(self.parser.parse('11.25Yib/8years'),
                         Speed(Information(13600415470664578215444480),
                               Duration(years=8)))

    def test_information_constructor(self):
        self.assertEqual(self.parser.parse('10.4Gb'),
                         Information(10.4, Information.GIGABITS))

    def test_information_duration_speed(self):
        self.assertEqual(self.parser.parse('11 minutes at 10Gb/s'),
                         Information(10 * 60 * 11, Information.GIGABITS))

    def test_information_speed_duration(self):
        self.assertEqual(self.parser.parse('10Gb/s for 11 minutes'),
                         Information(10 * 60 * 11, Information.GIGABITS))

    def test_information_conversion(self):
        self.assertEqual(self.parser.parse('12 Tb in Mb'), '12,000,000 Mb')

    def test_duration_duration_unit(self):
        self.assertEqual(self.parser.parse('minute'), Duration(minutes=1))

    def test_duration_number_duration_unit(self):
        self.assertEqual(self.parser.parse('14.7 hours'), Duration(hours=14.7))

    def test_duration_number_duration_unit_duration(self):
        self.assertEqual(self.parser.parse('14h 2s 8m'),
                         Duration(hours=14, minutes=8, seconds=2))

    def test_duration_information_speed(self):
        duration = Information(17.3, Information.GIGABYTES).at_speed(
            Speed(Information(688.3, Information.KILOBYTES)))
        self.assertEqual(self.parser.parse('17.3GB at 688.3kB/s'), duration)

    def test_duration_conversion(self):
        self.assertEqual(self.parser.parse('14y 2.5w in months'),
                         '168.58 months')

    def test_speed_constructor(self):
        self.assertEqual(self.parser.parse('12 MiB/3s'),
                         Speed(Information(4, Information.MEBIBYTES)))

    def test_speed_information_duration(self):
        self.assertEqual(self.parser.parse('11 b in 2 nanoseconds'),
                         Speed(Information(11), Duration(nanoseconds=2)))

    def test_speed_conversion(self):
        self.assertEqual(self.parser.parse('10 gigabits/s in tebibytes/hour'),
                         '4.09 tebibytes/hour')
