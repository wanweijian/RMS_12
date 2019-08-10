# coding=utf-8

'''
服务器：10.43.239.246  10.43.239.243   10.43.239.236 命令：snmpwalk -v 2c -c zte_public
录入相关信息，并根据录入的ip，获得MAC地址、系统信息、上电状怿
'''

import re
import psutil
import sqlite3
import os
from ..models import ServerModel, db
import sys


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


def snmpWalk(host, oid):
    result = os.popen('snmpwalk -v 2c -c zte_public ' + host + ' '+ oid).read()
    return result

# ------------------------------------------------------------
# get MAC Address of the host
# ------------------------------------------------------------

def getMAC(host):
    address = snmpWalk(host, '1.3.6.1.4.1.3902.6053.19.1.3.2.39.1.8')
    print('mac')
    return address

# ------------------------------------------------------------
# get System Information of the Host
# ------------------------------------------------------------

def getSysUpTime(host):
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
# insert the captured Information to the DB
# ------------------------------------------------------------


def insert_Info_to_DB_Ato(host, status, mac, uptime, modelserver, positionserver, ownerserver, assertnumserver):
    print('not success')
    servermodel = ServerModel(IP=host, MAC=mac, UPTIME=uptime, STATUS=status, MODEL=modelserver, POSITION=positionserver, OWNER=ownerserver,
                              AssertNum=assertnumserver)
    db.session.add(servermodel)
    db.session.commit()
    print('success')
    return True


def Mac_Filter(mac):
    if mac.find('"') >= 1:
        return mac.split('"')[1] 
    return ''


def get_r5300_info(ip, model, position, owner, assertnum):
    host = ip
    modelserver = model
    positionserver = position
    ownerserver = owner
    assertnumserver = assertnum
    if getMAC(host):
        print('get mac')
        mac = Mac_Filter(getMAC(host))
        print(mac)
        uptime = getSysUpTime(host)
        print('get uptime')
        if mac:
            status = 'ON'
        else:
            status = 'OFF'
        return insert_Info_to_DB_Ato(host, status, mac, uptime, modelserver, positionserver, ownerserver, assertnumserver)
    else:
        return False


def update_server_DB():
    servermodels = ServerModel.query.all()
    for server in servermodels:
        host = server.IP
        if getMAC(host):
            mac = Mac_Filter(getMAC(host))
            uptime = getSysUpTime(host)
            if mac:
                status = 'ON'
            else:
                status = 'OFF'
            server.STATUS = status
            server.MAC = mac
            server.UPTIME = uptime
            db.session.commit()

