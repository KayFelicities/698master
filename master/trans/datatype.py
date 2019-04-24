"""handle with 698 datatypes"""
from master.datas import k_data_s, base_data
from master import config
import copy


class TypeDo:
    """type do """
    def __init__(self, trans_res):
        """init"""
        self.trans_res = trans_res

    def take_PIID(self, m_list, brief='', depth=0):
        """take_PIID"""
        offset = 0
        piid = int(m_list[offset], 16)
        service_priority = '一般的' if piid >> 7 == 0 else '高级的'
        invoke_id = piid & 0x3f
        offset += 1
        self.trans_res.add_row(m_list[:offset], brief, 'PIID', \
                               '服务优先级:%s, 服务序号:%d'%(service_priority, invoke_id), depth=depth)
        return offset

    def take_PIID_ACD(self, m_list, brief='', depth=0):
        """take_PIID_ACD"""
        offset = 0
        piid_acd = int(m_list[offset], 16)
        service_priority = '一般的' if piid_acd >> 7 == 0 else '高级的'
        acd_text = '不请求' if (piid_acd >> 6) & 0x01 == 0 else '请求'
        invoke_id = piid_acd & 0x3f
        offset += 1
        self.trans_res.add_row(m_list[:offset], brief, 'PIID_ACD', \
                               '服务优先级:%s, 请求访问(ACD):%s, 服务序号:%d'%(service_priority, acd_text, invoke_id), depth=depth)
        return offset

    def take_OPTIONAL(self, m_list, brief='', depth=0):
        """take_OPTIONAL"""
        offset = 0
        optional = '有' if m_list[offset] == '01' else '无'
        offset += 1
        self.trans_res.add_row(m_list[:offset], brief, 'OPTIONAL', optional, depth=depth)
        return offset

    def take_CHOICE(self, m_list, brief='', depth=0, choice_dict=None):
        """take_CHOICE"""
        offset = 0
        choice = m_list[offset]
        if choice_dict is not None:
            choice_explain = choice_dict.get(choice, '错误')
        else:
            choice_explain = '未知'
        offset += 1
        self.trans_res.add_row(m_list[:offset], brief, 'CHOICE', choice_explain, depth=depth)
        return offset

    def take_axdr_len(self, m_list):
        """take_axdr_len"""
        offset = 0
        len_flag = int(m_list[offset], 16)
        offset += 1
        if len_flag >> 7 == 0:  # 单字节长度
            axdr_len = len_flag
        else:
            len_of_len = len_flag & 0x7f
            if len_of_len != 0:
                string_len = ''
                for count in range(len_of_len):
                    string_len += m_list[offset + count]
                offset += len_of_len
                axdr_len = int(string_len, 16)
            else:
                axdr_len = 128
        return {'offset': offset, 'len': axdr_len}

    def take_DAR(self, m_list, brief='', depth=0):
        """take_DAR"""
        offset = 0
        explain = base_data.get_dar(int(m_list[0], 16))
        offset += 1
        self.trans_res.add_row(m_list[:offset], brief, 'DAR', explain, depth=depth)
        return offset

    def take_ConnectMechanismInfo(self, m_list, brief='', depth=0):
        """take_ConnectMechanismInfo"""
        offset = 0
        connect_choice = m_list[offset]
        en_type = {'00': '公共连接', '01': '一般密码', '02': '对称加密', '03': '数字签名'}
        offset += self.take_CHOICE(m_list[offset:], brief, depth=depth, choice_dict=en_type)
        if connect_choice == '00':
            pass
        elif connect_choice == '01':
            offset += self.take_visible_string(m_list[offset:], 'PasswordSecurity', depth=depth + 1)
        elif connect_choice == '02':
            offset += self.take_octect_string(m_list[offset:], '密文1', depth=depth + 1)
            offset += self.take_octect_string(m_list[offset:], '客户机签名1', depth=depth + 1)
        elif connect_choice == '03':
            offset += self.take_octect_string(m_list[offset:], '密文2', depth=depth + 1)
            offset += self.take_octect_string(m_list[offset:], '客户机签名2', depth=depth + 1)
        return offset

    def take_ConnectResponseInfo(self, m_list, brief='', depth=0):
        """take_ConnectResponseInfo"""
        offset = 0
        connect_result = {
            '00': '允许建立应用连接',
            '01': '密码错误',
            '02': '对称解密错误',
            '03': '非对称解密错误',
            '04': '签名错误',
            '05': '协议版本不匹配',
            'FF': '其他错误'
        }
        offset += self.take_enum(m_list[offset:], '认证结果', depth=depth, enum_dict=connect_result)
        optional = m_list[offset]
        offset += self.take_OPTIONAL(m_list[offset:], '认证附加信息', depth=depth)
        if optional == '01':
            offset += self.take_RN(m_list[offset:], '服务器随机数', depth=depth)
            offset += self.take_octect_string(m_list[offset:], '服务器签名信息', depth=depth)
        return offset


    def take_FactoryVersion(self, m_list, brief='', depth=0):
        """take_FactoryVersion"""
        offset = 0
        offset += self.take_visible_string(m_list[offset:], '厂商代码:', 4, depth=depth)
        offset += self.take_visible_string(m_list[offset:], '软件版本号:', 4, depth=depth)
        offset += self.take_visible_string(m_list[offset:], '软件版本日期:', 6, depth=depth)
        offset += self.take_visible_string(m_list[offset:], '硬件版本号:', 4, depth=depth)
        offset += self.take_visible_string(m_list[offset:], '硬件版本日期:', 6, depth=depth)
        offset += self.take_visible_string(m_list[offset:], '厂家扩展信息:', 8, depth=depth)
        return offset


    def take_Data(self, m_list, brief='', depth=0, structure=None):
        """take data"""
        # print('data structure:', structure)
        offset = 0
        data_type = m_list[offset]
        if data_type == '00':    # 对null类型特殊处理
            data_info = structure.pop(0) if structure else None
            offset += self.take_NULL(m_list[offset:], depth=depth, data_info=data_info)
            return offset
        offset += 1
        self.trans_res.add_row(m_list[:offset], brief, 'Data', data_type, depth=depth)
        if data_type == '01':  # array
            data_info = structure.pop(0) if structure else None
            offset += self.take_array(m_list[offset:], brief=brief, depth=depth, data_info=data_info)
            return offset
        elif data_type == '02':  # structure
            data_info = structure.pop(0) if structure else None
            offset += self.take_structure(m_list[offset:], brief=brief, depth=depth, data_info=data_info)
            return offset
        elif data_type == '16':  # enum
            enum_dict = None
            if structure:
                member = structure.pop(0)
                brief = member[0]
                if member[1] == 'enum':
                    enum_dict = member[2]
            offset += self.take_enum(m_list[offset:], brief=brief, depth=depth, enum_dict=enum_dict)
            return offset
        else:
            data_info = structure.pop(0) if structure else None
            offset += {
                '00': self.take_NULL,
                # '01': self.take_array,
                # '02': self.take_structure,
                '03': self.take_bool,
                '04': self.take_bit_string,
                '05': self.take_double_long,
                '06': self.take_double_long_unsigned,
                '09': self.take_octect_string,
                '0A': self.take_visible_string,
                '0C': self.take_UTF8_string,
                '0F': self.take_integer,
                '10': self.take_long,
                '11': self.take_unsigned,
                '12': self.take_long_unsigned,
                '14': self.take_long64,
                '15': self.take_long64_unsigned,
                '16': self.take_enum,
                '17': self.take_float32,
                '18': self.take_float64,
                '19': self.take_date_time,
                '1A': self.take_date,
                '1B': self.take_time,
                '1C': self.take_date_time_s,
                '50': self.take_OI,
                '51': self.take_OAD,
                '52': self.take_ROAD,
                '53': self.take_OMD,
                '54': self.take_TI,
                '55': self.take_TSA,
                '56': self.take_MAC,
                '57': self.take_RN,
                '58': self.take_Region,
                '59': self.take_Scaler_Unit,
                '5A': self.take_RSD,
                '5B': self.take_CSD,
                '5C': self.take_MS,
                '5D': self.take_SID,
                '5E': self.take_SID_MAC,
                '5F': self.take_COMDCB,
                '60': self.take_RCSD,
            }[data_type](m_list[offset:], brief=brief, depth=depth, data_info=data_info)
            return offset


    def take_NULL(self, m_list, brief='', depth=0, data_info=None):
        """take_NULL"""
        offset = 0
        offset += 1
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'NULL', value='空', depth=depth)
        return offset


    def take_array(self, m_list, brief='', depth=0, data_info=None):
        """take_array"""
        offset = 0
        num = int(m_list[offset], 16)
        offset += 1
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, dtype='array[%d]'%num, \
                               value=num, unit='组', depth=depth)
        for _ in range(num):
            if data_info and data_info[1] == 'structure':  # fixme: rcsd array
                array_structure = [data_info[3].pop(0)] if data_info and data_info[3] else None
            else:
                array_structure = copy.deepcopy(data_info[3]) if data_info and data_info[3] else None
            offset += self.take_Data(m_list[offset:], depth=depth + 1, structure=array_structure)
        return offset


    def take_structure(self, m_list, brief='', depth=0, data_info=None):
        """take_structure"""
        offset = 0
        num = int(m_list[offset], 16)
        offset += 1
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, dtype='structure[%d]'%num, \
                               value=num, unit='个成员', depth=depth)
        for _ in range(num):
            structure_member = [data_info[3].pop(0)] if data_info and data_info[3] else None
            offset += self.take_Data(m_list[offset:], depth=depth + 1, structure=structure_member)
        return offset


    def take_bool(self, m_list, brief='', depth=0, data_info=None):
        """take_bool"""
        offset = 0
        bool_value = False if m_list[offset] == '00' else True
        offset += 1
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], \
                               brief + add_brief, 'bool', '是' if bool_value else '否', depth=depth)
        return offset


    def take_bit_string(self, m_list, bit_len=None, brief='', depth=0, data_info=None):
        """take_bit_string"""
        offset = 0
        if bit_len is None:
            res = self.take_axdr_len(m_list[offset:])
            offset += res['offset']
            bit_len = res['len']
        byte_len = (bit_len + 7) // 8
        bit_string_text = ''.join(m_list[offset: offset + byte_len])
        offset += byte_len
        bit_value = '空' if byte_len == 0 \
            else str(bin(int(bit_string_text, 16))).split('b')[1].rjust(bit_len, '0')
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'bit-string[%d]'%bit_len, \
                               bit_value, depth=depth)
        return offset


    def take_double_long(self, m_list, brief='', depth=0, data_info=None):
        """take_double_long"""
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = -(0x100000000 - int(''.join(m_list[offset : offset + 4]), 16))
        else:
            value = int(''.join(m_list[offset: offset + 4]), 16)
        offset += 4
        add_brief = data_info[0] if data_info else ''
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'double-long', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_double_long_unsigned(self, m_list, brief='', depth=0, data_info=None):
        """take_double_long_unsigned"""
        offset = 0
        value = int(''.join(m_list[offset: offset + 4]), 16)
        offset += 4
        add_brief = data_info[0] if data_info else ''
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'double-long-unsigned', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_octect_string(self, m_list, brief='', string_len=None, depth=0, data_info=None):
        """take_octect_string"""
        offset = 0
        if string_len is None:
            res = self.take_axdr_len(m_list[offset:])
            offset += res['offset']
            string_len = res['len']
        add_brief = data_info[0] if data_info else ''
        string_text = ''.join(m_list[offset: offset+string_len])
        if string_len == 4:
            string_text += '(' + '.'.join([str(int(x, 16)) for x in m_list[offset: offset+string_len]]) + ')'
        offset += string_len
        self.trans_res.add_row(m_list[:offset], brief + add_brief, \
                               'octect-string[%d]'%string_len, string_text, depth=depth)
        return offset


    def take_visible_string(self, m_list, brief='', string_len=None, depth=0, data_info=None):
        """take_visible_string"""
        offset = 0
        if string_len is None:
            res = self.take_axdr_len(m_list[offset:])
            offset += res['offset']
            string_len = res['len']
        string_text = ''
        for char in m_list[offset: offset + string_len]:
            string_text += chr(int(char, 16))
        offset += string_len
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, \
                               'visible-string[%d]'%string_len, string_text, depth=depth)
        return offset


    def take_UTF8_string(self, m_list, brief='', string_len=None, depth=0, data_info=None):
        """take_UTF8_string"""
        offset = 0
        if string_len is None:
            res = self.take_axdr_len(m_list[offset:])
            offset += res['offset']
            string_len = res['len']
        string_text = ''.join(m_list[offset: offset+string_len])
        offset += string_len
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, \
                               'UTF8-string[%d]'%string_len, string_text, depth=depth)
        return offset


    def take_integer(self, m_list, brief='', depth=0, data_info=None):
        """take_integer"""
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = -(0x100 - int(m_list[offset], 16))
        else:
            value = int(m_list[offset], 16)
        offset += 1
        add_brief = data_info[0] if data_info else ''
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'integer', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_long(self, m_list, brief='', depth=0, data_info=None):
        """take_long"""
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = -(0x10000 - int(m_list[offset] + m_list[offset + 1], 16))
        else:
            value = int(m_list[offset] + m_list[offset + 1], 16)
        offset += 2
        add_brief = data_info[0] if data_info else ''
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'long', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_unsigned(self, m_list, brief='', depth=0, data_info=None):
        """take_unsigned"""
        offset = 0
        value = int(m_list[offset], 16)
        offset += 1
        add_brief = data_info[0] if data_info else ''
        if add_brief.find('超时时间及重发次数') >= 0:
            value = '%d秒,%d次'%(value >> 2, value & 0x03)
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'unsigned', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_long_unsigned(self, m_list, brief='', depth=0, data_info=None):
        """take_long_unsigned"""
        offset = 0
        value = int(m_list[offset] + m_list[offset + 1], 16)
        offset += 2
        add_brief = data_info[0] if data_info else ''
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'long-unsigned', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_long64(self, m_list, brief='', depth=0, data_info=None):
        """take_long64"""
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = -(0x10000000000000000 - int(''.join(m_list[offset : offset + 8]), 16))
        else:
            value = int(''.join(m_list[offset : offset + 8]), 16)
        offset += 8
        add_brief = data_info[0] if data_info else ''
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'long64', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_long64_unsigned(self, m_list, brief='', depth=0, data_info=None):
        """take_long64_unsigned"""
        offset = 0
        value = int(''.join(m_list[offset : offset + 8]), 16)
        offset += 8
        add_brief = data_info[0] if data_info else ''
        unit = data_info[2].get('unit', '') if data_info else ''
        scaler = int(data_info[2].get('scaler', '0')) if data_info else 0
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'long64-unsigned', \
                               value, unit=unit, scaler=scaler, depth=depth)
        return offset


    def take_enum(self, m_list, brief='', depth=0, enum_dict=None, data_info=None):
        """take_enum"""
        offset = 0
        enum_explain = ''
        if enum_dict is not None:
            enum_explain = enum_dict.get(m_list[offset], '错误')
        offset += 1
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'enum', enum_explain, depth=depth)
        return offset


    def take_float32(self, m_list, brief='', depth=0, data_info=None):
        """take_float32, Kay check!"""
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = -(0x100000000 - int(''.join(m_list[offset : offset + 4]), 16))
        else:
            value = int(''.join(m_list[offset : offset + 4]), 16)
        offset += 4
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'float32', value, depth=depth)
        return offset


    def take_float64(self, m_list, brief='', depth=0, data_info=None):
        """take_float64"""
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = -(0x10000000000000000 - int(''.join(m_list[offset : offset + 8]), 16))
        else:
            value = int(''.join(m_list[offset : offset + 8]), 16)
        offset += 8
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'float64', value, depth=depth)
        return offset


    def take_date_time(self, m_list, brief='', depth=0, data_info=None):
        """take_date_time"""
        offset = 0
        year = int(m_list[0] + m_list[1], 16)
        month = int(m_list[2], 16)
        day = int(m_list[3], 16)
        hour = int(m_list[5], 16)
        minute = int(m_list[6], 16)
        second = int(m_list[7], 16)
        milliseconds = int(m_list[8] + m_list[9], 16)
        offset += 10
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'date_time', \
                               '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}:{6:03d}' \
                               .format(year, month, day, hour, minute, second, milliseconds), depth=depth)
        return offset


    def take_date(self, m_list, brief='', depth=0, data_info=None):
        """take_date"""
        offset = 0
        year = int(m_list[0] + m_list[1], 16)
        month = int(m_list[2], 16)
        day = int(m_list[3], 16)
        # week = int(m_list[4], 16)
        offset += 5
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'date', \
                               '{0:04d}-{1:02d}-{2:02d}'.format(year, month, day), depth=depth)
        return offset


    def take_time(self, m_list, brief='', depth=0, data_info=None):
        """take_time"""
        offset = 0
        hour = int(m_list[0], 16)
        minute = int(m_list[1], 16)
        second = int(m_list[2], 16)
        offset += 3
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'time', \
                               '{0:02d}:{1:02d}:{2:02d}'.format(hour, minute, second), depth=depth)
        return offset


    def take_date_time_s(self, m_list, brief='', depth=0, data_info=None):
        """take_date_time_s"""
        offset = 0
        year = int(m_list[0] + m_list[1], 16)
        month = int(m_list[2], 16)
        day = int(m_list[3], 16)
        hour = int(m_list[4], 16)
        minute = int(m_list[5], 16)
        second = int(m_list[6], 16)
        offset += 7
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'date_time_s', \
                               '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}' \
                               .format(year, month, day, hour, minute, second), depth=depth)
        return offset


    def take_OI(self, m_list, brief='', depth=0, data_info=None):
        """take_OI"""
        offset = 0
        explain = config.K_DATA.get_oi_explain(m_list[offset] + m_list[offset + 1])
        offset += 2
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'OI', explain, depth=depth, priority=2)
        return offset


    def take_OAD(self, m_list, brief='', depth=0, data_info=None):
        """take_OAD"""
        offset = 0
        explain = config.K_DATA.get_oad_explain(''.join(m_list[offset : offset + 4]))
        offset += 4
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'OAD', explain, depth=depth, priority=2)
        return offset


    def take_ROAD(self, m_list, brief='', depth=0, data_info=None):
        """take_ROAD"""
        offset = 0
        offset += self.take_OAD(m_list[offset:], depth=depth)
        oad_num = int(m_list[offset], 16)
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[offset: offset+1], brief + add_brief, 'ROAD[%d]'%oad_num, oad_num, depth=depth, unit='个')
        offset += 1
        for _ in range(oad_num):
            offset += self.take_OAD(m_list[offset:], depth=depth + 1)
        return offset


    def take_OMD(self, m_list, brief='', depth=0, data_info=None):
        """take_OMD"""
        offset = 0
        explain = config.K_DATA.get_omd_explain(''.join(m_list[offset : offset + 4]))
        offset += 4
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'OMD', explain, depth=depth, priority=2)
        return offset


    def take_TI(self, m_list, brief='', depth=0, data_info=None):
        """take_TI"""
        offset = 0
        uint = {
            '00': '秒',
            '01': '分',
            '02': '时',
            '03': '日',
            '04': '月',
            '05': '年',
        }.get(m_list[offset], '错误')
        value = int(m_list[offset + 1] + m_list[offset + 2], 16)
        offset = 3
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'TI', value, uint, depth=depth)
        return offset


    def take_TSA(self, m_list, brief='', depth=0, data_info=None):
        """take_TSA"""
        # print('Kay, take_TSA data:', data)
        offset = 0
        TSA_len = int(m_list[offset], 16)
        addr_text = ''
        if TSA_len != 0:
            addr_len = (int(m_list[offset + 1], 16) & 0x0f) + 1
            for tsa_count in range(addr_len):
                addr_text += m_list[offset + 2 + tsa_count]
        else:
            addr_len = 0
        offset += 1 + TSA_len
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'TSA[%d]'%addr_len, addr_text, depth=depth)
        return offset


    def take_MAC(self, m_list, brief='', depth=0, data_info=None):
        """take_MAC"""
        offset = 0
        offset += self.take_octect_string(m_list[offset:], 'MAC')
        return offset


    def take_RN(self, m_list, brief='', depth=0, data_info=None):
        """take_RN"""
        offset = 0
        offset += self.take_octect_string(m_list[offset:], 'RN')
        return offset


    def take_RN_MAC(self, m_list, brief='', depth=0, data_info=None):
        """take_RN_MAC"""
        offset = 0
        offset += self.take_octect_string(m_list[offset:], 'RN')
        offset += self.take_octect_string(m_list[offset:], 'MAC')
        return offset


    def take_Region(self, m_list, brief='', depth=0, data_info=None):
        """take_Region"""
        offset = 0
        r_uint = {
            '00': '前闭后开',
            '01': '前开后闭',
            '02': '前闭后闭',
            '03': '前开后开',
        }
        add_brief = data_info[0] if data_info else ''
        offset += self.take_enum(m_list[offset:], brief + add_brief, depth=depth, enum_dict=r_uint)
        offset += self.take_Data(m_list[offset:], brief='起始值', depth=depth)
        offset += self.take_Data(m_list[offset:], brief='结束值', depth=depth)
        return offset


    def take_Scaler_Unit(self, m_list, brief='', depth=0, data_info=None):
        """take_Scaler_Unit"""
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = -(0x100 - int(m_list[offset], 16))
        else:
            value = int(m_list[offset], 16)
        offset += 1

        unit = base_data.get_unit(int(m_list[offset], 16))
        offset += 1
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'Scaler_Unit', value, unit=unit, depth=depth)
        return offset


    def take_RSD(self, m_list, brief='', depth=0, data_info=None):
        """take_RSD"""
        offset = 0
        selector = m_list[offset]
        selector_choice = {'00': '不选择', '01': '方法1', '02': '方法2', '03': '方法3',
                           '04': '方法4', '05': '方法5', '06': '方法6', '07': '方法7',
                           '08': '方法8', '09': '方法9', '0A': '方法10',}
        offset += self.take_CHOICE(m_list[offset:], 'RSD选择方法', depth=depth, choice_dict=selector_choice)
        if selector == '00':
            pass
        elif selector == '01':
            offset += self.take_OAD(m_list[offset:], '对象属性描述符', depth=depth + 1)
            offset += self.take_Data(m_list[offset:], '数值', depth=depth + 1)
        elif selector == '02':
            offset += self.take_OAD(m_list[offset:], '对象属性描述符', depth=depth + 1)
            offset += self.take_Data(m_list[offset:], '起始值', depth=depth + 1)
            offset += self.take_Data(m_list[offset:], '结束值', depth=depth + 1)
            offset += self.take_Data(m_list[offset:], '数据间隔', depth=depth + 1)
        elif selector == '03':
            selector2_num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], '', 'SEQUENCE OF Selector2[%d]'%selector2_num, selector2_num, unit='个')
            offset += 1
            for _ in range(selector2_num):
                offset += self.take_OAD(m_list[offset:], '对象属性描述符', depth=depth + 1)
                offset += self.take_Data(m_list[offset:], '起始值', depth=depth + 1)
                offset += self.take_Data(m_list[offset:], '结束值', depth=depth + 1)
                offset += self.take_Data(m_list[offset:], '数据间隔', depth=depth + 1)
        elif selector in ['04', '05']:
            offset += self.take_date_time_s(m_list[offset:], \
                                            '采集启动时间' if selector == '04' else '采集存储时间', depth=depth + 1)
            offset += self.take_MS(m_list[offset:], '数值', depth=depth + 1)
        elif selector in ['06', '07', '08']:
            type_text = {
                '06': '采集启动时间',
                '07': '采集存储时间',
                '08': '采集成功时间',
            }.get(selector, '错误')
            offset += self.take_date_time_s(m_list[offset:], type_text + '起始值', depth=depth + 1)
            offset += self.take_date_time_s(m_list[offset:], type_text + '结束值', depth=depth + 1)
            offset += self.take_TI(m_list[offset:], '时间间隔', depth=depth + 1)
            offset += self.take_MS(m_list[offset:], '电能表集合', depth=depth + 1)
        elif selector == '09':
            offset += self.take_unsigned(m_list[offset:], '上第n次记录', depth=depth + 1)
        elif selector == '0A':
            offset += self.take_unsigned(m_list[offset:], '上n条记录', depth=depth + 1)
            offset += self.take_MS(m_list[offset:], '电能表集合', depth=depth + 1)
        return offset


    def take_CSD(self, m_list, brief='', depth=0, data_info=None):
        """take_CSD"""
        offset = 0
        csd_choice = m_list[offset]
        offset += 1
        # print('csd: ', csd_choice)
        if csd_choice == '00':
            self.trans_res.add_row(m_list[:offset], brief, 'CSD', 'OAD', depth=depth)
            offset += self.take_OAD(m_list[offset:], '', depth=depth + 1)
        elif csd_choice == '01':
            self.trans_res.add_row(m_list[:offset], brief, 'CSD', 'ROAD', depth=depth)
            offset += self.take_ROAD(m_list[offset:], '', depth=depth + 1)
        else:
            self.trans_res.add_row(m_list[:offset], brief, 'CSD', '未知CSD CHOICE', depth=depth)
        return offset


    def take_MS(self, m_list, brief='', depth=0, data_info=None):
        """take_MS"""
        offset = 0
        ms_choice = m_list[offset]
        ms_choice_dict = {'00': '无电能表', '01': '全部用户地址', '02': '一组用户类型',
                          '03': '一组用户地址', '04': '一组配置序号', '05': '一组用户类型区间',
                          '06': '一组用户地址区间', '07': '一组配置序号区间'}
        offset += self.take_CHOICE(m_list[offset:], 'MS', depth=depth, choice_dict=ms_choice_dict)
        # if ms_choice == '00':  # 无电能表
        #     offset += self.take_NULL(m_list[offset:], '无电能表')
        # elif ms_choice == '01':  # 全部用户地址
        #     offset += self.take_NULL(m_list[offset:], '全部用户地址')
        if ms_choice == '02':  # 一组用户类型
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], brief, \
                                   'SEQUENCE OF unsigned[%d]'%num, num, depth=depth, unit='组')
            offset += 1
            for _ in range(num):
                offset += self.take_unsigned(m_list[offset:], '用户类型', depth=depth + 1)
        elif ms_choice == '03':  # 一组用户地址
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], brief, \
                                   'SEQUENCE OF TSA[%d]'%num, num, depth=depth, unit='组')
            offset += 1
            for _ in range(num):
                offset += self.take_TSA(m_list[offset:], '用户地址', depth=depth + 1)
        elif ms_choice == '04':  # 一组配置序号
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], brief, \
                                   'SEQUENCE OF long-unsigned[%d]'%num, num, depth=depth, unit='组')
            offset += 1
            for _ in range(num):
                offset += self.take_long_unsigned(m_list[offset:], '配置序号', depth=depth + 1)
        elif ms_choice == '05':  # 一组用户类型区间
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], brief, \
                                   'SEQUENCE OF Region[%d]'%num, num, depth=depth, unit='组')
            offset += 1
            for _ in range(num):
                offset += self.take_Region(m_list[offset:], '用户类型区间', depth=depth + 1)
        elif ms_choice == '06':  # 一组用户地址区间
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], brief, \
                                   'SEQUENCE OF Region[%d]'%num, num, depth=depth, unit='组')
            offset += 1
            for _ in range(num):
                offset += self.take_Region(m_list[offset:], '用户地址区间', depth=depth + 1)
        elif ms_choice == '07':  # 一组配置序号区间
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], brief, \
                                   'SEQUENCE OF Region[%d]'%num, num, depth=depth, unit='组')
            offset += 1
            for _ in range(num):
                offset += self.take_Region(m_list[offset:], '配置序号区间:', depth=depth + 1)
        return offset


    def take_SID(self, m_list, brief='', depth=0, data_info=None):
        """take_SID"""
        offset = 0
        offset += self.take_double_long_unsigned(m_list[offset:], '标识', depth=depth)
        offset += self.take_octect_string(m_list[offset:], '附加数据', depth=depth)
        return offset


    def take_SID_MAC(self, m_list, brief='', depth=0, data_info=None):
        """take_SID_MAC"""
        offset = 0
        offset += self.take_SID(m_list[offset:], '安全标识', depth=depth)
        offset += self.take_MAC(m_list[offset:], '数据MAC', depth=depth)
        return offset


    def take_COMDCB(self, m_list, brief='', depth=0, data_info=None):
        """take_COMDCB"""
        offset = 0
        rate_dict = {
            '00': '300bps',
            '01': '600bps',
            '02': '1200bps',
            '03': '2400bps',
            '04': '4800bps',
            '05': '7200bps',
            '06': '9600bps',
            '07': '19200bps',
            '08': '38400bps',
            '09': '57600bps',
            '0A': '15200bps',
            'FF': '自适应',
        }
        offset += self.take_enum(m_list[offset:], brief='波特率', enum_dict=rate_dict, depth=depth)
        offset += self.take_enum(m_list[offset:], brief='校验位', \
                                 enum_dict={'00': '无校验', '01': '奇校验', '02': '偶校验'}, depth=depth)
        offset += self.take_enum(m_list[offset:], brief='数据位', \
                                 enum_dict={'05': '5', '06': '6', '07': '7', '08': '8'}, depth=depth)
        offset += self.take_enum(m_list[offset:], brief='停止位', \
                                 enum_dict={'01': '1', '02': '2'}, depth=depth)
        offset += self.take_enum(m_list[offset:], brief='流控', \
                                 enum_dict={'00': '无', '01': '硬件', '02': '软件'}, depth=depth)
        return offset


    def take_RCSD(self, m_list, brief='', depth=0, data_info=None):
        """take_RCSD"""
        offset = 0
        num = int(m_list[offset], 16)
        offset += 1
        add_brief = data_info[0] if data_info else ''
        self.trans_res.add_row(m_list[:offset], brief + add_brief, 'SEQUENCE OF CSD[%d]'%num, num, depth=depth, unit='个')
        for _ in range(num):
            offset += self.take_CSD(m_list[offset:], depth=depth + 1)
        return offset
