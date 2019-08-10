# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from app import app
import os

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'asdfhks38240134iowflkeshf02'


class ServerModel(db.Model):
    __tablename__ = 'servers'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MODEL = db.Column(db.String(128))
    AssertNum = db.Column(db.String(128), nullable=True)
    POSITION = db.Column(db.String(128))
    MAC = db.Column(db.String(128), nullable=True)
    IP = db.Column(db.String(128), unique=True)
    OWNER = db.Column(db.String(128))
    STATUS = db.Column(db.String(128), nullable=True, default='OFF')
    UPTIME = db.Column(db.String(128), nullable=True)


class RaidModel(db.Model):
    __tablename__ = 'raids'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MODEL = db.Column(db.String(128))
    AssertNum = db.Column(db.String(128), nullable=True)
    POSITION = db.Column(db.String(128))
    IP = db.Column(db.String(128), unique=True)
    OWNER = db.Column(db.String(128))
    STATUS = db.Column(db.String(128), nullable=True, default='OFF')
    UPTIME = db.Column(db.String(128), nullable=True)
    USEDPERCENT = db.Column(db.String(128), nullable=True)


class SwitchModel(db.Model):
    __tablename__ = 'switchs'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MODEL = db.Column(db.String(128))
    AssertNum = db.Column(db.String(128), nullable=True)
    POSITION = db.Column(db.String(128))
    IP = db.Column(db.String(128), unique=True)
    OWNER = db.Column(db.String(128))
    STATUS = db.Column(db.String(128), nullable=True, default='OFF')
    UPTIME = db.Column(db.String(128), nullable=True)
    IFNUMBER = db.Column(db.String(256), nullable=True)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.add(ServerModel(AssertNum='', MAC='', UPTIME='', MODEL='R5300', IP='10.43.166.141',
                               POSITION=u'一区二期-D区-6楼-666', OWNER=u'陈继猛'))
    db.session.add(RaidModel(AssertNum='', UPTIME='', USEDPERCENT='', MODEL='KS3200', IP='10.43.166.141',
                             POSITION=u'一区二期-D区-6楼-666', OWNER=u'陈继猛'))
    db.session.add(SwitchModel(AssertNum='', UPTIME='', IFNUMBER='', MODEL='Switch', IP='10.43.166.141',
                               POSITION=u'一区二期-D区-6楼-666', OWNER=u'陈继猛'))
    db.session.commit()
