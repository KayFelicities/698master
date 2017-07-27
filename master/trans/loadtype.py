"""load type"""
from master import config
if config.IS_USE_PYSIDE:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore


def take_axdr_len(m_list):
    """take_axdr_len"""
    offset = 0
    len_flag = int(m_list[offset], 16)
    offset += 1
    if len_flag >> 7 == 0:  # 单字节长度
        axdr_len = len_flag
    else:
        len_of_len = len_flag & 0x7f
        string_len = ''
        for count in range(len_of_len):
            string_len += m_list[offset + count]
        offset += len_of_len
        axdr_len = int(string_len, 16)
    return {'offset': offset, 'len': axdr_len}


def data2table(data_list, table):
    """data to table items"""
    take_Data(data_list, table, depth=0)


def take_Data(data_list, table, depth=0):
    offset = 0
    print('data list: ', data_list)
    data_type = data_list[offset]
    # if data_type == '00':    # 对null类型特殊处理
    #     offset += take_NULL(data_list[offset:], depth=depth)
    #     return offset
    offset += 1
    offset += {
        '00': take_NULL,
        '01': take_array,
        '02': take_structure,
        '03': take_bool,
        # '04': take_bit_string,
        '05': take_double_long,
        '06': take_double_long_unsigned,
        '09': take_octect_string,
        # '0A': take_visible_string,
        # '0C': take_UTF8_string,
        '0F': take_integer,
        '10': take_long,
        '11': take_unsigned,
        '12': take_long_unsigned,
        '14': take_long64,
        '15': take_long64_unsigned,
        '16': take_enum,
        # '17': take_float32,
        # '18': take_float64,
        '19': take_date_time,
        # '1A': take_date,
        # '1B': take_time,
        '1C': take_date_time_s,
        # '50': take_OI,
        # '51': take_OAD,
        # '52': take_ROAD,
        # '53': take_OMD,
        # '54': take_TI,
        # '55': take_TSA,
        # '56': take_MAC,
        # '57': take_RN,
        # '58': take_Region,
        # '59': take_Scaler_Unit,
        # '5A': take_RSD,
        # '5B': take_CSD,
        # '5C': take_MS,
        # '5D': take_SID,
        # '5E': take_SID_MAC,
        # '5F': take_COMDCB,
        # '60': take_RCSD,
    }[data_type](data_list[offset:], table)
    return offset


def take_NULL(data_list, table, depth=0):
    """take_NULL"""
    offset = 0
    offset += 1
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('NULL')
    table.setItem(table_row_num, 0, item)
    return offset


def take_array(data_list, table, depth=0):
    """take_array"""
    offset = 0
    num = int(data_list[offset], 16)
    offset += 1

    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('array')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QSpinBox()
    box.setRange(0, 30)
    box.setValue(num)
    table.setCellWidget(table_row_num, 1, box)

    for _ in range(num):
        offset += take_Data(data_list[offset:], table, depth=depth + 1)
    return offset


def take_structure(data_list, table, depth=0):
    """take_structure"""
    offset = 0
    num = int(data_list[offset], 16)
    offset += 1
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('structure')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QSpinBox()
    box.setRange(0, 30)
    box.setValue(num)
    table.setCellWidget(table_row_num, 1, box)

    for _ in range(num):
        offset += take_Data(data_list[offset:], table, depth=depth + 1)
    return offset


def take_bool(data_list, table, depth=0):
    """take_bool"""
    offset = 0
    bool_value = 0 if data_list[offset] == '00' else 1
    offset += 1
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('bool')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QComboBox()
    box.addItems(('False', 'True'))
    box.setv(bool_value)
    table.setCellWidget(table_row_num, 1, box)
    return offset


# def take_bit_string(data_list, bit_len=None, table, depth=0):
#     """take_bit_string"""
#     offset = 0
#     if bit_len is None:
#         res = take_axdr_len(data_list[offset:])
#         offset += res['offset']
#         bit_len = res['len']
#     byte_len = (bit_len + 7) // 8
#     bit_string_text = ''.join(data_list[offset: offset + byte_len])
#     offset += byte_len
#     bit_value = '空' if byte_len == 0\
#             else str(bin(int(bit_string_text, 16))).split('b')[1].rjust(bit_len, '0')
#     trans_res.add_row(data_list[:offset], brief, 'bit-string[%d]'%bit_len,\
#                             bit_value, depth=depth)
#     return offset


