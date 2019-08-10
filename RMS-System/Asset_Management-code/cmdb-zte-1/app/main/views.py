# -*- coding: utf-8 -*-

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


from flask import request, flash, render_template, redirect, url_for
from . import main
from .forms import ServerForm, RaidForm, SwitchForm
from ..models import ServerModel, RaidModel, SwitchModel, db
from ..initdb import get_ks3200_info, get_r5300_info, get_switch_info, update_server_DB, update_switch_DB, update_storage_DB
import regex as re
import xlwt
import xlrd
from flask import send_file, send_from_directory

import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import logging

main_logger = logging.getLogger('cmdb-zte-1.app.main')

@main.route('/', methods=['GET'])
def root():
    return redirect(url_for('main.index'))


@main.route('/index', methods=['GET'])
def index():
    server_on = ServerModel.query.filter(ServerModel.STATUS.endswith('ON')).all()
    server_on_count = len(server_on)
    server_all = ServerModel.query.all()
    server_all_count = len(server_all)
    switch_on = SwitchModel.query.filter(SwitchModel.STATUS.endswith('ON')).all()
    switch_on_count = len(switch_on)
    switch_all = SwitchModel.query.all()
    switch_all_count = len(switch_all)
    raid_on = RaidModel.query.filter(RaidModel.STATUS.endswith('ON')).all()
    raid_on_count = len(raid_on)
    raid_all = RaidModel.query.all()
    raid_all_count = len(raid_all)
    t1 = 0
    for server in server_on:
        t = server.UPTIME.split(' ')
        if len(t) > 1:
            if len(t) > 6:
                t_1 = t[0].split('天')
                t_2 = t[1].split('小时')
                t_3 = t[2].split('分钟')
                t1 = int(t_1[0])*24 + int(t_2[0]) + int(t_3[0]) % 60 + t1
            else:
                t_1 = t[0].split('小时')
                t_2 = t[1].split('分钟')
                t1 = int(t_1[0]) + int(t_2[0]) % 60 + t1
    t2 = 0
    for switch in switch_on:
        t = switch.UPTIME.split(' ')
        if len(t) > 1:
            if len(t) > 6:
                t_1 = t[0].split('天')
                t_2 = t[1].split('小时')
                t_3 = t[2].split('分钟')
                t2 = int(t_1[0]) * 24 + int(t_2[0]) + int(t_3[0]) % 60 + t2
            else:
                t_1 = t[0].split('小时')
                t_2 = t[1].split('分钟')
                t2 = int(t_1[0]) + int(t_2[0]) % 60 + t2
    t3 = 0
    raid_used = 0
    for raid in raid_on:
        t = raid.UPTIME.split(' ')
        if len(t) > 1:
            if len(t) > 6:
                t_1 = t[0].split('天')
                t_2 = t[1].split('小时')
                t_3 = t[2].split('分钟')
                t3 = int(t_1[0]) * 24 + int(t_2[0]) + int(t_3[0]) % 60 + t3
            else:
                t_1 = t[0].split('小时')
                t_2 = t[1].split('分钟')
                t3 = int(t_1[0]) + int(t_2[0]) % 60 + t3
        raid_used = float(raid.USEDPERCENT) + raid_used
    raid_used = raid_used*100/raid_on_count
    raid_used = round(raid_used, 2)
    return render_template('index.html', server_on_count=server_on_count, server_all_count=server_all_count,
                           switch_on_count=switch_on_count,switch_all_count=switch_all_count,
                           raid_on_count=raid_on_count, raid_all_count=raid_all_count, raid_used=raid_used,
                           server_time=t1, switch_time=t2, raid_time=t3)


@main.route('/manage', methods=['GET'])
def manage():
    return render_template('manage.html')


@main.route('/raid', methods=['GET', 'POST'])
def raid():
    raidmodels = RaidModel.query.all()
    return render_template('raid.html', raidmodels=raidmodels)


@main.route('/switch', methods=['GET', 'POST'])
def switch():
    switchmodels = SwitchModel.query.all()
    return render_template('switch.html', switchmodels=switchmodels)


