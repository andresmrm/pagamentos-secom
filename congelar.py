#!/usr/bin/env python3
# coding: utf-8

from flask_frozen import Freezer
from main import app

app.config['FREEZER_DESTINATION'] = 'docs'

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
