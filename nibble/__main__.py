#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import argparse
import logging

import nibble
from nibble import util, LexingError, Parser, ParsingError

logger = logging.getLogger(__name__)


def _parse_args(args):
    """
    Interpret command line arguments.

    :param args: `sys.argv`
    :return: The populated argparse namespace.
    """

    parser = argparse.ArgumentParser(prog='nibble',
                                     description='Speed, distance and time '
                                                 'calculations around '
                                                 'quantities of digital '
                                                 'information.')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + nibble.__version__)
    parser.add_argument('-v', '--verbosity',
                        help='increase output verbosity',
                        action='count',
                        default=0)
    parser.add_argument('expression',
                        type=util.decode_cli_arg,
                        nargs='+',
                        help='the calculation to execute')
    return parser.parse_args(args[1:])


def main(args):
    """
    Nibble's entry point.

    :param args: Command-line arguments, with the program in position 0.
    """

    args = _parse_args(args)

    # sort out logging output and level
    level = util.log_level_from_vebosity(args.verbosity)
    root = logging.getLogger()
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    root.addHandler(handler)

    logger.debug(args)

    expression = ' '.join(args.expression)
    try:
        print(Parser().parse(expression))
    except (LexingError, ParsingError) as e:
        util.print_error(e)
        return 1

    return 0


def main_cli():
    """
    Nibble's command-line entry point.

    :return: The return code of the program.
    """
    status = main(sys.argv)
    logger.debug('Returning exit status %d', status)
    return status


if __name__ == '__main__':
    sys.exit(main_cli())
