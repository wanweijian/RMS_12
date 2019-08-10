# -*- coding: utf-8 -*-

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class ServerForm(FlaskForm):
    ip = StringField(label=u'IP地址', validators=[DataRequired(message=u'请输入IP')])
    owner = StringField(label=u'持有人', validators=[DataRequired(message=u'请输入持有人')])
    assertnum = StringField(label=u'资产编号', validators=[])
    mac = StringField(label=u'MAC地址', validators=[])
    status = StringField(label=u'状态', validators=[])
    uptime = StringField(label=u'上电时长', validators=[])
    model = SelectField(label=u'型号', choices=[('R5300', 'R5300'), ('E9000', 'E9000'), ('HP', 'HP')],
                        validators=[DataRequired(message=u'请选择型号')],
                        coerce=str)
    position1 = SelectField(label=u'南研所', choices=[(u'一区一期', u'一区一期'),
                            (u'一区二期', u'一区二期'), (u'二区', u'二区')],
                            validators=[DataRequired(message=u'请选择地点')],
                            default=u'一区一期',
                            coerce=str)
    position2 = SelectField(label=u'区域', choices=[(u'A区', u'A区'), (u'B区', u'B区'), (u'C区', u'C区'), (u'D区', u'D区')],
                            validators=[DataRequired(message=u'请选择区域')],
                            default=u'A区',
                            coerce=str)
    position3 = SelectField(label=u'楼层', choices=[(u'1楼', u'1楼'), (u'2楼', u'2楼'), (u'3楼', u'3楼'),
                            (u'4楼', u'4楼'), (u'5楼', u'5楼'), (u'6楼', u'6楼')],
                            validators=[DataRequired(message=u'请选择楼层')],
                            default=u'1楼',
                            coerce=str)
    position4 = StringField(label=u'房间', validators=[DataRequired(message=u'请输入房间')])
    buttonserver = SubmitField(label=u'确定')


class RaidForm(FlaskForm):
    ip = StringField(label=u'IP地址', validators=[DataRequired(message=u'请输入IP')])
    owner = StringField(label=u'持有人', validators=[DataRequired(message=u'请输入持有人')])
    assertnum = StringField(label=u'资产编号', validators=[])
    status = StringField(label=u'状态', validators=[])
    uptime = StringField(label=u'上电时长', validators=[])
    usedpercent = StringField(label=u'使用率(%)', validators=[])
    model = SelectField(label=u'型号', choices=[('KS3200', 'KS3200'), ('KU5200', 'KU5200'), ('IBM', 'IBM')],
                        validators=[DataRequired(message=u'请选择型号')],
                        coerce=str)
    position1 = SelectField(label=u'南研所', choices=[(u'一区一期', u'一区一期'),
                            (u'一区二期', u'一区二期'), (u'二区', u'二区')],
                            default=u'一区一期',
                            coerce=str)
    position2 = SelectField(label=u'区域', choices=[(u'A区', u'A区'), (u'B区', u'B区'), (u'C区', u'C区'), (u'D区', u'D区')],
                            validators=[DataRequired(message=u'请选择区域')],
                            default=u'A区',
                            coerce=str)
    position3 = SelectField(label=u'楼层', choices=[(u'1楼', u'1楼'), (u'2楼', u'2楼'), (u'3楼', u'3楼'),
                            (u'4楼', u'4楼'), (u'5楼', u'5楼'), (u'6楼', u'6楼')],
                            validators=[DataRequired(message=u'请选择楼层')],
                            default=u'1楼',
                            coerce=str)
    position4 = StringField(label=u'房间', validators=[DataRequired(message=u'请输入房间')])
    buttonraid = SubmitField(label=u'确定')


class SwitchForm(FlaskForm):
    ip = StringField(label=u'IP地址', validators=[DataRequired(message=u'请输入IP')])
    owner = StringField(label=u'持有人', validators=[DataRequired(message=u'请输入持有人')])
    assertnum = StringField(label=u'资产编号', validators=[])
    status = StringField(label=u'状态', validators=[])
    uptime = StringField(label=u'上电时长', validators=[])
    ifnumber = StringField(label=u'使用率(%)', validators=[])
    model = SelectField(label=u'型号', choices=[('ZXR10', 'ZXR10')],
                        validators=[DataRequired(message=u'请选择型号')],
                        coerce=str)
    position1 = SelectField(label=u'南研所', choices=[(u'一区一期', u'一区一期'),
                            (u'一区二期', u'一区二期'), (u'二区', u'二区')],
                            validators=[DataRequired(message=u'请选择地点')],
                            default=u'一区一期',
                            coerce=str)
    position2 = SelectField(label=u'区域', choices=[(u'A区', u'A区'), (u'B区', u'B区'), (u'C区', u'C区'), (u'D区', u'D区')],
                            validators=[DataRequired(message=u'请选择区域')],
                            default=u'A区',
                            coerce=str)
    position3 = SelectField(label=u'楼层', choices=[(u'1楼', u'1楼'), (u'2楼', u'2楼'), (u'3楼', u'3楼'),
                            (u'4楼', u'4楼'), (u'5楼', u'5楼'), (u'6楼', u'6楼')],
                            validators=[DataRequired(message=u'请选择楼层')],
                            default=u'1楼',
                            coerce=str)
    position4 = StringField(label=u'房间', validators=[DataRequired(message=u'请输入房间')])
    buttonswitch = SubmitField(label=u'确定')
