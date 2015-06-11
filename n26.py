#!/usr/bin/env python3
# coding: utf-8

"""
Run with
./n26.py ynab-out-file.csv
"""

import sys
import json
import yaml
import logging
import requests


logger = logging.getLogger(__name__)


class Number26(object):

    def __init__(self, config):
        with open('n26_config.yml', 'r') as yfile:
            config = yaml.load(yfile)
        self.credentials = {
            'username': config['email'],
            'password': config['password'],
            'grant_type': 'password'
        }
        del config

    def read(self):
        return []


    def write(self, filename, data):
        pass


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
    parser.write(ynab_file, ynab_data)
