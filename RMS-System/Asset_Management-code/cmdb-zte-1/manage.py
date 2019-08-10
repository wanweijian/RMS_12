# -*- coding: utf-8 -*-

from app import app
from app.models import ServerModel, db
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, Server

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)
server = Server(host="127.0.0.1", port=8800)
manager.add_command("runserver", server)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, servermodel=ServerModel)


if __name__ == '__main__':
    manager.run()