def take_double_long(data_list, table, depth=0):
    """take_double_long"""
    offset = 0
    if int(data_list[offset], 16) >> 7 == 1:  # 负数
        value = -(0x100000000 - int(''.join(data_list[offset : offset + 4]), 16))
    else:
        value = int(''.join(data_list[offset: offset + 4]), 16)
    offset += 4
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_double_long_unsigned(data_list, table, depth=0):
    """take_double_long_unsigned"""
    offset = 0
    value = int(''.join(data_list[offset: offset + 4]), 16)
    offset += 4
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_octect_string(data_list, table, string_len=None, depth=0):
    """take_octect_string"""
    offset = 0
    if string_len is None:
        res = take_axdr_len(data_list[offset:])
        offset += res['offset']
        string_len = res['len']
    string_text = ''.join(data_list[offset: offset+string_len])
    offset += string_len
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('octect_string')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    if string_len == 4: # 暂时这样匹配ip
        box.setText('%d.%d.%d.%d'%(int(string_text[0:2], 16), int(string_text[2:4], 16),\
                                    int(string_text[4:6], 16), int(string_text[6:8], 16)))
    else:
        box.setText(string_text)
    table.setCellWidget(table_row_num, 1, box)
    return offset


# def take_visible_string(data_list, table, string_len=None, depth=0):
#     """take_visible_string"""
#     offset = 0
#     if string_len is None:
#         res = take_axdr_len(data_list[offset:])
#         offset += res['offset']
#         string_len = res['len']
#     string_text = ''
#     for char in data_list[offset: offset + string_len]:
#         string_text += chr(int(char, 16))
#     offset += string_len
#     trans_res.add_row(data_list[:offset], brief,\
#             'visible-string[%d]'%string_len, string_text, depth=depth)
#     return offset


# def take_UTF8_string(data_list, table, string_len=None, depth=0):
#     """take_UTF8_string"""
#     offset = 0
#     if string_len is None:
#         res = take_axdr_len(data_list[offset:])
#         offset += res['offset']
#         string_len = res['len']
#     string_text = ''.join(data_list[offset: offset+string_len])
#     offset += string_len
#     trans_res.add_row(data_list[:offset], brief,\
#             'UTF8-string[%d]'%string_len, string_text, depth=depth)
#     return offset


def take_integer(data_list, table, depth=0):
    """take_integer"""
    offset = 0
    if int(data_list[offset], 16) >> 7 == 1:  # 负数
        value = -(0x100 - int(data_list[offset], 16))
    else:
        value = int(data_list[offset], 16)
    offset += 1
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_long(data_list, table, depth=0):
    """take_long"""
    offset = 0
    if int(data_list[offset], 16) >> 7 == 1:  # 负数
        value = -(0x10000 - int(data_list[offset] + data_list[offset + 1], 16))
    else:
        value = int(data_list[offset] + data_list[offset + 1], 16)
    offset += 2
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_unsigned(data_list, table, depth=0):
    """take_unsigned"""
    offset = 0
    value = int(data_list[offset], 16)
    offset += 1
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_long_unsigned(data_list, table, depth=0):
    """take_long_unsigned"""
    offset = 0
    value = int(data_list[offset] + data_list[offset + 1], 16)
    offset += 2
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_long64(data_list, table, depth=0):
    """take_long64"""
    offset = 0
    if int(data_list[offset], 16) >> 7 == 1:  # 负数
        value = -(0x10000000000000000 - int(''.join(data_list[offset : offset + 8]), 16))
    else:
        value = int(''.join(data_list[offset : offset + 8]), 16)
    offset += 8
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_long64_unsigned(data_list, table, depth=0):
    """take_long64_unsigned"""
    offset = 0
    value = int(''.join(data_list[offset : offset + 8]), 16)
    offset += 8
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('long_unsigned')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


def take_enum(data_list, table, depth=0, enum_dict=None):
    """take_enum"""
    offset = 0
    value = data_list[offset]
    offset += 1
    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('enum')
    table.setItem(table_row_num, 0, item)
    box = QtGui.QTextEdit()
    box.setText(str(value))
    table.setCellWidget(table_row_num, 1, box)
    return offset


