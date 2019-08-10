# coding=utf-8
'''
服务器：10.43.239.246  10.43.239.243   10.43.239.236 命令：snmpwalk -v 2c -c zte_public
录入相关信息，并根据录入的ip，获得MAC地址、系统信息、上电状�?
'''
import re
import psutil
import os
import sqlite3

'''
# ------------------------------------------------------------
# simulation of  log in DB
# ------------------------------------------------------------
def insert_Info_to_DB(model, assetnum, parea, pbuilding, pfloor, proom, ip, owner):
    conn = sqlite3.connect('manage_sysDB.db')
    c = conn.cursor()
    #print "Opened database successfully"
    c.execute("insert into R5300_information(MODEL, AssetNum, PArea, PBuilding, PFloor, PRoom, IP, OWNER) values('%s','%s','%s','%s','%s','%s','%s','%s');"
              % (model, assetnum, parea, pbuilding, pfloor, proom, ip, owner, ))
    #print "Operation done successfully"
    conn.commit()
    conn.close()
'''
# ------------------------------------------------------------
# get ip from DB
# ------------------------------------------------------------
def get_IP_from_DB():
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("select IP from servers;")
    getIP = []
    rows = c.fetchall()
    for s in rows:
        getIP.append(s[0])
    #print(getIP)
    conn.close()
    return getIP

def snmpWalk(host, oid):
    result = os.popen('snmpwalk -v 2c -c zte_public ' + host + ' '+ oid).read()
    return result

# ------------------------------------------------------------
# get MAC Address of the host
# ------------------------------------------------------------

def getMAC(host):
    adress = snmpWalk(host, '1.3.6.1.4.1.3902.6053.19.1.3.2.39.1.8')
    return adress

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


def insert_Info_to_DB_Ato(ip, status, sysUpTime, mac):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    print "Opened database successfully!"
    c.execute("update servers set STATUS = '%s', UPTIME = '%s', MAC = '%s'where IP = '%s';" % (status, sysUpTime, mac,  ip))
    print "Operation done successfully!"
    conn.commit()
    conn.close()

# ------------------------------------------------------------
# review the Information of the DB
# ------------------------------------------------------------


def review_Information_of_DB():
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    print("cat db information")
    cursor = c.execute("SELECT *  from servers;")
    for row in cursor:
        print('=' * 10 + '=' * 10)
        print "MODEL = ", row[1]
        print "AssetNum = ", row[2]
        print "position = ", row[3]
        print "IP = ", row[4]
        print "OWNER = ", row[5]
        print "status = ", row[6]
        print "UPTIME = ", row[7]
        print "MAC = ", row[8], "\n"
    print "Operation done successfully"
    conn.commit()
    conn.close()

# ---------------------------------------------------------------
# filter the userful information of the captured MAC/SYSTEM information
# ---------------------------------------------------------------


def Mac_Filter(mac):
    if mac.find('"') >= 1:
        return mac.split('"')[1] 
    return ''

# ------------------------------------------------------------
# the main programe of the function
# ------------------------------------------------------------


def main():
  
    hosts = get_IP_from_DB()

    for host in hosts:
        print('=' * 10 + host + '=' * 10)
        try:
			mac =  Mac_Filter(getMAC(host))
			#print(mac)
			sysUpTime = getSysUpTime(host)
			#print(sysUpTime)
			if mac:
				status = 'ON'
			else:
				status = 'OFF'
		    #print(status)
			insert_Info_to_DB_Ato(host, status, sysUpTime, mac)
        except :
            continue 
            
    review_Information_of_DB()

if __name__ == '__main__':
    main()