@main.route('/server', methods=['GET', 'POST'])
def server():
    servermodels = ServerModel.query.all()
    return render_template('server.html', servermodels=servermodels)


@main.route('/server/add', methods=['GET', 'POST'])
def addServer():
    serverform = ServerForm()
    print('submit:')
    print(serverform.validate_on_submit())
    print(serverform)
    if serverform.validate_on_submit():
        if not re.match('[0-9]{2,3}', serverform.position4.data):
            main_logger.warning('%s 添加服务器失败:房间号格式不正确 %s', 'manager', serverform.ip.data)
        else:
            if ServerModel.query.filter_by(IP=serverform.ip.data).first():
                main_logger.warning('%s 添加服务器失败:IP地址冲突 %s', 'manager', serverform.ip.data)
            else:
                if serverform.assertnum.data and ServerModel.query.filter_by(AssertNum=serverform.assertnum.data).first():
                    main_logger.warning('%s 添加服务器失败:资产编号冲突 %s', 'manager', serverform.ip.data)
                else:
                    position = serverform.position1.data + '-' + serverform.position2.data + '-' + \
                               serverform.position3.data + '-' + serverform.position4.data
                    a = get_r5300_info(serverform.ip.data, serverform.model.data,
                                position, serverform.owner.data, serverform.assertnum.data)
                    if not a:
                        servermodel = ServerModel(MODEL=serverform.model.data,  POSITION=position,
                                                  OWNER=serverform.owner.data, AssertNum=serverform.assertnum.data,
                                                  IP=serverform.ip.data, MAC='', STATUS='OFF', UPTIME='')
                        db.session.add(servermodel)
                        db.session.commit()
                    main_logger.info('%s 添加服务器成功: %s', 'manager', serverform.ip.data)
                    servermodels = ServerModel.query.all()
                    return redirect(url_for('main.server', servermodels=servermodels))
    return render_template('addserver.html', form=serverform)


@main.route('/server/modify', methods=['GET', 'POST'])
def modifyServer():
    serverid = request.args.get('id', '')
    servermodel = ServerModel.query.filter_by(ID=serverid).first()
    serverposition = servermodel.POSITION.split('-')
    serverform = ServerForm(model=servermodel.MODEL, ip=servermodel.IP,
            mac=servermodel.MAC, owner=servermodel.OWNER,
            status=servermodel.STATUS, uptime=servermodel.UPTIME,
            assertnum=servermodel.AssertNum, position1=serverposition[0],
            position2=serverposition[1], position3=serverposition[2], position4=serverposition[3])
    if serverform.validate_on_submit():
        flash('已提交')
        if not re.match('[0-9]{2,3}', serverform.position4.data):
            flash('房间号格式不正确')
        else:
            # if not re.match('([A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2}', serverform.mac.data):
            #     flash('MAC地址格式不正确')
            # else:
                if serverform.ip.data != servermodel.IP and ServerModel.query.filter_by(IP=serverform.ip.data).first():
                    flash('IP地址冲突')
                else:
                    if serverform.mac.data != servermodel.MAC and ServerModel.query.filter_by(MAC=serverform.mac.data).first():
                        flash('MAC地址冲突')
                    else:
                        if serverform.assertnum.data != servermodel.AssertNum and \
                                ServerModel.query.filter_by(AssertNum=serverform.assertnum.data).first():
                            flash('资产编号冲突')
                        else:
                            serverposition = serverform.position1.data + '-' + serverform.position2.data + '-' + \
                                       serverform.position3.data + '-' + serverform.position4.data
                            servermodel.MODEL = serverform.model.data
                            servermodel.IP = serverform.ip.data
                            servermodel.POSITION = serverposition
                            servermodel.MAC = serverform.mac.data
                            servermodel.OWNER = serverform.owner.data
                            servermodel.STATUS = serverform.status.data
                            servermodel.UPTIME = serverform.uptime.data
                            servermodel.AssertNum = serverform.assertnum.data
                            db.session.commit()
                            main_logger.info('%s 修改服务器成功: %s', 'manager', serverform.ip.data)
                            servermodels = ServerModel.query.all()
                            return redirect(url_for('main.server', servermodels=servermodels))
    return render_template('modifyserver.html', form=serverform)


