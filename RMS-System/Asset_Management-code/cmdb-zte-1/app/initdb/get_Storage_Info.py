# coding=utf-8

'''
磁阵�?.43.203.28   10.43.203.26   10.43.203.29
录入相关信息，并根据录入的ip，获得一些信�?
'''

import re
import psutil
import os
import sqlite3
import string

from ..models import RaidModel, db
import sys


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


def snmpWalk(host, oid):
    result = os.popen('snmpwalk -v 2c -c platform ' + host + ' '+ oid).read()
    return result

# def getSysname(host):
    # Sysname = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.1.1')
    # if Sysname.find('STRING:') >= 0:
        # return Sysname.split(' STRING:')[1] 
    # print(Sysname)
    # return ''


def getsysUpTime(host):
    sysUpTime = snmpWalk(host, '1.3.6.1.2.1.1.3')
    print('uptime')
    if sysUpTime.find('Timeticks: ') >= 1:
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



# def getSerialnum(host):
    # serialnum = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.1.5')
    # if serialnum.find('"') >= 0:
        # return serialnum.split('"')[1] 
    # print(serialnum)
    # return ''


def getSystemstate(host):
    systemstate = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.1.6')
    print('state')
    if systemstate.find('"') >= 1:
        return systemstate.split('"')[1] 
    return ''


# def getDeviceid(host):
    # deviceid = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.2.1.4')
    # if not deviceid:
        # return ''
    # return deviceid


def getTotalcapacity(host):
    totalcapacity = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.3.12')
    print('totalcapacity')
    if totalcapacity.find('Counter64: ') >= 1:
        return totalcapacity.split('Counter64: ')[1]
    return ''


def getUsedcapacity(host):
    usedcapacity = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.3.13')
    print('usedcapacity')
    if usedcapacity.find('Counter64: ') >= 1:
        return usedcapacity.split('Counter64: ')[1]
    return ''


def getMAC(host):
    adress = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.21.1.9')
    print('mac')
    return adress


# def getSystem(host):
#     system = snmpWalk(host, 'system')
#     if not system:
#         return ''
#     return system


def insert_Info_to_DB_Ato(modelraid, assertnumraid, host, status, uptime, usedpercent, positionraid, ownerraid):
    print('not success')
    raidmodel = RaidModel(IP=host, UPTIME=uptime, USEDPERCENT=usedpercent, STATUS=status, MODEL=modelraid, POSITION=positionraid, OWNER=ownerraid,
                          AssertNum=assertnumraid)
    db.session.add(raidmodel)
    db.session.commit()
    print('success')
    return True


# def Mac_Filter(mac):
#     macList = mac.split('"')
#     return macList[1]+'\n'+macList[4]


def get_ks3200_info(ip, position, owner, model, assertnum):
    host = ip
    positionraid = position
    ownerraid = owner
    modelraid = model
    assertnumraid = assertnum
    if getMAC(host):
        print('get mac')
        uptime = getsysUpTime(host)
        print('get uptime')
        status = getSystemstate(host)
        print('get status')
        status = 'ON'
        totalcapacity = getTotalcapacity(host)
        print('get totalcapacity')
        usedcapacity = getUsedcapacity(host)
        print('get usedcapacity')
        if totalcapacity and usedcapacity:
            usedpercent = round(string.atof(usedcapacity)/string.atof(totalcapacity)*100,2)
        else:
            usedpercent = ''
        return insert_Info_to_DB_Ato(modelraid, assertnumraid, host, status, uptime, usedpercent, positionraid, ownerraid)
    else:
        return False


def update_storage_DB():
    raidmodels = RaidModel.query.all()
    for raid in raidmodels:
        host = raid.IP
        if getMAC(host):
            uptime = getsysUpTime(host)
            status = 'ON'
            totalcapacity = getTotalcapacity(host)
            usedcapacity = getUsedcapacity(host)
            if totalcapacity and usedcapacity:
                usedpercent = round(string.atof(usedcapacity)/string.atof(totalcapacity)*100,2)
            else:
                usedpercent = ''
            raid.STATUS = status
            raid.USEDPERCENT = usedpercent
            raid.UPTIME = uptime
            db.session.commit()
