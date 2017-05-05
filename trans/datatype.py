'''handle with 698 datatypes'''
import trans.datas as database

class TypeDo():
    '''type do '''
    def __init__(self, trans_res):
        '''init'''
        self.trans_res = trans_res

    def take_PIID(self, m_list, add_text='', depth=0):
        '''take_PIID'''
        offset = 0
        piid = int(m_list[offset], 16)
        service_priority = '一般的' if piid >> 7 == 0 else '高级的'
        invoke_id = piid & 0x3f
        self.trans_res.add_row(m_list[offset:], 1,\
                '%s(服务优先级:%s, 服务序号:%d'%(add_text, service_priority, invoke_id), depth=depth)
        offset += 1
        return offset

    def take_PIID_ACD(self, m_list, add_text='', depth=0):
        '''take_PIID_ACD'''
        offset = 0
        piid_acd = int(m_list[offset], 16)
        service_priority = '一般的' if piid_acd >> 7 == 0 else '高级的'
        acd_text = '不请求' if (piid_acd >> 6) & 0x01 == 0 else '请求'
        invoke_id = piid_acd & 0x3f
        self.trans_res.add_row(m_list[offset:], 1,\
                '%s(服务优先级:%s, 请求访问(ACD):%s, 服务序号:%d)'\
                %(add_text, service_priority, acd_text, invoke_id), depth=depth)
        offset += 1
        return offset

    # def take_FollowReport(self, m_list, add_text='', depth=0):
    #     offset = 0
    #     follow_report_option = m_list[offset]
    #     offset += take_OPTIONAL(m_list[offset:], '跟随上报信息域')
    #     if follow_report_option == '01':
    #         follow_report_choice = m_list[offset]
    #         show_data_source(m_list[offset:], 1)
    #         if follow_report_choice == '01':
    #             result_normal_num = get_num_of_SEQUENCE(m_list[offset:], '对象属性及其数据')
    #             offset += 1
    #             config.line_depth += 1
    #             for result_normal_count in range(result_normal_num):
    #                 end_flag = 1 if result_normal_count == result_normal_num - 1 else 0
    #                 offset += take_A_ResultNormal(m_list[offset:], end_flag=end_flag)
    #             config.line_depth -= 1
    #         elif follow_report_choice == '02':
    #             result_record_num = get_num_of_SEQUENCE(m_list[offset:], '对象属性及其数据')
    #             offset += 1
    #             config.line_depth += 1
    #             for result_record_count in range(result_record_num):
    #                 end_flag = 1 if result_record_count == result_record_num - 1 else 0
    #                 offset += take_A_ResultRecord(m_list[offset:], end_flag=end_flag)
    #             config.line_depth -= 1
    #     return offset

    # def take_TimeTag(self, m_list, add_text='', depth=0):
    #     offset = 0
    #     timetag_option = m_list[offset]
    #     offset += take_OPTIONAL(m_list[offset:], '时间标签')
    #     if timetag_option == '01':
    #         offset += take_date_time_s(m_list[offset:], '发送时标')
    #         offset += take_TI(m_list[offset:], '允许传输延时时间')
    #     return offset

    def take_OPTIONAL(self, m_list, add_text='', depth=0):
        '''take_OPTIONAL'''
        offset = 0
        optional = '有' if m_list[offset] == '01' else '无'
        self.trans_res.add_row(m_list[offset:], 1, '%s(OPTIONAL:%s)'%(add_text, optional), depth=depth)
        offset += 1
        return offset

    def take_CHOICE(self, m_list, add_text='', choice_dict=None):
        '''take_CHOICE'''
        offset = 0
        choice = m_list[offset]
        if choice_dict is not None:
            choice_explain = choice_dict.get(choice, '错误')
        else:
            choice_explain = '未知'
        self.trans_res.add_row(m_list[offset:], 1,\
                '%s(CHOICE:%s)'%(add_text, choice_explain))
        offset += 1
        return offset

    def take_axdr_len(self, m_list):
        '''take_axdr_len'''
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
            print('string_len:', string_len)
            axdr_len = int(string_len, 16)
        return {'offset': offset, 'len': axdr_len}

    def take_DAR(self, m_list, add_text='', depth=0):
        '''take_DAR'''
        offset = 0
        explain = database.DAR.get(m_list[0], '无效DAR')
        self.trans_res.add_row(m_list[offset:], 1, '(DAR:%s)'%explain, depth=depth)
        offset += 1
        return offset

    def take_Get_Result(self, m_list, add_text='', depth=0):
        '''take_Get_Result'''
        offset = 0
        result = m_list[offset]
        if result == '00':  # 错误信息
            self.trans_res.add_row(m_list[offset:], 1, '错误信息', depth=depth)
            offset += 1
            offset += self.take_DAR(m_list[offset:], '错误信息', depth=depth)
        elif result == '01':  # 数据
            self.trans_res.add_row(m_list[offset:], 1, '数据', depth=depth)
            offset += 1
            offset += self.take_Data(m_list[offset:], depth=depth)
        return offset


    def take_ConnectMechanismInfo(self, m_list, add_text='', depth=0):
        '''take_ConnectMechanismInfo'''
        offset = 0
        connect_choice = m_list[offset]
        en_type = {
            '00': '公共连接',
            '01': '一般密码',
            '02': '对称加密',
            '03': '数字签名',
        }.get(connect_choice, '错误')
        self.trans_res.add_row(m_list[offset:], 1, '%s(%s)'%(add_text, en_type), depth=depth)
        offset += 1
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

    def take_ConnectResponseInfo(self, m_list, add_text='', depth=0):
        '''take_ConnectResponseInfo'''
        offset = 0
        connect_result = {
            '00': '允许建立应用连接',
            '01': '密码错误',
            '02': '对称解密错误',
            '03': '非对称解密错误',
            '04': '签名错误',
            '05': '协议版本不匹配',
            'FF': '其他错误'
        }.get(m_list[offset], '错误')
        self.trans_res.add_row(m_list[offset:], 1, '%s(认证结果:%s)'%(add_text, connect_result), depth=depth)
        offset += 1
        optional = m_list[offset]
        offset += self.take_OPTIONAL(m_list[offset:], '认证附加信息')
        if optional == '01':
            offset += self.take_RN(m_list[offset:], '服务器随机数')
            offset += self.take_octect_string(m_list[offset:], '服务器签名信息')
        return offset

    def take_FactoryVersion(self, m_list, add_text='', depth=0):
        '''take_FactoryVersion'''
        offset = 0
        offset += self.take_visible_string(m_list[offset:], '厂商代码:', 4)
        offset += self.take_visible_string(m_list[offset:], '软件版本号:', 4)
        offset += self.take_visible_string(m_list[offset:], '软件版本日期:', 6)
        offset += self.take_visible_string(m_list[offset:], '硬件版本号:', 4)
        offset += self.take_visible_string(m_list[offset:], '硬件版本日期:', 6)
        offset += self.take_visible_string(m_list[offset:], '厂家扩展信息:', 8)
        return offset

    def take_Data(self, m_list, add_text='', depth=0):
        '''take data'''
        offset = 0
        if m_list[offset] == '00':    # 对null类型特殊处理
            offset += self.take_NULL(m_list[offset:], depth=depth)
            return offset
        offset += {
            '00': self.take_NULL,
            '01': self.take_array,
            '02': self.take_structure,
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
        }[m_list[offset]](m_list[offset:], add_text=add_text, depth=depth + 1)
        return offset

    def take_NULL(self, m_list, add_text='', depth=0, withtype=False):
        '''take_NULL'''
        offset = 0
        self.trans_res.add_row(m_list[offset:], 1, '%s(NULL)'%add_text, depth=depth)
        offset += 1
        return offset

    def take_array(self, m_list, add_text='', depth=0, withtype=False):
        '''take_array'''
        offset = 0
        member_num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1, '%s(array[%d])'%(add_text, member_num), depth=depth)
        offset += 1
        for _ in range(member_num):
            offset += self.take_Data(m_list[offset:], depth=depth + 1)
        return offset

    def take_structure(self, m_list, add_text='', depth=0, withtype=False):
        '''take_structure'''
        offset = 0
        member_num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1,\
                    '%s(structure[%d])'%(add_text, member_num), depth=depth)
        offset += 1
        for _ in range(member_num):
            offset += self.take_Data(m_list[offset:], depth=depth + 1)
        return offset

    def take_bool(self, m_list, add_text='', depth=0, withtype=False):
        '''take_bool'''
        offset = 0
        bool_value = 'False' if m_list[offset] == '00' else 'True'
        self.trans_res.add_row(m_list[offset:], 1, '%s(bool:%s)'%(add_text, bool_value), depth=depth)
        offset += 1
        return offset

    def take_bit_string(self, m_list, bit_len=None, add_text='', depth=0, withtype=False):
        '''take_bit_string'''
        offset = 0
        if bit_len is None:
            bit_len = int(m_list[offset], 16)
            offset += 1
        byte_len = bit_len // 8 if bit_len % 8 == 0 else bit_len // 8 + 1
        bit_string_text = ''
        for count in range(byte_len):
            bit_string_text += m_list[offset + count]
        offset += byte_len
        bit_value = str(bin(int(bit_string_text, 16))).split('b')[1].rjust(bit_len, '0')
        self.trans_res.add_row(m_list[0:offset], 0,\
                    '%s(bit-string[%d]:%s)'%(add_text, bit_len, bit_value), depth=depth)
        return offset

    def take_double_long(self, m_list, add_text='', depth=0, withtype=False):
        '''take_double_long'''
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = (int(''.join(m_list[offset : offset + 4]), 16) & 0x7fffffff) * (-1)
        else:
            value = int(''.join(m_list[offset: offset + 4]), 16)
        self.trans_res.add_row(m_list[offset:], 4, '%s(double_long:%d)'%(add_text, value), depth=depth)
        offset += 4
        return offset

    def take_double_long_unsigned(self, m_list, add_text='', depth=0, withtype=False):
        '''take_double_long_unsigned'''
        offset = 0
        value = int(''.join(m_list[offset: offset + 4]), 16)
        self.trans_res.add_row(m_list[offset:], 4,\
                    '%s(double_long_unsigned:%d)'%(add_text, value), depth=depth)
        offset += 4
        return offset

    def take_octect_string(self, m_list, add_text='', string_len=None, depth=0, withtype=False):
        '''take_octect_string'''
        offset = 0
        if string_len is None:
            res = self.take_axdr_len(m_list[offset:])
            print('Kay, ', res)
            offset += res['offset']
            string_len = res['len']
        offset += string_len
        self.trans_res.add_row(m_list[:offset], 0,\
                            '%s(octect_string[%d])'%(add_text, string_len), depth=depth)
        return offset

    def take_visible_string(self, m_list, add_text='', string_len=None, depth=0, withtype=False):
        '''take_visible_string'''
        offset = 0
        if string_len is None:
            res = self.take_axdr_len(m_list[offset:])
            offset += res['offset']
            string_len = res['len']
        visible_string = ''
        for char in m_list[offset: offset + string_len]:
            visible_string += chr(int(char, 16))
        offset += string_len
        self.trans_res.add_row(m_list[:offset], 0,\
                 '%s(visible_string[%d]:%s)'%(add_text, string_len, visible_string), depth=depth)
        return offset

    def take_UTF8_string(self, m_list, add_text='', string_len=None, depth=0, withtype=False):
        '''take_UTF8_string'''
        offset = 0
        if string_len is None:
            res = self.take_axdr_len(m_list[offset:])
            offset += res['offset']
            string_len = res['len']
        offset += string_len
        self.trans_res.add_row(m_list[:offset], 0,\
                                '%s(UFT8_string[%d])'%(add_text, string_len), depth=depth)
        return offset

    def take_integer(self, m_list, add_text='', depth=0, withtype=False):
        '''take_integer'''
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = (int(m_list[offset], 16) & 0x7f) * (-1)
        else:
            value = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1, '%s(integer:%d)'%(add_text, value), depth=depth)
        offset += 1
        return offset

    def take_long(self, m_list, add_text='', depth=0, withtype=False):
        '''take_long'''
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = int(str(int(m_list[offset], 16) & 0x7f) + m_list[offset + 1], 16) * (-1)
        else:
            value = int(m_list[offset] + m_list[offset + 1], 16)
        self.trans_res.add_row(m_list[offset:], 2, '%s(long:%d)'%(add_text, value), depth=depth)
        offset += 2
        return offset

    def take_unsigned(self, m_list, add_text='', depth=0, withtype=False):
        '''take_unsigned'''
        offset = 0
        value = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1, '%s(unsigned:%d)'%(add_text, value), depth=depth)
        offset += 1
        return offset

    def take_long_unsigned(self, m_list, add_text='', depth=0, withtype=False):
        '''take_long_unsigned'''
        offset = 0
        value = int(m_list[offset] + m_list[offset + 1], 16)
        self.trans_res.add_row(m_list[offset:], 2, '%s(long_unsigned:%d)'%(add_text, value), depth=depth)
        offset += 2
        return offset

    def take_long64(self, m_list, add_text='', depth=0, withtype=False):
        '''take_long64'''
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = int(str(int(m_list[offset], 16) & 0x7f\
                        + ''.join(m_list[offset + 1 : offset + 8]), 16) * (-1))
        else:
            value = int(''.join(m_list[offset : offset + 8]), 16)
        self.trans_res.add_row(m_list[offset:], 8, '%s(long64:%d)'%(add_text, value), depth=depth)
        offset += 8
        return offset

    def take_long64_unsigned(self, m_list, add_text='', depth=0, withtype=False):
        '''take_long64_unsigned'''
        offset = 0
        value = int(''.join(m_list[offset : offset + 8]), 16)
        self.trans_res.add_row(m_list[offset:], 8,\
                               '%s(long64_unsigned:%d)'%(add_text, value), depth=depth)
        offset += 8
        return offset

    def take_enum(self, m_list, add_text='', depth=0, enum_dict=None):
        '''take_enum'''
        offset = 0
        enum_explain = ''
        if enum_dict is not None:
            enum_explain = enum_dict.get(m_list[offset], '错误')
        self.trans_res.add_row(m_list[offset:], 1, '%s(enum:%s)'%(add_text, enum_explain), depth=depth)
        offset += 1
        return offset

    def take_float32(self, m_list, add_text='', depth=0, withtype=False):
        '''take_float32, Kay check!'''
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = (int(''.join(m_list[offset : offset + 4]), 16) & 0x7fffffff) * (-1)
        else:
            value = int(''.join(m_list[offset : offset + 4]), 16)
        self.trans_res.add_row(m_list[offset:], 4, '%s(float32:%d)'%(add_text, value), depth=depth)
        offset += 4
        return offset

    def take_float64(self, m_list, add_text='', depth=0, withtype=False):
        '''take_float64'''
        offset = 0
        if int(m_list[offset], 16) >> 7 == 1:  # 负数
            value = int(str(int(m_list[offset], 16) & 0x7f)\
                    + ''.join(m_list[offset + 1 : offset + 8]), 16) * (-1)
        else:
            value = int(''.join(m_list[offset : offset + 8]), 16)
        self.trans_res.add_row(m_list[offset:], 8, '%s(float64:%d)'%(add_text, value), depth=depth)
        offset += 8
        return offset

    def take_date_time(self, m_list, add_text='', depth=0, withtype=False):
        '''take_date_time'''
        offset = 0
        year = int(m_list[0] + m_list[1], 16)
        month = int(m_list[2], 16)
        day = int(m_list[3], 16)
        hour = int(m_list[5], 16)
        minute = int(m_list[6], 16)
        second = int(m_list[7], 16)
        milliseconds = int(m_list[8] + m_list[9], 16)
        self.trans_res.add_row(m_list[offset:], 10, add_text\
            + '(date_time:{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}:{6:03d})'\
            .format(year, month, day, hour, minute, second, milliseconds), depth=depth)
        offset += 10
        return offset

    def take_date(self, m_list, add_text='', depth=0, withtype=False):
        '''take_date'''
        offset = 0
        year = int(m_list[0] + m_list[1], 16)
        month = int(m_list[2], 16)
        day = int(m_list[3], 16)
        # week = int(m_list[4], 16)
        self.trans_res.add_row(m_list[offset:], 5, add_text\
            + '(date:{0:04d}-{1:02d}-{2:02d})'\
            .format(year, month, day), depth=depth)
        offset += 5
        return offset

    def take_time(self, m_list, add_text='', depth=0, withtype=False):
        '''take_time'''
        offset = 0
        hour = int(m_list[0], 16)
        minute = int(m_list[1], 16)
        second = int(m_list[2], 16)
        self.trans_res.add_row(m_list[offset:], 3, add_text\
            + '(time:{0:02d}:{1:02d}:{2:02d})'\
            .format(hour, minute, second), depth=depth)
        offset += 3
        return offset

    def take_date_time_s(self, m_list, add_text='', depth=0, withtype=False):
        '''take_date_time_s'''
        offset = 0
        year = int(m_list[0] + m_list[1], 16)
        month = int(m_list[2], 16)
        day = int(m_list[3], 16)
        hour = int(m_list[4], 16)
        minute = int(m_list[5], 16)
        second = int(m_list[6], 16)
        self.trans_res.add_row(m_list[offset:], 7, add_text\
            + '(date_time_s:{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d})'\
            .format(year, month, day, hour, minute, second), depth=depth)
        offset += 7
        return offset

    def take_OI(self, m_list, add_text='', depth=0, withtype=False):
        '''take_OI'''
        offset = 0
        explain = database.OAD.get(m_list[offset] + m_list[offset + 1] + '01', '未知OI').split('，')[0]
        # print('OI_explain:', OI_explain, 'over')
        self.trans_res.add_row(m_list[offset:], 2, '%s(OI:%s)'%(add_text, explain), depth=depth)
        offset += 2
        return offset

    def take_OAD(self, m_list, add_text='', depth=0, withtype=False):
        '''take_OAD'''
        offset = 0
        attr = int(m_list[offset + 2], 16)
        index = int(m_list[offset + 3], 16)
        explain = database.OAD.get(''.join(m_list[offset : offset + 3]),\
                    database.OAD.get(''.join(m_list[offset : offset + 2]) + '01',\
                    '未知OAD') + '，属性%d'%attr) + '，索引%d'%index
        self.trans_res.add_row(m_list[offset:], 4, '%s(OAD:%s)'%(add_text, explain), depth=depth)
        offset += 4
        return offset

    def take_ROAD(self, m_list, add_text='', depth=0, withtype=False):
        '''take_ROAD'''
        offset = 0
        offset += self.take_OAD(m_list[offset:], depth=depth)
        oad_num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1, '%s(ROAD[%d])'%(add_text, oad_num), depth=depth)
        offset += 1
        for _ in range(oad_num):
            offset += self.take_OAD(m_list[offset:], depth=depth + 1)
        return offset

    def take_OMD(self, m_list, add_text='', depth=0, withtype=False):
        '''take_OMD'''
        offset = 0
        method = int(m_list[offset + 2], 16)
        mode = int(m_list[offset + 3], 16)
        explain = database.OMD.get(''.join(m_list[offset : offset + 3]),\
            database.OMD.get(''.join(m_list[offset : offset + 2] + '01'),\
            '未知OMD') + '，方法%d'%method) + '，操作模式%d'%mode
        self.trans_res.add_row(m_list[offset:], 4, '%s(OMD:%s)'%(add_text, explain), depth=depth)
        offset += 4
        return offset

    def take_TI(self, m_list, add_text='', depth=0, withtype=False):
        '''take_TI'''
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
        self.trans_res.add_row(m_list[offset:], 4, '%s(TI:%d%s)'%(add_text, value, uint), depth=depth)
        offset = 3
        return offset

    def take_TSA(self, m_list, add_text='', depth=0, withtype=False):
        '''take_TSA'''
        # print('Kay, take_TSA data:', data)
        offset = 0
        TSA_len = int(m_list[offset], 16)
        addr_text = ''
        if TSA_len != 0:
            addr_len = int(m_list[offset + 1], 16) + 1
            for tsa_count in range(addr_len):
                addr_text += m_list[offset + 2 + tsa_count]
        else:
            addr_len = 0
        self.trans_res.add_row(m_list[offset:], 1 + TSA_len,\
                    '%s(TSA[%d]:%s)'%(add_text, addr_len, addr_text), depth=depth)
        offset += 1 + TSA_len
        return offset

    def take_MAC(self, m_list, add_text='', depth=0, withtype=False):
        '''take_MAC'''
        offset = 0
        offset += self.take_octect_string(m_list[offset:], 'MAC')
        return offset

    def take_RN(self, m_list, add_text='', depth=0, withtype=False):
        '''take_RN'''
        offset = 0
        offset += self.take_octect_string(m_list[offset:], 'RN')
        return offset

    def take_RN_MAC(self, m_list, add_text='', depth=0, withtype=False):
        '''take_RN_MAC'''
        offset = 0
        offset += self.take_octect_string(m_list[offset:], 'RN')
        offset += self.take_octect_string(m_list[offset:], 'MAC')
        return offset

    def take_Region(self, m_list, add_text='', depth=0, withtype=False):
        '''take_Region'''
        offset = 0
        uint = {
            '00': '前闭后开',
            '01': '前开后闭',
            '02': '前闭后闭',
            '03': '前开后开',
        }.get(m_list[offset], '错误')
        self.trans_res.add_row(m_list[offset:], 1, '%s(Region[%s])'%(add_text, uint), depth=depth)
        offset += 1
        offset += self.take_Data(m_list, add_text='起始值', depth=depth)
        offset += self.take_Data(m_list, add_text='结束值', depth=depth)
        return offset

    def take_Scaler_Unit(self, m_list, add_text='', depth=0, withtype=False):
        '''take_Scaler_Unit'''
        offset = 0
        offset += self.take_integer(m_list[offset:], '换算:', depth=depth)
        offset += self.take_enum(m_list[offset:], '单位:', depth=depth)
        return offset

    def take_RSD(self, m_list, add_text='', depth=0, withtype=False):
        '''take_RSD'''
        offset = 0
        selector = m_list[offset]
        self.trans_res.add_row(m_list[offset:], 1,\
                        '%s(RSD[Selector%s])'%(add_text, selector), depth=depth)
        offset += 1
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
            selector2_count = int(m_list[offset], 16)
            offset += 1
            for _ in range(selector2_count):
                offset += self.take_OAD(m_list[offset:], '对象属性描述符', depth=depth + 1)
                offset += self.take_Data(m_list[offset:], '起始值', depth=depth + 1)
                offset += self.take_Data(m_list[offset:], '结束值', depth=depth + 1)
                offset += self.take_Data(m_list[offset:], '数据间隔', depth=depth + 1)
        elif selector in ['04', '05']:
            offset += self.take_date_time_s(m_list[offset:],\
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

    def take_CSD(self, m_list, add_text='', depth=0, withtype=False):
        '''take_CSD'''
        offset = 0
        csd_choice = m_list[offset]
        self.trans_res.add_row(m_list[offset:], 1,\
                        '%s(CSD->%s)'%(add_text, 'OAD' if csd_choice == '00' else 'ROAD'), depth=depth)
        offset += 1
        if csd_choice == '00':
            offset += self.take_OAD(m_list[offset:], '对象属性描述符', depth=depth + 1)
        elif csd_choice == '01':
            offset += self.take_ROAD(m_list[offset:], '记录型对象属性描述符', depth=depth + 1)
        return offset

    def take_MS(self, m_list, add_text='', depth=0, withtype=False):
        '''take_MS'''
        offset = 0
        MS_choice = m_list[0]
        if MS_choice == '00':  # 无电能表
            offset += self.take_NULL(m_list[offset:], 'MS:无电能表')
        elif MS_choice == '01':  # 全部用户地址
            offset += self.take_NULL(m_list[offset:], 'MS:全部用户地址')
        elif MS_choice == '02':  # 一组用户类型
            num = int(m_list[1], 16)
            self.trans_res.add_row(m_list[offset:], 2, '%s(MS:用户类型[%d])'%(add_text, num), depth=depth)
            offset += 2
            for _ in range(num):
                offset += self.take_unsigned(m_list[offset:], '用户类型', depth=depth + 1)
        elif MS_choice == '03':  # 一组用户地址
            num = int(m_list[1], 16)
            self.trans_res.add_row(m_list[offset:], 2, '%s(MS:用户地址[%d])'%(add_text, num), depth=depth)
            offset += 2
            for _ in range(num):
                offset += self.take_TSA(m_list[offset:], '用户地址', depth=depth + 1)
        elif MS_choice == '04':  # 一组配置序号
            num = int(m_list[1], 16)
            self.trans_res.add_row(m_list[offset:], 2, '%s(MS:配置序号[%d])'%(add_text, num), depth=depth)
            offset += 2
            for _ in range(num):
                offset += self.take_long_unsigned(m_list[offset:], '配置序号', depth=depth + 1)
        elif MS_choice == '05':  # 一组用户类型区间
            offset = 0
            num = int(m_list[1], 16)
            self.trans_res.add_row(m_list[offset:], 2, '%s(MS:用户类型区间[%d])'%(add_text, num), depth=depth)
            offset += 2
            for _ in range(num):
                offset += self.take_Region(m_list[offset:], '用户类型区间', depth=depth + 1)
        elif MS_choice == '06':  # 一组用户地址区间
            offset = 0
            num = int(m_list[1], 16)
            self.trans_res.add_row(m_list[offset:], 2, '%s(MS:用户地址区间[%d])'%(add_text, num), depth=depth)
            offset += 2
            for _ in range(num):
                offset += self.take_Region(m_list[offset:], '用户地址区间', depth=depth + 1)
        elif MS_choice == '07':  # 一组配置序号区间
            offset = 0
            num = int(m_list[1], 16)
            self.trans_res.add_row(m_list[offset:], 2, '%s(MS:配置序号区间[%d])'%(add_text, num), depth=depth)
            offset += 2
            for _ in range(num):
                offset += self.take_Region(m_list[offset:], '配置序号区间:', depth=depth + 1)
        return offset

    def take_SID(self, m_list, add_text='', depth=0, withtype=False):
        '''take_SID'''
        offset = 0
        offset += self.take_double_long_unsigned(m_list[offset:], '标识', depth=depth)
        offset += self.take_octect_string(m_list[offset:], '附加数据', depth=depth)
        return offset

    def take_SID_MAC(self, m_list, add_text='', depth=0, withtype=False):
        '''take_SID_MAC'''
        offset = 0
        offset += self.take_SID(m_list[offset:], '安全标识', depth=depth)
        offset += self.take_MAC(m_list[offset:], '数据MAC', depth=depth)
        return offset

    def take_COMDCB(self, m_list, add_text='', depth=0, withtype=False):
        '''take_COMDCB'''
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
        offset += self.take_enum(m_list[offset:], add_text='波特率', enum_dict=rate_dict, depth=depth)
        offset += self.take_enum(m_list[offset:], add_text='校验位',\
                enum_dict={'00': '无校验', '01': '奇校验', '02': '偶校验'}, depth=depth)
        offset += self.take_enum(m_list[offset:], add_text='数据位',\
                enum_dict={'05': '5', '06': '6', '07': '7', '08': '8'}, depth=depth)
        offset += self.take_enum(m_list[offset:], add_text='停止位',\
                enum_dict={'01': '1', '02': '2'}, depth=depth)
        offset += self.take_enum(m_list[offset:], add_text='流控',\
                enum_dict={'00': '无', '01': '硬件', '02': '软件'}, depth=depth)
        return offset

    def take_RCSD(self, m_list, add_text='', depth=0, withtype=False):
        '''take_RCSD'''
        offset = 0
        csd_num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1,\
                        '%s(CSD[%d])'%(add_text, csd_num), depth=depth)
        offset += 1
        for _ in range(csd_num):
            offset += self.take_CSD(m_list[offset:], depth=depth + 1)
        return offset
