#!/usr/bin/env python3
# coding: utf-8

"""
Run with
./sparkasse.py
"""

import io
import csv
import sys
import logging
import time
from decimal import Decimal

from converter import Converter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sparkasse(Converter):
    """
    Implementation for Sparkasse bank
    """
    def __init__(self, *args, **kwargs):
        super(Sparkasse, self).__init__(*args, **kwargs)

    def load_transactions(self, filename):
        data = []
        with io.open(filename, 'r', encoding='cp1252') as csvfile:
            rd = csv.DictReader(csvfile, delimiter=';')
            for row in rd:
                data.append(row)
        return data

if __name__ == '__main__':
    ynab_file = "ynab_data_sparkasse.csv"
    spk_file = sys.argv[1]
    converter = Sparkasse()
    input_data = converter.load_transactions(spk_file)
    ynab_data = []
    for row in input_data:
        ynab_data.append(converter.convert_row(row))
    converter.export_file(ynab_file, ynab_data)
