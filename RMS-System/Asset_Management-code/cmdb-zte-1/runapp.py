# -*- coding: utf-8 -*-
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

from app import app

import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger('cmdb-zte-1')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log/log.txt')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
rh = RotatingFileHandler("log/log.txt", maxBytes=10*1024*1024, backupCount=3)
rh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)-15s  %(name)s  %(levelname)s  %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
rh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(rh)


if __name__ == '__main__':
    app.run(port=8800, debug=False)
