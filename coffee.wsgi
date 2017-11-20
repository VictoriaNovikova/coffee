#!/usr/bin/python

import sys
sys.path.insert(0,'/home/flaskappuser/flaskapp/coffee/')

from server import app as application
application.secret_key = 'you-will-never-guess_this_key'