# def take_float32(data_list, table, depth=0):
#     """take_float32, Kay check!"""
#     offset = 0
#     if int(data_list[offset], 16) >> 7 == 1:  # 负数
#         value = -(0x100000000 - int(''.join(data_list[offset : offset + 4]), 16))
#     else:
#         value = int(''.join(data_list[offset : offset + 4]), 16)
#     offset += 4
#     trans_res.add_row(data_list[:offset], brief, 'float32', value, depth=depth)
#     return offset


# def take_float64(data_list, table, depth=0):
#     """take_float64"""
#     offset = 0
#     if int(data_list[offset], 16) >> 7 == 1:  # 负数
#         value = -(0x10000000000000000 - int(''.join(data_list[offset : offset + 8]), 16))
#     else:
#         value = int(''.join(data_list[offset : offset + 8]), 16)
#     offset += 8
#     trans_res.add_row(data_list[:offset], brief, 'float64', value, depth=depth)
#     return offset


def take_date_time(data_list, table, depth=0):
    """take_date_time"""
    offset = 0
    year = int(data_list[0] + data_list[1], 16)
    month = int(data_list[2], 16)
    day = int(data_list[3], 16)
    hour = int(data_list[5], 16)
    minute = int(data_list[6], 16)
    second = int(data_list[7], 16)
    milliseconds = int(data_list[8] + data_list[9], 16)
    offset += 10

    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('date_time')
    table.setItem(table_row_num, 0, item)
    dt_w = QtGui.QDateTimeEdit()
    dt_read = QtCore.QDateTime(year, month, day, hour, minute, second)
    dt_w.setDateTime(dt_read)
    table.setCellWidget(table_row_num, 1, dt_w)
    return offset


# def take_date(data_list, table, depth=0):
#     """take_date"""
#     offset = 0
#     year = int(data_list[0] + data_list[1], 16)
#     month = int(data_list[2], 16)
#     day = int(data_list[3], 16)
#     # week = int(data_list[4], 16)
#     offset += 5
#     trans_res.add_row(data_list[:offset], brief, 'date',\
#         '{0:04d}-{1:02d}-{2:02d}'.format(year, month, day), depth=depth)
#     return offset


# def take_time(data_list, table, depth=0):
#     """take_time"""
#     offset = 0
#     hour = int(data_list[0], 16)
#     minute = int(data_list[1], 16)
#     second = int(data_list[2], 16)
#     offset += 3
#     trans_res.add_row(data_list[:offset], brief, 'time',\
#         '{0:02d}:{1:02d}:{2:02d}'.format(hour, minute, second), depth=depth)
#     return offset


def take_date_time_s(data_list, table, depth=0):
    """take_date_time_s"""
    offset = 0
    year = int(data_list[0] + data_list[1], 16)
    month = int(data_list[2], 16)
    day = int(data_list[3], 16)
    hour = int(data_list[4], 16)
    minute = int(data_list[5], 16)
    second = int(data_list[6], 16)
    offset += 7

    table_row_num = table.rowCount()
    table.insertRow(table_row_num)
    item = QtGui.QTableWidgetItem('date_time_s')
    table.setItem(table_row_num, 0, item)
    dt_w = QtGui.QDateTimeEdit()
    dt_read = QtCore.QDateTime(year, month, day, hour, minute, second)
    dt_w.setDateTime(dt_read)
    table.setCellWidget(table_row_num, 1, dt_w)
    return offset


# def take_OI(data_list, table, depth=0):
#     """take_OI"""
#     offset = 0
#     explain = oads.OAD.get(data_list[offset] + data_list[offset + 1] + '01', '未知OI').split('，')[0]
#     offset += 2
#     trans_res.add_row(data_list[:offset], brief, 'OI', explain, depth=depth, priority=2)
#     return offset


# def take_OAD(data_list, table, depth=0):
#     """take_OAD"""
#     offset = 0
#     attr = int(data_list[offset + 2], 16)
#     index = int(data_list[offset + 3], 16)
#     explain = oads.OAD.get(''.join(data_list[offset : offset + 3]),\
#                 oads.OAD.get(''.join(data_list[offset : offset + 2]) + '01',\
#                 '未知OAD').split('[')[0] + '[属性%d]'%attr) + '[索引%d]'%index
#     offset += 4
#     trans_res.add_row(data_list[:offset], brief, 'OAD', explain, depth=depth, priority=2)
#     return offset


