# coding=utf-8

'''
纾侀樀锛?0.43.203.28   10.43.203.26   10.43.203.29
褰曞叆鐩稿叧淇℃伅锛屽苟鏍规嵁褰曞叆鐨刬p锛岃幏寰椾竴浜涗俊鎭?
'''

import re
import psutil
import os
import sqlite3
import string 
import time

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
    c.execute("select IP from switchs;")
    getIP = []
    rows = c.fetchall()
    for s in rows:
        getIP.append(s[0])
    #print(getIP)
    conn.close()
    return getIP

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
    result = os.popen('snmpwalk -v 2c -c public ' + host + ' '+ oid).read()
    return result


# ------------------------------------------------------------
# get sysname of the host
# ------------------------------------------------------------
def getSysname(host):
    Sysname = snmpWalk(host, '1.3.6.1.2.1.1.5.0').split(' STRING:')[1]
    return Sysname

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
            return unicode( hour+"小时 "+minute+"分钟 "+second+"秒", 'gbk')
    return ''

# ------------------------------------------------------------
# get sysstatus of the host
# ------------------------------------------------------------
def getsysStatus(host):
    sysUpTime=getsysUpTime(host)
    if(sysUpTime):
        status = 'ON'
    else:
        status = 'OFF'
    return status  




# ------------------------------------------------------------
# get ifnumber of the host网络接口的数目
# ------------------------------------------------------------
def getifNumber(host):
    ifNumber = snmpWalk(host, '1.3.6.1.2.1.2.1.0').split('INTEGER: ')[1]
    return ifNumber  


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

def insert_Info_to_DB_Ato(ip, status, uptime,ifnumber):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    print "Opened database successfully"
    c.execute("update switchs set STATUS = '%s', UPTIME = '%s', IFNUMBER = '%s'where IP = '%s';" % (status, uptime, ifnumber, ip))
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
    cursor = c.execute("SELECT *  from switchs;")
    for row in cursor:
        print('=' * 10 + '=' * 10)
        print "MODEL = ", row[1],"\n"
        print "AssetNum = ", row[2],"\n"
        print "POSITION = ", row[3],"\n"
        print "IP = ", row[4],"\n"
        print "OWNER = ", row[5], "\n"
        print "STATUS = ", row[6],"\n"
        print "UPTIME = ", row[7],"\n"
        print "IFNUMBER = ", row[8], "\n"
    print "Operation done successfully"
    conn.commit()
    conn.close()



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
        #try:
        sysname = getSysname(host)
        print(sysname)
        sysUpTime = getsysUpTime(host)
        print(sysUpTime)
        ifNumber=getifNumber(host)
        print(ifNumber)
        sysStatus=getsysStatus(host)
        print(sysStatus)
            #print('begin')
        insert_Info_to_DB_Ato(host, sysStatus, sysUpTime,ifNumber)
            #print("goodbye")
        #except :
        #    continue 
    review_Information_of_DB()

if __name__ == '__main__':
    main()
