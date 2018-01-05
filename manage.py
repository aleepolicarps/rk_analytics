from flask import Flask
import analytics
import argparse
import logging
import sys

def __runserver():
    analytics.app.run(debug=True)

parser = argparse.ArgumentParser(description='Application commands.')
parser.add_argument('command', default=None)

if __name__ == '__main__':
    args = parser.parse_args()
    command = args.command

    if command == 'runserver':
        __runserver()
