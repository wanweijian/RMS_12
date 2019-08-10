# -*- coding: utf-8 -*-

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


from flask import Blueprint
 
main = Blueprint('main', __name__)
 
from . import views, errors 

#由于路由和错误处理页面定义在这个文件里面，导入到蓝本把他们关联起来，又因为views.py，error.py需要导入蓝本main，防止循环导入所以放到最后


