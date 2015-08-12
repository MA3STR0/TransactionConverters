Transaction Converters
======================

This software helps to parse transaction data of popular banks and save in
format user likes. Currently implemented for Sparkasse and Number26,
supported output format is YNAB csv.


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
