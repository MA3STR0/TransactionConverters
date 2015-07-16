#!/usr/bin/env python3
# coding: utf-8

"""
Run with
./n26.py ynab-out-file.csv
"""

import sys
import json
import csv
import yaml
import logging
import requests
import time
from decimal import Decimal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Converter(object):
    """
    Base class for bank transactions processing
    """
    def __init__(self, config):
        with open('public_payees.yml', 'r') as yfile:
            self.payees = yaml.load(yfile)
        with open('private_payees.yml', 'r') as yfile:
            self.payees.update(yaml.load(yfile))


class Number26(Converter):
    """
    Implementation for Number25 bank
    """
    def __init__(self, *args, **kwargs):
        super(Number26, self).__init__(*args, **kwargs)
        with open('n26_config.yml', 'r') as yfile:
            config = yaml.load(yfile)
        self.credentials = {
            'username': config['email'],
            'password': config['password'],
            'grant_type': 'password'
        }
        del config

    def find_payee(self, *sources):
        # first check startswith
        for match, payee in self.payees.items():
            if [source for source in sources
                    if source.lower().startswith(match.lower())]:
                return payee
        # then check contains
        for match, payee in self.payees.items():
            if [source for source in sources
                    if match.lower() in source.lower()]:
                return payee

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
        logger.info('bank token aquired')

        resp = json.loads(page.text)
        session.headers.update({
            'Authorization': 'bearer %s' % resp['access_token']
        })
        del session.headers['content-type']
        page = session.get('https://api.tech26.de/api/smrt/transactions',
                           params={'limit': 50})
        if page.status_code != 200:
            raise Exception("Could not load transactions: %s" % page.text)
        logger.info('transactions loaded')
        resp = json.loads(page.text)
        return resp

    def convert_row(self, row):
        _timestamp = row['visibleTS'] / 1000
        _raw_payee = row.get('merchantName') or row.get('partnerName', '')
        _comment = row.get('referenceText', '')
        _raw_amount = row['amount']
        _category = row.get('category', '').replace('micro-', '')
        _city = row.get('merchantCity', '')
        date = time.strftime('%m/%d/%y', time.gmtime(_timestamp))
        payee = self.find_payee(_raw_payee, _comment, _category)
        amount = Decimal(str(_raw_amount))
        memo = "%s %s %s" % (_raw_payee, _comment, _city)
        category = ""   # let client software determine category based on payee
        ynab = {
            'Date': date,
            'Payee': payee,
            'Memo': memo,
            'Outflow': -amount if amount < 0 else '',
            'Inflow': amount if amount > 0 else '',
            'Category': category,
        }
        return ynab

    def write(self, filename, data):
        with open(filename, 'w') as csvfile:
            fieldnames = ['Date', 'Payee', 'Category', 'Memo', 'Outflow',
                          'Inflow']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        logger.error("Wrong parameters provided. Run with:"
                     "./n26")
        sys.exit(1)
    ynab_file = "ynab_data_n26.csv"
    parser = Number26(config="n26_config.yml")
    input_data = parser.read()
    ynab_data = []
    for row in input_data:
        ynab_data.append(parser.convert_row(row))
    parser.write(ynab_file, ynab_data)
