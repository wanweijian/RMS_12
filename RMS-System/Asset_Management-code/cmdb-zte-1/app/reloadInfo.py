# -*- coding: UTF-8 -*-

import threading
import time
import os

def DeltaSeconds():
    SECONDS_PER_DAY = 24 * 60 * 60
    from datetime import datetime, timedelta
    curTime = datetime.now()
    desTime = curTime.replace(hour=14, minute=0, second=0, microsecond=0)  #这里添加时间
    delta = desTime - curTime
    skipSeconds = delta.total_seconds() % SECONDS_PER_DAY
    print "Must sleep %d seconds" % skipSeconds
    return skipSeconds

def excuteScript():
    os.system('python get_ServerIp_Info.py')
    os.system('python get_StorageIp_Info.py')
    os.system('python get_SwitchIP_Info.py')



class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name


    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        reloadInfo()


def reloadInfo():
    while 1:
        s = DeltaSeconds()
        time.sleep(s)
        print "work it!"  # 这里可以替换成作�?
        excuteScript()

def main():
    # 创建新线�?
    thread = myThread(1, "Thread-reloadInfomation")

    # 开启线�?
    thread.start()


if __name__ == '__main__':
    main()