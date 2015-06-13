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
        session = requests.Session()
        session.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.8',
            'accept-encoding': 'gzip, deflate',
            'content-type': 'application/x-www-form-urlencoded',
            'Origin': 'https://my.number26.de',
            'Referer': 'https://my.number26.de/',
            'Authorization': 'Basic bXktdHJ1c3RlZC13ZHBDbGllbnQ6c2VjcmV0',
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/47.0.2526.111 Safari/537.36')
        })
        page = session.post("https://api.tech26.de/oauth/token",
                            data=self.credentials)
        del self.credentials
        if page.status_code != 200:
            raise Exception("Wrong email/password")
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
