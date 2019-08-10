# coding=utf-8

'''
磁阵�?0.43.203.28   10.43.203.26   10.43.203.29
录入相关信息，并根据录入的ip，获得一些信�?
'''

import re
import psutil
import os
import sqlite3
import string 

'''
# ------------------------------------------------------------
# simulation of  log in DB
# ------------------------------------------------------------
def insert_Info_to_DB(parea, pbuilding, pfloor, proom, ip, owner):
    conn = sqlite3.connect('manage_sysDB.db')
    c = conn.cursor()
    print "Opened database successfully"
    c.execute( "insert into KS3200_information( PArea, PBuilding, PFloor, PRoom, IP, OWNER) values('%s','%s','%s','%s','%s','%s');"% (parea, pbuilding, pfloor, proom, ip, owner,))
    print "Operation done successfully"
    conn.commit()
    conn.close()
'''

# ------------------------------------------------------------
# get ip from DB
# ------------------------------------------------------------
def get_IP_from_DB():
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("select IP from raids;")
    getIP = []
    rows = c.fetchall()
    for s in rows:
        getIP.append(s[0])
    #print(getIP)
    conn.close()
    return getIP


def snmpWalk(host, oid):
    result = os.popen('snmpwalk -v 2c -c platform ' + host + ' '+ oid).read()
    return result


# ------------------------------------------------------------
# get sysname of the host
# ------------------------------------------------------------
def getSysname(host):
    Sysname = snmpWalk(host, '1.3.6.1.4.1.3902.6050.19.1.20.1.1').split(' STRING:')[1]
    return Sysname

# ------------------------------------------------------------
# get sysUpTime of the host
# ------------------------------------------------------------
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
    if(systemstate):
        status = 'ON'
    else:
        status = 'OFF'
    return status 

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

# ------------------------------------------------------------
# insert the captured Information to the DB
# ------------------------------------------------------------

def insert_Info_to_DB_Ato(status, uptime,usedpercent,ip):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    print "Opened database successfully"
    c.execute("update raids set STATUS = '%s', UPTIME = '%s', USEDPERCENT = '%s'where IP = '%s';" % (status, uptime,usedpercent, ip))
    print "Operation done successfully"
    conn.commit()
    conn.close()
    return

# ------------------------------------------------------------
# review the Information of the DB
# ------------------------------------------------------------

def review_Information_of_DB():
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    print("cat db information")
    cursor = c.execute("SELECT *  from raids;")
    for row in cursor:
        #print('=' * 10 + '=' * 10)
        print "MODEL = ", row[1],"\n"
        print "AssetNum = ", row[2],"\n"
        print "POSITION = ", row[3],"\n"
        print "IP = ", row[4],"\n"
        print "OWNER = ", row[5], "\n"
        print "STATUS = ", row[6],"\n"
        print "UPTIME = ", row[7],"\n"
        print "USEDPERCENT = ", row[8], "\n"
    print "Operation done successfully"
    conn.commit()
    conn.close()


# ---------------------------------------------------------------
# filter the userful information of the captured MAC information
# ---------------------------------------------------------------


def Mac_Filter(mac):
    macList = mac.split('"')
    return macList[1]+'\n'+macList[4]

# ------------------------------------------------------------
# the main programe of the function
# ------------------------------------------------------------


def main():
    #insert_Info_to_DB( '2', 'C', '5FLOOR', '5-17', '10.43.203.28', 'KebinLi10257780')
    #insert_Info_to_DB( '2', 'C', '5FLOOR', '5-17', '10.43.203.205', 'WeiKong10034463')
    #insert_Info_to_DB( '2', 'C', '5FLOOR', '5-19', '10.43.203.29', 'WeijianWan10257705')
    hosts = get_IP_from_DB()
    print(hosts)
    for host in hosts:
        print('=' * 10 + host + '=' * 10)
        try:  
            #sysname = getSysname(host)
            #print(sysname)
            sysUpTime = getsysUpTime(host)
            #print(sysUpTime)
            #serialnum = getSerialnum(host)
            systemstate = getSystemstate(host)
            totalcapacity = getTotalcapacity(host)
            usedcapacity = getUsedcapacity(host)
            usedpercentcapacity = round(string.atof(usedcapacity)/string.atof(totalcapacity),3)
            insert_Info_to_DB_Ato(systemstate, sysUpTime, usedpercentcapacity, host)

        except :
            continue 
            
    review_Information_of_DB()

if __name__ == '__main__':
    main()
