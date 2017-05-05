'''handle with 698 service'''
import trans.datatype as typedo

class Service():
    '''service class'''
    def __init__(self, trans_res):
        '''init'''
        self.trans_res = trans_res
        self.typedo = typedo.TypeDo(trans_res)

    def link_request(self, m_list):
        '''link_request'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:])
        link_type = {'00': '登录', '01': '心跳', '02': '退出登录'}
        offset += self.typedo.take_enum(m_list[offset:], add_text='请求类型', enum_dict=link_type)
        offset += self.typedo.take_long_unsigned(m_list[offset:], '心跳周期s')
        offset += self.typedo.take_date_time(m_list[offset:], '请求时间')
        return offset

    def link_response(self, m_list):
        '''link_response'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:])
        time_credible_flag = int(m_list[offset], 16) >> 7
        self.trans_res.add_row(m_list[offset:], 1,\
                    '(结果Result：可信)' if time_credible_flag == 1 else '结果(Result：不可信)', 0)
        offset += 1
        offset += self.typedo.take_date_time(m_list[offset:], '请求时间')
        offset += self.typedo.take_date_time(m_list[offset:], '收到时间')
        offset += self.typedo.take_date_time(m_list[offset:], '响应时间')
        return offset

    def connect_request(self, m_list):
        '''connect_request'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:])
        offset += self.typedo.take_long_unsigned(m_list[offset:], '期望的应用层协议版本号')
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=64, add_text='期望的协议一致性块')
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=128, add_text='期望的功能一致性块')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '客户机发送帧最大尺寸')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '客户机接收帧最大尺寸')
        offset += self.typedo.take_unsigned(m_list[offset:], '客户机接收帧最大窗口尺寸')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '客户机最大可处理APDU尺寸')
        offset += self.typedo.take_double_long_unsigned(m_list[offset:], '期望的应用连接超时时间')
        offset += self.typedo.take_ConnectMechanismInfo(m_list[offset:], '认证请求对象')
        return offset

    def connect_response(self, m_list):
        '''connect_response'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:])
        offset += self.typedo.take_FactoryVersion(m_list[offset:])
        offset += self.typedo.take_long_unsigned(m_list[offset:], '商定的应用层协议版本号')
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=64, add_text='期望的协议一致性块')
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=128, add_text='期望的功能一致性块')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '服务器发送帧最大尺寸')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '服务器发送帧最大尺寸')
        offset += self.typedo.take_unsigned(m_list[offset:], '服务器发送帧最大窗口尺寸')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '服务器最大可处理APDU尺寸')
        offset += self.typedo.take_double_long_unsigned(m_list[offset:], '商定的应用连接超时时间')
        offset += self.typedo.take_ConnectResponseInfo(m_list[offset:], '连接响应对象')
        return offset

    def release_request(self, m_list):
        '''release_request'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:])
        return offset

    def release_response(self, m_list):
        '''release_response'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:])
        offset += self.typedo.take_enum(m_list[offset:], '结果', enum_dict={'00': '成功'})
        return offset

    def GetRequestNormal(self, m_list):
        '''GetRequestNormal'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        offset += self.typedo.take_OAD(m_list[offset:], '一个对象属性描述符')
        return offset


    def GetRequestNormalList(self, m_list):
        '''GetRequestNormalList'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1, '若干个对象属性描述符(SEQUENCE OF OAD[%d])'%num)
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], depth=1)
        return offset


    def GetRequestRecord(self, m_list):
        '''GetRequestRecord'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        offset += self.typedo.take_OAD(m_list[offset:], '对象属性描述符')
        offset += self.typedo.take_RSD(m_list[offset:], '记录选择描述符')
        offset += self.typedo.take_RCSD(m_list[offset:], '记录列选择描述符')
        return offset


    def GetRequestRecordList(self, m_list):
        '''GetRequestRecordList'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1, '读取若干个记录型对象属性(SEQUENCE OF GetRecord[%d])'%num)
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], '对象属性描述符', depth=1)
            offset += self.typedo.take_RSD(m_list[offset:], '记录选择描述符', depth=1)
            offset += self.typedo.take_RCSD(m_list[offset:], '记录列选择描述符', depth=1)
        return offset

    def GetRequestNext(self, m_list):
        '''GetRequestNext'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '正确接收的最近一次数据块序号')
        return offset

    def GetRequestMD5(self, m_list):
        '''GetRequestNext'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        offset += self.typedo.take_OAD(m_list[offset:], '一个对象属性描述符')
        return offset


    def take_A_ResultNormal(self, m_list, depth=0):
        '''take_A_ResultNormal'''
        offset = 0
        offset += self.typedo.take_OAD(m_list[offset:], '对象属性描述符', depth=depth)
        offset += self.typedo.take_Get_Result(m_list[offset:], '结果', depth=depth)
        return offset

    def GetResponseNormal(self, m_list):
        '''GetResponseNormal'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        offset += self.take_A_ResultNormal(m_list[offset:])
        return offset

    def GetResponseNormalList(self, m_list):
        '''GetResponseNormalList'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1,\
                '若干个对象属性及其结果(SEQUENCE OF A_ResultNormal[%d])'%num)
        offset += 1
        for _ in range(num):
            offset += self.take_A_ResultNormal(m_list[offset:], depth=1)
        return offset

    def take_A_ResultRecord(self, m_list, depth=0):
        '''take_A_ResultRecord'''
        offset = 0
        offset += self.typedo.take_OAD(m_list[offset:], '记录型对象属性描述符', depth=depth)
        csd_num = int(m_list[offset], 16)
        offset += self.typedo.take_RCSD(m_list[offset:], '一行记录N列属性描述符', depth=depth)
        re_data_choice = m_list[offset]
        if re_data_choice == '00':
            self.trans_res.add_row(m_list[offset:], 1, '错误信息', depth=depth)
            offset += 1
            offset += self.typedo.take_DAR(m_list[offset:], '错误信息', depth=depth)
        elif re_data_choice == '01':  # M条记录
            record_num = int(m_list[offset + 1], 16)
            self.trans_res.add_row(m_list[offset:], 2, 'n条记录[%d]'%record_num, depth=depth)
            offset += 2
            for _ in range(record_num):
                for csd_count in range(csd_num):
                    offset += self.typedo.take_Data(m_list[offset:],\
                                    '第%d列数据'%(csd_count+1), depth=depth)
        return offset

    def GetResponseRecord(self, m_list):
        '''GetResponseRecord'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        offset += self.take_A_ResultRecord(m_list[offset:])
        return offset


    def GetResponseRecordList(self, m_list):
        '''GetResponseRecordList'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset:], 1,\
                '若干个记录型对象属性及其结果(SEQUENCE OF A_ResultNormal[%d])'%num)
        offset += 1
        for _ in range(num):
            offset += self.take_A_ResultRecord(m_list[offset:], depth=1)
        return offset


    def GetResponseNext(self, m_list):
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        offset += self.typedo.take_bool(m_list[offset:], '末帧标志')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '分帧序号')

        re_m_list_choice = m_list[offset]
        choice = {'00': '错误信息', '01': '对象属性', '02': '记录型对象属性'}
        offset += self.typedo.take_CHOICE(m_list[offset:], '分帧响应', choice_dict=choice)
        if re_m_list_choice == '00':
            offset += self.typedo.take_DAR(m_list[offset + 1:], '错误信息')
        elif re_m_list_choice == '01':  # SEQUENCE OF A-ResultNormal
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset:], 1,\
                    '对象属性(SEQUENCE OF A_ResultNormal[%d])'%num)
            offset += 1
            for _ in range(num):
                offset += self.take_A_ResultNormal(m_list[offset:], depth=1)
        elif re_m_list_choice == '02':  # SEQUENCE OF A-ResultRecord
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset:], 1,\
                    '记录型对象属性(SEQUENCE OF A-ResultRecord[%d])'%num)
            offset += 1
            for _ in range(num):
                offset += self.take_A_ResultRecord(m_list[offset:], depth=1)
        return offset

    def GetResponseMD5(self, m_list):
        '''GetResponseMD5'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        re_choice = m_list[offset]
        choice = {'00': '错误信息', '01': 'MD5值'}
        offset += self.typedo.take_CHOICE(m_list[offset:], '结果', choice_dict=choice)
        if re_choice == '00':
            offset += self.typedo.take_DAR(m_list[offset + 1:], '错误信息')
        elif re_choice == '01':
            offset += self.typedo.take_octect_string(m_list[offset + 1:], 'MD5值')
        return offset
