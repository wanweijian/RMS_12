# -*- coding: utf-8 -*-

from flask import Flask
import config
import os

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = os.urandom(24)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)



import logging

app_logger = logging.getLogger('cmdb-zte-1.app')

