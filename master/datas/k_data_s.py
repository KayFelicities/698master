# coding: utf-8
"""oi attr explain"""
import re
import time
import traceback
from collections import namedtuple


class Data698():
    def __init__(self, kay):
        if kay != '123456':
            return
        if time.localtime()[0] > 2022:
            return
        ic_table =\
        [
            ('1', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('1', '属性', '2', 'dyn.', '总及费率电能量数组', 'array:CHOICE{:double-long-unsigned[6],:double-long[5]},'),
            ('1', '属性', '3', 'static', '换算及单位', 'Scaler_Unit,'),
            ('1', '属性', '4', 'dyn.', '高精度总及费率电能量数组', 'array:CHOICE{:long64-unsigned[21],:long64[20]},'),
            ('1', '属性', '5', 'static', '高精度换算及单位', 'Scaler_Unit,'),
            ('1', '方法', '1', '', '复位', 'integer,'),
            ('1', '方法', '2', '', '执行', 'Data,'),
            ('2', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('2', '属性', '2', 'dyn.', '总及费率最大需量数组', 'array:structure{最大需量值CHOICE{:double-long[5],:double-long-unsigned[6]},发生时间:date_time_s},'),
            ('2', '属性', '3', 'static', '换算及单位', 'Scaler_Unit,'),
            ('2', '方法', '1', '', '复位', 'integer,'),
            ('2', '方法', '2', '', '执行', 'Data,'),
            ('3', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('3', '属性', '2', 'dyn.', '分相数值组', 'array:instance-specific,'),
            ('3', '属性', '3', 'static', '换算及单位', 'Scaler_Unit,'),
            ('3', '方法', '1', '', '复位', 'integer,'),
            ('3', '方法', '2', '', '执行', 'Data,'),
            ('4', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('4', '属性', '2', 'dyn.', '总及分相数值组', 'array:instance-specific,'),
            ('4', '属性', '3', 'static', '换算及单位', 'Scaler_Unit,'),
            ('4', '方法', '1', '', '复位', 'integer,'),
            ('4', '方法', '2', '', '执行', 'Data,'),
            ('5', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('5', '属性', '2', 'dyn.', 'A相n次数值组', 'array:instance-specific,'),
            ('5', '属性', '3', 'dyn.', 'B相n次数值组', 'array:instance-specific,'),
            ('5', '属性', '4', 'dyn.', 'C相n次数值组', 'array:instance-specific,'),
            ('5', '属性', '5', 'static', '谐波次数 n', 'unsigned,'),
            ('5', '属性', '6', 'static', '换算及单位', 'Scaler_Unit,'),
            ('5', '方法', '1', '', '复位', 'integer,'),
            ('5', '方法', '2', '', '执行', 'Data,'),
            ('6', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('6', '属性', '2', 'dyn.', '数值', 'instance-specific,'),
            ('6', '属性', '3', 'static', '换算及单位', 'Scaler_Unit,'),
            ('6', '方法', '1', '', '复位', 'integer,'),
            ('6', '方法', '2', '', '执行', 'Data,'),
            ('7', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('7', '属性', '2', 'dyn.', '事件记录表', 'array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},事件特殊数据1:instance-specific,…事件特殊数据N:instance-specific,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('7', '属性', '3', 'static', '关联对象属性表', 'array:OAD,'),
            ('7', '属性', '4', 'dyn.', '当前记录数', 'long-unsigned,'),
            ('7', '属性', '5', 'static', '最大记录数', 'long-unsigned,'),
            ('7', '属性', '6', 'static', '配置参数', 'structure{参数1:instance-specific,…参数n:instance-specific},'),
            ('7', '属性', '7', 'dyn.', '当前值记录表', 'array:structure{事件发生源:instance-specific,累计时间及发生次数:structure{事件发生次数:double-long-unsigned,事件累计时间:double-long-unsigned}},'),
            ('7', '属性', '8', 'static', '上报标识', '上报标识enum[不上报<0>,事件发生上报<1>,事件恢复上报<2>,事件发生恢复均上报<3>],'),
            ('7', '属性', '9', 'static', '有效标识', 'bool,'),
            ('7', '方法', '1', '', '复位', 'integer,'),
            ('7', '方法', '2', '', '执行', 'Data,'),
            ('7', '方法', '3', '', '触发一次记录', 'structure{事件发生源:instance-specific, 参数:long-unsigned},'),
            ('7', '方法', '4', '', '添加一个事件关联对象属性', 'OAD,'),
            ('7', '方法', '5', '', '删除一个事件关联对象属性', 'OAD,'),
            ('8', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('8', '属性', '2', 'static', '参数', 'instance-specific,'),
            ('8', '方法', '1', '', '复位', 'integer,'),
            ('8', '方法', '2', '', '执行', 'Data,'),
            ('9', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('9', '属性', '2', 'dyn.', '冻结数据表', 'array:structure{冻结记录序号:double-long-unsigned,冻结时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('9', '属性', '3', 'static', '关联对象属性表', 'array:structure{冻结周期:long-unsigned,关联对象属性描述符:OAD,存储深度:long-unsigned},'),
            ('9', '属性', '4', 'static', '配置参数', 'structureinstance-specific,'),
            ('9', '方法', '1', '', '复位', 'integer,'),
            ('9', '方法', '2', '', '执行', 'Data,'),
            ('9', '方法', '3', '', '触发一次冻结', 'long-unsigned,'),
            ('9', '方法', '4', '', '添加一个冻结对象属性', 'structure{冻结周期:long-unsigned,关联对象属性描述符:OAD,存储深度:long-unsigned},'),
            ('9', '方法', '5', '', '删除一个冻结对象属性', 'OAD,'),
            ('9', '方法', '6', '', '触发数据补冻结', 'structure{起始时间:date_time_s,截止时间:date_time_s},'),
            ('9', '方法', '7', '', '批量添加冻结对象属性', 'array:冻结对象:structure{冻结周期:long-unsigned,关联对象属性描述符:OAD,存储深度:long-unsigned},'),
            ('9', '方法', '8', '', '清除关联对象属性表（参数）', ','),
            ('10', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('10', '属性', '2', 'static', '配置表', 'array:instance-specific,'),
            ('10', '属性', '3', 'dyn.', '记录表', 'array:instance-specific,'),
            ('10', '方法', '1', '', '复位', 'integer,'),
            ('10', '方法', '2', '', '执行', 'Data,'),
            ('10', '方法', '3', '', '清空记录表', ','),
            ('11', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('11', '属性', '2', 'dyn.', '集合', 'array:instance-specific,'),
            ('11', '属性', '3', 'dyn.', '当前元素个数', 'long-unsigned,'),
            ('11', '属性', '4', 'static', '最大元素个数', 'long-unsigned,'),
            ('11', '方法', '1', '', '复位', 'integer,'),
            ('11', '方法', '2', '', '执行', 'Data,'),
            ('12', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('12', '属性', '2', 'static', '通信地址', 'octet-string,'),
            ('12', '属性', '3', 'static', '互感器倍率', 'structure{PT:long-unsigned,CT:long-unsigned},'),
            ('12', '属性', '4', 'static', '脉冲配置', 'array:structure{脉冲输入端口号:OAD,脉冲属性:enum[正向有功<0>,正向无功<1>,反向有功<2>,反向无功<3>],脉冲常数k:long-unsigned},'),
            ('12', '属性', '5', 'dyn.', '有功功率', 'double-long,'),
            ('12', '属性', '6', 'dyn.', '无功功率', 'double-long,'),
            ('12', '属性', '7', 'dyn.', '当日正向有功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '8', 'dyn.', '当月正向有功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '9', 'dyn.', '当日反向有功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '10', 'dyn.', '当月反向有功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '11', 'dyn.', '当日正向无功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '12', 'dyn.', '当月正向无功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '13', 'dyn.', '当日反向无功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '14', 'dyn.', '当月反向无功电量', 'array:double-long-unsigned,'),
            ('12', '属性', '15', 'dyn.', '正向有功电能示值', 'array:double-long-unsigned,'),
            ('12', '属性', '16', 'dyn.', '正向无功电能示值', 'array:double-long-unsigned,'),
            ('12', '属性', '17', 'dyn.', '反向有功电能示值', 'array:double-long-unsigned,'),
            ('12', '属性', '18', 'dyn.', '反向无功电能示值', 'array:double-long-unsigned,'),
            ('12', '属性', '19', 'static', '换算及单位', 'structure{属性5单位及换算:Scaler_Unit,属性6单位及换算:Scaler_Unit,属性7单位及换算:Scaler_Unit,属性8单位及换算:Scaler_Unit,属性9单位及换算:Scaler_Unit,属性10单位及换算:Scaler_Unit,属性11单位及换算:Scaler_Unit,属性12单位及换算:Scaler_Unit,属性13单位及换算:Scaler_Unit,属性14单位及换算:Scaler_Unit,属性15单位及换算:Scaler_Unit,属性16单位及换算:Scaler_Unit,属性17单位及换算:Scaler_Unit,属性18单位及换算:Scaler_Unit},'),
            ('12', '方法', '1', '', '复位', 'bit-string,'),
            ('12', '方法', '2', '', '执行', 'Data,'),
            ('12', '方法', '3', '', '添加脉冲输入单元', ','),
            ('12', '方法', '4', '', '删除脉冲输入单元', ','),
            ('13', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('13', '属性', '2', 'static', '控制方案集', 'array:instance-specific,'),
            ('13', '属性', '3', 'dyn.', '控制投入状态', 'array:structure{总加组对象:OI,投入状态:enum[未投入<0>,投入<1>]},'),
            ('13', '属性', '4', 'dyn.', '控制输出状态', 'array:structure{总加组对象:OI,控制输出状态:bit-string(SIZE(8))},'),
            ('13', '属性', '5', 'dyn.', '越限告警状态', 'array:structure{总加组对象:OI,告警输出状态:enum[未告警<0>,告警<1>]},'),
            ('13', '方法', '1', '', '复位', 'integer,'),
            ('13', '方法', '2', '', '执行', 'Data,'),
            ('13', '方法', '3', '', '添加控制单元', 'instance-specific,'),
            ('13', '方法', '4', '', '删除控制单元', 'OI,'),
            ('13', '方法', '5', '', '更新控制单元', 'instance-specific,'),
            ('13', '方法', '6', '', '控制投入', 'OI,'),
            ('13', '方法', '7', '', '控制解除', 'OI,'),
            ('14', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('14', '属性', '2', 'dyn.', '统计结果表', 'array:structure{对象属性描述符:OAD,区间统计值:array:structure{累计时间:double-long-unsigned,累计次数:double-long-unsigned}},'),
            ('14', '属性', '3', 'static', '关联对象属性表', 'array:structure{关联对象属性描述符:OAD,越限判断参数:array:Data,统计周期:unsigned,统计频率:TI},'),
            ('14', '方法', '1', '', '复位', 'integer,'),
            ('14', '方法', '2', '', '执行', 'Data,'),
            ('14', '方法', '3', '', '添加一个统计对象属性', 'structure{关联对象属性描述符:OAD,越限判断参数:array:Data,统计周期:unsigned,统计频率:TI},'),
            ('14', '方法', '4', '', '删除一个统计对象属性', 'OAD,'),
            ('15', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('15', '属性', '2', 'dyn.', '运算结果', 'structure{对象属性描述符:OAD,累加和:instance-specific,平均值:instance-specific},'),
            ('15', '属性', '3', 'static', '关联对象属性表', 'array:structure{关联对象属性描述符:OAD,统计周期:unsigned,统计频率:TI},'),
            ('15', '方法', '1', '', '复位', 'integer,'),
            ('15', '方法', '2', '', '执行', 'Data,'),
            ('15', '方法', '3', '', '添加一个关联对象属性', 'structure{关联对象属性描述符:OAD,统计周期:unsigned,统计频率:TI},'),
            ('15', '方法', '4', '', '删除一个关联对象属性', 'OAD,'),
            ('16', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('16', '属性', '2', 'dyn.', '极值结果表', 'array:structure{对象属性描述符:OAD,最大值:instance-specific,及其发生时间:date_time_s,最小值:instance-specific,及其发生时间:date_time_s},'),
            ('16', '属性', '3', 'static', '关联对象属性表', 'array:structure{关联对象属性描述符:OAD,统计周期:unsigned,统计频率:TI},'),
            ('16', '方法', '1', '', '复位', 'integer,'),
            ('16', '方法', '2', '', '执行', 'Data,'),
            ('16', '方法', '3', '', '添加一个关联对象属性', 'structure{关联对象属性描述符:OAD,统计周期:unsigned,统计频率:TI},'),
            ('16', '方法', '4', '', '删除一个关联对象属性', 'OAD,'),
            ('17', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('17', '属性', '2', 'static', '显示对象列表', 'array:structure{显示对象:CSD,屏序号:unsigned},'),
            ('17', '属性', '3', 'static', '显示时间', 'double-long-unsigned,'),
            ('17', '属性', '4', 'static', '显示参数', 'structure{当前总对象数:unsigned,允许最大对象数:unsigned},'),
            ('17', '方法', '1', '', '复位', 'integer,'),
            ('17', '方法', '2', '', '执行', 'Data,'),
            ('17', '方法', '3', '', '下翻', 'NULL,'),
            ('17', '方法', '4', '', '上翻', 'NULL,'),
            ('17', '方法', '5', '', '显示查看', 'structure{显示列信息:CSD,屏序号:unsigned,显示持续时间:long-unsigned},'),
            ('17', '方法', '6', '', '全显', 'long-unsigned,'),
            ('18', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('18', '属性', '2', 'dyn.', '文件信息', 'structure{源文件:visible-string,目标文件:visible-string,文件大小:double-long-unsigned,文件属性:bit-string(SIZE(3)),文件版本:visible-string文件类别:enum[终端文件<0>,本地通信模块文件<1>,远程通信模块文件<2>,采集器文件<3>,从节点通信模块文件<4>,其它文件<255>]},'),
            ('18', '属性', '3', 'dyn.', '命令结果', ':enum[文件传输进度0~99%<0-99>,传输或执行操作成功<100>,正在建立连接<扩展传输><101>,正在远程登录<扩展传输><102>,正在执行文件<103>,文件或目录不存在<104>,操作不允许<创建/删除/读写/执行><105>,文件传输中断<106>,文件校验失败<107>,文件转发失败<108>,文件代收失败<109>,建立连接失败<扩展传输><110>,远程登录失败<扩展传输><111>,存储空间不足<112>,复位后默认值<255>],'),
            ('18', '方法', '1', '', '复位', 'integer,'),
            ('18', '方法', '2', '', '执行', 'Data,'),
            ('18', '方法', '3', '', '删除', 'null,'),
            ('18', '方法', '4', '', '校验', 'structure{校验类型:enum[CRC校验<默认><0>,md5校验<1>,SHA1校验<2>,其他<255>],校验值:octet-string},'),
            ('18', '方法', '5', '', '代发', 'TSA,'),
            ('18', '方法', '6', '', '代收', 'TSA,'),
            ('18', '方法', '7', '', '上传', 'Data,'),
            ('18', '方法', '8', '', '下载', 'Data,'),
            ('19', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('19', '属性', '2', 'static', '设备描述符', 'visible-string,'),
            ('19', '属性', '3', 'static', '版本信息', 'structure{厂商代码:visible-string(SIZE(4)),软件版本号:visible-string(SIZE(4)),软件版本日期:visible-string(SIZE(6)),硬件版本号:visible-string(SIZE(4)),硬件版本日期:visible-string(SIZE(6)),厂家扩展信息:visible-string(SIZE(8))},'),
            ('19', '属性', '4', 'static', '生产日期', 'date_time_s,'),
            ('19', '属性', '5', 'static', '子设备列表', 'array:OI,'),
            ('19', '属性', '6', 'static', '支持规约列表', 'array:visible-string,'),
            ('19', '属性', '7', 'static', '允许跟随上报', 'bool,'),
            ('19', '属性', '8', 'static', '允许主动上报', 'bool,'),
            ('19', '属性', '9', 'static', '允许与主站通话', 'bool,'),
            ('19', '属性', '10', 'static', '上报通道', 'array:OAD,'),
            ('19', '方法', '1', '', '复位', 'NULL,'),
            ('19', '方法', '2', '', '执行', 'Data,'),
            ('19', '方法', '3', '', '数据初始化', ','),
            ('19', '方法', '4', '', '恢复出厂参数', 'array:OAD,'),
            ('19', '方法', '5', '', '事件初始化', ','),
            ('19', '方法', '6', '', '需量初始化', ','),
            ('20', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('20', '属性', '2', 'static', '对象列表', 'array:structure{对象标识:OI,访问权限:structure{属性访问权限:array:structure{属性ID:unsigned,属性访问权限类别:enum[不可访问<0>,只读<1>,只写<2>,可读写<3>]},方法访问权限:array:structure{方法ID:unsigned,方法访问权限:bool}}},'),
            ('20', '属性', '3', 'static', '应用语境信息', 'structure{协议版本信息:long-unsigned,最大接收APDU尺寸:long-unsigned,最大发送APDU尺寸:long-unsigned,最大可处理APDU尺寸:long-unsigned,协议一致性块:bit-string(64),功能一致性块:bit-string(128),静态超时时间:double-long-unsigned},'),
            ('20', '属性', '4', 'dyn.', '当前连接的客户机地址', 'unsigned,'),
            ('20', '属性', '5', 'static', '身份验证机制', ':enum[公共连接<0>,普通密码<1>,对称加密<2>,数字签名<3>],'),
            ('20', '方法', '1', '', '复位', 'integer,'),
            ('20', '方法', '2', '', '执行', 'Data,'),
            ('21', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('21', '属性', '2', 'static', 'ESAM 序列号', 'octet-string,'),
            ('21', '属性', '3', 'static', 'ESAM 版本号', 'octet-string,'),
            ('21', '属性', '4', 'static', '对称密钥版本', 'octet-string,'),
            ('21', '属性', '5', 'static', '会话时效门限', 'double-long-unsigned,'),
            ('21', '属性', '6', 'dyn.', '会话时效剩余时间', 'double-long-unsigned,'),
            ('21', '属性', '7', 'static', '当前计数器', 'structure{单地址应用协商计数器:double-long-unsigned,主动上报计数器:double-long-unsigned,应用广播通信序列号:double-long-unsigned},'),
            ('21', '属性', '8', 'static', '证书版本', 'structure{终端证书版本:octet-string,主站证书版本:octet-string},'),
            ('21', '属性', '9', 'static', '终端证书序列号', 'octet-string,'),
            ('21', '属性', '10', 'static', '终端证书', 'octet-string,'),
            ('21', '属性', '11', 'static', '主站证书序列号', 'octet-string,'),
            ('21', '属性', '12', 'static', '主站证书', 'octet-string,'),
            ('21', '属性', '13', 'static', 'ESAM 安全存储对象列表', 'array:OAD,'),
            ('21', '方法', '1', '', '复位', 'integer,'),
            ('21', '方法', '2', '', '执行', 'Data,'),
            ('21', '方法', '3', '', 'ESAM 数据读取', 'SID,'),
            ('21', '方法', '4', '', '数据更新', 'structure{参数内容:octet-string,数据验证码:SID_MAC},'),
            ('21', '方法', '5', '', '协商失效', 'NULL,'),
            ('21', '方法', '6', '', '钱包操作（开户、充值、退费）', 'structure{操作类型:integer,购电金额:double-long-unsigned,购电次数:double-long-unsigned,户号:octet-string,数据验证码:SID_MAC,表号:octet-string},'),
            ('21', '方法', '7', '', '密钥更新', 'structure{密钥密文:octet-string,数据验证码:SID_MAC},'),
            ('21', '方法', '8', '', '证书更新', 'structure{证书内容:octet-string,安全标识:SID},'),
            ('21', '方法', '9', '', '设置协商时效', 'structure{参数内容:octet-string,安全标识:SID},'),
            ('21', '方法', '10', '', '钱包初始化', 'structure{预置金额:double-long-unsigned,数据验证码:SID_MAC},'),
            ('22', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('22', '属性', '2', 'static', '设备对象列表', 'array,'),
            ('22', '属性', '3', 'static', '设备对象数量', 'unsigned,'),
            ('22', '属性', '4', 'static', '配置参数', 'instance-specific,'),
            ('22', '方法', '1', '', '复位', 'bit-string,'),
            ('22', '方法', '2', '', '执行', 'Data,'),
            ('23', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('23', '属性', '2', 'static', '总加配置表', 'array:structure{参与总加的分路通信地址:TSA,总加标志:enum[正向<0>,反向<1>],运算符标志:enum[加<0>,减<1>]},'),
            ('23', '属性', '3', 'dyn.', '总加有功功率', 'long64,'),
            ('23', '属性', '4', 'dyn.', '总加无功功率', 'long64,'),
            ('23', '属性', '5', 'dyn.', '总加滑差时间内平均有功功率', 'long64,'),
            ('23', '属性', '6', 'dyn.', '总加滑差时间内平均无功功率', 'long64,'),
            ('23', '属性', '7', 'dyn.', '总加日有功电量', 'array:long64,'),
            ('23', '属性', '8', 'dyn.', '总加日无功电量', 'array:long64,'),
            ('23', '属性', '9', 'dyn.', '总加月有功电量', 'array:long64,'),
            ('23', '属性', '10', 'dyn.', '总加月无功电量', 'array:long64,'),
            ('23', '属性', '11', 'dyn.', '总加剩余电量（费）', 'long64,'),
            ('23', '属性', '12', 'dyn.', '当前功率下浮控控后总加有功功率冻结值', 'long64,'),
            ('23', '属性', '13', 'static', '总加组滑差时间周期', 'unsigned<分|0>,'),
            ('23', '属性', '14', 'static', '总加组功控轮次配置', 'bit-string,'),
            ('23', '属性', '15', 'static', '总加组电控轮次配置', 'bit-string,'),
            ('23', '属性', '16', 'dyn.', '总加组控制设置状态', 'structure{时段控定值方案号:unsigned,功控时段有效标志位:bit-string(SIZE(8)),功控状态:bit-string(SIZE(8)),电控状态:bit-string(SIZE(8)),功控轮次状态:bit-string(SIZE(8)),电控轮次状态:bit-string(SIZE(8))},'),
            ('23', '属性', '17', 'dyn.', '总加组当前控制状态', 'structure{当前功控定值:long64<W|-1>,当前功率下浮控浮动系数:integer<%|0>,功控跳闸输出状态:bit-string(SIZE(8)),月电控跳闸输出状态:bit-string(SIZE(8)),购电控跳闸输出状态:bit-string(SIZE(8)),功控越限告警状态:bit-string(SIZE(8)),电控越限告警状态:bit-string(SIZE(8))},'),
            ('23', '属性', '18', 'static', '换算及单位', 'structure{属性3单位换算:Scaler_Unit,属性4单位换算:Scaler_Unit,属性5单位换算:Scaler_Unit,属性6单位换算:Scaler_Unit,属性7单位换算:Scaler_Unit,属性8单位换算:Scaler_Unit,属性9单位换算:Scaler_Unit,属性10单位换算:Scaler_Unit,属性11单位换算:Scaler_Unit,属性12单位换算:Scaler_Unit},'),
            ('23', '方法', '1', '', '清空总加配置单元', 'NULL,'),
            ('23', '方法', '2', '', '执行', 'Data,'),
            ('23', '方法', '3', '', '添加一个总加配置单元', 'structure{参与总加的分路通信地址:TSA,总加标志:enum[正向<0>,反向<1>],运算符标志:enum[加<0>,减<1>]},'),
            ('23', '方法', '4', '', '批量添加总加配置单元', 'array:structure{参与总加的分路通信地址:TSA,总加标志:enum[正向<0>,反向<1>],运算符标志:enum[加<0>,减<1>]},'),
            ('23', '方法', '5', '', '删除一个总加配置单元', '参与总加的分路通信地址:TSA,'),
            ('24', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('24', '属性', '2', 'static', '关联对象属性表', 'array:OAD,'),
            ('24', '属性', '3', 'dyn.', '当前记录数', 'structure{记录表1当前记录数:long-unsigned,记录表2当前记录数:long-unsigned,记录表3当前记录数:long-unsigned,记录表4当前记录数:long-unsigned,},'),
            ('24', '属性', '4', 'static', '最大记录数', 'long-unsigned,'),
            ('24', '属性', '5', 'static', '配置参数', 'structure{参数1:instance-specific,…参数n:instance-specific},'),
            ('24', '属性', '6', 'dyn.', '事件记录表 1', 'array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件上报状态:array通道上报状态,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('24', '属性', '7', 'dyn.', '事件记录表 2', 'array:array,'),
            ('24', '属性', '8', 'dyn.', '事件记录表 3', 'array:array,'),
            ('24', '属性', '9', 'dyn.', '事件记录表 4', 'array:array,'),
            ('24', '属性', '10', 'dyn.', '当前值记录表', 'array:structure{事件发生次数:double-long-unsigned,事件累计时间:double-long-unsigned},'),
            ('24', '属性', '11', 'static', '上报标识', ':enum[不上报<0>,事件发生上报<1>,事件恢复上报<2>,事件发生恢复均上报<3>],'),
            ('24', '属性', '12', 'static', '有效标识', 'bool,'),
            ('24', '方法', '1', '', '复位', 'integer,'),
            ('24', '方法', '2', '', '执行', 'Data,'),
            ('24', '方法', '3', '', '触发一次记录', ':enum[事件记录1<0>,事件记录2<1>,事件记录3<2>,事件记录4<3>],'),
            ('24', '方法', '4', '', '添加一个事件关联对象属性', 'OAD,'),
            ('24', '方法', '5', '', '删除一个事件关联对象属性', 'OAD,'),
            ('25', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('25', '属性', '2', 'static', '通信配置', 'structure{工作模式:enum[混合模式<0>,客户机模式<1>,服务器模式<2>],在线方式:enum[永久在线<0>,被动激活<1>],连接方式:enum[TCP<0>,UDP<1>],连接应用方式:enum[主备模式<0>,多连接模式<1>],侦听端口列表:array:long-unsigned,APN:visible-string,用户名:visible-string,密码:visible-string,代理服务器地址:octet-string,代理端口:long-unsigned,超时时间及重发次数:unsigned,心跳周期(秒):long-unsigned},'),
            ('25', '属性', '3', 'static', '主站通信参数表', 'array:structure{IP地址:octet-string,端口:long-unsigned},'),
            ('25', '属性', '4', 'static', '短信通信参数', 'structure{短信中心号码:visible-string(SIZE(16)),主站号码:array:visible-string(SIZE(16)),短信通知目的号码:array:visible-string(SIZE(16))},'),
            ('25', '属性', '5', 'static', '版本信息', 'structure{厂商代码:visible-string(SIZE(4)),软件版本号:visible-string(SIZE(4)),软件版本日期:visible-string(SIZE(6)),硬件版本号:visible-string(SIZE(4)),硬件版本日期:visible-string(SIZE(6)),厂家扩展信息:visible-string(SIZE(8))},'),
            ('25', '属性', '6', 'static', '支持规约列表', 'array:visible-string,'),
            ('25', '属性', '7', 'static', 'SIM 卡的 ICCID', 'visible-string(SIZE(20)),'),
            ('25', '属性', '8', 'static', 'IMSI', 'visible-string(SIZE(15)),'),
            ('25', '属性', '9', 'dyn', '信号强度', 'long<dBm|0>,'),
            ('25', '属性', '10', 'dyn.', 'SIM 卡号码', 'visible-string(SIZE(16)),'),
            ('25', '属性', '11', 'dyn', '拨号 IP', 'octet-string,'),
            ('25', '方法', '1', '', '复位', 'NULL,'),
            ('26', '属性', '1', 'static', '逻辑名', 'octet-string,'),
            ('26', '属性', '2', 'static', '通信配置', 'structure{工作模式:enum[混合模式<0>,客户机模式<1>,服务器模式<2>],连接方式:enum[TCP<0>,UDP<1>],连接应用方式:enum[主备模式<0>,多连接模式<1>],侦听端口列表:array:long-unsigned,代理服务器地址:octet-string,代理端口:long-unsigned,超时时间及重发次数:unsigned,心跳周期(秒):long-unsigned},'),
            ('26', '属性', '3', 'static', '主站通信参数表', 'array:structure{IP地址:octet-string,端口:long-unsigned},'),
            ('26', '属性', '4', 'static', '终端 IP', 'structure{IP配置方式:enum[DHCP<0>,静态<1>,PPPoE<2>],IP地址:octet-string,子网掩码:octet-string,网关地址:octet-string,PPPoE用户名:visible-string,PPPoE密码:visible-string},'),
            ('26', '属性', '5', 'static', 'MAC 地址', 'octet-string,'),
            ('26', '方法', '1', '', '复位', 'NULL,'),
        ]

        oi_table =\
        [
            ('0000', '组合有功电能', '1', '电能量类', '属性', '2', '', '组合有功电能:array:double-long<kWh|-2>,'),
            ('0000', '组合有功电能', '1', '电能量类', '属性', '4', '', '组合有功电能:array:long64<kWh|-4>,'),
            ('0010', '正向有功电能', '1', '电能量类', '属性', '2', '', '正向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0010', '正向有功电能', '1', '电能量类', '属性', '4', '', '正向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0011', 'A相正向有功电能', '1', '电能量类', '属性', '2', '', 'A相正向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0011', 'A相正向有功电能', '1', '电能量类', '属性', '4', '', 'A相正向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0012', 'B相正向有功电能', '1', '电能量类', '属性', '2', '', 'B相正向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0012', 'B相正向有功电能', '1', '电能量类', '属性', '4', '', 'B相正向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0013', 'C相正向有功电能', '1', '电能量类', '属性', '2', '', 'C相正向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0013', 'C相正向有功电能', '1', '电能量类', '属性', '4', '', 'C相正向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0020', '反向有功电能', '1', '电能量类', '属性', '2', '', '反向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0020', '反向有功电能', '1', '电能量类', '属性', '4', '', '反向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0021', 'A相反向有功电能', '1', '电能量类', '属性', '2', '', 'A相反向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0021', 'A相反向有功电能', '1', '电能量类', '属性', '4', '', 'A相反向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0022', 'B相反向有功电能', '1', '电能量类', '属性', '2', '', 'B相反向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0022', 'B相反向有功电能', '1', '电能量类', '属性', '4', '', 'B相反向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0023', 'C相反向有功电能', '1', '电能量类', '属性', '2', '', 'C相反向有功电能:array:double-long-unsigned<kWh|-2>,'),
            ('0023', 'C相反向有功电能', '1', '电能量类', '属性', '4', '', 'C相反向有功电能:array:long64-unsigned<kWh|-4>,'),
            ('0030', '组合无功1电能', '1', '电能量类', '属性', '2', '', '组合无功1电能:array:double-long<kvarh|-2>,'),
            ('0030', '组合无功1电能', '1', '电能量类', '属性', '4', '', '组合无功1电能:array:long64<kvarh|-4>,'),
            ('0031', 'A相组合无功1电能', '1', '电能量类', '属性', '2', '', 'A相组合无功1电能:array:double-long<kvarh|-2>,'),
            ('0031', 'A相组合无功1电能', '1', '电能量类', '属性', '4', '', 'A相组合无功1电能:array:long64<kvarh|-4>,'),
            ('0032', 'B相组合无功1电能', '1', '电能量类', '属性', '2', '', 'B相组合无功1电能:array:double-long<kvarh|-2>,'),
            ('0032', 'B相组合无功1电能', '1', '电能量类', '属性', '4', '', 'B相组合无功1电能:array:long64<kvarh|-4>,'),
            ('0033', 'C相组合无功1电能', '1', '电能量类', '属性', '2', '', 'C相组合无功1电能:array:double-long<kvarh|-2>,'),
            ('0033', 'C相组合无功1电能', '1', '电能量类', '属性', '4', '', 'C相组合无功1电能:array:long64<kvarh|-4>,'),
            ('0040', '组合无功2电能', '1', '电能量类', '属性', '2', '', '组合无功2电能:array:double-long<kvarh|-2>,'),
            ('0040', '组合无功2电能', '1', '电能量类', '属性', '4', '', '组合无功2电能:array:long64<kvarh|-4>,'),
            ('0041', 'A相组合无功2电能', '1', '电能量类', '属性', '2', '', 'A相组合无功2电能:array:double-long<kvarh|-2>,'),
            ('0041', 'A相组合无功2电能', '1', '电能量类', '属性', '4', '', 'A相组合无功2电能:array:long64<kvarh|-4>,'),
            ('0042', 'B相组合无功2电能', '1', '电能量类', '属性', '2', '', 'B相组合无功2电能:array:double-long<kvarh|-2>,'),
            ('0042', 'B相组合无功2电能', '1', '电能量类', '属性', '4', '', 'B相组合无功2电能:array:long64<kvarh|-4>,'),
            ('0043', 'C相组合无功2电能', '1', '电能量类', '属性', '2', '', 'C相组合无功2电能:array:double-long<kvarh|-2>,'),
            ('0043', 'C相组合无功2电能', '1', '电能量类', '属性', '4', '', 'C相组合无功2电能:array:long64<kvarh|-4>,'),
            ('0050', '第一象限无功电能', '1', '电能量类', '属性', '2', '', '第一象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0050', '第一象限无功电能', '1', '电能量类', '属性', '4', '', '第一象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0051', 'A相第一象限无功电能', '1', '电能量类', '属性', '2', '', 'A相第一象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0051', 'A相第一象限无功电能', '1', '电能量类', '属性', '4', '', 'A相第一象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0052', 'B相第一象限无功电能', '1', '电能量类', '属性', '2', '', 'B相第一象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0052', 'B相第一象限无功电能', '1', '电能量类', '属性', '4', '', 'B相第一象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0053', 'C相第一象限无功电能', '1', '电能量类', '属性', '2', '', 'C相第一象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0053', 'C相第一象限无功电能', '1', '电能量类', '属性', '4', '', 'C相第一象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0060', '第二象限无功电能', '1', '电能量类', '属性', '2', '', '第二象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0060', '第二象限无功电能', '1', '电能量类', '属性', '4', '', '第二象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0061', 'A相第二象限无功电能', '1', '电能量类', '属性', '2', '', 'A相第二象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0061', 'A相第二象限无功电能', '1', '电能量类', '属性', '4', '', 'A相第二象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0062', 'B相第二象限无功电能', '1', '电能量类', '属性', '2', '', 'B相第二象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0062', 'B相第二象限无功电能', '1', '电能量类', '属性', '4', '', 'B相第二象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0063', 'C相第二象限无功电能', '1', '电能量类', '属性', '2', '', 'C相第二象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0063', 'C相第二象限无功电能', '1', '电能量类', '属性', '4', '', 'C相第二象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0070', '第三象限无功电能', '1', '电能量类', '属性', '2', '', '第三象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0070', '第三象限无功电能', '1', '电能量类', '属性', '4', '', '第三象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0071', 'A相第三象限无功电能', '1', '电能量类', '属性', '2', '', 'A相第三象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0071', 'A相第三象限无功电能', '1', '电能量类', '属性', '4', '', 'A相第三象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0072', 'B相第三象限无功电能', '1', '电能量类', '属性', '2', '', 'B相第三象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0072', 'B相第三象限无功电能', '1', '电能量类', '属性', '4', '', 'B相第三象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0073', 'C相第三象限无功电能', '1', '电能量类', '属性', '2', '', 'C相第三象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0073', 'C相第三象限无功电能', '1', '电能量类', '属性', '4', '', 'C相第三象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0080', '第四象限无功电能', '1', '电能量类', '属性', '2', '', '第四象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0080', '第四象限无功电能', '1', '电能量类', '属性', '4', '', '第四象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0081', 'A相第四象限无功电能', '1', '电能量类', '属性', '2', '', 'A相第四象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0081', 'A相第四象限无功电能', '1', '电能量类', '属性', '4', '', 'A相第四象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0082', 'B相第四象限无功电能', '1', '电能量类', '属性', '2', '', 'B相第四象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0082', 'B相第四象限无功电能', '1', '电能量类', '属性', '4', '', 'B相第四象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0083', 'C相第四象限无功电能', '1', '电能量类', '属性', '2', '', 'C相第四象限无功电能:array:double-long-unsigned<kvarh|-2>,'),
            ('0083', 'C相第四象限无功电能', '1', '电能量类', '属性', '4', '', 'C相第四象限无功电能:array:long64-unsigned<kvarh|-4>,'),
            ('0090', '正向视在电能', '1', '电能量类', '属性', '2', '', '正向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('0090', '正向视在电能', '1', '电能量类', '属性', '4', '', '正向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('0091', 'A相正向视在电能', '1', '电能量类', '属性', '2', '', 'A相正向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('0091', 'A相正向视在电能', '1', '电能量类', '属性', '4', '', 'A相正向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('0092', 'B相正向视在电能', '1', '电能量类', '属性', '2', '', 'B相正向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('0092', 'B相正向视在电能', '1', '电能量类', '属性', '4', '', 'B相正向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('0093', 'C相正向视在电能', '1', '电能量类', '属性', '2', '', 'C相正向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('0093', 'C相正向视在电能', '1', '电能量类', '属性', '4', '', 'C相正向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('00A0', '反向视在电能', '1', '电能量类', '属性', '2', '', '反向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('00A0', '反向视在电能', '1', '电能量类', '属性', '4', '', '反向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('00A1', 'A相反向视在电能', '1', '电能量类', '属性', '2', '', 'A相反向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('00A1', 'A相反向视在电能', '1', '电能量类', '属性', '4', '', 'A相反向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('00A2', 'B相反向视在电能', '1', '电能量类', '属性', '2', '', 'B相反向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('00A2', 'B相反向视在电能', '1', '电能量类', '属性', '4', '', 'B相反向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('00A3', 'C相反向视在电能', '1', '电能量类', '属性', '2', '', 'C相反向视在电能:array:double-long-unsigned<kVAh|-2>,'),
            ('00A3', 'C相反向视在电能', '1', '电能量类', '属性', '4', '', 'C相反向视在电能:array:long64-unsigned<kVAh|-4>,'),
            ('0110', '正向有功基波总电能', '1', '电能量类', '属性', '2', '', '正向有功基波总电能:array:double-long-unsigned<kWh|-2>,'),
            ('0110', '正向有功基波总电能', '1', '电能量类', '属性', '4', '', '正向有功基波总电能:array:long64-unsigned<kWh|-4>,'),
            ('0111', 'A相正向有功基波电能', '1', '电能量类', '属性', '2', '', 'A相正向有功基波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0111', 'A相正向有功基波电能', '1', '电能量类', '属性', '4', '', 'A相正向有功基波电能:array:long64-unsigned<kWh|-4>,'),
            ('0112', 'B相正向有功基波电能', '1', '电能量类', '属性', '2', '', 'B相正向有功基波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0112', 'B相正向有功基波电能', '1', '电能量类', '属性', '4', '', 'B相正向有功基波电能:array:long64-unsigned<kWh|-4>,'),
            ('0113', 'C相正向有功基波电能', '1', '电能量类', '属性', '2', '', 'C相正向有功基波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0113', 'C相正向有功基波电能', '1', '电能量类', '属性', '4', '', 'C相正向有功基波电能:array:long64-unsigned<kWh|-4>,'),
            ('0120', '反向有功基波总电能', '1', '电能量类', '属性', '2', '', '反向有功基波总电能:array:double-long-unsigned<kWh|-2>,'),
            ('0120', '反向有功基波总电能', '1', '电能量类', '属性', '4', '', '反向有功基波总电能:array:long64-unsigned<kWh|-4>,'),
            ('0121', 'A相反向有功基波电能', '1', '电能量类', '属性', '2', '', 'A相反向有功基波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0121', 'A相反向有功基波电能', '1', '电能量类', '属性', '4', '', 'A相反向有功基波电能:array:long64-unsigned<kWh|-4>,'),
            ('0122', 'B相反向有功基波电能', '1', '电能量类', '属性', '2', '', 'B相反向有功基波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0122', 'B相反向有功基波电能', '1', '电能量类', '属性', '4', '', 'B相反向有功基波电能:array:long64-unsigned<kWh|-4>,'),
            ('0123', 'C相反向有功基波电能', '1', '电能量类', '属性', '2', '', 'C相反向有功基波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0123', 'C相反向有功基波电能', '1', '电能量类', '属性', '4', '', 'C相反向有功基波电能:array:long64-unsigned<kWh|-4>,'),
            ('0210', '正向有功谐波总电能', '1', '电能量类', '属性', '2', '', '正向有功谐波总电能:array:double-long-unsigned<kWh|-2>,'),
            ('0210', '正向有功谐波总电能', '1', '电能量类', '属性', '4', '', '正向有功谐波总电能:array:long64-unsigned<kWh|-4>,'),
            ('0211', 'A相正向有功谐波电能', '1', '电能量类', '属性', '2', '', 'A相正向有功谐波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0211', 'A相正向有功谐波电能', '1', '电能量类', '属性', '4', '', 'A相正向有功谐波电能:array:long64-unsigned<kWh|-4>,'),
            ('0212', 'B相正向有功谐波电能', '1', '电能量类', '属性', '2', '', 'B相正向有功谐波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0212', 'B相正向有功谐波电能', '1', '电能量类', '属性', '4', '', 'B相正向有功谐波电能:array:long64-unsigned<kWh|-4>,'),
            ('0213', 'C相正向有功谐波电能', '1', '电能量类', '属性', '2', '', 'C相正向有功谐波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0213', 'C相正向有功谐波电能', '1', '电能量类', '属性', '4', '', 'C相正向有功谐波电能:array:long64-unsigned<kWh|-4>,'),
            ('0220', '反向有功谐波总电能', '1', '电能量类', '属性', '2', '', '反向有功谐波总电能:array:double-long-unsigned<kWh|-2>,'),
            ('0220', '反向有功谐波总电能', '1', '电能量类', '属性', '4', '', '反向有功谐波总电能:array:long64-unsigned<kWh|-4>,'),
            ('0221', 'A相反向有功谐波电能', '1', '电能量类', '属性', '2', '', 'A相反向有功谐波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0221', 'A相反向有功谐波电能', '1', '电能量类', '属性', '4', '', 'A相反向有功谐波电能:array:long64-unsigned<kWh|-4>,'),
            ('0222', 'B相反向有功谐波电能', '1', '电能量类', '属性', '2', '', 'B相反向有功谐波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0222', 'B相反向有功谐波电能', '1', '电能量类', '属性', '4', '', 'B相反向有功谐波电能:array:long64-unsigned<kWh|-4>,'),
            ('0223', 'C相反向有功谐波电能', '1', '电能量类', '属性', '2', '', 'C相反向有功谐波电能:array:double-long-unsigned<kWh|-2>,'),
            ('0223', 'C相反向有功谐波电能', '1', '电能量类', '属性', '4', '', 'C相反向有功谐波电能:array:long64-unsigned<kWh|-4>,'),
            ('0300', '铜损有功总电能补偿量', '1', '电能量类', '属性', '2', '', '铜损有功总电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0300', '铜损有功总电能补偿量', '1', '电能量类', '属性', '4', '', '铜损有功总电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0301', 'A相铜损有功电能补偿量', '1', '电能量类', '属性', '2', '', 'A相铜损有功电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0301', 'A相铜损有功电能补偿量', '1', '电能量类', '属性', '4', '', 'A相铜损有功电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0302', 'B相铜损有功电能补偿量', '1', '电能量类', '属性', '2', '', 'B相铜损有功电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0302', 'B相铜损有功电能补偿量', '1', '电能量类', '属性', '4', '', 'B相铜损有功电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0303', 'C相铜损有功电能补偿量', '1', '电能量类', '属性', '2', '', 'C相铜损有功电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0303', 'C相铜损有功电能补偿量', '1', '电能量类', '属性', '4', '', 'C相铜损有功电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0400', '铁损有功总电能补偿量', '1', '电能量类', '属性', '2', '', '铁损有功总电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0400', '铁损有功总电能补偿量', '1', '电能量类', '属性', '4', '', '铁损有功总电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0401', 'A相铁损有功电能补偿量', '1', '电能量类', '属性', '2', '', 'A相铁损有功电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0401', 'A相铁损有功电能补偿量', '1', '电能量类', '属性', '4', '', 'A相铁损有功电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0402', 'B相铁损有功电能补偿量', '1', '电能量类', '属性', '2', '', 'B相铁损有功电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0402', 'B相铁损有功电能补偿量', '1', '电能量类', '属性', '4', '', 'B相铁损有功电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0403', 'C相铁损有功电能补偿量', '1', '电能量类', '属性', '2', '', 'C相铁损有功电能补偿量:array:double-long-unsigned<kWh|-2>,'),
            ('0403', 'C相铁损有功电能补偿量', '1', '电能量类', '属性', '4', '', 'C相铁损有功电能补偿量:array:long64-unsigned<kWh|-4>,'),
            ('0500', '关联总电能', '1', '电能量类', '属性', '2', '', '关联总电能:array:double-long-unsigned<kWh|-2>,'),
            ('0500', '关联总电能', '1', '电能量类', '属性', '4', '', '关联总电能:array:long64-unsigned<kWh|-4>,'),
            ('0501', 'A相关联电能', '1', '电能量类', '属性', '2', '', 'A相关联电能:array:double-long-unsigned<kWh|-2>,'),
            ('0501', 'A相关联电能', '1', '电能量类', '属性', '4', '', 'A相关联电能:array:long64-unsigned<kWh|-4>,'),
            ('0502', 'B相关联电能', '1', '电能量类', '属性', '2', '', 'B相关联电能:array:double-long-unsigned<kWh|-2>,'),
            ('0502', 'B相关联电能', '1', '电能量类', '属性', '4', '', 'B相关联电能:array:long64-unsigned<kWh|-4>,'),
            ('0503', 'C相关联电能', '1', '电能量类', '属性', '2', '', 'C相关联电能:array:double-long-unsigned<kWh|-2>,'),
            ('0503', 'C相关联电能', '1', '电能量类', '属性', '4', '', 'C相关联电能:array:long64-unsigned<kWh|-4>,'),
            ('1010', '正向有功最大需量', '2', '最大需量类', '属性', '2', '', '正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1011', 'A相正向有功最大需量', '2', '最大需量类', '属性', '2', '', 'A相正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1012', 'B相正向有功最大需量', '2', '最大需量类', '属性', '2', '', 'B相正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1013', 'C相正向有功最大需量', '2', '最大需量类', '属性', '2', '', 'C相正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1020', '反向有功最大需量', '2', '最大需量类', '属性', '2', '', '反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1021', 'A相反向有功最大需量', '2', '最大需量类', '属性', '2', '', 'A相反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1022', 'B相反向有功最大需量', '2', '最大需量类', '属性', '2', '', 'B相反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1023', 'C相反向有功最大需量', '2', '最大需量类', '属性', '2', '', 'C相反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1030', '组合无功1最大需量', '2', '最大需量类', '属性', '2', '', '组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1031', 'A相组合无功1最大需量', '2', '最大需量类', '属性', '2', '', 'A相组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1032', 'B相组合无功1最大需量', '2', '最大需量类', '属性', '2', '', 'B相组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1033', 'C相组合无功1最大需量', '2', '最大需量类', '属性', '2', '', 'C相组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1040', '组合无功2最大需量', '2', '最大需量类', '属性', '2', '', '组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1041', 'A相组合无功2最大需量', '2', '最大需量类', '属性', '2', '', 'A相组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1042', 'B相组合无功2最大需量', '2', '最大需量类', '属性', '2', '', 'B相组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1043', 'C相组合无功2最大需量', '2', '最大需量类', '属性', '2', '', 'C相组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1050', '第一象限最大需量', '2', '最大需量类', '属性', '2', '', '第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1051', 'A相第一象限最大需量', '2', '最大需量类', '属性', '2', '', 'A相第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1052', 'B相第一象限最大需量', '2', '最大需量类', '属性', '2', '', 'B相第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1053', 'C相第一象限最大需量', '2', '最大需量类', '属性', '2', '', 'C相第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1060', '第二象限最大需量', '2', '最大需量类', '属性', '2', '', '第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1061', 'A相第二象限最大需量', '2', '最大需量类', '属性', '2', '', 'A相第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1062', 'B相第二象限最大需量', '2', '最大需量类', '属性', '2', '', 'B相第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1063', 'C相第二象限最大需量', '2', '最大需量类', '属性', '2', '', 'C相第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1070', '第三象限最大需量', '2', '最大需量类', '属性', '2', '', '第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1071', 'A相第三象限最大需量', '2', '最大需量类', '属性', '2', '', 'A相第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1072', 'B相第三象限最大需量', '2', '最大需量类', '属性', '2', '', 'B相第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1073', 'C相第三象限最大需量', '2', '最大需量类', '属性', '2', '', 'C相第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1080', '第四象限最大需量', '2', '最大需量类', '属性', '2', '', '第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1081', 'A相第四象限最大需量', '2', '最大需量类', '属性', '2', '', 'A相第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1082', 'B相第四象限最大需量', '2', '最大需量类', '属性', '2', '', 'B相第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1083', 'C相第四象限最大需量', '2', '最大需量类', '属性', '2', '', 'C相第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1090', '正向视在最大需量', '2', '最大需量类', '属性', '2', '', '正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('1091', 'A相正向视在最大需量', '2', '最大需量类', '属性', '2', '', 'A相正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('1092', 'B相正向视在最大需量', '2', '最大需量类', '属性', '2', '', 'B相正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('1093', 'C相正向视在最大需量', '2', '最大需量类', '属性', '2', '', 'C相正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('10A0', '反向视在最大需量', '2', '最大需量类', '属性', '2', '', '反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('10A1', 'A相反向视在最大需量', '2', '最大需量类', '属性', '2', '', 'A相反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('10A2', 'B相反向视在最大需量', '2', '最大需量类', '属性', '2', '', 'B相反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('10A3', 'C相反向视在最大需量', '2', '最大需量类', '属性', '2', '', 'C相反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('1110', '冻结周期内正向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1111', '冻结周期内A相正向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1112', '冻结周期内B相正向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1113', '冻结周期内C相正向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相正向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1120', '冻结周期内反向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1121', '冻结周期内A相反向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1122', '冻结周期内B相反向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1123', '冻结周期内C相反向有功最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相反向有功最大需量:array:structure{最大需量值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('1130', '冻结周期内组合无功1最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1131', '冻结周期内A相组合无功1最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1132', '冻结周期内B相组合无功1最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1133', '冻结周期内冻结周期内C相组合无功1最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内冻结周期内C相组合无功1最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1140', '冻结周期内组合无功2最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1141', '冻结周期内A相组合无功2最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1142', '冻结周期内B相组合无功2最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1143', '冻结周期内C相组合无功2最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相组合无功2最大需量:array:structure{最大需量值:double-long<kvar|-4>,发生时间:date_time_s},'),
            ('1150', '冻结周期内第一象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1151', '冻结周期内A相第一象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1152', '冻结周期内B相第一象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1153', '冻结周期内C相第一象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相第一象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1160', '冻结周期内第二象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1161', '冻结周期内A相第二象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1162', '冻结周期内B相第二象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1163', '冻结周期内C相第二象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相第二象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1170', '冻结周期内第三象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1171', '冻结周期内A相第三象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1172', '冻结周期内B相第三象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1173', '冻结周期内C相第三象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相第三象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1180', '冻结周期内第四象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1181', '冻结周期内A相第四象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1182', '冻结周期内B相第四象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1183', '冻结周期内C相第四象限最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相第四象限最大需量:array:structure{最大需量值:double-long-unsigned<kvar|-4>,发生时间:date_time_s},'),
            ('1190', '冻结周期内正向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('1191', '冻结周期内A相正向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('1192', '冻结周期内B相正向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('1193', '冻结周期内冻结周期内C相正向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内冻结周期内C相正向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('11A0', '冻结周期内反向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('11A1', '冻结周期内A相反向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内A相反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('11A2', '冻结周期内B相反向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内B相反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('11A3', '冻结周期内C相反向视在最大需量', '2', '最大需量类', '属性', '2', '', '冻结周期内C相反向视在最大需量:array:structure{最大需量值:double-long-unsigned<kVA|-4>,发生时间:date_time_s},'),
            ('2000', '电压', '3', '变量类', '属性', '2', '', '电压:array:long-unsigned<V|-1>,'),
            ('2001', '电流', '3', '变量类', '属性', '2', '', '电流:array:double-long<A|-3>,'),
            ('2001', '电流', '3', '变量类', '属性', '4', '零线电流', '零线电流:double-long<A|-3>,'),
            ('2002', '电压相角', '3', '变量类', '属性', '2', '', '电压相角:array:long-unsigned<度|-1>,'),
            ('2003', '电压电流相角', '3', '变量类', '属性', '2', '', '电压电流相角:array:long-unsigned<度|-1>,'),
            ('2004', '有功功率', '4', '变量类', '属性', '2', '', '有功功率:array:double-long<W|-1>,'),
            ('2005', '无功功率', '4', '变量类', '属性', '2', '', '无功功率:array:double-long<var|-1>,'),
            ('2006', '视在功率', '4', '变量类', '属性', '2', '', '视在功率:array:double-long<VA|-1>,'),
            ('2007', '一分钟平均有功功率', '4', '变量类', '属性', '2', '', '一分钟平均有功功率:array:double-long<W|-1>,'),
            ('2008', '一分钟平均无功功率', '4', '变量类', '属性', '2', '', '一分钟平均无功功率:array:double-long<var|-1>,'),
            ('2009', '一分钟平均视在功率', '4', '变量类', '属性', '2', '', '一分钟平均视在功率:array:double-long<VA|-1>,'),
            ('200A', '功率因数', '4', '变量类', '属性', '2', '', '功率因数:array:long<|-3>,'),
            ('200B', '电压波形失真度', '3', '变量类', '属性', '2', '', '电压波形失真度:array:long<%|-2>,'),
            ('200C', '电流波形失真度', '3', '变量类', '属性', '2', '', '电流波形失真度:array:long<%|-2>,'),
            ('200D', '电压谐波含有量（总及2…n次）', '5', '变量类', '属性', '2', '', '电压谐波含有量（总及2…n次）:array:long<%|-2>,'),
            ('200E', '电流谐波含有量（总及2…n次）', '5', '变量类', '属性', '2', '', '电流谐波含有量（总及2…n次）:array:long<%|-2>,'),
            ('200F', '电网频率', '6', '变量类', '属性', '2', '', '电网频率:long-unsigned<Hz|-2>,'),
            ('2010', '表内温度', '6', '变量类', '属性', '2', '', '表内温度:long<℃|-1>,'),
            ('2011', '时钟电池电压', '6', '变量类', '属性', '2', '', '时钟电池电压:long-unsigned<V|-2>,'),
            ('2012', '停电抄表电池电压', '6', '变量类', '属性', '2', '', '停电抄表电池电压:long-unsigned<V|-2>,'),
            ('2013', '时钟电池工作时间', '6', '变量类', '属性', '2', '', '时钟电池工作时间:double-long-unsigned<分钟|0>,'),
            ('2014', '电能表运行状态字', '6', '变量类', '属性', '2', '', '电能表运行状态字:array:bit-string,'),
            ('2017', '当前有功需量', '6', '变量类', '属性', '2', '', '当前有功需量:double-long<kW|-4>,'),
            ('2018', '当前无功需量', '6', '变量类', '属性', '2', '', '当前无功需量:double-long<kvar|-4>,'),
            ('2019', '当前视在需量', '6', '变量类', '属性', '2', '', '当前视在需量:double-long<kVA|-4>,'),
            ('201A', '当前电价', '6', '变量类', '属性', '2', '', '当前电价:double-long-unsigned<元/kWh|-4>,'),
            ('201B', '当前费率电价', '6', '变量类', '属性', '2', '', '当前费率电价:double-long-unsigned<元/kWh|-4>,'),
            ('201C', '当前阶梯电价', '6', '变量类', '属性', '2', '', '当前阶梯电价:double-long-unsigned<元/kWh|-4>,'),
            ('201E', '事件发生时间', '8', '变量类', '属性', '2', '', '事件发生时间:date_time_s,'),
            ('2020', '事件结束时间', '8', '变量类', '属性', '2', '', '事件结束时间:date_time_s,'),
            ('2021', '数据冻结时间', '8', '变量类', '属性', '2', '', '数据冻结时间:date_time_s,'),
            ('2022', '事件记录序号', '8', '变量类', '属性', '2', '', '事件记录序号:double-long-unsigned,'),
            ('2023', '冻结记录序号', '8', '变量类', '属性', '2', '', '冻结记录序号:double-long-unsigned,'),
            ('2024', '事件发生源', '8', '变量类', '属性', '2', '', ''),
            ('2025', '事件当前值', '8', '变量类', '属性', '2', '', '事件当前值:structure{事件发生次数:double-long-unsigned,事件累计时间:double-long-unsigned<秒|0>},'),
            ('2026', '电压不平衡率', '6', '变量类', '属性', '2', '', '电压不平衡率:long-unsigned<%|-2>,'),
            ('2027', '电流不平衡率', '6', '变量类', '属性', '2', '', '电流不平衡率:long-unsigned<%|-2>,'),
            ('2028', '负载率', '6', '变量类', '属性', '2', '', '负载率:long-unsigned<%|-2>,'),
            ('2029', '安时值', '6', '变量类', '属性', '2', '安时数值', '安时数值:array:相安时值:double-long-unsigned<Ah|-2>,'),
            ('202A', '目标服务器地址', '8', '变量类', '属性', '2', '', '目标服务器地址:TSA,'),
            ('202C', '（当前）钱包文件', '8', '变量类', '属性', '2', '', '（当前）钱包文件:structure{剩余金额:double-long-unsigned<元|-2>,购电次数:double-long-unsigned},'),
            ('202D', '（当前）透支金额', '6', '变量类', '属性', '2', '', '（当前）透支金额:double-long-unsigned<元|-2>,'),
            ('202E', '累计购电金额', '6', '变量类', '属性', '2', '', '累计购电金额:double-long-unsigned<元|-2>,'),
            ('2031', '月度用电量', '6', '变量类', '属性', '2', '用电量', '用电量:double-long-unsigned<kWh|-2>,'),
            ('2032', '阶梯结算用电量', '6', '变量类', '属性', '2', '用电量', '用电量:double-long-unsigned<kWh|-2>,'),
            ('2040', '控制命令执行状态字', '6', '变量类', '属性', '2', '', '控制命令执行状态字:bit-string(SIZE(16)),'),
            ('2041', '控制命令错误状态字', '6', '变量类', '属性', '2', '', '控制命令错误状态字:bit-string(SIZE(16)),'),
            ('2100', '分钟区间统计', '14', '变量类', '属性', '0', '', ''),
            ('2101', '小时区间统计', '14', '变量类', '属性', '0', '', ''),
            ('2102', '日区间统计', '14', '变量类', '属性', '0', '', ''),
            ('2103', '月区间统计', '14', '变量类', '属性', '0', '', ''),
            ('2104', '年区间统计', '14', '变量类', '属性', '0', '', ''),
            ('2110', '分钟平均', '15', '变量类', '属性', '0', '', ''),
            ('2111', '小时平均', '15', '变量类', '属性', '0', '', ''),
            ('2112', '日平均', '15', '变量类', '属性', '0', '', ''),
            ('2113', '月平均', '15', '变量类', '属性', '0', '', ''),
            ('2114', '年平均', '15', '变量类', '属性', '0', '', ''),
            ('2120', '分钟极值', '16', '变量类', '属性', '0', '', ''),
            ('2121', '小时极值', '16', '变量类', '属性', '0', '', ''),
            ('2122', '日极值', '16', '变量类', '属性', '0', '', ''),
            ('2123', '月极值', '16', '变量类', '属性', '0', '', ''),
            ('2124', '年极值', '16', '变量类', '属性', '0', '', ''),
            ('2130', '总电压合格率', '6', '变量类', '属性', '2', '电压合格率数据', '电压合格率数据:structure{当日电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}|当月电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}},'),
            ('2131', '当月A相电压合格率', '6', '变量类', '属性', '2', '电压合格率数据', '电压合格率数据:structure{当日电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}|当月电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}},'),
            ('2132', '当月B相电压合格率', '6', '变量类', '属性', '2', '电压合格率数据', '电压合格率数据:structure{当日电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}|当月电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}},'),
            ('2133', '当月C相电压合格率', '6', '变量类', '属性', '2', '电压合格率数据', '电压合格率数据:structure{当日电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}|当月电压合格率电压合格率:structure{电压监测时间:double-long-unsigned<分钟|0>,电压合格率:long-unsigned<%|-2>,电压超限率:long-unsigned<%|-2>,电压超上限时间:double-long-unsigned<分钟|0>,电压超下限时间:double-long-unsigned<分钟|0>}},'),
            ('2140', '日最大有功功率及发生时间', '2', '变量类', '属性', '2', '', '日最大有功功率及发生时间:array:structure{最大功率值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('2141', '月最大有功功率及发生时间', '2', '变量类', '属性', '2', '', '月最大有功功率及发生时间:array:structure{最大功率值:double-long-unsigned<kW|-4>,发生时间:date_time_s},'),
            ('2200', '通信流量', '6', '变量类', '属性', '2', '', '通信流量:structure{当日通信流量:double-long-unsigned<Byte|0>,当月通信流量:double-long-unsigned<Byte|0>},'),
            ('2203', '供电时间', '6', '变量类', '属性', '2', '', '供电时间:structure{日供电累计时间:double-long-unsigned<分钟|0>,月供电累计时间:double-long-unsigned<分钟|0>},'),
            ('2204', '复位次数', '6', '变量类', '属性', '2', '', '复位次数:structure{日复位累计次数:long-unsigned,月复位累计次数:long-unsigned},'),
            ('2301', '总加组1', '23', '变量类', '属性', '0', '', ''),
            ('2302', '总加组2', '23', '变量类', '属性', '0', '', ''),
            ('2303', '总加组3', '23', '变量类', '属性', '0', '', ''),
            ('2304', '总加组4', '23', '变量类', '属性', '0', '', ''),
            ('2305', '总加组5', '23', '变量类', '属性', '0', '', ''),
            ('2306', '总加组6', '23', '变量类', '属性', '0', '', ''),
            ('2307', '总加组7', '23', '变量类', '属性', '0', '', ''),
            ('2308', '总加组8', '23', '变量类', '属性', '0', '', ''),
            ('2401', '脉冲计量1', '12', '变量类', '属性', '0', '', ''),
            ('2402', '脉冲计量2', '12', '变量类', '属性', '0', '', ''),
            ('2403', '脉冲计量3', '12', '变量类', '属性', '0', '', ''),
            ('2404', '脉冲计量4', '12', '变量类', '属性', '0', '', ''),
            ('2405', '脉冲计量5', '12', '变量类', '属性', '0', '', ''),
            ('2406', '脉冲计量6', '12', '变量类', '属性', '0', '', ''),
            ('2407', '脉冲计量7', '12', '变量类', '属性', '0', '', ''),
            ('2408', '脉冲计量8', '12', '变量类', '属性', '0', '', ''),
            ('2500', '累计水（热）流量', '6', '变量类', '属性', '2', '', '累计水（热）流量:double-long-unsigned<m3|-4>,'),
            ('2501', '累计气流量', '6', '变量类', '属性', '2', '', '累计气流量:double-long-unsigned<m3|-4>,'),
            ('2502', '累计热量', '6', '变量类', '属性', '2', '', '累计热量:double-long-unsigned<J|-2>,'),
            ('2503', '热功率', '6', '变量类', '属性', '2', '', '热功率:double-long-unsigned<J/h|-2>,'),
            ('2504', '累计工作时间', '6', '变量类', '属性', '2', '', '累计工作时间:double-long-unsigned<小时|0>,'),
            ('2505', '水温', '6', '变量类', '属性', '2', '', '水温:structure{供水温度:double-long-unsigned<℃|-2>,回水温度:double-long-unsigned<℃|-2>},'),
            ('2506', '（仪表）状态ST', '6', '变量类', '属性', '2', '', '（仪表）状态ST:structure{阀门状态:enum[开<0>,关<1>,保留<2>,异常<3>],电池电压:enum[正常<0>,欠压<0>]},'),
            ('3000', '电能表失压事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{电压触发上限:long-unsigned<V|-1>,电压恢复下限:long-unsigned<V|-1>,电流触发下限:double-long<A|-4>,判定延时时间:unsigned<s|0>},'),
            ('3000', '电能表失压事件', '24', '事件类', '属性', '13', '失压统计', '失压统计:structure{事件发生总次数:double-long-unsigned,事件总累计时间:double-long-unsigned<秒|0>,最近一次失压发生时间:date_time_s,最近一次失压结束时间:date_time_s},'),
            ('3001', '电能表欠压事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{电压触发上限:long-unsigned<V|-1>,判定延时时间:unsigned<s|0>},'),
            ('3002', '电能表过压事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{电压触发下限:long-unsigned<V|-1>,判定延时时间:unsigned<s|0>},'),
            ('3003', '电能表断相事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{电压触发上限:long-unsigned<V|-1>,电流触发上限:double-long<A|-4>,判定延时时间:unsigned<s|0>},'),
            ('3004', '电能表失流事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{电压触发下限:long-unsigned<V|-1>,电流触发上限:double-long<A|-4>,电流触发下限:double-long<A|-4>,判定延时时间:unsigned<s|0>},'),
            ('3005', '电能表过流事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{电流触发下限:double-long<A|-4>,判定延时时间:unsigned<s|0>},'),
            ('3006', '电能表断流事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{电压触发下限:long-unsigned<V|-1>,电流触发上限:double-long<A|-4>,判定延时时间:unsigned<s|0>},'),
            ('3007', '电能表功率反向事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{有功功率触发下限:double-long<W|-1>,判定延时时间:unsigned<s|0>},'),
            ('3008', '电能表过载事件', '24', '事件类', '属性', '2', '', '电能表过载事件:structure{有功功率触发下限:double-long<W|-1>,判定延时时间:unsigned<s|0>},'),
            ('3009', '电能表正向有功需量超限事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},超限期间需量最大值:double-long-unsigned,超限期间正向有功需量最大值:double-long-unsigned,超限期间需量最大值发生时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3009', '电能表正向有功需量超限事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{触发下限:double-long-unsigned<kW|-4>,判定延时时间:unsigned<s|0>},'),
            ('300A', '电能表反向有功需量超限事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},超限期间需量最大值:double-long-unsigned,超限期间正向有功需量最大值:double-long-unsigned,超限期间需量最大值发生时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300A', '电能表反向有功需量超限事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{触发下限:double-long-unsigned<kW|-4>,判定延时时间:unsigned<s|0>},'),
            ('300B', '电能表无功需量超限事件', '24', '事件类', '属性', '5', '配置参数', '配置参数:structure{触发下限:double-long-unsigned<kvar|-4>,判定延时时间:unsigned<s|0>},'),
            ('300B', '电能表无功需量超限事件', '24', '事件类', '属性', '6', '事件记录表 1', '事件记录表 1:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},超限期间需量最大值:double-long-unsigned,超限期间正向有功需量最大值:double-long-unsigned,超限期间需量最大值发生时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300B', '电能表无功需量超限事件', '24', '事件类', '属性', '7', '事件记录表 2', '事件记录表 2:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},超限期间需量最大值:double-long-unsigned,超限期间正向有功需量最大值:double-long-unsigned,超限期间需量最大值发生时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300B', '电能表无功需量超限事件', '24', '事件类', '属性', '8', '事件记录表 3', '事件记录表 3:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},超限期间需量最大值:double-long-unsigned,超限期间正向有功需量最大值:double-long-unsigned,超限期间需量最大值发生时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300B', '电能表无功需量超限事件', '24', '事件类', '属性', '9', '事件记录表 4', '事件记录表 4:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},超限期间需量最大值:double-long-unsigned,超限期间正向有功需量最大值:double-long-unsigned,超限期间需量最大值发生时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300C', '电能表功率因数超下限事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300C', '电能表功率因数超下限事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{下限阀值:long<%|-1>,判定延时时间:unsigned<s|0>},'),
            ('300D', '电能表全失压事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300D', '电能表全失压事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('300E', '电能表辅助电源掉电事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300E', '电能表辅助电源掉电事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('300F', '电能表电压逆相序事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('300F', '电能表电压逆相序事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('3010', '电能表电流逆相序事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3010', '电能表电流逆相序事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('3011', '电能表掉电事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3011', '电能表掉电事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('3012', '电能表编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},编程对象列表:array:OAD,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3012', '电能表编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3013', '电能表清零事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3013', '电能表清零事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3014', '电能表需量清零事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3014', '电能表需量清零事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3015', '电能表事件清零事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},事件清零列表:array:OMD},'),
            ('3015', '电能表事件清零事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3016', '电能表校时事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3016', '电能表校时事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3017', '电能表时段表编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},编程时段表对象:OAD,编程前时段表内容:array:structure{时:unsigned,分:unsigned,费率号:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3017', '电能表时段表编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3018', '电能表时区表编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3018', '电能表时区表编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3019', '电能表周休日编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3019', '电能表周休日编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('301A', '电能表结算日编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('301A', '电能表结算日编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('301B', '电能表开盖事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('301B', '电能表开盖事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('301C', '电能表开端钮盒事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('301C', '电能表开端钮盒事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('301D', '电能表电压不平衡事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('301D', '电能表电压不平衡事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{限值:long<%|-2>,判定延时时间:unsigned<s|0>},'),
            ('301E', '电能表电流不平衡事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('301E', '电能表电流不平衡事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{限值:long<%|-2>,判定延时时间:unsigned<s|0>},'),
            ('301F', '电能表跳闸事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('301F', '电能表跳闸事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3020', '电能表合闸事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3020', '电能表合闸事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3021', '电能表节假日编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3021', '电能表节假日编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3022', '电能表有功组合方式编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3022', '电能表有功组合方式编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3023', '电能表无功组合方式编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 节假日编程事件记录单元,'),
            ('3023', '电能表无功组合方式编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{}事件发生源∷=:enum[无功组合方式1特征字<0>,无功组合方式2特征字<1>],'),
            ('3024', '电能表费率参数表编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3024', '电能表费率参数表编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3025', '电能表阶梯表编程事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3025', '电能表阶梯表编程事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3026', '电能表密钥更新事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3026', '电能表密钥更新事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3027', '电能表异常插卡事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 电能表异常插卡记录单元,'),
            ('3027', '电能表异常插卡事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3027', '电能表异常插卡事件', '7', '事件类', '属性', '10', '非法插卡总次数', '非法插卡总次数:double-long-unsigned,'),
            ('3028', '电能表购电记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3028', '电能表购电记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3029', '电能表退费记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 电能表,'),
            ('3029', '电能表退费记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('302A', '电能表恒定磁场干扰事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('302A', '电能表恒定磁场干扰事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('302B', '电能表负荷开关误动作事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('302B', '电能表负荷开关误动作事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('302C', '电能表电源异常事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('302C', '电能表电源异常事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('302D', '电能表电流严重不平衡事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('302D', '电能表电流严重不平衡事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{限值:long<%|-2>判定延时时间:unsigned<s|0>},'),
            ('302E', '电能表时钟故障事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('302E', '电能表时钟故障事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('302F', '电能表计量芯片故障事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('302F', '电能表计量芯片故障事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('3030', '通信模块变更事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OAD,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},模块对应的通信地址:octet-string,变更前的模块描述符:visible-string,变更后的模块描述符:visible-string},'),
            ('3030', '通信模块变更事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时:unsigned<s|0>},'),
            ('3100', '终端初始化事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3100', '终端初始化事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3101', '终端版本变更事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3101', '终端版本变更事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3104', '终端状态量变位事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3104', '终端状态量变位事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3105', '电能表时钟超差事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:TSA,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},电能表时钟DATE:TIME_S,终端当前时钟DATE:TIME_S,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3105', '电能表时钟超差事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{异常判别阈值:long-unsigned<秒|0>,关联采集任务号:unsigned},'),
            ('3106', '终端停/上电事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:enum[停电(0),上电(1)],事件上报状态:array:structure{通道:OAD,上报状态:unsigned},属性标志:bit-string<SIZE(8)>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3106', '终端停/上电事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{停电数据采集配置参数:structure{采集标志:bit-string(SIZE(8)),停电事件抄读时间间隔<小时>:unsigned,停电事件抄读时间限值<分钟>:unsigned,需要读取停电事件电能表:array:TSA},停电事件甄别限值参数:structure{停电时间最小有效间隔<分钟>:long-unsigned,停电时间最大有效间隔<分钟>:long-unsigned,停电事件起止时间偏差限值<分钟>:long-unsigned,停电事件时间区段偏差限值<分钟>:long-unsigned,停电发生电压限值:long-unsigned<V|-1>,停电恢复电压限值:long-unsigned<V|-1>}},'),
            ('3107', '终端直流模拟量越上限事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3107', '终端直流模拟量越上限事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{直流模拟量上限:double-long},'),
            ('3108', '终端直流模拟量越下限事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3108', '终端直流模拟量越下限事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{直流模拟量下限:double-long},'),
            ('3109', '终端消息认证错误事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3109', '终端消息认证错误事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('310A', '设备故障记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('310A', '设备故障记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{}事件发生源∷=:enum[终端主板内存故障<0>,时钟故障<1>,主板通信故障<2>,485抄表故障<3>,显示板故障<4>,载波通道异常<5>,内卡初始化错误<6>,ESAM错误<7>],'),
            ('310B', '电能表示度下降事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('310B', '电能表示度下降事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{关联采集任务号:unsigned},'),
            ('310C', '电能量超差事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('310C', '电能量超差事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{阈值:double-long-unsigned<%|0>,关联采集任务号:unsigned},'),
            ('310D', '电能表飞走事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('310D', '电能表飞走事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{阈值:double-long-unsigned<%|0>,关联采集任务号:unsigned},'),
            ('310E', '电能表停走事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('310E', '电能表停走事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{阈值:TI,关联采集任务号:unsigned},'),
            ('310F', '终端抄表失败事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('310F', '终端抄表失败事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{重试轮次:unsigned,关联采集任务号:unsigned},'),
            ('3110', '月通信流量超限事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3110', '月通信流量超限事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{通信流量门限:double-long-unsigned<byte|0>},'),
            ('3111', '发现未知电能表事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},搜表结果:array一个搜表结果,},'),
            ('3111', '发现未知电能表事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3112', '跨台区电能表事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 垮台区电能表事件单元,'),
            ('3112', '跨台区电能表事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3114', '终端对时事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3114', '终端对时事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3115', '遥控跳闸记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OAD,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},控后2分钟总加组功率:array:long64,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3115', '遥控跳闸记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3116', '有功总电能量差动越限事件记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 差动越限,'),
            ('3116', '有功总电能量差动越限事件记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:array:structure{有功总电能量差动组序号:unsigned,对比的总加组:OI,参照的总加组:OI,参与差动的电能量的时间区间及对比方法标志:unsigned,差动越限相对偏差值:integer<%|0>,差动越限绝对偏差值:long64<kWh|-4>},'),
            ('3117', '输出回路接入状态变位事件记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3117', '输出回路接入状态变位事件记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3118', '终端编程记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},编程对象列表:array:OAD,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3118', '终端编程记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3119', '终端电流回路异常事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3119', '终端电流回路异常事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{}事件发生源∷=:enum[短路(0),开路(1)],'),
            ('311A', '电能表在网状态切换事件', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},状态变迁事件:array:structure{电能表地址:TSA,在网状态:bool}},'),
            ('311A', '电能表在网状态切换事件', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{判定延时时间long-:unsigned<s|0>},'),
            ('311B', '终端对电表校时记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 终端对电表校时记录,'),
            ('311B', '终端对电表校时记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('311C', '电能表数据变更监控记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 电能表数据变更监控记录,'),
            ('311C', '电能表数据变更监控记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{关联采集任务序号:unsigned},'),
            ('3200', '功控跳闸记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OI,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},事件发生后2分钟功率:long64(W,-1),控制对象:OI,跳闸轮次:bit-string(SIZE(8)),功控定值:long64<kWh|-4>,跳闸发生前总加有功功率:long64<kW|-4>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3200', '功控跳闸记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3201', '电控跳闸记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array 电控跳闸记录,'),
            ('3201', '电控跳闸记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3202', '购电参数设置记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3202', '购电参数设置记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3203', '电控告警事件记录', '7', '事件类', '属性', '2', '事件记录表', '事件记录表:array:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OI,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},控制对象:OI,电控定值:long64<kWh|-4>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3203', '电控告警事件记录', '7', '事件类', '属性', '6', '配置参数', '配置参数:structure{},'),
            ('3300', '通道上报状态', '8', '事件类', '属性', '2', '', '通道上报状态:array:structure{通道:OAD,上报状态:unsigned},'),
            ('3301', '标准事件记录单元', '8', '事件类', '属性', '2', '', '标准事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:instance-specific,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3302', '编程记录事件单元', '8', '事件类', '属性', '2', '', '编程记录事件单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},编程对象列表:array:OAD,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3303', '发现未知电能表事件单元', '8', '事件类', '属性', '2', '', '发现未知电能表事件单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},搜表结果:array一个搜表结果,},'),
            ('3304', '跨台区电能表事件单元', '8', '事件类', '属性', '2', '', '跨台区电能表事件单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},跨台区搜表结果:array一个跨台区结果,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3305', '功控跳闸记录单元', '8', '事件类', '属性', '2', '', '功控跳闸记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OI,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},事件发生后2分钟功率:long64(W,-1),控制对象:OI,跳闸轮次:bit-string(SIZE(8)),功控定值:long64<kWh|-4>,跳闸发生前总加有功功率:long64<kW|-4>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3306', '电控跳闸记录单元', '8', '事件类', '属性', '2', '', '电控跳闸记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OI,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},控制对象:OI,跳闸轮次:bit-string(SIZE(8)),电控定值:long64<kWh|-4>,跳闸发生时总加电能量:long64<kwh/元|-4>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3307', '电控告警事件单元', '8', '事件类', '属性', '2', '', '电控告警事件单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OI,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},控制对象:OI,电控定值:long64<kWh|-4>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3308', '电能表需量超限事件单元', '8', '事件类', '属性', '2', '', '电能表需量超限事件单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},超限期间需量最大值:double-long-unsigned,超限期间正向有功需量最大值:double-long-unsigned,超限期间需量最大值发生时间:date_time_s,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3309', '停/上电事件记录单元', '8', '事件类', '属性', '2', '', '停/上电事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:enum[停电<0>,上电<1>],事件上报状态:array:structure{通道:OAD,上报状态:unsigned},属性标志:bit-string<SIZE(8)>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('330A', '遥控事件记录单元', '8', '事件类', '属性', '2', '', '遥控事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OAD,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},控后2分钟总加组功率:array:long64,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('330B', '有功总电能量差动越限事件记录单元', '8', '事件类', '属性', '2', '', '有功总电能量差动越限事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:unsigned,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},越限时对比总加组有功总电能量:long64<kWh|-4>,越限时参照总加组有功总电能量:long64<kWh|-4>,越限时差动越限相对偏差值:integer<%|0>,越限时差动越限绝对偏差值:long64<kWh|-4>},'),
            ('330C', '事件清零事件记录单元', '8', '事件类', '属性', '2', '', '事件清零事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},事件清零列表:array:OMD},'),
            ('330D', '终端对电表校时记录单元', '8', '事件类', '属性', '2', '', '终端对电表校时记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:TSA,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},校时前时钟:date_time_s,时钟误差:integer<秒|0>},'),
            ('330E', '电能表在网状态切换事件单元', '8', '事件类', '属性', '2', '', '电能表在网状态切换事件单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},状态变迁事件:array:structure{电能表地址:TSA,在网状态:bool}},'),
            ('330F', '电能表数据变更监控记录单元', '8', '事件类', '属性', '2', '', '电能表数据变更监控记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:TSA,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},监控数据对象:CSD,变化前数据:Data,变化后数据:Data},'),
            ('3310', '异常插卡事件记录单元', '8', '事件类', '属性', '2', '', '异常插卡事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},卡序列号:octet-string,插卡错误信息字:unsigned,插卡操作命令头:octet-string,插卡错误响应状态:long-unsigned,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3311', '退费事件记录单元', '8', '事件类', '属性', '2', '', '退费事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},退费金额:double-long-unsigned<元|-2>,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3312', '通信模块变更事件单元', '8', '事件类', '属性', '2', '通信模块变更事件单元', '通信模块变更事件单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:OAD,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},模块对应的通信地址:octet-string,变更前的模块描述符:visible-string,变更后的模块描述符:visible-string},'),
            ('3313', '电能表时钟超差记录单元', '8', '事件类', '属性', '2', '', '电能表时钟超差记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:TSA,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},电能表时钟DATE:TIME_S,终端当前时钟DATE:TIME_S,第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3314', '电能表时段表编程事件', '8', '事件类', '属性', '2', '', '电能表时段表编程事件:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},编程时段表对象:OAD,编程前时段表内容:array:structure{时:unsigned,分:unsigned,费率号:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data},'),
            ('3315', '电能表节假日编程事件记录单元', '8', '事件类', '属性', '2', '', '电能表节假日编程事件记录单元:structure{事件记录序号:double-long-unsigned,事件发生时间:date_time_s,事件结束时间:date_time_s,事件发生源:NULL,事件上报状态:array:structure{通道:OAD,上报状态:unsigned},编程节假日对象:OAD,编程前节假日内容:structure{日期:date,日时段表号:unsigned},第1个关联对象属性的数据:Data,…第n个关联对象属性的数据:Data}'),
            ('3320', '新增事件列表', '8', '事件类', '属性', '2', '', '新增事件列表:array:structure{事件对象属性:OAD,上报标志BOOELAN},'),
            ('3320', '新增事件列表', '8', '事件类', '属性', '2', '新增事件列表', ''),
            ('3320', '新增事件列表', '8', '事件类', '属性', '3', '需上报事件对象列表，', ''),
            ('4000', '日期时间', '8', '参变量类', '属性', '2', '', '日期时间:date_time_s,'),
            ('4000', '日期时间', '8', '参变量类', '属性', '3', '校时模式', '校时模式:enum[主站授时<0>,终端精确校时<1>,北斗/GPS<2>,其它<255>],'),
            ('4000', '日期时间', '8', '参变量类', '属性', '4', '精准校时参数', '精准校时参数:structure{最近心跳时间总个数:unsigned,最大值剔除个数:unsigned,最小值剔除个数:unsigned,通讯延时阈值:unsigned<秒|0>,最少有效个数:unsigned},'),
            ('4000', '日期时间', '8', '参变量类', '方法', '127', '广播校时(参数)', '广播校时(参数):date_time_s,'),
            ('4001', '通信地址', '8', '参变量类', '属性', '2', '', '通信地址:octet-string,'),
            ('4002', '表号', '8', '参变量类', '属性', '2', '', '表号:octet-string,'),
            ('4003', '客户编号', '8', '参变量类', '属性', '2', '', '客户编号:octet-string,'),
            ('4004', '设备地理位置', '8', '参变量类', '属性', '2', '', '设备地理位置:structure{经度:structure{方位:enum[E<0>,W<1>],度:unsigned,分:unsigned,秒:unsigned},纬度:structure{方位:enum[S<0>,N<1>],度:unsigned,分:unsigned,秒:unsigned},高度<cm>:double-long-unsigned},'),
            ('4005', '组地址', '8', '参变量类', '属性', '2', '', '组地址:array:octet-string,'),
            ('4006', '时钟源', '8', '参变量类', '属性', '2', '', '时钟源:structure{时钟源:enum[内部<0>,时钟芯片<1>,互联网时钟<2>,卫星时钟<3>,长波时钟<4>],状态:enum[可用<0>,不可用<1>]},'),
            ('4006', '时钟源', '8', '参变量类', '方法', '127', '启用()', ''),
            ('4006', '时钟源', '8', '参变量类', '方法', '128', '禁用()', ''),
            ('4007', 'LCD参数', '8', '参变量类', '属性', '2', '', 'LCD参数:structure{上电全显时间:unsigned<秒|0>,背光点亮时间:long-unsigned<秒|0>,显示查看背光点亮时间:long-unsigned<秒|0>,无电按键屏幕驻留最大时间:long-unsigned<秒|0>,显示电能小数位数:unsigned,显示功率<最大需量>小数位数:unsigned,液晶①②字样意义:unsigned},'),
            ('4008', '备用套时区表切换时间', '8', '参变量类', '属性', '2', '', '备用套时区表切换时间:date_time_s,'),
            ('4009', '备用套日时段切换时间', '8', '参变量类', '属性', '2', '', '备用套日时段切换时间:date_time_s,'),
            ('400A', '备用套分时费率切换时间', '8', '参变量类', '属性', '2', '', '备用套分时费率切换时间:date_time_s,'),
            ('400B', '备用套阶梯电价切换时间', '8', '参变量类', '属性', '2', '', '备用套阶梯电价切换时间:date_time_s,'),
            ('400C', '时区时段数', '8', '参变量类', '属性', '2', '', '时区时段数:structure{年时区数(p≤14):unsigned,日时段表数(q≤8):unsigned,日时段数(每日切换数)(m≤14):unsigned,费率数(k≤63):unsigned,公共假日数(n≤254):unsigned},'),
            ('400D', '阶梯数', '8', '参变量类', '属性', '2', '', '阶梯数:unsigned,'),
            ('400E', '谐波分析次数', '8', '参变量类', '属性', '2', '', '谐波分析次数:unsigned,'),
            ('400F', '密钥总条数', '8', '参变量类', '属性', '2', '', '密钥总条数:unsigned,'),
            ('4010', '计量元件数', '8', '参变量类', '属性', '2', '', '计量元件数:unsigned,'),
            ('4011', '公共假日表', '8', '参变量类', '属性', '2', '', '公共假日表:array:structure{日期:date,日时段表号:unsigned},'),
            ('4012', '周休日特征字', '8', '参变量类', '属性', '2', '', '周休日特征字:bit-string(SIZE(8)),'),
            ('4013', '周休日釆用的日时段表号', '8', '参变量类', '属性', '2', '', '周休日釆用的日时段表号:unsigned,'),
            ('4014', '当前套时区表', '8', '参变量类', '属性', '2', '', 'array:时区:structure{月:unsigned,日:unsigned,日时段表号:unsigned},'),
            ('4015', '备用套时区表', '8', '参变量类', '属性', '2', '', 'array:时区:structure{月:unsigned,日:unsigned,日时段表号:unsigned},'),
            ('4016', '当前套日时段表', '8', '参变量类', '属性', '2', '', 'array:日时段表:array:时段:structure{时:unsigned,分:unsigned,费率号:unsigned},'),
            ('4017', '备用套日时段表', '8', '参变量类', '属性', '2', '', 'array:日时段表:array:时段:structure{时:unsigned,分:unsigned,费率号:unsigned},'),
            ('4018', '当前套费率电价', '8', '参变量类', '属性', '2', '', '当前套费率电价:array:double-long-unsigned<元/kWh|-4>,'),
            ('4019', '备用套费率电价', '8', '参变量类', '属性', '2', '', '当前套费率电价:array:double-long-unsigned<元/kWh|-4>,'),
            ('401A', '当前套阶梯电价', '8', '参变量类', '属性', '2', '阶梯参数', '阶梯参数:structure{阶梯值数组:array:double-long-unsigned<kWh|-2>,阶梯电价数组:array:double-long-unsigned<元/kWh|-4>,阶梯结算日数组:array:阶梯结算日:structure{月:unsigned,日:unsigned,时:unsigned}},'),
            ('401B', '备用套阶梯电价', '8', '参变量类', '属性', '2', '', '阶梯参数:structure{阶梯值数组:array:double-long-unsigned<kWh|-2>,阶梯电价数组:array:double-long-unsigned<元/kWh|-4>,阶梯结算日数组:array:阶梯结算日:structure{月:unsigned,日:unsigned,时:unsigned}},'),
            ('401C', '电流互感器变比', '8', '参变量类', '属性', '2', '', '电流互感器变比:double-long-unsigned<|-2>,'),
            ('401D', '电压互感器变比', '8', '参变量类', '属性', '2', '', '电压互感器变比:double-long-unsigned<|-2>,'),
            ('401E', '报警金额限值', '8', '参变量类', '属性', '2', '参数', '参数:structure{报警金额限值1:double-long-unsigned<元|-2>,报警金额限值2:double-long-unsigned<元|-2>,},'),
            ('401F', '其它金额限值', '8', '参变量类', '属性', '2', '参数', '参数:structure{透支金额限值:double-long-unsigned<元|-2>,囤积金额限值:double-long-unsigned<元|-2>,合闸允许金额限值:double-long-unsigned<元|-2>,},'),
            ('4020', '报警电量限值', '8', '参变量类', '属性', '2', '', '报警电量限值:structure{报警电量限值1:double-long-unsigned<kWh|-2>,报警电量限值2:double-long-unsigned<kWh|-2>,},'),
            ('4021', '其它电量限值', '8', '参变量类', '属性', '2', '', '其它电量限值:structure{囤积电量限值:double-long-unsigned<kWh|-2>,透支电量限值:double-long-unsigned<kWh|-2>,合闸允许电量限值:double-long-unsigned<kWh|-2>,},'),
            ('4022', '插卡状态字', '8', '参变量类', '属性', '2', '', '插卡状态字:bit-string(SIZE(16)),'),
            ('4024', '剔除', '8', '参变量类', '属性', '2', '', '剔除:enum[剔除投入<1>,剔除解除<2>],'),
            ('4025', '采集器升级结果表', '8', '参变量类', '属性', '2', '升级结果列表', '升级结果列表:array:采集器升级结果:structure{序号:long-unsigned,采集器地址:TSA,采集器升级结果标识:unsigned,补发开始时间:date_time_s,升级成功时间:date_time_s,广播成功块数:long-unsigned,补发块数:long-unsigned,升级前采集器版本:structure{厂商代码:visible-string(SIZE(4)),软件版本号:visible-string(SIZE(4)),软件版本日期:visible-string(SIZE(6)),硬件版本号:visible-string(SIZE(4)),硬件版本日期:visible-string(SIZE(6)),厂家扩展信息:visible-string(SIZE(8))},升级后采集器版本:structure{厂商代码:visible-string(SIZE(4)),软件版本号:visible-string(SIZE(4)),软件版本日期:visible-string(SIZE(6)),硬件版本号:visible-string(SIZE(4)),硬件版本日期:visible-string(SIZE(6)),厂家扩展信息:visible-string(SIZE(8))}},'),
            ('4025', '采集器升级结果表', '8', '参变量类', '属性', '3', '采集器升级控制参数', '采集器升级控制参数:structure{允许一次升级广播轮次数:unsigned,允许一次升级点对点补发天数:unsigned},'),
            ('4026', '采集器升级结果', '8', '参变量类', '属性', '2', '升级结果', '升级结果:structure{序号:long-unsigned,采集器地址:TSA,采集器升级结果标识:unsigned,补发开始时间:date_time_s,升级成功时间:date_time_s,广播成功块数:long-unsigned,补发块数:long-unsigned,升级前采集器版本:structure{厂商代码:visible-string(SIZE(4)),软件版本号:visible-string(SIZE(4)),软件版本日期:visible-string(SIZE(6)),硬件版本号:visible-string(SIZE(4)),硬件版本日期:visible-string(SIZE(6)),厂家扩展信息:visible-string(SIZE(8))},升级后采集器版本:structure{厂商代码:visible-string(SIZE(4)),软件版本号:visible-string(SIZE(4)),软件版本日期:visible-string(SIZE(6)),硬件版本号:visible-string(SIZE(4)),硬件版本日期:visible-string(SIZE(6)),厂家扩展信息:visible-string(SIZE(8))}},'),
            ('4030', '电压合格率参数', '8', '参变量类', '属性', '2', '', '电压合格率参数:structure{电压考核上限:long-unsigned<V|-1>,电压考核下限:long-unsigned<V|-1>,电压合格上限:long-unsigned<V|-1>,电压合格下限:long-unsigned<V|-1>},'),
            ('4100', '最大需量周期', '8', '参变量类', '属性', '2', '', '最大需量周期:unsigned<分钟|0>,'),
            ('4101', '滑差时间', '8', '参变量类', '属性', '2', '', '滑差时间:unsigned<分钟|0>,'),
            ('4102', '校表脉冲宽度', '8', '参变量类', '属性', '2', '', '校表脉冲宽度:unsigned<毫秒|0>,'),
            ('4103', '资产管理编码', '8', '参变量类', '属性', '2', '', '资产管理编码:visible-string(SIZE(32)),'),
            ('4104', '额定电压', '8', '参变量类', '属性', '2', '', '额定电压:visible-string(SIZE(6)),'),
            ('4105', '额定电流/基本电流', '8', '参变量类', '属性', '2', '', '额定电流/基本电流:visible-string(SIZE(6)),'),
            ('4106', '最大电流', '8', '参变量类', '属性', '2', '', '最大电流:visible-string(SIZE(6)),'),
            ('4107', '有功准确度等级', '8', '参变量类', '属性', '2', '', '有功准确度等级:visible-string(SIZE(4)),'),
            ('4108', '无功准确度等级', '8', '参变量类', '属性', '2', '', '无功准确度等级:visible-string(SIZE(4)),'),
            ('4109', '电能表有功常数', '8', '参变量类', '属性', '2', '', '电能表有功常数:double-long-unsigned<imp/kWh|0>,'),
            ('410A', '电能表无功常数', '8', '参变量类', '属性', '2', '', '电能表无功常数:double-long-unsigned<imp/kvarh|0>,'),
            ('410B', '电能表型号', '8', '参变量类', '属性', '2', '', '电能表型号:visible-string(SIZE(32)),'),
            ('410C', 'ABC各相电导系数', '8', '参变量类', '属性', '2', '', 'ABC各相电导系数:structure{A相电导:long<|-3>,B相电导:long<|-3>,C相电导:long<|-3>},'),
            ('410D', 'ABC各相电抗系数', '8', '参变量类', '属性', '2', '', 'ABC各相电抗系数:structure{A相电抗:long<|-3>,B相电抗:long<|-3>,C相电抗:long<|-3>},'),
            ('410E', 'ABC各相电阻系数', '8', '参变量类', '属性', '2', '', 'ABC各相电阻系数:structure{A相电阻:long<|-3>,B相电阻:long<|-3>,C相电阻:long<|-3>},'),
            ('410F', 'ABC各相电纳系数', '8', '参变量类', '属性', '2', '', 'ABC各相电纳系数:structure{A相电纳:long<|-3>,B相电纳:long<|-3>,C相电纳:long<|-3>},'),
            ('4110', '电能表运行特征字1', '8', '参变量类', '属性', '2', '', '电能表运行特征字1:bit-string(SIZE,'),
            ('4111', '软件备案号', '8', '参变量类', '属性', '2', '', '软件备案号:visible-string,'),
            ('4112', '有功组合方式特征字', '8', '参变量类', '属性', '2', '', '有功组合方式特征字:bit-string(SIZE(8)),'),
            ('4113', '无功组合方式1特征字', '8', '参变量类', '属性', '2', '', '无功组合方式1特征字:bit-string(SIZE(8)),'),
            ('4114', '无功组合方式2特征字', '8', '参变量类', '属性', '2', '', '无功组合方式2特征字:bit-string(SIZE(8)),'),
            ('4116', '结算日', '8', '参变量类', '属性', '2', '配置参数', '配置参数:array:structure{日:unsigned,时:unsigned},'),
            ('4117', '期间需量冻结周期', '8', '参变量类', '属性', '2', '配置参数', '配置参数:TI,'),
            ('4200', '路由表', '11', '参变量类', '属性', '2', '配置表', '配置表:array 路由信息单元,'),
            ('4200', '路由表', '11', '参变量类', '方法', '127', 'Add(路由信息单元)', ''),
            ('4200', '路由表', '11', '参变量类', '方法', '128', 'AddBatch(array 路由信息单元)', ''),
            ('4200', '路由表', '11', '参变量类', '方法', '129', 'Update(TSA ，路由信息单元)', ''),
            ('4200', '路由表', '11', '参变量类', '方法', '134', 'Clear()', ''),
            ('4201', '路由信息单元', '8', '参变量类', '属性', '2', 'routing definition', 'routing definition:structure{通信地址:TSA,父节点集合:array:TSA},'),
            ('4202', '级联通信参数', '8', '参变量类', '属性', '2', '', '级联通信参数:structure{级联标志:bool,级联通信端口号:OAD,总等待超时<10ms>:long-unsigned,字节超时<10ms>:long-unsigned,重发次数:unsigned,巡测周期<min>:unsigned,级联<被>端口数:unsigned,级联<被>终端地址:array:TSA},'),
            ('4204', '终端广播校时', '8', '参变量类', '属性', '2', '终端广播校时参数', '终端广播校时参数:structure{终端广播校时启动时间:time,是否启用:bool},'),
            ('4204', '终端广播校时', '8', '参变量类', '属性', '3', '终端单地址广播校时参数', '终端单地址广播校时参数:structure{时钟误差阈值:integer<秒|0>,终端广播校时启动时间:time,是否启用:bool},'),
            ('4300', '电气设备', '19', '参变量类', '属性', '0', '', ''),
            ('4307', '水表', '19', '参变量类', '方法', '127', '出厂启用()', ''),
            ('4307', '水表', '19', '参变量类', '方法', '128', '阀门控制(参数)', '阀门控制(参数):enum[开阀<85>,关阀<153>],'),
            ('4307', '水表', '19', '参变量类', '方法', '129', '机电同步()', ':double-long-unsigned'),
            ('4308', '气表', '19', '参变量类', '方法', '127', '出厂启用()', ''),
            ('4308', '气表', '19', '参变量类', '方法', '128', '阀门控制(参数)', '阀门控制(参数):enum[开阀<85>,关阀<153>],'),
            ('4308', '气表', '19', '参变量类', '方法', '129', '机电同步()', ':double-long-unsigned'),
            ('4309', '热表', '19', '参变量类', '方法', '127', '出厂启用()', ''),
            ('4309', '热表', '19', '参变量类', '方法', '128', '阀门控制(参数)', '阀门控制(参数):enum[开阀<85>,关阀<153>],'),
            ('4309', '热表', '19', '参变量类', '方法', '129', '机电同步', 'structure{热量:double-long-unsigned,热流量(水流量):double-long-unsigned},'),
            ('4400', '应用连接', '20', '参变量类', '属性', '0', '', ''),
            ('4401', '认证密码', '8', '参变量类', '属性', '2', '只写', ':visible-string,'),
            ('4500', '公网通信模块1', '25', '参变量类', '属性', '0', '', ''),
            ('4501', '公网通信模块2', '25', '参变量类', '属性', '0', '', ''),
            ('4510', '以太网通信模块1', '26', '参变量类', '属性', '0', '', ''),
            ('4511', '以太网通信模块2', '26', '参变量类', '属性', '0', '', ''),
            ('4512', '以太网通信模块3', '26', '参变量类', '属性', '0', '', ''),
            ('4513', '以太网通信模块4', '26', '参变量类', '属性', '0', '', ''),
            ('4514', '以太网通信模块5', '26', '参变量类', '属性', '0', '', ''),
            ('4515', '以太网通信模块6', '26', '参变量类', '属性', '0', '', ''),
            ('4516', '以太网通信模块7', '26', '参变量类', '属性', '0', '', ''),
            ('4517', '以太网通信模块8', '26', '参变量类', '属性', '0', '', ''),
            ('4520', '备用通道', '8', '参变量类', '属性', '2', '', '备用通道:array:structure{运营商:enum[CMCC（移动）<0>,CTCC（电信）<1>,CUCC（联通）<2>,未知<255>],网络类型:enum[2G<0>,3G<1>,4G<2>,未知<255>],APN:visible-string,用户名:visible-string,密码:visible-string,代理服务器地址:octet-string,代理端口:long-unsigned,主站通信参数:array:structure{IP地址:octet-string,端口:long-unsigned,},'),
            ('5000', '瞬时冻结', '9', '冻结类', '属性', '2', '', '瞬时冻结:,'),
            ('5001', '秒冻结', '9', '冻结类', '属性', '2', '', '秒冻结:,'),
            ('5002', '分钟冻结', '9', '冻结类', '属性', '2', '', '分钟冻结:,'),
            ('5003', '小时冻结', '9', '冻结类', '属性', '2', '', '小时冻结:,'),
            ('5004', '日冻结', '9', '冻结类', '属性', '2', '', '日冻结:,'),
            ('5005', '结算日冻结', '9', '冻结类', '属性', '2', '', '结算日冻结:,'),
            ('5006', '月冻结', '9', '冻结类', '属性', '2', '', '月冻结:,'),
            ('5007', '年冻结', '9', '冻结类', '属性', '2', '', '年冻结:,'),
            ('5008', '时区表切换冻结', '9', '冻结类', '属性', '2', '', '时区表切换冻结:,'),
            ('5009', '日时段表切换冻结', '9', '冻结类', '属性', '2', '', '日时段表切换冻结:,'),
            ('500A', '费率电价切换冻结', '9', '冻结类', '属性', '2', '', '费率电价切换冻结:,'),
            ('500B', '阶梯切换冻结', '9', '冻结类', '属性', '2', '', '阶梯切换冻结:,'),
            ('5011', '阶梯结算冻结', '9', '冻结类', '属性', '2', '', '阶梯结算冻结:,'),
            ('6000', '采集档案配置表', '11', '采集监控类', '属性', '2', '配置表', '配置表:array:structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}},'),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '127', 'Add(采集档案配置单元)', '采集档案配置单元:structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}},'),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '128', 'AddBatch(array 采集档案配置单元)', 'array:采集档案配置单元:structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}},'),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '129', 'Update(配置序号，基本信息)', 'structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>}},'),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '130', 'Update(配置序号，扩展信息，附属信息)', 'structure{配置序号:long-unsigned,扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}},'),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '131', 'Delete(配置序号)', '配置序号:long-unsigned,'),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '132', 'Delete(基本信息)', ''),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '133', 'Delete(通信地址， 端口号)', ''),
            ('6000', '采集档案配置表', '11', '采集监控类', '方法', '134', 'Clear()', ''),
            ('6001', '采集档案配置单元', '8', '采集监控类', '属性', '2', 'Acquisition document definition', 'structure{配置序号:long-unsigned,基本信息:structure{通信地址:TSA,波特率:enum[300bps<0>,600bps<1>,1200bps<2>,2400bps<3>,4800bps<4>,7200bps<5>,9600bps<6>,19200bps<7>,38400bps<8>,57600bps<9>,115200bps<10>,自适应<255>],规约类型:enum[未知(0),DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],端口:OAD,通信密码:octet-string,费率个数:unsigned,用户类型:unsigned,接线方式:enum[未知<0>,单相<1>,三相三线<2>,三相四线<3>],额定电压:long-unsigned<V|-1>,额定电流:long-unsigned<A|-1>},扩展信息:structure{采集器地址:TSA,资产号:octet-string,PT:long-unsigned,CT:long-unsigned},附属信息:array:structure{对象属性描述:OAD,属性值:Data}},'),
            ('6002', '搜表', '11', '采集监控类', '属性', '2', '所有搜表结果', '所有搜表结果:array:structure{通信地址:TSA,所属采集器地址:TSA,规约类型:enum[未知<0>,DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],相位:enum[未知<0>,A<1>,B<2>,C<3>],信号品质:unsigned,搜到的时间:date_time_s,搜到的附加信息:array:structure{对象属性描述:OAD,属性值:Data}},'),
            ('6002', '搜表', '11', '采集监控类', '属性', '5', '跨台区搜表结果', '跨台区搜表结果:array:structure{通信地址:TSA,主节点地址:TSA,变更时间:date_time_s},'),
            ('6002', '搜表', '11', '采集监控类', '属性', '6', '所有搜表结果记录数', '所有搜表结果记录数:long-unsigned,'),
            ('6002', '搜表', '11', '采集监控类', '属性', '7', '跨台区搜表结果记录数', '跨台区搜表结果记录数:long-unsigned,'),
            ('6002', '搜表', '11', '采集监控类', '属性', '8', '', '搜表:structure{是否启用每天周期搜表:bool,自动更新采集档案:bool,是否产生搜表相关事件:bool,清空搜表结果选项:enum[不清空<0>,每天周期搜表前清空<1>,每次搜表前清空<2>]},'),
            ('6002', '搜表', '11', '采集监控类', '属性', '9', '每天周期搜表参数配置', '每天周期搜表参数配置:array:structure{开始时间:time,搜表时长<min>:long-unsigned},'),
            ('6002', '搜表', '11', '采集监控类', '属性', '10', '', '搜表:enum[空闲<0>,搜表中<1>],'),
            ('6002', '搜表', '11', '采集监控类', '方法', '127', '实时启动搜表(搜表时长)', '实时启动搜表(搜表时长):long-unsigned<分钟|0>,'),
            ('6002', '搜表', '11', '采集监控类', '方法', '128', '清空搜表结果()', ''),
            ('6002', '搜表', '11', '采集监控类', '方法', '129', '清空跨台区搜表结果()', ''),
            ('6003', '一个搜表结果', '8', '采集监控类', '属性', '2', '', '一个搜表结果:structure{通信地址:TSA,所属采集器地址:TSA,规约类型:enum[未知<0>,DL/T645-1997<1>,DL/T645-2007<2>,DL/T698.45<3>,CJ/T188-2004<4>],相位:enum[未知<0>,A<1>,B<2>,C<3>],信号品质:unsigned,搜到的时间:date_time_s,搜到的附加信息:array:structure{对象属性描述:OAD,属性值:Data}},'),
            ('6004', '一个跨台区结果', '8', '采集监控类', '属性', '2', '', '一个跨台区结果:structure{通信地址:TSA,主节点地址:TSA,变更时间:date_time_s},'),
            ('6012', '任务配置表', '10', '采集监控类', '属性', '2', '配置表', '配置表:array:structure{任务ID:unsigned,执行频率:TI,方案类型:enum[普通采集方案<1>,事件采集方案<2>,透明方案<3>,上报方案<4>,脚本方案<5>],方案编号:unsigned,开始时间:date_time_s,结束时间:date_time_s,延时:TI,执行优先级:unsigned,状态:enum[正常<1>,停用<2>],任务开始前脚本id:long-unsigned,任务完成后脚本id:long-unsigned,任务运行时段:structure{类型:enum[前闭后开<0>,前开后闭<1>,前闭后闭<2>,前开后开<3>],时段表:array:structure{起始小时:unsigned,起始分钟:unsigned,结束小时:unsigned,结束分钟:unsigned}},}'),
            ('6012', '任务配置表', '10', '采集监控类', '属性', '3', '记录表', '记录表:array:structure{采集启动时标:date_time_s,采集成功时标:date_time_s,采集存储时标:date_time_s,采集通信地址:TSA,采集的数据1:Data,…采集的数据N:Data},'),
            ('6012', '任务配置表', '10', '采集监控类', '方法', '127', 'Add(array 任务配置单元)', 'array:任务配置单元:structure{任务ID:unsigned,执行频率:TI,方案类型:enum[普通采集方案<1>,事件采集方案<2>,透明方案<3>,上报方案<4>,脚本方案<5>],方案编号:unsigned,开始时间:date_time_s,结束时间:date_time_s,延时:TI,执行优先级:unsigned,状态:enum[正常<1>,停用<2>],任务开始前脚本id:long-unsigned,任务完成后脚本id:long-unsigned,任务运行时段:structure{类型:enum[前闭后开<0>,前开后闭<1>,前闭后闭<2>,前开后开<3>],时段表:array:structure{起始小时:unsigned,起始分钟:unsigned,结束小时:unsigned,结束分钟:unsigned}},}'),
            ('6012', '任务配置表', '10', '采集监控类', '方法', '128', 'Delete(array 任务ID)', 'array:任务ID:unsigned,'),
            ('6012', '任务配置表', '10', '采集监控类', '方法', '129', 'Clear()', ''),
            ('6012', '任务配置表', '10', '采集监控类', '方法', '130', 'Update(任务ID，状态)', 'structure{任务ID:unsigned,状态:enum[正常<1>,停用<2>]},'),
            ('6013', '任务配置单元', '8', '采集监控类', '属性', '2', '任务配置单元', '任务配置单元:structure{任务ID:unsigned,执行频率:TI,方案类型:enum[普通采集方案<1>,事件采集方案<2>,透明方案<3>,上报方案<4>,脚本方案<5>],方案编号:unsigned,开始时间:date_time_s,结束时间:date_time_s,延时:TI,执行优先级:unsigned,状态:enum[正常<1>,停用<2>],任务开始前脚本id:long-unsigned,任务完成后脚本id:long-unsigned,任务运行时段:structure{类型:enum[前闭后开<0>,前开后闭<1>,前闭后闭<2>,前开后开<3>],时段表:array:structure{起始小时:unsigned,起始分钟:unsigned,结束小时:unsigned,结束分钟:unsigned}},}'),
            ('6014', '普通采集方案集', '11', '采集监控类', '属性', '2', '', '普通采集方案集:array:structure{方案编号:unsigned,存储深度:long-unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data},记录列选择:array:CSD,电能表集合:MS,存储时标选择:enum[未定义<0>,任务开始时间<1>,相对当日0点0分<2>,相对上日23点59分<3>,相对上日0点0分<4>,相对当月1日0点0分<5>,数据冻结时标<6>,相对上月月末23点59分<7>]},'),
            ('6014', '普通采集方案集', '11', '采集监控类', '方法', '127', 'Add(array 普通采集方案)', 'array:普通采集方案:structure{方案编号:unsigned,存储深度:long-unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data},记录列选择:array:CSD,电能表集合:MS,存储时标选择:enum[未定义<0>,任务开始时间<1>,相对当日0点0分<2>,相对上日23点59分<3>,相对上日0点0分<4>,相对当月1日0点0分<5>,数据冻结时标<6>,相对上月月末23点59分<7>]},'),
            ('6014', '普通采集方案集', '11', '采集监控类', '方法', '128', 'Delete(array 方案编号)', 'array:方案编号:unsigned,'),
            ('6014', '普通采集方案集', '11', '采集监控类', '方法', '129', 'Clear()', ''),
            ('6014', '普通采集方案集', '11', '采集监控类', '方法', '130', 'Set_CSD(方案编号)', 'array:方案编号:CSD,'),
            ('6015', '普通采集方案', '8', '采集监控类', '属性', '2', '普通采集方案', '普通采集方案:structure{方案编号:unsigned,存储深度:long-unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data},记录列选择:array:CSD,电能表集合:MS,存储时标选择:enum[未定义<0>,任务开始时间<1>,相对当日0点0分<2>,相对上日23点59分<3>,相对上日0点0分<4>,相对当月1日0点0分<5>,数据冻结时标<6>,相对上月月末23点59分<7>]},'),
            ('6016', '事件采集方案集', '11', '采集监控类', '属性', '2', '', '事件采集方案集:array:structure{方案编号:unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data}电能表集合:MS,上报标识:bool,存储深度:long-unsigned},,'),
            ('6016', '事件采集方案集', '11', '采集监控类', '方法', '127', 'Add(array 事件采集方案)', 'array:事件采集方案:structure{方案编号:unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data}电能表集合:MS,上报标识:bool,存储深度:long-unsigned},'),
            ('6016', '事件采集方案集', '11', '采集监控类', '方法', '128', 'Delete(array 方案编号)', 'array:方案编号:unsigned,'),
            ('6016', '事件采集方案集', '11', '采集监控类', '方法', '129', 'Clear()', ''),
            ('6016', '事件采集方案集', '11', '采集监控类', '方法', '130', 'UpdateReportFlag(方案编号，上报标识)', 'structure{方案编号:unsigned,上报标识:bool},'),
            ('6017', '事件采集方案', '8', '采集监控类', '属性', '2', '事件采集方案 Event acq plan', '事件采集方案:structure{方案编号:unsigned,采集方式:structure{采集类型:unsigned,采集内容:Data}电能表集合:MS,上报标识:bool,存储深度:long-unsigned},'),
            ('6018', '透明方案集', '11', '采集监控类', '属性', '2', '', '透明方案集:array:structure{方案编号:unsigned,方案内容集:array:structure{序号:long-unsigned,通信地址:TSA,开始前脚本id:long-unsigned,完成后脚本id:long-unsigned,方案控制标志:structure{上报透明方案结果并等待后续报文:bool,等待后续报文超时时间<秒>:long-unsigned,结果比对标识:enum[不比对<0>,比<1>,比对上报<2>],结果比对参数:structure{特征字节:unsigned,截取开始:long-unsigned,截取长度:long-unsigned}},方案报文集:array:structure{报文序号:unsigned,报文内容:octet-string}},存储深度:long-unsigned},'),
            ('6018', '透明方案集', '11', '采集监控类', '方法', '127', 'Add(透明方案)', '透明方案:structure{方案编号:unsigned,方案内容集:array:structure{序号:long-unsigned,通信地址:TSA,开始前脚本id:long-unsigned,完成后脚本id:long-unsigned,方案控制标志:structure{上报透明方案结果并等待后续报文:bool,等待后续报文超时时间<秒>:long-unsigned,结果比对标识:enum[不比对<0>,比<1>,比对上报<2>],结果比对参数:structure{特征字节:unsigned,截取开始:long-unsigned,截取长度:long-unsigned}},方案报文集:array:structure{报文序号:unsigned,报文内容:octet-string}},存储深度:long-unsigned},'),
            ('6018', '透明方案集', '11', '采集监控类', '方法', '128', 'AddMeterFrame(方案编号，通信地址，方案控制标志，方案报文集)', ''),
            ('6018', '透明方案集', '11', '采集监控类', '方法', '129', 'Delete(方案编号， array 通信地址)', 'structure{方案编号:unsigned,array:通信地址:TSA},'),
            ('6018', '透明方案集', '11', '采集监控类', '方法', '130', 'Delete(array 方案编号)', 'array:方案编号:unsigned,'),
            ('6018', '透明方案集', '11', '采集监控类', '方法', '131', 'Clear()', ''),
            ('6019', '透明方案', '8', '采集监控类', '属性', '2', '透明方案', '透明方案:structure{方案编号:unsigned,方案内容集:array:structure{序号:long-unsigned,通信地址:TSA,开始前脚本id:long-unsigned,完成后脚本id:long-unsigned,方案控制标志:structure{上报透明方案结果并等待后续报文:bool,等待后续报文超时时间<秒>:long-unsigned,结果比对标识:enum[不比对<0>,比<1>,比对上报<2>],结果比对参数:structure{特征字节:unsigned,截取开始:long-unsigned,截取长度:long-unsigned}},方案报文集:array:structure{报文序号:unsigned,报文内容:octet-string}},存储深度:long-unsigned},'),
            ('601A', '透明方案结果集', '11', '采集监控类', '属性', '2', '', '透明方案结果集:array:structure{方案编号:unsigned,方案执行时间:date_time_s,通信地址:TSA,结果集:array:structure{报文序号:unsigned,报文响应时间:date_time_s,命令结果:octet-string}},'),
            ('601B', '一个透明方案结果', '8', '采集监控类', '属性', '2', '', '一个透明方案结果:structure{方案编号:unsigned,方案执行时间:date_time_s,通信地址:TSA,结果集:array:structure{报文序号:unsigned,报文响应时间:date_time_s,命令结果:octet-string}},'),
            ('601C', '上报方案集', '11', '采集监控类', '属性', '2', '', '上报方案集:array:structure{方案编号:unsigned,上报通道:array:OAD,上报响应超时时间:TI,最大上报次数:unsigned,上报内容:structure{类型:unsigned,数据:Data}},'),
            ('601C', '上报方案集', '11', '采集监控类', '方法', '127', 'Add(array 上报方案)', '上报方案集:array:structure{方案编号:unsigned,上报通道:array:OAD,上报响应超时时间:TI,最大上报次数:unsigned,上报内容:structure{类型:unsigned,数据:Data}},'),
            ('601C', '上报方案集', '11', '采集监控类', '方法', '128', 'Delete(array 方案编号)', 'array:方案编号:unsigned,'),
            ('601C', '上报方案集', '11', '采集监控类', '方法', '129', 'Clear()', ''),
            ('601D', '上报方案', '8', '采集监控类', '属性', '2', '上报方案 report plan', '上报方案:structure{方案编号:unsigned,上报通道:array:OAD,上报响应超时时间:TI,最大上报次数:unsigned,上报内容:structure{类型:unsigned,数据:Data}},'),
            ('601E', '采集规则库', '11', '采集监控类', '属性', '2', '采集规则库', '采集规则库:array:structure{数据列选择描述符:CSD,规则描述:structure{AcqCmd_2007:structure{主用DI:array:octet-string(SIZE(4)),备用DI:array:octet-string(SIZE(4))},AcqCmd_1997:structure{主用DI:array:octet-string(SIZE(2)),备用DI:array:octet-string(SIZE(2))},AcqCmd_Trans:structure{Frame:octet-string}}},'),
            ('601E', '采集规则库', '11', '采集监控类', '方法', '127', 'Add(array 采集规则)', 'array:采集规则:structure{数据列选择描述符:CSD,规则描述:structure{AcqCmd_2007:structure{主用DI:array:octet-string(SIZE(4)),备用DI:array:octet-string(SIZE(4))},AcqCmd_1997:structure{主用DI:array:octet-string(SIZE(2)),备用DI:array:octet-string(SIZE(2))},AcqCmd_Trans:structure{Frame:octet-string}}},'),
            ('601E', '采集规则库', '11', '采集监控类', '方法', '128', 'Delete(array:CSD)', 'array:CSD,'),
            ('601E', '采集规则库', '11', '采集监控类', '方法', '129', 'Clear()', ''),
            ('601F', '采集规则', '8', '采集监控类', '属性', '2', '', '采集规则:structure{数据列选择描述符:CSD,规则描述:structure{AcqCmd_2007:structure{主用DI:array:octet-string(SIZE(4)),备用DI:array:octet-string(SIZE(4))},AcqCmd_1997:structure{主用DI:array:octet-string(SIZE(2)),备用DI:array:octet-string(SIZE(2))},AcqCmd_Trans:structure{Frame:octet-string}}},'),
            ('6032', '采集状态集', '11', '采集监控类', '属性', '2', '', '采集状态集:array:structure{通信地址:TSA,中继级别:unsigned,中继地址:TSA,端口:OAD,最后一次采集成功时间:date_time_s,采集失败次数:unsigned,相位:enum[未知<0>,A相<1>,B相<2>,C相<3>],相序异常:enum[正常<0>,LN互易<1>,逆相序<2>]},'),
            ('6033', '一个采集状态', '8', '采集监控类', '属性', '2', '', '一个采集状态:structure{通信地址:TSA,中继级别:unsigned,中继地址:TSA,端口:OAD,最后一次采集成功时间:date_time_s,采集失败次数:unsigned,相位:enum[未知<0>,A相<1>,B相<2>,C相<3>],相序异常:enum[正常<0>,LN互易<1>,逆相序<2>]},'),
            ('6034', '采集任务监控集', '11', '采集监控类', '属性', '2', '', '采集任务监控集:array:structure{任务ID:unsigned任务执行状态:enum[未执行<0>,执行中<1>,已执行<2>],任务执行开始时间:date_time_s,任务执行结束时间:date_time_s,采集总数量:long-unsigned,采集成功数量:long-unsigned,已发送报文条数:long-unsigned,已接收报文条数:long-unsigned},'),
            ('6035', '采集任务监控单元', '8', '采集监控类', '属性', '2', '', '采集任务监控单元:structure{任务ID:unsigned任务执行状态:enum[未执行<0>,执行中<1>,已执行<2>],任务执行开始时间:date_time_s,任务执行结束时间:date_time_s,采集总数量:long-unsigned,采集成功数量:long-unsigned,已发送报文条数:long-unsigned,已接收报文条数:long-unsigned},'),
            ('6040', '采集启动时标', '8', '采集监控类', '属性', '2', '', '采集启动时标:date_time_s,'),
            ('6041', '采集成功时标', '8', '采集监控类', '属性', '2', '', '采集成功时标:date_time_s,'),
            ('6042', '采集存储时标', '8', '采集监控类', '属性', '2', '', '采集存储时标:date_time_s,'),
            ('7000', '文件集合', '11', '集合类', '方法', '127', 'WriteFile(文件名，偏移，内容)', ''),
            ('7000', '文件集合', '11', '集合类', '方法', '128', 'Execute(文件名)', '文件名:visible-string,'),
            ('7000', '文件集合', '11', '集合类', '方法', '129', 'DeleteFile(文件名)', '文件名:visible-string,'),
            ('7001', '文件', '8', '集合类', '属性', '2', '文件 文件', '文件 文件:structure{文件名:visible-string,扩展名:visible-string,文件长度:long-unsigned,创建时间:date_time_s,修改时间:date_time_s,数据来源:enum[主站<0>,终端自身<1>,采集器<2>,电能表<3>,其它<255>],文件内容:octet-string},'),
            ('7010', '脚本集合', '11', '集合类', '属性', '2', '', '脚本集合:array:脚本:structure{脚本ID:long-unsigned,操作集:array一个操作},'),
            ('7010', '脚本集合', '11', '集合类', '方法', '127', 'Add(脚本)', '脚本ID:long-unsigned,'),
            ('7010', '脚本集合', '11', '集合类', '方法', '128', 'Delete(脚本 id)', '脚本ID:long-unsigned,'),
            ('7010', '脚本集合', '11', '集合类', '方法', '129', 'Execute(脚本 id)', '脚本ID:long-unsigned,'),
            ('7010', '脚本集合', '11', '集合类', '方法', '130', 'Clear()', '脚本ID:long-unsigned,'),
            ('7011', '脚本', '8', '集合类', '属性', '2', '', '脚本:脚本:structure{脚本ID:long-unsigned,操作集:array一个操作},'),
            ('7012', '脚本执行结果集', '11', '集合类', '属性', '2', '', '脚本执行结果集:array:structure{脚本ID:long-unsigned,脚本执行时间:date_time_s,脚本执行结果集:array一个执行结果},'),
            ('7013', '一个脚本执行结果', '8', '集合类', '属性', '2', '', '一个脚本执行结果:structure{脚本ID:long-unsigned,脚本执行时间:date_time_s,脚本执行结果集:array一个执行结果},'),
            ('7100', '扩展变量对象集合', '11', '集合类', '属性', '2', '', 'array:变量类对象:Data,'),
            ('7101', '扩展参变量对象集合', '11', '集合类', '属性', '2', '', 'array:变量类对象:Data,'),
            ('8000', '遥控远程遥控', '8', '控制类', '属性', '2', '配置参数', '配置参数:structure{继电器拉闸电流门限值:double-long-unsigned<A|-4>,超电流门限保护延时时间:long-unsigned<分钟|0>},'),
            ('8000', '遥控远程遥控', '8', '控制类', '属性', '3', '继电器输出状态', '继电器输出状态:bit-string(SIZE(8)),'),
            ('8000', '遥控远程遥控', '8', '控制类', '属性', '4', '告警状态', '告警状态:bit-string(SIZE(8)),'),
            ('8000', '遥控远程遥控', '8', '控制类', '属性', '5', '命令状态', '命令状态:bit-string(SIZE(8)),'),
            ('8000', '遥控远程遥控', '8', '控制类', '方法', '127', '触发告警(参数)', '触发告警(参数):NULL,'),
            ('8000', '遥控远程遥控', '8', '控制类', '方法', '128', '解除报警(参数)', '解除报警(参数):NULL,'),
            ('8000', '遥控远程遥控', '8', '控制类', '方法', '129', '跳闸(参数)', '跳闸(参数):array:structure{继电器:OAD,告警延时:unsigned<分钟|0>,限电时间:long-unsigned<分钟|0>,自动合闸:bool<True：自动合闸；False：非自动合闸>},'),
            ('8000', '遥控远程遥控', '8', '控制类', '方法', '130', '合闸(参数)', '合闸(参数):array:structure{继电器:OAD,命令:enum[合闸允许<0>,直接合闸<1>]},'),
            ('8001', '保电', '8', '控制类', '属性', '2', '保电状态', '保电状态:enum[解除<0>,保电<1>,自动保电<2>],'),
            ('8001', '保电', '8', '控制类', '属性', '3', '允许与主站最大无通信时长(分钟)', '保电:long-unsigned,'),
            ('8001', '保电', '8', '控制类', '属性', '4', '上电自动保电时长(分钟)', '保电:long-unsigned,'),
            ('8001', '保电', '8', '控制类', '属性', '5', '自动保电时段', '保电:array:structure{起始时间<时>:unsigned,结束时间<时>:unsigned},'),
            ('8001', '保电', '8', '控制类', '方法', '127', '投入保电(参数)', '投入保电(参数):NULL,'),
            ('8001', '保电', '8', '控制类', '方法', '128', '解除保电(参数)', '解除保电(参数):NULL,'),
            ('8001', '保电', '8', '控制类', '方法', '129', '解除自动保电(参数)', '解除自动保电(参数):NULL,'),
            ('8002', '催费告警', '8', '控制类', '属性', '2', '催费告警状态', '催费告警状态:enum[未告警<0>,告警<1>],'),
            ('8002', '催费告警', '8', '控制类', '方法', '127', '催费告警投入(参数)', '催费告警投入(参数):structure{告警时段：:octet-string(SIZE(3)),告警信息:visible-string(SIZE(200))},'),
            ('8002', '催费告警', '8', '控制类', '方法', '128', '取消催费告警(参数)', '取消催费告警(参数):NULL,'),
            ('8003', '一般中文信息', '11', '控制类', '属性', '2', '', '一般中文信息:array:structure{序号:unsigned,发布时间:date_time_s,已阅读标识:bool<True:已阅读,False:未阅读>,信息内容:visible-string(SIZE(200))},'),
            ('8003', '一般中文信息', '11', '控制类', '方法', '127', '添加信息(序号，发布时间，信息内容)', 'structure{序号:unsigned,发布时间:date_time_s,信息内容:visible-string(SIZE(200))},'),
            ('8003', '一般中文信息', '11', '控制类', '方法', '128', '删除信息(序号)', ''),
            ('8004', '重要中文信息', '11', '控制类', '属性', '2', '', '重要中文信息:array:structure{序号:unsigned,发布时间:date_time_s,已阅读标识:bool<True:已阅读,False:未阅读>,信息内容:visible-string(SIZE(200))},'),
            ('8004', '重要中文信息', '11', '控制类', '方法', '127', '添加信息(序号，发布时间，信息内容)', 'structure{序号:unsigned,发布时间:date_time_s,信息内容:visible-string(SIZE(200))},'),
            ('8004', '重要中文信息', '11', '控制类', '方法', '128', '删除信息(序号)', '序号:unsigned,'),
            ('8100', '终端保安定值', '8', '控制类', '属性', '2', '', '终端保安定值:long64<W|-1>,'),
            ('8101', '终端功控时段', '8', '控制类', '属性', '2', '配置参数', '配置参数:array:unsigned,'),
            ('8102', '功控告警时间', '8', '控制类', '属性', '2', '配置参数', '配置参数:array:<分钟|0>,'),
            ('8103', '时段功控', '13', '控制类', '属性', '2', '控制方案集', '控制方案集:array:structure{总加组对象:OI,方案标识:bit-string(SIZE(8)),第一套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第二套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第三套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},时段功控定值浮动系数:integer<%|0>},'),
            ('8103', '时段功控', '13', '控制类', '方法', '3', '添加时段功控单元', '时段功控配置单元:structure{总加组对象:OI,方案标识:bit-string(SIZE(8)),第一套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第二套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第三套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},时段功控定值浮动系数:integer<%|0>},'),
            ('8103', '时段功控', '13', '控制类', '方法', '5', '更新时段功控单元', '时段功控配置单元:structure{总加组对象:OI,方案标识:bit-string(SIZE(8)),第一套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第二套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第三套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},时段功控定值浮动系数:integer<%|0>},'),
            ('8103', '时段功控', '13', '控制类', '方法', '127', '时段功控方案切换(总加组对象，控制方案)', '时段功控方案切换(总加组对象，控制方案):structure{总加组对象:OI,structure{时段功控投入标识:bit-string(SIZE(8)),时段功控定值方案号:unsigned}},'),
            ('8104', '厂休控', '13', '控制类', '属性', '2', '控制方案集', '控制方案集:array:structure{总加组对象:OI,厂休控定值:long64<W|-1>,限电起始时间:date_time_s,限电延续时间:long-unsigned<分钟|0>,每周限电日:bit-string(SIZE(8))},'),
            ('8104', '厂休控', '13', '控制类', '方法', '3', '添加厂休控单元', 'structure{总加组对象:OI,厂休控定值:long64<W|-1>,限电起始时间:date_time_s,限电延续时间:long-unsigned<分钟|0>,每周限电日:bit-string(SIZE(8))},'),
            ('8104', '厂休控', '13', '控制类', '方法', '5', '更新厂休控单元', 'structure{总加组对象:OI,厂休控定值:long64<W|-1>,限电起始时间:date_time_s,限电延续时间:long-unsigned<分钟|0>,每周限电日:bit-string(SIZE(8))},'),
            ('8105', '营业报停控', '13', '控制类', '属性', '2', '控制方案集', '控制方案集:array:structure{总加组对象:OI,报停起始时间:date_time_s,报停结束时间:date_time_s,报停控功率定值:long64<W|-1>},'),
            ('8105', '营业报停控', '13', '控制类', '方法', '3', '添加营业报停控单元', 'structure{总加组对象:OI,报停起始时间:date_time_s,报停结束时间:date_time_s,报停控功率定值:long64<W|-1>},'),
            ('8105', '营业报停控', '13', '控制类', '方法', '5', '更新营业报停控单元', 'structure{总加组对象:OI,报停起始时间:date_time_s,报停结束时间:date_time_s,报停控功率定值:long64<W|-1>},'),
            ('8106', '当前功率下浮控', '13', '控制类', '方法', '127', '投入(总加组对象，控制方案)', '投入(总加组对象，控制方案):structure{总加组对象:OI,structure{当前功率下浮控定值滑差时间:unsigned<分钟|0>,当前功率下浮控定值浮动系数:integer<%|0>,控后总加有功功率冻结延时时间:unsigned<分钟|0>,当前功率下浮控的控制时间:unsigned<0.5小时>,当前功率下浮控第1轮告警时间:unsigned<分钟|0>,当前功率下浮控第2轮告警时间:unsigned<分钟|0>,当前功率下浮控第3轮告警时间:unsigned<分钟|0>,当前功率下浮控第4轮告警时间:unsigned<分钟|0>}},'),
            ('8107', '购电控', '13', '控制类', '属性', '2', '控制方案集', '控制方案集:array:structure{总加组对象:OI,购电单号:double-long-unsigned,追加/刷新标识:enum[追加<0>,刷新<1>],购电类型:enum[电量<0>,电费<1>],购电量<费>值:long64<kWh/元|-4>,报警门限值:long64<kWh/元|-4>,跳闸门限值:long64<kWh/元|-4>购电控模式:enum[本地模式<0>,远程模式<1>]},'),
            ('8107', '购电控', '13', '控制类', '方法', '3', '添加购电控单元', '购电控配置单元:structure{总加组对象:OI,购电单号:double-long-unsigned,追加/刷新标识:enum[追加<0>,刷新<1>],购电类型:enum[电量<0>,电费<1>],购电量<费>值:long64<kWh/元|-4>,报警门限值:long64<kWh/元|-4>,跳闸门限值:long64<kWh/元|-4>购电控模式:enum[本地模式<0>,远程模式<1>]},'),
            ('8107', '购电控', '13', '控制类', '方法', '5', '更新购电控单元', '购电控配置单元:structure{总加组对象:OI,购电单号:double-long-unsigned,追加/刷新标识:enum[追加<0>,刷新<1>],购电类型:enum[电量<0>,电费<1>],购电量<费>值:long64<kWh/元|-4>,报警门限值:long64<kWh/元|-4>,跳闸门限值:long64<kWh/元|-4>购电控模式:enum[本地模式<0>,远程模式<1>]},'),
            ('8108', '月电控', '13', '控制类', '属性', '2', '控制方案集', '控制方案集:array:structure{总加组对象:OI,月电量控定值:long64<kWh|-4>,报警门限值系数:unsigned<%|0>,月电量控定值浮动系数:integer<%|0>},'),
            ('8108', '月电控', '13', '控制类', '方法', '3', '添加月电控单元', '月电控配置单元:structure{总加组对象:OI,月电量控定值:long64<kWh|-4>,报警门限值系数:unsigned<%|0>,月电量控定值浮动系数:integer<%|0>},'),
            ('8108', '月电控', '13', '控制类', '方法', '5', '更新月电控单元', '月电控配置单元:structure{总加组对象:OI,月电量控定值:long64<kWh|-4>,报警门限值系数:unsigned<%|0>,月电量控定值浮动系数:integer<%|0>},'),
            ('8109', '时段功控配置单元', '8', '控制类', '属性', '2', '', '时段功控配置单元:structure{总加组对象:OI,方案标识:bit-string(SIZE(8)),第一套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第二套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},第三套定值:structure{时段号:bit-string(SIZE(8)),时段1功控定值:long64<W|-1>,时段2功控定值:long64<W|-1>,时段3功控定值:long64<W|-1>,时段4功控定值:long64<W|-1>,时段5功控定值:long64<W|-1>,时段6功控定值:long64<W|-1>,时段7功控定值:long64<W|-1>,时段8功控定值:long64<W|-1>},时段功控定值浮动系数:integer<%|0>},'),
            ('810A', '厂休控配置单元', '8', '控制类', '属性', '2', '', '厂休控配置单元:structure{总加组对象:OI,厂休控定值:long64<W|-1>,限电起始时间:date_time_s<年=FFFFH,月=FFH,日=FFH>,限电延续时间:long-unsigned<分钟|0>,每周限电日:bit-string(SIZE(8))},'),
            ('810B', '营业报停控配置单元', '8', '控制类', '属性', '2', '', '营业报停控配置单元:structure{总加组对象:OI,报停起始时间:date_time_s<时=FFH,分=FFH>,报停结束时间:date_time_s<时=FFH,分=FFH>,报停控功率定值:long64<W|-1>},'),
            ('810C', '购电控配置单元', '8', '控制类', '属性', '2', '', '购电控配置单元:structure{总加组对象:OI,购电单号:double-long-unsigned,追加/刷新标识:enum[追加<0>,刷新<1>],购电类型:enum[电量<0>,电费<1>],购电量<费>值:long64<kWh/元|-4>,报警门限值:long64<kWh/元|-4>,跳闸门限值:long64<kWh/元|-4>购电控模式:enum[本地模式<0>,远程模式<1>]},'),
            ('810D', '月电控配置单元', '8', '控制类', '属性', '2', '', '月电控配置单元:structure{总加组对象:OI,月电量控定值:long64<kWh|-4>,报警门限值系数:unsigned<%|0>,月电量控定值浮动系数:integer<%|0>},'),
            ('810E', '控制对象', '8', '控制类', '属性', '0', '', ''),
            ('810F', '跳闸轮次', '8', '控制类', '属性', '0', '', ''),
            ('8110', '电控定值', '8', '控制类', '属性', '0', '', ''),
            ('F000', '文件分帧传输管理', '18', '文件传输类', '属性', '4', '文件内容', '文件内容:octet-string,'),
            ('F000', '文件分帧传输管理', '18', '文件传输类', '属性', '5', '当前指针', '当前指针:double-long-unsigned<Byte|0>,'),
            ('F001', '文件分块传输管理', '18', '文件传输类', '属性', '4', '传输块状态字', '传输块状态字:bit-string,'),
            ('F001', '文件分块传输管理', '18', '文件传输类', '方法', '7', '启动传输(参数)', 'structure{文件信息:structure{源文件:visible-string,目标文件:visible-string,文件大小:double-long-unsigned,文件属性:bit-string(SIZE(3)),文件版本:visible-string文件类别:enum[终端文件<0>,本地通信模块文件<1>,远程通信模块文件<2>,采集器文件<3>,从节点通信模块文件<4>,其它文件<255>]},传输块大小:long-unsigned,校验:structure{校验类型:enum[CRC校验<默认><0>,md5校验<1>,SHA1校验<2>,其他<255>],校验值:octet-string}},'),
            ('F001', '文件分块传输管理', '18', '文件传输类', '方法', '8', '写文件(参数)', '写文件(参数):structure{块序号:long-unsigned,块数据:octet-string},'),
            ('F001', '文件分块传输管理', '18', '文件传输类', '方法', '9', '读文件(参数)', '读文件(参数):structure{块序号:long-unsigned},'),
            ('F001', '文件分块传输管理', '18', '文件传输类', '方法', '10', '软件比对(参数)', '软件比对(参数):structure{CPU编号:unsigned,密钥索引:unsigned,因子起始地址:double-long-unsigned,数据起始地址:double-long-unsigned,待加密数据长度:long-unsigned},'),
            ('F002', '文件扩展传输管理', '18', '文件传输类', '属性', '4', '服务器信息', '服务器信息:structure{IP地址:octet-string,端口:long-unsigned,用户名:visible-string,密码:visible-string},'),
            ('F002', '文件扩展传输管理', '18', '文件传输类', '方法', '7', '从服务器下载(文件信息，协议类型)', 'structure{文件信息:Data，协议类型:enum[telnet+zmodem协议<0>,ftp协议<1>,sftp协议<2>,http协议<3>,https协议<4>]},'),
            ('F002', '文件扩展传输管理', '18', '文件传输类', '方法', '8', '上传到服务器(文件信息，协议类型)', 'structure{文件信息:Data，协议类型:enum[telnet+zmodem协议<0>,ftp协议<1>,sftp协议<2>,http协议<3>,https协议<4>]},'),
            ('F100', 'ESAM', '21', 'ESAM接口类', '属性', '0', '', ''),
            ('F101', '安全模式参数', '8', 'ESAM接口类', '属性', '2', '安全模式选择', '安全模式选择:enum[不启用安全模式参数<0>,启用安全模式参数<1>],'),
            ('F101', '安全模式参数', '8', 'ESAM接口类', '属性', '3', '显式安全模式参数', '显式安全模式参数:array:structure{对象标识:OI,安全模式:long-unsigned},'),
            ('F101', '安全模式参数', '8', 'ESAM接口类', '方法', '1', '复位(参数)', ':integer,'),
            ('F101', '安全模式参数', '8', 'ESAM接口类', '方法', '127', '增加显式安全模式参数(对象标识，权限)', 'structure{对象标识:OI,权限:long-unsigned},'),
            ('F101', '安全模式参数', '8', 'ESAM接口类', '方法', '128', '删除显式安全模式参数(对象标识)', '对象标识:OI,'),
            ('F101', '安全模式参数', '8', 'ESAM接口类', '方法', '129', '批量增加显式安全模式参数(array 安全模式参数)', 'array:structure{对象标识:OI,安全模式:long-unsigned},'),
            ('F200', 'RS232', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{端口描述符:visible-string,端口参数:COMDCB,端口功能:enum[上行通信<0>,抄表<1>,级联<2>,停用<3>]},'),
            ('F200', 'RS232', '22', '输入输出设备类', '方法', '127', '配置端口(端口号，端口参数，端口功能)', 'structure{端口号:OAD,端口参数:COMDCB,端口功能:enum[上行通信<0>,抄表<1>,级联<2>,停用<3>]},'),
            ('F201', 'RS485', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{端口描述符:visible-string,端口参数:COMDCB,端口功能:enum[上行通信<0>,抄表<1>,级联<2>,停用<3>]},'),
            ('F201', 'RS485', '22', '输入输出设备类', '方法', '127', '配置端口(端口号，端口参数，端口功能)', 'structure{端口号:OAD,端口参数:COMDCB,端口功能:enum[上行通信<0>,抄表<1>,级联<2>,停用<3>]},'),
            ('F202', '红外', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{端口描述符:visible-string,端口参数:COMDCB},'),
            ('F202', '红外', '22', '输入输出设备类', '方法', '127', '配置端口(端口号，端口参数)', 'structure{端口号:OAD,端口参数:COMDCB},'),
            ('F203', '开关量输入', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{状态ST:unsigned,变位CD:unsigned},'),
            ('F203', '开关量输入', '22', '输入输出设备类', '属性', '4', '', '开关量输入:structure{开关量接入标志:bit-string(SIZE<8>),开关量属性标志:bit-string(SIZE<8>)},'),
            ('F204', '直流模拟量', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:array:structure{量程起始值:double-long,量程结束值:double-long,换算及单位:Scaler_Unit},'),
            ('F204', '直流模拟量', '22', '输入输出设备类', '属性', '4', '', '直流模拟量:array:structure{量程起始值:double-long,量程结束值:double-long,换算及单位:Scaler_Unit},'),
            ('F205', '继电器输出', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{描述符:visible-string,当前状态:enum[未输出<0>,输出<1>],开关属性:enum[脉冲式<0>,保持式<1>],接线状态:enum[接入<0>,未接入（1)]},'),
            ('F205', '继电器输出', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{描述符:visible-string,当前状态:enum[合闸<0>,跳闸<1>],开关属性:enum[脉冲式<0>,保持式<1>],接线状态:enum[接入<0>,未接入（1)]},'),
            ('F205', '继电器输出', '22', '输入输出设备类', '方法', '127', '修改开关属性(继电器号，开关属性)', '修改开关属性(继电器号，开关属性):OAD,'),
            ('F206', '告警输出', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:enum[未输出<0>,输出<1>],'),
            ('F206', '告警输出', '22', '输入输出设备类', '属性', '4', '', '告警输出:array:structure{起始时间Time,结束时间Time},'),
            ('F207', '多功能端子', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:enum[秒脉冲输出<0>,需量周期<1>,时段投切<2>],'),
            ('F207', '多功能端子', '22', '输入输出设备类', '方法', '127', '修改工作模式(路号，工作模式)', '修改工作模式(路号，工作模式):OAD,'),
            ('F208', '交采接口', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{交采描述符:visible-string},'),
            ('F209', '载波/微功率无线接口', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{端口描述符:visible-string,通信参数:COMDCB,版本信息:structure{厂商代码:visible-string(SIZE(2)),芯片代码:visible-string(SIZE(2)),版本日期Date,软件版本:long-unsigned}},'),
            ('F209', '载波/微功率无线接口', '22', '输入输出设备类', '属性', '5', '从节点对象列表', '从节点对象列表:array 从节点单元,'),
            ('F209', '载波/微功率无线接口', '22', '输入输出设备类', '属性', '6', '从节点对象列表更新周期', '从节点对象列表更新周期:TI,'),
            ('F209', '载波/微功率无线接口', '22', '输入输出设备类', '方法', '127', '透明转发(参数)', '透明转发(参数):structure{通信地址:TSA,接收等到报文超时时间<秒>:long-unsigned,透明转发命令:octet-string},'),
            ('F209', '载波/微功率无线接口', '22', '输入输出设备类', '方法', '128', '配置端口参数(端口号，通信参数)', '配置端口参数(端口号，通信参数):OAD,'),
            ('F20C', '230M无线专网接口对象', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{端口描述符:visible-string,},'),
            ('F20C', '230M无线专网接口对象', '22', '输入输出设备类', '属性', '4', '', '230M无线专网接口对象:array 频道设置,'),
            ('F20C', '230M无线专网接口对象', '22', '输入输出设备类', '属性', '5', '', '230M无线专网接口对象:array:integer<dBμV|0>,'),
            ('F210', '从节点单元', '22', '输入输出设备类', '属性', '0', '', ''),
            ('F20A', '脉冲输入设备', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:visible-string,'),
            ('F20B', '蓝牙', '22', '输入输出设备类', '属性', '2', '设备对象列表', '设备对象列表:array:structure{端口描述符:visible-string,通信参数:COMDCB},'),
            ('F20B', '蓝牙', '22', '输入输出设备类', '方法', '127', '配置端口(端口号，通信参数)', '配置端口(端口号，通信参数):OAD,'),
            ('F300', '自动轮显', '17', '显示类', '属性', '0', '', ''),
            ('F301', '按键轮显', '17', '显示类', '属性', '0', '', ''),
        ]

        # 类编号 ic, 属性/方法 am_choice, 属性/方法编号 am_no, 读写属性 rw_type, 属性/方法名 am_name, 数据类型<单位, 换算> data_type(structure)
        iclass = namedtuple('iclass', ['ic', 'am_choice', 'am_no', 'rw_type', 'am_name', 'structure'])
        self.ic_list = []
        for row in ic_table:
            self.ic_list.append(iclass._make(row))

        # 对象编号 oi, 对象名 oi_name, 类编号 ic, 类名 ic_name, 属性/方法 am_choice, 属性/方法编号 am_no, 属性/方法名 am_name, 数据类型<单位, 换算> data_type(structure)
        obj = namedtuple('obj', ['oi', 'oi_name', 'ic', 'ic_name', 'am_choice', 'am_no', 'am_name', 'structure'])
        self.oi_list = []
        for row in oi_table:
            self.oi_list.append(obj._make(row))

    def get_structure(self, type, oad_omd_text):
        """format: [(brief, type, {link dict}, [link structure]),]"""
        am_type = '属性' if type.strip() in ['oad', 'OAD'] else '方法'
        oad = re.sub(r'[^0-9a-fA-F]', '', oad_omd_text)[:8].upper()
        if len(oad) != 8:
            raise 'format error'
        oi_text = oad[:4]
        am_no = (int(oad[4:6], 16) & 0x1f) if am_type == '属性' else int(oad[4:6], 16)
        index = int(oad[6:8], 16)
        # print('oi_text', oi_text, 'am_no', am_no, 'index', index, 'am_type', am_type)

        # find OI
        for oi_row in self.oi_list:
            if oi_row.oi == oi_text:
                ic_no = int(oi_row.ic)
                break
        else:
            print(oi_text, 'not found')
            return []
        oi_row = [row for row in self.oi_list if row.am_choice == am_type\
                    and row.oi == oi_text and int(row.am_no) == am_no]
        ic_row = [row for row in self.ic_list if row.am_choice == am_type\
                    and int(row.ic) == ic_no and int(row.am_no) == am_no]
        if (not ic_row) and (not oi_row):
            print(oad, 'not defined')
            return []
        # print('oi_row:', oi_row)
        # print('ic_row:', ic_row)

        structure_text = ''
        if oi_row:
            if oi_row[0].structure:
                structure_text = oi_row[0].structure
        elif ic_row and ic_row[0]:
            structure_text = ic_row[0].am_name + ':' + ic_row[0].structure
        # print('structure_text:', structure_text)

        def get_enum_dict(enum_text):
            member_match = re.search(r'(.*?)(enum\[.*?\])', enum_text)
            enum_dict = {}
            if member_match.group(2): # enum
                enum_list = member_match.group(2).replace('enum[', '').split(',')
                for enum in enum_list:
                    enum_match = re.search(r'(.*)[\(<](\d+)[\)>]', enum)
                    if enum_match:
                        enum_dict.update({'%02X'%int(enum_match.group(2)): enum_match.group(1)})
            return enum_dict

        def loop(structure_text, max_count=0):
            count = 0
            structure_list = []
            while max_count == 0 or count < max_count:
                count += 1
                if not structure_text:
                    break
                if structure_text[0] in [',', ':', ' ']:
                    structure_text = structure_text[1:]
                    count -= 1
                elif re.match(r'([^:,\{\}]+:)?array:', structure_text):
                    array_match = re.match(r'([^:,\{\}]+:)?array:', structure_text)
                    structure_text = structure_text[len(array_match.group(0)):]
                    brief = array_match.group(1)[:-1] if array_match.group(1) else ''
                    array_structure, structure_text = loop(structure_text, max_count=1)
                    structure_list.append((brief, 'array', {}, array_structure))
                elif re.match(r'([^:,\{\}]+:)?structure\{', structure_text):
                    structure_match = re.match(r'([^:,\{\}]+:)?structure\{', structure_text)
                    structure_text = structure_text[len(structure_match.group(0)):]
                    brief = structure_match.group(1)[:-1] if structure_match.group(1) else ''
                    structure_structure, structure_text = loop(structure_text)
                    structure_list.append((brief, 'structure', {}, structure_structure))
                elif re.match(r'enum', structure_text):
                    data_type = 'enum'
                    link_dict = {}
                    member_match = re.search(r'enum\[.*?\]', structure_text)
                    if member_match.group(0): # enum
                        link_dict = get_enum_dict(member_match.group(0))
                    structure_list.append(('', data_type, link_dict, []))
                    structure_text = structure_text[len(member_match.group(0)):]
                elif re.match(r'\{', structure_text):
                    structure_text = structure_text[1:]
                    structure_list, structure_text = loop(structure_text)
                elif re.match(r'\}', structure_text):
                    structure_text = structure_text[1:]
                    return structure_list, structure_text
                elif re.match(r'[^:]+[,\}\{]', structure_text):
                    member_match = re.search(r'(.*?)(enum\[.*?\])?[,\}\{]', structure_text)
                    data_type = member_match.group(1)
                    link_dict = {}
                    if member_match.group(2): # enum
                        link_dict = get_enum_dict(member_match.group(2))
                        data_type = 'enum'
                    else:
                        unit_match = re.search(r'(.*?)<(.*?\|.*?)>', data_type)
                        if unit_match: # unit & scaler
                            data_type = unit_match.group(1)
                            unit, scaler = unit_match.group(2).split('|')
                            if unit:
                                link_dict['unit'] = unit
                            if scaler:
                                link_dict['scaler'] = scaler
                    structure_list.append(('', data_type, link_dict, []))
                    structure_text = structure_text[len(member_match.group(0)) - 1:]
                elif re.match(r'.*?:', structure_text):
                    member_match = re.search(r'(.*?):(.*?)(enum\[.*?\])?[:,\}\{]', structure_text)
                    data_type = member_match.group(2)
                    link_dict = {}
                    if member_match.group(3): # enum
                        link_dict = get_enum_dict(member_match.group(3))
                        data_type = 'enum'
                    else:
                        unit_match = re.search(r'(.*?)<(.*?\|.*?)>', data_type)
                        if unit_match: # unit & scaler
                            data_type = unit_match.group(1)
                            unit, scaler = unit_match.group(2).split('|')
                            if unit:
                                link_dict['unit'] = unit
                            if scaler:
                                link_dict['scaler'] = scaler
                    structure_list.append((member_match.group(1), data_type, link_dict, []))
                    structure_text = structure_text[len(member_match.group(0)) - 1:] # chk last character
                else:
                    data_type = structure_text
                    link_dict = {}
                    unit_match = re.search(r'(.*?)<(.*?\|.*?)>', data_type)
                    if unit_match: # unit & scaler
                        data_type = unit_match.group(1)
                        unit, scaler = unit_match.group(2).split('|')
                        if unit:
                            link_dict['unit'] = unit
                        if scaler:
                            link_dict['scaler'] = scaler
                    structure_list.append(('', data_type, link_dict, []))
                    structure_text = []
            # print('structure_list:', structure_list)
            return structure_list, structure_text
                
        structure_list = loop(structure_text)[0]

        if index != 0:
            try:
                if structure_list[0][1] == 'array':
                    structure_list = structure_list[0][3]
                elif structure_list[0][1] == 'structure':
                    structure_list = [structure_list[0][3][index - 1]]
            except IndexError:
                traceback.print_exc()
                structure_list = []
        print('structure_list:', structure_list)
        return structure_list

    def __get_explain(self, type, oad_omd_text):
        """get oad explain, return dict"""
        am_type = '属性' if type.strip() in ['oad', 'OAD'] else '方法'
        oad = re.sub(r'[^0-9a-fA-F]', '', oad_omd_text)[:8].upper()
        if len(oad) != 8:
            return {}
        oi_text = oad[:4]
        am_no = int(oad[4:6], 16) & 0x1f if am_type == '属性' else int(oad[4:6], 16)
        index = int(oad[6:8], 16)
        # print('oi_text', oi_text, 'am_no', am_no, 'index', index, 'am_type', am_type)

        for oi_row in self.oi_list:
            if oi_row.oi == oi_text:
                ic_no = int(oi_row.ic)
                oi_explain = oi_row.oi_name
                break
        else:
            return {}
        oi_row = [row for row in self.oi_list if row.am_choice == am_type\
                    and row.oi == oi_text and int(row.am_no) == am_no]
        ic_row = [row for row in self.ic_list if row.am_choice == am_type\
                    and int(row.ic) == ic_no and int(row.am_no) == am_no]
        if (not ic_row) and (not oi_row):
            return {}
        am_explain = oi_row[0].am_name if oi_row and oi_row[0].am_name else ic_row[0].am_name\
                        if ic_row and ic_row[0].am_name else ''
        if not am_explain:
            am_explain = '%s%d'%(am_type, am_no)
        
        index_explain = ''
        if index > 0:
            member_info = self.get_structure(type, oad[:6] + '00')[0]
            if member_info[1] == 'array':
                index_explain = '组%d'%index
            elif member_info[1] == 'structure':
                try:
                    index_explain = member_info[3][index-1][0]
                except IndexError:
                    print('index err: %d'%index)
                    index_explain += '索引%d'%index
            else:
                index_explain += '索引%d'%index

        return {'oi': oi_explain, 'am': am_explain, 'index': index_explain}

    def get_oi_explain(self, oi_text):
        """get oad explain"""
        return self.__get_explain('oad', oi_text + '0100').get('oi', '未定义')

    def get_oad_explain(self, oad_text):
        """get oad explain"""
        explain = self.__get_explain('oad', oad_text)
        if explain:
            ret = '%s-%s'%(explain.get('oi', ''), explain.get('am', ''))
            ret += '-%s'%explain.get('index', '') if explain.get('index', '') else ''
        else:
            ret = '未定义'
        return ret

    def get_omd_explain(self, omd_text):
        """get omd explain"""
        explain = self.__get_explain('omd', omd_text)
        return explain.get('oi', '') + explain.get('am', '')\
                + explain.get('index', '') if explain else '未定义'

    def get_rcsd_structure(self, m_list):
        """get rcsd structure"""
        offset = 0
        num = int(m_list[offset], 16)
        rcsd_structure = []
        offset += 1
        for _ in range(num):
            csd_choice = m_list[offset]
            offset += 1
            if csd_choice == '00':
                rcsd_structure.append(self.get_structure('oad', ''.join(m_list[offset: offset + 4])))
                offset += 4
            elif csd_choice == '01':
                link_type = self.get_oi_explain(''.join(m_list[offset: offset + 4]))
                link_load_structure = []
                offset += 4
                oad_num = int(m_list[offset], 16)
                offset += 1
                for _ in range(oad_num):
                    link_load_structure += self.get_structure('oad', ''.join(m_list[offset: offset + 4]))
                    offset += 4
                road_structure = [(link_type, 'structure', {}, link_load_structure)]
                rcsd_structure.append(road_structure)
            else:
                return []
        return rcsd_structure

    def get_class_oi(self, class_text):
        """get class oi"""
        oi_list = []
        last_oi = ''
        for row in self.oi_list:
            if row.ic_name == class_text.strip() and row.oi != last_oi:
                oi_list.append(row.oi + ' ' + row.oi_name)
                last_oi = row.oi
        return oi_list

    def get_oi_attr(self, oi_text):
        """get_oi_attr"""
        attr_list = []
        oi_row = [row for row in self.oi_list if row.am_choice == '属性'\
                    and row.oi == oi_text.strip()]
        if not oi_row:
            return attr_list
        ic_no = oi_row[0].ic
        ic_row = [row for row in self.ic_list if row.am_choice == '属性'\
                    and row.ic == ic_no]

        for count in range(31):
            for oi_r in oi_row:
                if count == int(oi_r.am_no) and oi_r.am_name:
                    attr_list.append(oi_r.am_no + ' ' + oi_r.am_name)
                    break
            else:
                for ic_r in ic_row:
                    if count == int(ic_r.am_no):
                        attr_list.append(ic_r.am_no + ' ' + ic_r.am_name)
                        break
        return attr_list


if __name__ == '__main__':
    test = Data698('123456')
    print(test.get_structure('oad', '24011300'))
    # print(test.get_omd_explain('601c7f00'))
    # print(test.get_structure('omd', '601c7f00'))
    # print(test.get_oi_explain('4401'))
    # print(test.get_class_oi('控制类'))