@main.route('/server/deleteserver', methods=['GET', 'POST'])
def deleteServer():
    serverid = request.args.get('id', '')
    servermodel = ServerModel.query.filter_by(ID=serverid).first()
    ip = servermodel.IP
    db.session.delete(servermodel)
    db.session.commit()
    main_logger.info('%s 删除服务器成功: %s', 'manager', ip)
    servermodels = ServerModel.query.all()
    return render_template('server.html', servermodels=servermodels)


@main.route('/raid/add', methods=['GET', 'POST'])
def addRaid():
    raidform = RaidForm()
    print("submit")
    print(raidform.validate_on_submit())
    print(raidform.data)
    if raidform.validate_on_submit():
        flash('已提交')
        if not re.match('[0-9]{2,3}', raidform.position4.data):
            flash('房间号格式不正确')
        else:
            if RaidModel.query.filter_by(IP=raidform.ip.data).first():
                flash('IP地址冲突')
            else:
                if raidform.assertnum.data and RaidModel.query.filter_by(AssertNum=raidform.assertnum.data).first():
                    flash('资产编号冲突')
                else:
                    position = raidform.position1.data + '-' + raidform.position2.data + '-' + \
                               raidform.position3.data + '-' + raidform.position4.data
                    print('not a')
                    a = get_ks3200_info(raidform.ip.data, position, raidform.owner.data, raidform.model.data, raidform.assertnum.data)
                    print('a')
                    print(a)
                    if not a:
                        raidmodel = RaidModel(MODEL=raidform.model.data,  POSITION=position,
                                              OWNER=raidform.owner.data, AssertNum=raidform.assertnum.data,
                                              IP=raidform.ip.data, UPTIME='', STATUS='OFF', USEDPERCENT='')
                        db.session.add(raidmodel)
                        db.session.commit()
                    main_logger.info('%s 添加磁阵成功: %s', 'manager', raidform.ip.data)
                    raidmodels = ServerModel.query.all()
                    return redirect(url_for('main.raid', raidmodels=raidmodels))
    return render_template('addraid.html', form=raidform)


@main.route('/raid/modify', methods=['GET', 'POST'])
def modifyRaid():
    raidid = request.args.get('id', '')
    raidmodel = RaidModel.query.filter_by(ID=raidid).first()
    position = raidmodel.POSITION.split('-')
    form = RaidForm(model=raidmodel.MODEL, ip=raidmodel.IP,
            uptime=raidmodel.UPTIME, owner=raidmodel.OWNER,
            status=raidmodel.STATUS, usedpercent=raidmodel.USEDPERCENT,
            assertnum=raidmodel.AssertNum, position1=position[0],
            position2=position[1], position3=position[2], position4=position[3])
    if form.validate_on_submit():
        flash('已提交')
        if not re.match('[0-9]{2,3}', form.position4.data):
            flash('房间号格式不正确')
        else:
            if form.ip.data != raidmodel.IP and ServerModel.query.filter_by(IP=form.ip.data).first():
                flash('IP地址冲突')
            else:
                if form.assertnum.data != raidmodel.AssertNum and \
                        ServerModel.query.filter_by(AssertNum=form.assertnum.data).first():
                    flash('资产编号冲突')
                else:
                    serverposition = form.position1.data + '-' + form.position2.data + '-' + \
                               form.position3.data + '-' + form.position4.data
                    raidmodel.MODEL = form.model.data
                    raidmodel.IP = form.ip.data
                    raidmodel.POSITION = serverposition
                    raidmodel.UPTIME = form.uptime.data
                    raidmodel.OWNER = form.owner.data
                    raidmodel.STATUS = form.status.data
                    raidmodel.USEDPERCENT = form.usedpercent.data
                    raidmodel.AssertNum = form.assertnum.data
                    db.session.commit()
                    main_logger.info('%s 修改磁阵成功: %s', 'manager', form.ip.data)
                    raidmodels = RaidModel.query.all()
                    return redirect(url_for('main.raid', raidmodels=raidmodels))
    return render_template('modifyraid.html', form=form)