# def take_ROAD(data_list, table, depth=0):
#     """take_ROAD"""
#     offset = 0
#     offset += take_OAD(data_list[offset:], depth=depth)
#     oad_num = int(data_list[offset], 16)
#     trans_res.add_row(data_list[offset: offset+1], brief, 'ROAD[%d]'%oad_num, oad_num, depth=depth)
#     offset += 1
#     for _ in range(oad_num):
#         offset += take_OAD(data_list[offset:], depth=depth + 1)
#     return offset


# def take_OMD(data_list, table, depth=0):
#     """take_OMD"""
#     offset = 0
#     method = int(data_list[offset + 2], 16)
#     mode = int(data_list[offset + 3], 16)
#     explain = omds.OMD.get(''.join(data_list[offset : offset + 3]),\
#                 omds.OMD.get(''.join(data_list[offset : offset + 2]) + '01',\
#                 '未知OMD').split('[')[0] + '[方法%d]'%method) + '[操作模式%d]'%mode
#     offset += 4
#     trans_res.add_row(data_list[:offset], brief, 'OMD', explain, depth=depth, priority=2)
#     return offset


# def take_TI(data_list, table, depth=0):
#     """take_TI"""
#     offset = 0
#     uint = {
#         '00': '秒',
#         '01': '分',
#         '02': '时',
#         '03': '日',
#         '04': '月',
#         '05': '年',
#     }.get(data_list[offset], '错误')
#     value = int(data_list[offset + 1] + data_list[offset + 2], 16)
#     offset = 3
#     trans_res.add_row(data_list[:offset], brief, 'TI', value, uint, depth=depth)
#     return offset


# def take_TSA(data_list, table, depth=0):
#     """take_TSA"""
#     # print('Kay, take_TSA data:', data)
#     offset = 0
#     TSA_len = int(data_list[offset], 16)
#     addr_text = ''
#     if TSA_len != 0:
#         addr_len = int(data_list[offset + 1], 16) + 1
#         for tsa_count in range(addr_len):
#             addr_text += data_list[offset + 2 + tsa_count]
#     else:
#         addr_len = 0
#     offset += 1 + TSA_len
#     trans_res.add_row(data_list[:offset], brief, 'TSA[%d]'%addr_len, addr_text, depth=depth)
#     return offset


# def take_MAC(data_list, table, depth=0):
#     """take_MAC"""
#     offset = 0
#     offset += take_octect_string(data_list[offset:], 'MAC')
#     return offset


# def take_RN(data_list, table, depth=0):
#     """take_RN"""
#     offset = 0
#     offset += take_octect_string(data_list[offset:], 'RN')
#     return offset


# def take_RN_MAC(data_list, table, depth=0):
#     """take_RN_MAC"""
#     offset = 0
#     offset += take_octect_string(data_list[offset:], 'RN')
#     offset += take_octect_string(data_list[offset:], 'MAC')
#     return offset


# def take_Region(data_list, table, depth=0):
#     """take_Region"""
#     offset = 0
#     r_uint = {
#         '00': '前闭后开',
#         '01': '前开后闭',
#         '02': '前闭后闭',
#         '03': '前开后开',
#     }
#     offset += take_enum(data_list[offset:], brief, depth=depth, enum_dict=r_uint)
#     offset += take_Data(data_list, brief='起始值', depth=depth)
#     offset += take_Data(data_list, brief='结束值', depth=depth)
#     return offset


# def take_Scaler_Unit(data_list, table, depth=0):
#     """take_Scaler_Unit"""
#     offset = 0
#     if int(data_list[offset], 16) >> 7 == 1:  # 负数
#         value = -(0x100 - int(data_list[offset], 16))
#     else:
#         value = int(data_list[offset], 16)
#     offset += 1

#     unit = units.UNIT.get(int(data_list[offset], 16), '无效单位')
#     offset += 1
#     trans_res.add_row(data_list[:offset], brief, 'Scaler_Unit', value, unit=unit, depth=depth)
#     return offset


