# -*- coding: utf-8 -*-

import os

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # 获取环境变量作为密钥
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'manage_sysDB.db')
WTF_CSRF_SECRET_KEY = 'sadfasoiuf7892534jfg934750189234jrf9234857'
