# Password Manager
Password manager created using Python

## Requirements

* Passlib: pip install passlib
* Validators: pip install validators

## Versions

There are 2 versions:

* cli.py is the command line version (deprecated)

* gui.py is the graphical version created using TkInter (up to date)

## What I learnt

* Working with offline databases in python

* Creating a GUI using the TkInter module

* Formatting and displaying a table

* Using the csv module to work with csv files

* Storing and verifying hashed passwords


## Run

1. Create a environment variable _PM_PASSWORD_ that stores hashed master password:

  * Run hash.py file

  * Use function hashPassword(_password_) to generate sha256 hash

  * Use function storeHash(_hash_) to store hash in _PM_PASSWORD_

  * Verify using verifyPassword(_password_)

2. Run gui.py