# def take_RSD(data_list, table, depth=0):
#     """take_RSD"""
#     offset = 0
#     selector = data_list[offset]
#     selector_choice = {'00': '不选择', '01': '方法1', '02': '方法2', '03': '方法3',
#                         '04': '方法4', '05': '方法5', '06': '方法6', '07': '方法7',
#                         '08': '方法8', '09': '方法9', '0A': '方法10',}
#     offset += take_CHOICE(data_list[offset:], 'RSD选择方法', depth=depth, choice_dict=selector_choice)
#     if selector == '00':
#         pass
#     elif selector == '01':
#         offset += take_OAD(data_list[offset:], '对象属性描述符', depth=depth + 1)
#         offset += take_Data(data_list[offset:], '数值', depth=depth + 1)
#     elif selector == '02':
#         offset += take_OAD(data_list[offset:], '对象属性描述符', depth=depth + 1)
#         offset += take_Data(data_list[offset:], '起始值', depth=depth + 1)
#         offset += take_Data(data_list[offset:], '结束值', depth=depth + 1)
#         offset += take_Data(data_list[offset:], '数据间隔', depth=depth + 1)
#     elif selector == '03':
#         selector2_num = int(data_list[offset], 16)
#         trans_res.add_row(data_list[offset: offset+1], '', 'SEQUENCE OF Selector2[%d]'%selector2_num, selector2_num)
#         offset += 1
#         for _ in range(selector2_num):
#             offset += take_OAD(data_list[offset:], '对象属性描述符', depth=depth + 1)
#             offset += take_Data(data_list[offset:], '起始值', depth=depth + 1)
#             offset += take_Data(data_list[offset:], '结束值', depth=depth + 1)
#             offset += take_Data(data_list[offset:], '数据间隔', depth=depth + 1)
#     elif selector in ['04', '05']:
#         offset += take_date_time_s(data_list[offset:],\
#                         '采集启动时间' if selector == '04' else '采集存储时间', depth=depth + 1)
#         offset += take_MS(data_list[offset:], '数值', depth=depth + 1)
#     elif selector in ['06', '07', '08']:
#         type_text = {
#             '06': '采集启动时间',
#             '07': '采集存储时间',
#             '08': '采集成功时间',
#         }.get(selector, '错误')
#         offset += take_date_time_s(data_list[offset:], type_text + '起始值', depth=depth + 1)
#         offset += take_date_time_s(data_list[offset:], type_text + '结束值', depth=depth + 1)
#         offset += take_TI(data_list[offset:], '时间间隔', depth=depth + 1)
#         offset += take_MS(data_list[offset:], '电能表集合', depth=depth + 1)
#     elif selector == '09':
#         offset += take_unsigned(data_list[offset:], '上第n次记录', depth=depth + 1)
#     elif selector == '0A':
#         offset += take_unsigned(data_list[offset:], '上n条记录', depth=depth + 1)
#         offset += take_MS(data_list[offset:], '电能表集合', depth=depth + 1)
#     return offset


# def take_CSD(data_list, table, depth=0):
#     """take_CSD"""
#     offset = 0
#     csd_choice = data_list[offset]
#     offset += 1
#     print('csd: ', csd_choice)
#     if csd_choice == '00':
#         trans_res.add_row(data_list[:offset], brief, 'CSD', 'OAD', depth=depth)
#         offset += take_OAD(data_list[offset:], '对象属性描述符', depth=depth)
#     elif csd_choice == '01':
#         trans_res.add_row(data_list[:offset], brief, 'CSD', 'ROAD', depth=depth)
#         offset += take_ROAD(data_list[offset:], '记录型对象属性描述符', depth=depth)
#     else:
#         trans_res.add_row(data_list[:offset], brief, 'CSD', '未知CSD CHOICE', depth=depth)
#     return offset