@main.route('/server/deleteraid', methods=['GET', 'POST'])
def deleteRaid():
    raidid = request.args.get('id', '')
    raidmodel = RaidModel.query.filter_by(ID=raidid).first()
    ip = raidmodel.IP
    db.session.delete(raidmodel)
    db.session.commit()
    main_logger.info('%s 删除磁阵成功: %s', 'manager', ip)
    raidmodels = RaidModel.query.all()
    return render_template('raid.html', raidmodels=raidmodels)


@main.route('/switch/add', methods=['GET', 'POST'])
def addSwitch():
    switchform = SwitchForm()
    print("submit")
    print(switchform.validate_on_submit())
    print(switchform)
    if switchform.validate_on_submit():
        flash('已提交')
        if not re.match('[0-9]{2,3}', switchform.position4.data):
            flash('房间号格式不正确')
        else:
            if SwitchModel.query.filter_by(IP=switchform.ip.data).first():
                flash('IP地址冲突')
            else:
                if switchform.assertnum.data and SwitchModel.query.filter_by(AssertNum=switchform.assertnum.data).first():
                    flash('资产编号冲突')
                else:
                    position = switchform.position1.data + '-' + switchform.position2.data + '-' + \
                               switchform.position3.data + '-' + switchform.position4.data
                    print('not a')
                    a = get_switch_info(switchform.ip.data, position, switchform.owner.data, switchform.model.data, switchform.assertnum.data)
                    print('a')
                    print(a)
                    if not a:
                        switchmodel = SwitchModel(MODEL=switchform.model.data,  POSITION=position,
                                              OWNER=switchform.owner.data, AssertNum=switchform.assertnum.data,
                                              IP=switchform.ip.data, UPTIME='', STATUS='OFF', IFNUMBER='')
                        db.session.add(switchmodel)
                        db.session.commit()
                    main_logger.info('%s 添加交换机成功: %s', 'manager', switchform.ip.data)
                    switchmodels = SwitchModel.query.all()
                    return redirect(url_for('main.switch', switichmodels=switchmodels))
    return render_template('addswitch.html', form=switchform)


@main.route('/switch/modify', methods=['GET', 'POST'])
def modifySwitch():
    switchid = request.args.get('id', '')
    switchmodel = SwitchModel.query.filter_by(ID=switchid).first()
    position = switchmodel.POSITION.split('-')
    form = SwitchForm(model=switchmodel.MODEL, ip=switchmodel.IP,
            uptime=switchmodel.UPTIME, owner=switchmodel.OWNER,
            status=switchmodel.STATUS, ifnumber=switchmodel.IFNUMBER,
            assertnum=switchmodel.AssertNum, position1=position[0],
            position2=position[1], position3=position[2], position4=position[3])
    if form.validate_on_submit():
        flash('已提交')
        if not re.match('[0-9]{2,3}', form.position4.data):
            flash('房间号格式不正确')
        else:
            if form.ip.data != switchmodel.IP and ServerModel.query.filter_by(IP=form.ip.data).first():
                flash('IP地址冲突')
            else:
                if form.assertnum.data != switchmodel.AssertNum and \
                        ServerModel.query.filter_by(AssertNum=form.assertnum.data).first():
                    flash('资产编号冲突')
                else:
                    serverposition = form.position1.data + '-' + form.position2.data + '-' + \
                               form.position3.data + '-' + form.position4.data
                    switchmodel.MODEL = form.model.data
                    switchmodel.IP = form.ip.data
                    switchmodel.POSITION = serverposition
                    switchmodel.UPTIME = form.uptime.data
                    switchmodel.OWNER = form.owner.data
                    switchmodel.STATUS = form.status.data
                    switchmodel.IFNUMBER = form.ifnumber.data
                    switchmodel.AssertNum = form.assertnum.data
                    db.session.commit()
                    main_logger.info('%s 修改交换机成功: %s', 'manager', form.ip.data)
                    switchmodels = SwitchModel.query.all()
                    return redirect(url_for('main.switch', switchmodels=switchmodels))
    return render_template('modifyswitch.html', form=form)


