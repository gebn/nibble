# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest
from decimal import Decimal
import six

from nibble import util


class TestRoundTwoNonZeroDp(unittest.TestCase):
    _CASES = {
        Decimal('123'): Decimal('123'),
        Decimal('12.3'): Decimal('12.3'),
        Decimal('1.23'): Decimal('1.23'),
        Decimal('1.01'): Decimal('1.01'),
        Decimal('0.1234'): Decimal('0.12'),
        Decimal('0.01234'): Decimal('0.012'),
        Decimal('0.00266'): Decimal('0.0027'),
        Decimal('0.00236'): Decimal('0.0024'),
        Decimal('0.000010101'): Decimal('0.00001'),
        Decimal('0.00000805'): Decimal('0.0000081'),
        Decimal('0.000000031709791983764586'): Decimal('0.000000032')
    }

    def test_all(self):
        for input_, output in six.iteritems(self._CASES):
            self.assertEqual(util.round_two_non_zero_dp(input_), output)
