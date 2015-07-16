#!/usr/bin/env python3
# coding: utf-8

import csv
import yaml


class Converter(object):
    """
    Base class for bank transactions processing
    """
    def __init__(self):
        with open('public_payees.yml', 'r') as yfile:
            self.payees = yaml.load(yfile)
        with open('private_payees.yml', 'r') as yfile:
            self.payees.update(yaml.load(yfile))

    def find_payee(self, *sources):
        """exctract matching payee name from lise of sources"""
        for match, payee in self.payees.items():
            # first check startswith
            if [source for source in sources
                    if source.lower().startswith(match.lower())]:
                return payee
        for match, payee in self.payees.items():
            # then check contains
            if [source for source in sources
                    if match.lower() in source.lower()]:
                return payee

    def export_file(self, filename, data):
        with open(filename, 'w') as csvfile:
            fieldnames = ['Date', 'Payee', 'Category', 'Memo', 'Outflow',
                          'Inflow']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
