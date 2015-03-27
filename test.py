#!/usr/bin/env python

import nose
import os

from model import database

os.environ['APP_ENVIRONMENT'] = 'testing'
args = ['tests', '--with-spec', '--spec-color', '--nologcapture']

database.connect()

nose.run(argv=args)
