# aBot
keychain bot

# ALPHA
This is currently an alpha.
delete and full password history list not coded in app.

This is a bot that will store password records, but store the password encrypted.

Use at your own risk!!!


# Installation
pip install -r requirements.txt


# Usage
- change the AppKey in config.ini
- currently configured to put the sqlite db in memory. change to the desired filename
- run
 - python app.py
 - (bot) set_password
 - #enter password, this will be used to encrypt account password in the database

Important!!!
You must backup the app_key and password.


# Features
- If app_key and password do not much, randomized password will be output. provides security abstraction.
- Timed display of password
- Keystoke to send username and password
- Timed password to clipboard

