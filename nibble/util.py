# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP


def round_two_non_zero_dp(decimal):
    """
    Rounds a number to the first two non-zero decimal places.
    Adapted from https://stackoverflow.com/a/38838513/2765666.
    
    :param decimal: The decimal number to round.
    :return: A new decimal representing the rounded value.
    """
    log10 = decimal.log10().to_integral_exact(rounding=ROUND_FLOOR) \
        if decimal else 0
    div = Decimal(10) ** (Decimal(1) - log10) if log10 < 0 else Decimal(100)
    return (decimal * div).to_integral_exact(rounding=ROUND_HALF_UP) / div
