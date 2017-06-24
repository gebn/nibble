# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import mock
import sys
import os
import contextlib
import six

from nibble import __main__ as main


@contextlib.contextmanager
def _suppress_stderr():
    save_stderr = sys.stderr
    try:
        sys.stderr = open(os.devnull, 'w')
        yield
    finally:
        sys.stderr.close()
        sys.stderr = save_stderr


class CaptureStdOut(list):
    """
    https://stackoverflow.com/a/16571630
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = six.StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class TestParseArgs(unittest.TestCase):

    _CMD = ['nibble']
    _BASE_ARGV = _CMD + ['10Gb']

    def test_version(self):
        with self.assertRaises(SystemExit), _suppress_stderr():
            main._parse_args(['-V'])

    def test_verbosity_implicit(self):
        self.assertEqual(main._parse_args(self._BASE_ARGV).verbosity, 0)

    def test_verbosity_count(self):
        self.assertEqual(main._parse_args(self._BASE_ARGV +
                                          ['-vvvv']).verbosity,
                         4)

    def test_no_expression(self):
        with self.assertRaises(SystemExit), _suppress_stderr():
            main._parse_args(self._CMD)

    def test_expression(self):
        self.assertEqual(main._parse_args(self._BASE_ARGV +
                                          ['in MiB/s']).expression,
                         ['10Gb', 'in MiB/s'])


class TestMain(unittest.TestCase):
    def test_lex_fail(self):
        with CaptureStdOut() as stdout, _suppress_stderr():
            self.assertEqual(main.main('nibble afljslndf'.split(' ')), 1)
        self.assertFalse(stdout)

    def test_parse_fail(self):
        with CaptureStdOut() as stdout, _suppress_stderr():
            self.assertEqual(main.main('nibble 10 10 10'.split(' ')), 1)
        self.assertFalse(stdout)

    def test_information_duration(self):
        with CaptureStdOut() as stdout:
            self.assertEqual(main.main('nibble 400GiB at .87Mb/s'.split(' ')),
                             0)
        self.assertListEqual(stdout, ['1 month 2 weeks 1 day 7 hours 3 minutes '
                                      '15 seconds 214 milliseconds 712 '
                                      'microseconds 644 nanoseconds'])


class TestMainCli(unittest.TestCase):

    def test_status_0(self):
        with mock.patch('sys.argv', ['nibble', '10Gb']):
            self.assertEqual(main.main_cli(), 0)

    def test_status_1(self):
        with mock.patch('sys.argv', ['nibble', 'fsdfasdf']), _suppress_stderr():
            self.assertEqual(main.main_cli(), 1)
