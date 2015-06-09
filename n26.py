#!/usr/bin/env python3
# coding: utf-8

"""
Run with
./n26.py ynab-out-file.csv
"""

import sys
import logging


logger = logging.getLogger(__name__)


class Number26(object):
    def read(self):
        data = []
        return data


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        logger.error("Wrong parameters provided. Run with:"
                     "./n26 ynab-out-file.csv")
        sys.exit(1)
    ynab_file = sys.argv[1]
    parser = Number26()
    input_data = parser.read()
    ynab_data = []
    for row in input_data:
        ynab_data.append(parser.convert_line(row))
    parser.write_ynab(ynab_file, ynab_data)