@main.route('/switch/deleteswitch', methods=['GET', 'POST'])
def deleteSwitch():
    switchid = request.args.get('id', '')
    switchmodel = SwitchModel.query.filter_by(ID=switchid).first()
    ip = switchmodel.IP
    db.session.delete(switchmodel)
    db.session.commit()
    main_logger.info('%s 删除交换机成功: %s', 'manager', ip)
    switchmodels = SwitchModel.query.all()
    return render_template('switch.html', switchmodels=switchmodels)

@main.route('/server/batchadd', methods=['GET', 'POST'])
def batchadd():
    return render_template('server1.html')
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['xlsx'])

@main.route('/server/upload', methods=['GET', 'POST'])
def upload():
    #print("de")
    #print("de")
    print(request.files)
    file = request.files.get('file')
    print(file)
    #print("de1")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #print("de2")
        print(filename)
        file_path = '/opt/'
        file.save(os.path.join(file_path, filename))
        #print("de3")
        work_file = file_path + filename
        print(work_file)
        ExcelFile = xlrd.open_workbook(work_file)
        print("start batch insert\n") 
        table = ExcelFile.sheets()[0]
  
        #get rows number
        nrows = table.nrows 
        #print(nrows) 
        #get cols number
        ncols = table.ncols 
        data_list = []
  
        #start row from index 2, first row is the title
        for col in range(ncols):
            row_values = table.col_values(col, 1, nrows)
            data_list.append(row_values)
        print(data_list)
        try:
            for row in range(nrows-1):
                print("aaa")
                servermodel = ServerModel(MODEL=data_list[0][row], POSITION=data_list[2][row],
                                          OWNER=data_list[5][row], AssertNum=data_list[1][row],
                                          IP=data_list[4][row], MAC=data_list[3][row],
                                          STATUS=data_list[6][row], UPTIME=data_list[7][row])
                print(" WWJ")
                db.session.add(servermodel)
                db.session.commit()
            print("\ninsert sucessful\n")
        except Exception: 
            print("DB insert Exception")
            print(Exception)
    else:
        print("qingshuru1")
        #tkinter.messagebox.showerror("提示","请选择excel文件")
        print("aaa")
    servermodels = ServerModel.query.all()
    return redirect(url_for('main.server', servermodels=servermodels))
   #pass
   # pass


@main.route('/server/download', methods=['GET', 'POST'])
def Serverdownload():
    file_export_path = ""
    workbook = xlwt.Workbook(encoding = "UTF-8")
    servermodels_list = ServerModel.query.all()
    read_data_list = servermodels_list
    #print("de")
    for i in read_data_list:
        print("de"+i.MAC+"de")
    sheet = workbook.add_sheet('Asset Server information table')
    #insert the db_head to the generated excel
    head_list = [u"型号",u"资产编号",u"位置",\
                 u"MAC",u"IP",u"持有人", u"上电状态",u"上电时间"]
    col_head_insert_index = 0
    print("de1")
    for element in head_list:
        print("de2")
        sheet.write(0, col_head_insert_index, element)
        col_head_insert_index += 1
    #insert DB_data to generated excel
    row_insert_index = 1
    col_insert_index = 0
    for list in read_data_list:
        list_temp = [list.MODEL, list.AssertNum,\
                list.POSITION, list.MAC, list.IP,\
                list.OWNER, list.STATUS, list.UPTIME]
        print(list_temp)
        for element in list_temp:
            #print("de22")
            #print("a"+element+"b") 
            sheet.write(row_insert_index, col_insert_index, element)
            col_insert_index += 1
        row_insert_index += 1
        col_insert_index = 0
        #list_temp = [] 
    #print(row_insert_index)
    #print("de33")
    workbook.save(file_export_path.join(["Asset_server_information", ".xlsx"]))
    print("export sucessful")
    filename = "Asset_server_information.xlsx"
    directory = "/home/RMS_11/Asset_Management-code/cmdb-zte-1/"
    response = send_from_directory(directory, filename, as_attachment=True)
    return response
    #pass
