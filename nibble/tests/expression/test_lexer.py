# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from ply.lex import LexToken

from nibble import Lexer, LexingError


class TestLexer(unittest.TestCase):

    @staticmethod
    def make_tok(type_, value, lineno, lexpos):
        token = LexToken()
        token.type = type_
        token.value = value
        token.lineno = lineno
        token.lexpos = lexpos
        return token

    def assert_tok_equal(self, a, b):
        self.assertTrue(a.type == b.type and
                        a.value == b.value and
                        a.lineno == b.lineno and
                        a.lexpos == b.lexpos,
                        'Tokens {0} and {1} differ'.format(repr(a), repr(b)))

    def assert_lex_produces(self, input, tokens):
        result = list(self.lexer.lex(input))
        self.assertEqual(len(result), len(tokens),
                         'Token streams are of different length ({0} and '
                         '{1})'.format(len(result), len(tokens)))
        for expected, actual in zip(tokens, result):
            self.assert_tok_equal(expected, actual)

    @classmethod
    def setUpClass(cls):
        cls.lexer = Lexer()

    def test_empty(self):
        with self.assertRaises(StopIteration):
            next(self.lexer.lex(''))

    def test_no_valid_tokens(self):
        with self.assertRaises(LexingError):
            next(self.lexer.lex('sdfgs foo bar'))

    def test_garbage(self):
        with self.assertRaises(LexingError):
            next(self.lexer.lex(' ̇ ̈ ̉ ̊ ̋ ̌ ̍̒'))

    def test_invalid_middle(self):
        with self.assertRaises(LexingError):
            list(self.lexer.lex('12MiB/s in 12z in GiB/d'))

    def test_at(self):
        self.assert_lex_produces('at', [self.make_tok('AT', 'at', 1, 0)])

    def test_in(self):
        self.assert_lex_produces('in', [self.make_tok('IN', 'in', 1, 0)])

    def test_for(self):
        self.assert_lex_produces('for', [self.make_tok('FOR', 'for', 1, 0)])

    def test_per_slash(self):
        self.assert_lex_produces('/', [self.make_tok('PER', '/', 1, 0)])

    def test_per_literal(self):
        self.assert_lex_produces('per', [self.make_tok('PER', 'per', 1, 0)])

    def test_information_unit(self):
        self.assert_lex_produces(
            'GiB', [self.make_tok('INFORMATION_UNIT', 'GiB', 1, 0)])

    def test_duration_unit(self):
        self.assert_lex_produces(
            'd', [self.make_tok('DURATION_UNIT', 'd', 1, 0)])

    def test_number_integral(self):
        self.assert_lex_produces(
            '9', [self.make_tok('NUMBER', 9.0, 1, 0)])

    def test_number_fractional(self):
        self.assert_lex_produces(
            '2.33', [self.make_tok('NUMBER', 2.33, 1, 0)])

    def test_whitespace(self):
        self.assert_lex_produces(
            '2.55          MiB/     y',
            [
                self.make_tok('NUMBER', 2.55, 1, 0),
                self.make_tok('INFORMATION_UNIT', 'MiB', 1, 14),
                self.make_tok('PER', '/', 1, 17),
                self.make_tok('DURATION_UNIT', 'y', 1, 23)
            ])
