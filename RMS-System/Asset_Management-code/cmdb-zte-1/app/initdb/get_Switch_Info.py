# coding=utf-8

'''
10.43.203.28   10.43.203.26   10.43.203.29
'''

import re
import psutil
import os
import sqlite3
import string
import time
from ..models import SwitchModel, db
import sys


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

'''
# ------------------------------------------------------------
# convert second to a ISO format time 
#from: 23123123 to: 2006-04-12 16:46:40    把给定的秒转化为定义的格式   
# ------------------------------------------------------------
def Time2ISOString( s ):    
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( float(s) ) )  


#------------------------------------------------------------
#convert time to static type
#------------------------------------------------------------
def convertTime(sysUpTime):
    seconds=re.findall(r'[(](.*?)[)]', sysUpTime) 
    Second_float=float(seconds[0])
    #Second_float="".join(seconds)
    #Second_float=Time2ISOString(seconds[0])
    return Second_float
'''


def snmpWalk(host, oid):
    result = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read()
    return result


def getMAC(host):
    adress = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.21.1.9')
    print('mac')
    return adress

# ------------------------------------------------------------
# get sysname of the host
# ------------------------------------------------------------
# def getSysname(host):
    # Sysname = snmpWalk(host, '1.3.6.1.2.1.1.5.0').split(' STRING:')[1]
    # return Sysname


# ------------------------------------------------------------
# get sysUpTime of the host
# ------------------------------------------------------------
def getsysUpTime(host):
    sysUpTime = snmpWalk(host, '1.3.6.1.2.1.1.3.0')
    print('uptime')
    if sysUpTime.find(') ') >= 1:
        time = sysUpTime.split(') ')[1]
        if time.find("day"):
            day = time.split(" day")[0]
        else:
            day = ''
        temp = time.split(":")
        hour = temp[0][-1]
        minute = temp[1]
        second = temp[2].split(".")[0]
        if len(day) == 0:
            return unicode( day+"天 "+hour+"小时 "+minute+"分钟 "+second+"秒", 'utf-8')
        else:
            return unicode(hour+"小时 "+minute+"分钟 "+second+"秒", 'utf-8')
    return ''


# ------------------------------------------------------------
# get sysstatus of the host
# ------------------------------------------------------------
def getsysStatus(host):
    mac = getMAC(host)
    print('status')
    if (mac):
        status = 'ON'
    else:
        status = 'OFF'
    return status


# ------------------------------------------------------------
# get ifnumber of the host网络接口的数目
# ------------------------------------------------------------
def getifNumber(host):
    ifNumber = snmpWalk(host, '1.3.6.1.2.1.2.1.0')
    print('ifnumber')
    if ifNumber.find('INTEGER: ') >= 1:
        return ifNumber.split('INTEGER: ')[1] 
    return ''


# def getSerialnum(host):
    # serialnum = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.1.5').split('"')[1]
    # return serialnum

'''
# ------------------------------------------------------------
# get serialnum of the host
# ------------------------------------------------------------
def getSerialnum(host):
    serialnum = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.1.5').split('"')[1]
    return serialnum

# ------------------------------------------------------------
# get systemstate of the host
# ------------------------------------------------------------
def getSystemstate(host):
    systemstate = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.1.6').split('"')[1]
    return systemstate

# ------------------------------------------------------------
# get deviceid of the host
# ------------------------------------------------------------
def getDeviceid(host):
    deviceid = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.2.1.4')
    return deviceid


# ------------------------------------------------------------
# get totalcapacity of the host
# ------------------------------------------------------------ 
def getTotalcapacity(host):
    totalcapacity = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.3.12').split('Counter64: ')[1]
    return totalcapacity


# ------------------------------------------------------------
# get usedcapacity of the host
# ------------------------------------------------------------ 
def getUsedcapacity(host):
    usedcapacity = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.3.13').split('Counter64: ')[1]
    return usedcapacity

# ------------------------------------------------------------
# get MAC Address of the host
# ------------------------------------------------------------
def getMAC(host):
    adress = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.21.1.9')
    return adress


# ------------------------------------------------------------
# get System Information of the Host
# ------------------------------------------------------------
def getSystem(host):
    system = snmpWalk(host, 'system')
    return system
'''


# ------------------------------------------------------------
# insert the captured Information to the DB
# ------------------------------------------------------------

def insert_Info_to_DB_Ato(host, sysStatus, sysUpTime, ifNumber, modelswitch, ownerswitch, positionswitch, assertnumswitch):
    print('not success')
    switchmodel = SwitchModel(IP=host, UPTIME=sysUpTime, IFNUMBER=ifNumber, STATUS=sysStatus, MODEL=modelswitch, POSITION=positionswitch, OWNER=ownerswitch,
                              AssertNum=assertnumswitch)
    print('success')
    db.session.add(switchmodel)
    db.session.commit()
    print('success11')
    return True


# ------------------------------------------------------------
# the main programe of the function
# ------------------------------------------------------------


def get_switch_info(ip, position, owner, model, assertnum):
    # insert_Info_to_DB( '2', 'C', '5FLOOR', '5-17', '10.43.203.28', 'KebinLi10257780')
    # insert_Info_to_DB( '2', 'C', '5FLOOR', '5-17', '10.43.203.205', 'WeiKong10034463')
    # insert_Info_to_DB( '2', 'C', '5FLOOR', '5-19', '10.43.203.29', 'WeijianWan10257705')
    host = ip
    modelswitch = model
    ownerswitch = owner
    positionswitch = position
    assertnumswitch = assertnum
    if getMAC(host):
        print('mac')
        sysUpTime = getsysUpTime(host)
        print('sysUpTime')
        ifNumber = getifNumber(host)
        print('ifNumber: ')
        sysStatus = getsysStatus(host)
        print('sysStatus')
        # seconds=convertTime(sysUpTime)
        # day_hour_mim_sed=Time2ISOString(seconds)
        return insert_Info_to_DB_Ato(host, sysStatus, sysUpTime, ifNumber, modelswitch, ownerswitch, positionswitch, assertnumswitch)
    else:
        return False


def update_switch_DB():
    switchmodels = SwitchModel.query.all()
    for switch in switchmodels:
        host = switch.IP
        if getMAC(host):
            sysUpTime = getsysUpTime(host)
            ifNumber = getifNumber(host)
            sysStatus = getsysStatus(host)
            switch.STATUS = sysStatus
            switch.IFNUMBER = ifNumber
            switch.UPTIME = sysUpTime
            db.session.commit()
