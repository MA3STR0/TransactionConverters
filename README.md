Transaction Converters
======================

This software helps to parse transaction data of popular banks and save in
format user likes. Currently implemented for Sparkasse and Number26,
supported output format is YNAB csv.

In other words, at this point it helps to export your Sparkasse/Number26
transactions and import them into YNAB. It also gives you easy hooks to
extend this functinality.


Installation
------------

* You need Python 3 and pip
* Clone this repository
* Install dependencies: `pip3 install -r requirements.txt`
* create config files if necessary


Running
-------

* Sparkasse
    1. Download a csv transaction dump from online-banking
    2. Run ./sparkasse.py

* Number 26
    1. Create and fill 'n26_config.yml'
    2. Run ./number26.py


Payee Mapping
-------------
Main files responsible for transaction payee mapping are `public_payees.yml`
and `private_payees.yml`. Feel free to extend both files, and share you changes
to `public_payees.yml` using pull requests.


Extending
---------
Adding your own bank backends is easy, since most of banks have transaction
csv export. Inherit from Converter and implement methods responsible for
field mapping. Sparkasse class is a good exmaple and starting point.