@main.route('/raid/download', methods=['GET', 'POST'])
def Raiddownload():
    file_export_path = ""
    workbook = xlwt.Workbook(encoding = "UTF-8")
    servermodels_list = RaidModel.query.all()
    read_data_list = servermodels_list
    #print("de")
    sheet = workbook.add_sheet('Asset Raid information table')
    #insert the db_head to the generated excel
    head_list = [u"型号",u"位置",u"持有人",\
                 u"资产编号",u"IP","上电时间", u"上电状态",u"使用率"]
    col_head_insert_index = 0
    print(read_data_list[0].MODEL)
    print(read_data_list[0].POSITION)
    print(read_data_list[0].AssertNum)
    print(read_data_list[0].IP)
    print(read_data_list[0].STATUS)
    print(read_data_list[0].USEDPERCENT)
    print(read_data_list[0].OWNER)
    print(read_data_list[0].UPTIME)
    for element in head_list:
        print("de2")
        sheet.write(0, col_head_insert_index, element)
        col_head_insert_index += 1
    #insert DB_data to generated excel
    row_insert_index = 1
    col_insert_index = 0
    for list in read_data_list:
        print("de3")
        list_temp = [list.MODEL, list.POSITION,\
                     list.OWNER, list.AssertNum, list.IP,\
                     list.UPTIME, list.STATUS, list.USEDPERCENT]
        print(list_temp)
        for element in list_temp:
            #print("de22")
            #print("a"+element+"b") 
            sheet.write(row_insert_index, col_insert_index, element)
            col_insert_index += 1
        row_insert_index += 1
        col_insert_index = 0
        #list_temp = [] 
    #print(row_insert_index)
    #print("de33")
    workbook.save(file_export_path.join(["Asset_raid_information", ".xlsx"]))
    print("export sucessful")
    filename = "Asset_raid_information.xlsx"
    directory = "/home/RMS_11/Asset_Management-code/cmdb-zte-1/"
    response = send_from_directory(directory, filename, as_attachment=True)
    return response
    #pass

@main.route('/switch/download', methods=['GET', 'POST'])
def Switchdownload():
    file_export_path = ""
    workbook = xlwt.Workbook(encoding = "UTF-8")
    servermodels_list = SwitchModel.query.all()
    read_data_list = servermodels_list
    #print("de")
    sheet = workbook.add_sheet('Asset Switch information table')
    #insert the db_head to the generated excel
    head_list = [u"型号",u"位置",u"持有人",\
                 u"资产编号",u"IP",u"上电时间", u"上电状态",u"网络接口数量"]
    col_head_insert_index = 0
    print(read_data_list)
    for element in head_list:
        print("de2")
        sheet.write(0, col_head_insert_index, element)
        col_head_insert_index += 1
    #insert DB_data to generated excel
    row_insert_index = 1
    col_insert_index = 0
    for list in read_data_list:
        list_temp = [list.MODEL, list.POSITION,\
                list.OWNER, list.AssertNum, list.IP,\
                list.UPTIME, list.STATUS, list.IFNUMBER]
        print(list_temp)
        for element in list_temp:
            #print("de22")
            #print("a"+element+"b") 
            sheet.write(row_insert_index, col_insert_index, element)
            col_insert_index += 1
        row_insert_index += 1
        col_insert_index = 0
        #list_temp = [] 
    #print(row_insert_index)
    #print("de33")
    workbook.save(file_export_path.join(["Asset_switch_information", ".xlsx"]))
    print("export sucessful")
    filename = "Asset_switch_information.xlsx"
    directory = "/home/RMS_11/Asset_Management-code/cmdb-zte-1/"
    response = send_from_directory(directory, filename, as_attachment=True)
    return response
    #pass


@main.route('/update', methods=['GET', 'POST'])
def update():
    update_server_DB()
    update_storage_DB()
    update_switch_DB()
    servermodels = ServerModel.query.all()
    return redirect(url_for('main.server', servermodels=servermodels))