# def take_MS(data_list, table, depth=0):
#     """take_MS"""
#     offset = 0
#     ms_choice = data_list[0]
#     ms_choice_dict = {'00': '无电能表', '01': '全部用户地址', '02': '一组用户类型',
#                         '03': '一组用户地址', '04': '一组配置序号', '05': '一组用户类型区间',
#                         '06': '一组用户地址区间', '07': '一组配置序号区间'}
#     offset += take_CHOICE(data_list[offset:], 'MS', depth=depth, choice_dict=ms_choice_dict)
#     # if ms_choice == '00':  # 无电能表
#     #     offset += take_NULL(data_list[offset:], '无电能表')
#     # elif ms_choice == '01':  # 全部用户地址
#     #     offset += take_NULL(data_list[offset:], '全部用户地址')
#     if ms_choice == '02':  # 一组用户类型
#         num = int(data_list[1], 16)
#         trans_res.add_row(data_list[offset: offset+1], brief,\
#                                 'SEQUENCE OF unsigned[%d]'%num, num, depth=depth)
#         offset += 1
#         for _ in range(num):
#             offset += take_unsigned(data_list[offset:], '用户类型', depth=depth + 1)
#     elif ms_choice == '03':  # 一组用户地址
#         num = int(data_list[1], 16)
#         trans_res.add_row(data_list[offset: offset+1], brief,\
#                                 'SEQUENCE OF TSA[%d]'%num, num, depth=depth)
#         offset += 1
#         for _ in range(num):
#             offset += take_TSA(data_list[offset:], '用户地址', depth=depth + 1)
#     elif ms_choice == '04':  # 一组配置序号
#         num = int(data_list[1], 16)
#         trans_res.add_row(data_list[offset: offset+1], brief,\
#                                 'SEQUENCE OF long-unsigned[%d]'%num, num, depth=depth)
#         offset += 1
#         for _ in range(num):
#             offset += take_long_unsigned(data_list[offset:], '配置序号', depth=depth + 1)
#     elif ms_choice == '05':  # 一组用户类型区间
#         offset = 0
#         num = int(data_list[1], 16)
#         trans_res.add_row(data_list[offset: offset+1], brief,\
#                                 'SEQUENCE OF Region[%d]'%num, num, depth=depth)
#         offset += 1
#         for _ in range(num):
#             offset += take_Region(data_list[offset:], '用户类型区间', depth=depth + 1)
#     elif ms_choice == '06':  # 一组用户地址区间
#         offset = 0
#         num = int(data_list[1], 16)
#         trans_res.add_row(data_list[offset: offset+1], brief,\
#                                 'SEQUENCE OF Region[%d]'%num, num, depth=depth)
#         offset += 1
#         for _ in range(num):
#             offset += take_Region(data_list[offset:], '用户地址区间', depth=depth + 1)
#     elif ms_choice == '07':  # 一组配置序号区间
#         offset = 0
#         num = int(data_list[1], 16)
#         trans_res.add_row(data_list[offset: offset+1], brief,\
#                                 'SEQUENCE OF Region[%d]'%num, num, depth=depth)
#         offset += 1
#         for _ in range(num):
#             offset += take_Region(data_list[offset:], '配置序号区间:', depth=depth + 1)
#     return offset


# def take_SID(data_list, table, depth=0):
#     """take_SID"""
#     offset = 0
#     offset += take_double_long_unsigned(data_list[offset:], '标识', depth=depth)
#     offset += take_octect_string(data_list[offset:], '附加数据', depth=depth)
#     return offset


# def take_SID_MAC(data_list, table, depth=0):
#     """take_SID_MAC"""
#     offset = 0
#     offset += take_SID(data_list[offset:], '安全标识', depth=depth)
#     offset += take_MAC(data_list[offset:], '数据MAC', depth=depth)
#     return offset


# def take_COMDCB(data_list, table, depth=0):
#     """take_COMDCB"""
#     offset = 0
#     rate_dict = {
#         '00': '300bps',
#         '01': '600bps',
#         '02': '1200bps',
#         '03': '2400bps',
#         '04': '4800bps',
#         '05': '7200bps',
#         '06': '9600bps',
#         '07': '19200bps',
#         '08': '38400bps',
#         '09': '57600bps',
#         '0A': '15200bps',
#         'FF': '自适应',
#     }
#     offset += take_enum(data_list[offset:], brief='波特率', enum_dict=rate_dict, depth=depth)
#     offset += take_enum(data_list[offset:], brief='校验位',\
#             enum_dict={'00': '无校验', '01': '奇校验', '02': '偶校验'}, depth=depth)
#     offset += take_enum(data_list[offset:], brief='数据位',\
#             enum_dict={'05': '5', '06': '6', '07': '7', '08': '8'}, depth=depth)
#     offset += take_enum(data_list[offset:], brief='停止位',\
#             enum_dict={'01': '1', '02': '2'}, depth=depth)
#     offset += take_enum(data_list[offset:], brief='流控',\
#             enum_dict={'00': '无', '01': '硬件', '02': '软件'}, depth=depth)
#     return offset


# def take_RCSD(data_list, table, depth=0):
#     """take_RCSD"""
#     offset = 0
#     num = int(data_list[offset], 16)
#     offset += 1
#     trans_res.add_row(data_list[:offset], brief, 'SEQUENCE OF CSD[%d]'%num, num, depth=depth)
#     for _ in range(num):
#         offset += take_CSD(data_list[offset:], depth=depth + 1)
#     return offset
