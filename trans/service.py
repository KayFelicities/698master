'''handle with 698 service'''
import trans.datatype as typedo
import trans.datas as database

def take_applayer(m_list, trans_res):
    '''take_applayer'''
    offset = 0
    service = Service(trans_res)
    offset += service.take_service(m_list[offset:], trans_res)
    return offset


class Service():
    '''service class'''
    def __init__(self, trans_res):
        '''init'''
        self.trans_res = trans_res
        self.typedo = typedo.TypeDo(trans_res)

    def take_service(self, m_list, trans_res):
        '''take app layer'''
        offset = 0
        service_type = m_list[offset]
        if service_type not in ['01', '02', '03', '10', '81', '82', '83', '84', '90']:
            service_type += m_list[offset + 1]
            explain = database.SERVICE.get(service_type, '未知服务')
            offset += 2
        else:
            explain = database.SERVICE.get(service_type, '未知服务')
            offset += 1
        trans_res.add_row(m_list[:offset], '服务类型', 'service', explain, '', 0, 0)
        offset += {
            '01': self.link_request,
            '02': self.connect_request,
            '03': self.release_request,
            '81': self.link_response,
            '82': self.connect_response,
            '83': self.release_response,
            '0501': self.GetRequestNormal,
            '0502': self.GetRequestNormalList,
            '0503': self.GetRequestRecord,
            '0504': self.GetRequestRecordList,
            '0505': self.GetRequestNext,
            '0506': self.GetRequestMD5,
            '8501': self.GetResponseNormal,
            '8502': self.GetResponseNormalList,
            '8503': self.GetResponseRecord,
            '8504': self.GetResponseRecordList,
            '8505': self.GetResponseNext,
            '8506': self.GetRequestMD5,
            '0601': self.SetRequestNormal,
            '0602': self.SetRequestNormalList,
            '0603': self.SetThenGetRequestNormalList,
            '8601': self.SetResponseNormal,
            '8602': self.SetResponseNormalList,
            '8603': self.SetThenGetResponseNormalList,
            # '0701': self.ActionRequest,
            # '0702': self.ActionRequestList,
            # '0703': self.ActionThenGetRequestNormalList,
            # '8701': self.ActionResponseNormal,
            # '8702': self.ActionResponseNormalList,
            # '8703': self.ActionThenGetResponseNormalList,
            # '0801': self.ReportResponseList,
            # '0802': self.ReportResponseRecordList,
            # '8801': self.ReportNotificationList,
            # '8802': self.ReportNotificationRecordList,
            # '0901': self.proxy_get_request_list,
            # '0902': self.ProxyGetRequestRecord,
            # '0903': self.ProxySetRequestList,
            # '0904': self.ProxySetThenGetRequestList,
            # '0905': self.ProxyActionRequestList,
            # '0906': self.ProxyActionThenGetRequestList,
            # '0907': self.ProxyTransCommandRequest,
            # '8901': self.ProxyGetResponseList,
            # '8902': self.ProxyGetResponseRecord,
            # '8903': self.ProxySetResponseList,
            # '8904': self.ProxySetThenGetResponseList,
            # '8905': self.ProxyActionResponseList,
            # '8906': self.ProxyActionThenGetResponseList,
            # '8907': self.ProxyTransCommandResponse,
            # '10': self.security_request,
            # '90': self.security_response,
        }.get(service_type)(m_list[offset:])
        if m_list[0] in ['82', '83', '84', '85', '86', '87', '88', '89']:
            offset += self.take_FollowReport(m_list[offset:])
            offset += self.take_TimeTag(m_list[offset:])
        elif m_list[0] in ['02', '03', '05', '06', '07', '08', '09']:
            offset += self.take_TimeTag(m_list[offset:])
        return offset

    def take_Get_Result(self, m_list, brief='', depth=0):
        '''take_Get_Result'''
        offset = 0
        result = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], brief, depth=depth,\
                                    choice_dict={'00': '错误信息', '01': '数据'})
        if result == '00':  # 错误信息
            offset += self.typedo.take_DAR(m_list[offset:], '错误信息', depth=depth)
        elif result == '01':  # 数据
            offset += self.typedo.take_Data(m_list[offset:], '数据', depth=depth)
        return offset

    def take_A_ResultNormal(self, m_list, brief='', depth=0):
        '''take_A_ResultNormal'''
        offset = 0
        offset += self.typedo.take_OAD(m_list[offset:], '对象属性描述符', depth=depth)
        offset += self.take_Get_Result(m_list[offset:], '结果', depth=depth)
        return offset

    def take_A_ResultRecord(self, m_list, brief='', depth=0):
        '''take_A_ResultRecord'''
        offset = 0
        offset += self.typedo.take_OAD(m_list[offset:], '记录型对象属性描述符', depth=depth)
        csd_num = int(m_list[offset], 16)
        offset += self.typedo.take_RCSD(m_list[offset:], '一行记录N列属性描述符', depth=depth)
        re_data_choice = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], '响应数据',\
                                            choice_dict={'00': '错误信息', '01': 'M条记录'})
        if re_data_choice == '00':
            offset += self.typedo.take_DAR(m_list[offset:], '错误信息', depth=depth)
        elif re_data_choice == '01':  # M条记录
            record_num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], 'M条记录',\
                                    'SEQUENCE OF A-RecordRow', record_num, depth=depth)
            offset += 1
            for _ in range(record_num):
                for csd_count in range(csd_num):
                    offset += self.typedo.take_Data(m_list[offset:],\
                                    '第%d列数据'%(csd_count+1), depth=depth)
        return offset

    def take_FollowReport(self, m_list, depth=0):
        '''take_FollowReport'''
        offset = 0
        follow_report_option = m_list[offset]
        offset += self.typedo.take_OPTIONAL(m_list[offset:], '跟随上报信息域')
        if follow_report_option == '01':
            follow_report_choice = m_list[offset]
            offset += self.typedo.take_CHOICE(m_list[offset:], 'FollowReport', depth=depth,\
                                choice_dict={'01': '若干个对象属性及其数据', '02': '若干个记录型对象属性及其数据'})
            if follow_report_choice == '01':
                num = int(m_list[offset], 16)
                self.trans_res.add_row(m_list[offset: offset+1], '若干个对象属性及其数据',\
                                        'SEQUENCE OF A-ResultNormal[%d]'%num, num)
                offset += 1
                for _ in range(num):
                    offset += self.take_A_ResultNormal(m_list[offset:], depth=depth)
            elif follow_report_choice == '02':
                num = int(m_list[offset], 16)
                self.trans_res.add_row(m_list[offset: offset+1], '若干个记录型对象属性及其数据',\
                                        'SEQUENCE OF A-ResultRecord[%d]'%num, num)
                offset += 1
                for _ in range(num):
                    offset += self.take_A_ResultRecord(m_list[offset:], depth=depth)
        return offset

    def take_TimeTag(self, m_list, depth=0):
        '''take_TimeTag'''
        offset = 0
        timetag_option = m_list[offset]
        offset += self.typedo.take_OPTIONAL(m_list[offset:], '时间标签', depth=depth)
        if timetag_option == '01':
            offset += self.typedo.take_date_time_s(m_list[offset:], '发送时标', depth=depth)
            offset += self.typedo.take_TI(m_list[offset:], '允许传输延时时间', depth=depth)
        return offset

    def link_request(self, m_list):
        '''link_request'''
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:])
        link_type = {'00': '登录', '01': '心跳', '02': '退出登录'}
        offset += self.typedo.take_enum(m_list[offset:], brief='请求类型', enum_dict=link_type)
        offset += self.typedo.take_long_unsigned(m_list[offset:], '心跳周期s')
        offset += self.typedo.take_date_time(m_list[offset:], '请求时间')
        return offset

    def link_response(self, m_list):
        '''link_response'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:])
        time_credible_flag = int(m_list[offset], 16) >> 7
        offset += 1
        self.trans_res.add_row(m_list[:offset], '结果', 'Result',\
                                '可信' if time_credible_flag == 1 else '不可信')
        offset += self.typedo.take_date_time(m_list[offset:], '请求时间')
        offset += self.typedo.take_date_time(m_list[offset:], '收到时间')
        offset += self.typedo.take_date_time(m_list[offset:], '响应时间')
        return offset

    def connect_request(self, m_list):
        '''connect_request'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:])
        offset += self.typedo.take_long_unsigned(m_list[offset:], '期望的应用层协议版本号')
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=64, brief='期望的协议一致性块')
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=128, brief='期望的功能一致性块')
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
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=64, brief='期望的协议一致性块')
        offset += self.typedo.take_bit_string(m_list[offset:], bit_len=128, brief='期望的功能一致性块')
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
        self.trans_res.add_row(m_list[offset: offset+1], '若干个对象属性描述符', 'SEQUENCE OF OAD', num)
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
        self.trans_res.add_row(m_list[offset: offset+1], '读取若干个记录型对象属性',\
                                'SEQUENCE OF GetRecord', num)
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
        self.trans_res.add_row(m_list[offset: offset+1], '若干个对象属性及其结果',\
                                'SEQUENCE OF A_ResultNormal', num)
        offset += 1
        for _ in range(num):
            offset += self.take_A_ResultNormal(m_list[offset:], depth=1)
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
        self.trans_res.add_row(m_list[offset: offset+1],\
                '若干个记录型对象属性及其结果', 'SEQUENCE OF A_ResultNormal', num)
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
            self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象属性', 'SEQUENCE OF A_ResultNormal', num)
            offset += 1
            for _ in range(num):
                offset += self.take_A_ResultNormal(m_list[offset:], depth=1)
        elif re_m_list_choice == '02':  # SEQUENCE OF A-ResultRecord
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                    '记录型对象属性', 'SEQUENCE OF A-ResultRecord', num)
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




    def SetRequestNormal(self, m_list):
        '''SetRequestNormal'''
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        offset += self.typedo.take_OAD(m_list[offset:], '一个对象属性描述符')
        offset += self.typedo.take_Data(m_list[offset:], '数据')
        return offset


    def SetRequestNormalList(self, m_list):
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '若干个对象属性', 'SEQUENCE OF[%d]'%num, num)
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], '一个对象属性描述符', depth=1)
            offset += self.typedo.take_Data(m_list[offset:], '数据', depth=1)
        return offset


    def SetThenGetRequestNormalList(self, m_list):
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], '服务序号-优先级')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '若干个设置后读取对象属性', 'SEQUENCE OF[%d]'%num, num)
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], '一个设置的对象属性', depth=1)
            offset += self.typedo.take_Data(m_list[offset:], '数据', depth=1)
            offset += self.typedo.take_OAD(m_list[offset:], '一个读取的对象属性', depth=1)
            offset += self.typedo.take_unsigned(m_list[offset:], '延时读取时间', depth=1)
        return offset


    def SetResponseNormal(self, m_list):
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        offset += self.typedo.take_OAD(m_list[offset:], '一个对象属性描述符')
        offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果')
        return offset


    def SetResponseNormalList(self, m_list):
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '若干个对象属性设置结果', 'SEQUENCE OF[%d]'%num, num)
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], '一个对象属性描述符', depth=1)
            offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果', depth=1)
        return offset


    def SetThenGetResponseNormalList(self, m_list):
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], '服务序号-优先级-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '若干个对象属性设置后读取结果', 'SEQUENCE OF[%d]'%num, num)
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], '一个设置的对象属性描述符', depth=1)
            offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果', depth=1)
            offset += self.typedo.take_OAD(m_list[offset:], '一个读取的对象属性描述符', depth=1)
            offset += self.take_Get_Result(m_list[offset:], '读取响应数据', depth=1)
        return offset


    # def ActionRequest(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_OMD(m_list[offset:], '')
    #     offset += self.typedo.take_Data(m_list[offset:], '')
    #     return offset


    # def ActionRequestList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     object_num = get_num_of_SEQUENCE(m_list[offset:], '对象方法')
    #     offset += 1
    #     config.line_level += 1
    #     for object_count in range(object_num):
    #         end_flag = 1 if object_count == object_num - 1 else 0
    #         offset += self.typedo.take_OMD(m_list[offset:], '')
    #         offset += self.typedo.take_Data(m_list[offset:], end_flag=end_flag)
    #     config.line_level -= 1
    #     return offset


    # def ActionThenGetRequestNormalList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     object_num = get_num_of_SEQUENCE(m_list[offset:], '设置后读取对象属性')
    #     offset += 1
    #     config.line_level += 1
    #     for object_count in range(object_num):
    #         end_flag = 1 if object_count == object_num - 1 else 0
    #         offset += self.typedo.take_OMD(m_list[offset:], '设置的对象方法:')
    #         offset += self.typedo.take_Data(m_list[offset:], '方法参数:')
    #         offset += self.typedo.take_OMD(m_list[offset:], '读取的对象属性:')
    #         offset += self.typedo.take_Data(m_list[offset:], '读取延时:', end_flag=end_flag)
    #     config.line_level -= 1
    #     return offset


    # def ActionResponseNormal(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     offset += self.typedo.take_OMD(m_list[offset:], '')
    #     offset += self.typedo.take_DAR(m_list[offset:], '操作执行结果')
    #     optional = m_list[offset]
    #     offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据')
    #     if optional == '01':
    #         offset += self.typedo.take_Data(m_list[offset:], '')
    #     return offset


    # def ActionResponseNormalList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     action_result_num = get_num_of_SEQUENCE(m_list[offset:], '对象方法操作结果')
    #     offset += 1
    #     config.line_level += 1
    #     for action_result_count in range(action_result_num):
    #         end_flag = 1 if action_result_count == action_result_num - 1 else 0
    #         offset += self.typedo.take_OMD(m_list[offset:], '')
    #         offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果')
    #         optional = m_list[offset]
    #         offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据')
    #         if optional == '01':
    #             offset += self.typedo.take_Data(m_list[offset:], end_flag=end_flag)
    #     config.line_level -= 1
    #     return offset


    # def ActionThenGetResponseNormalList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     action_result_num = get_num_of_SEQUENCE(m_list[offset:], '对象方法操作结果')
    #     offset += 1
    #     config.line_level += 1
    #     for action_result_count in range(action_result_num):
    #         end_flag = 1 if action_result_count == action_result_num - 1 else 0
    #         offset += self.typedo.take_OMD(m_list[offset:], '')
    #         offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果', level=config.line_level)
    #         optional = m_list[offset]
    #         offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据')
    #         if optional == '01':
    #             offset += self.typedo.take_Data(m_list[offset:], '')
    #         offset += self.typedo.take_OAD(m_list[offset:], '')
    #         offset += self.typedo.take_Get_Result(m_list[offset:], end_flag=end_flag)
    #     config.line_level -= 1
    #     return offset


    # def ReportResponseList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     OAD_num = get_num_of_SEQUENCE(m_list[offset:], '上报的对象')
    #     offset += 1
    #     config.line_level += 1
    #     for OAD_count in range(OAD_num):
    #         end_flag = 1 if OAD_count == OAD_num - 1 else 0
    #         offset += self.typedo.take_OAD(m_list[offset:], end_flag=end_flag)
    #     config.line_level -= 1
    #     return offset


    # def ReportResponseRecordList(self, m_list):
    #     return ReportResponseList(m_list)


    # def ReportNotificationList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     A_ResultNormal_num = get_num_of_SEQUENCE(m_list[offset:], 'A_ResultNormal')
    #     offset += 1
    #     config.line_level += 1
    #     for A_ResultNormal_count in range(A_ResultNormal_num):
    #         end_flag = 1 if A_ResultNormal_count == A_ResultNormal_num - 1 else 0
    #         offset += self.typedo.take_A_ResultNormal(m_list[offset:], end_flag=end_flag)
    #     config.line_level -= 1
    #     return offset


    # def ReportNotificationRecordList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     A_ResultRecord_num = get_num_of_SEQUENCE(m_list[offset:], 'A_ResultNormal')
    #     offset += 1
    #     config.line_level += 1
    #     for A_ResultRecord_count in range(A_ResultRecord_num):
    #         end_flag = 1 if A_ResultRecord_count == A_ResultRecord_num - 1 else 0
    #         offset += self.typedo.take_A_ResultRecord(m_list[offset:], end_flag=end_flag)
    #     config.line_level -= 1
    #     return offset

    # def proxy_get_request_list(self, m_list):
    #     '''proxy get request list'''
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间:')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址:')
    #         offset += self.typedo.take_long_unsigned(m_list[offset:], '代理一个服务器的超时时间:')
    #         oad_num = get_num_of_SEQUENCE(m_list[offset:], 'OAD')
    #         offset += 1
    #         for _ in range(oad_num):
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #     return offset


    # def ProxyGetRequestRecord(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '代理请求的超时时间:')
    #     offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址:')
    #     offset += self.typedo.take_OAD(m_list[offset:], '')
    #     offset += self.typedo.take_RSD(m_list[offset:], '')
    #     offset += self.typedo.take_RCSD(m_list[offset:], '')
    #     return offset


    # def ProxySetRequestList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间:')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址:')
    #         offset += self.typedo.take_long_unsigned(m_list[offset:], '代理一个服务器的超时时间:')
    #         oad_num = get_num_of_SEQUENCE(m_list[offset:], 'OAD及其数据')
    #         offset += 1
    #         for _ in range(oad_num):
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_Data(m_list[offset:], '')
    #     return offset


    # def ProxySetThenGetRequestList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间:')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址:')
    #         offset += self.typedo.take_long_unsigned(m_list[offset:], '代理一个服务器的超时时间:')
    #         oad_num = get_num_of_SEQUENCE(m_list[offset:], '对象属性的设置后读取')
    #         offset += 1
    #         for _ in range(oad_num):
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_Data(m_list[offset:], '')
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_unsigned(m_list[offset:], '延时读取时间:')
    #     return offset


    # def ProxyActionRequestList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间:')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址:')
    #         offset += self.typedo.take_long_unsigned(m_list[offset:], '代理一个服务器的超时时间:')
    #         oad_num = get_num_of_SEQUENCE(m_list[offset:], 'OAD及其参数')
    #         offset += 1
    #         for _ in range(oad_num):
    #             offset += self.typedo.take_OMD(m_list[offset:], '')
    #             offset += self.typedo.take_Data(m_list[offset:], '')
    #     return offset


    # def ProxyActionThenGetRequestList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间:')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址:')
    #         offset += self.typedo.take_long_unsigned(m_list[offset:], '代理一个服务器的超时时间:')
    #         oad_num = get_num_of_SEQUENCE(m_list[offset:], '对象方法及属性的操作后读取')
    #         offset += 1
    #         for _ in range(oad_num):
    #             offset += self.typedo.take_OMD(m_list[offset:], '')
    #             offset += self.typedo.take_Data(m_list[offset:], '')
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_unsigned(m_list[offset:], '延时读取时间:')
    #     return offset


    # def ProxyTransCommandRequest(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:], '')
    #     offset += self.typedo.take_OAD(m_list[offset:], '')
    #     offset += self.typedo.take_COMDCB(m_list[offset:], '端口通信控制块:')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '接收等待报文超时时间（秒）:')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '接收等待字节超时时间（毫秒）:')
    #     offset += self.typedo.take_octect_string(m_list[offset:], '透明转发命令')
    #     return offset


    # def ProxyGetResponseList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器的读取结果')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '')
    #         oad_num = get_num_of_SEQUENCE(m_list[offset:], 'OAD及其结果')
    #         offset += 1
    #         for _ in range(oad_num):
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_Get_Result(m_list[offset:], '')
    #     return offset


    # def ProxyGetResponseRecord(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     offset += self.typedo.take_TSA(m_list[offset:], '')
    #     offset += self.typedo.take_A_ResultRecord(m_list[offset:], '')
    #     return offset


    # def ProxySetResponseList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器的读取结果')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '')
    #         set_result_num = get_num_of_SEQUENCE(m_list[offset:], '对象属性设置结果')
    #         offset += 1
    #         for _ in range(set_result_num):
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_DAR(m_list[offset:], '设置结果')
    #     return offset


    # def ProxySetThenGetResponseList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器的读取结果')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '')
    #         set_result_num = get_num_of_SEQUENCE(m_list[offset:], '对象属性设置后读取结果')
    #         offset += 1
    #         for _ in range(set_result_num):
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_DAR(m_list[offset:], '设置结果')
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_Get_Result(m_list[offset:], '')
    #     return offset


    # def ProxyActionResponseList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器的读取结果')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '')
    #         set_result_num = get_num_of_SEQUENCE(m_list[offset:], '对象属性设置后读取结果')
    #         offset += 1
    #         for _ in range(set_result_num):
    #             offset += self.typedo.take_OMD(m_list[offset:], '')
    #             offset += self.typedo.take_DAR(m_list[offset:], '操作结果')
    #             optional = m_list[offset]
    #             offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据')
    #             if optional == '01':
    #                 offset += self.typedo.take_Data(m_list[offset:], '')
    #     return offset


    # def ProxyActionThenGetResponseList(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     proxy_num = get_num_of_SEQUENCE(m_list[offset:], '代理服务器的读取结果')
    #     offset += 1
    #     for _ in range(proxy_num):
    #         offset += self.typedo.take_TSA(m_list[offset:], '')
    #         set_result_num = get_num_of_SEQUENCE(m_list[offset:], '对象属性设置后读取结果')
    #         offset += 1
    #         for _ in range(set_result_num):
    #             offset += self.typedo.take_OMD(m_list[offset:], '')
    #             offset += self.typedo.take_DAR(m_list[offset:], '操作结果')
    #             optional = m_list[offset]
    #             offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据')
    #             if optional == '01':
    #                 offset += self.typedo.take_Data(m_list[offset:], '')
    #             offset += self.typedo.take_OAD(m_list[offset:], '')
    #             offset += self.typedo.take_Get_Result(m_list[offset:], '')
    #     return offset


    # def ProxyTransCommandResponse(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:], '')
    #     offset += self.typedo.take_OAD(m_list[offset:], '')
    #     trans_result_choice = m_list[offset]
    #     if trans_result_choice == '00':
    #         show_m_list_source(m_list[offset:], 2)
    #         offset += self.typedo.take_DAR(m_list[offset + 1:], '错误信息') + 1
    #     elif trans_result_choice == '01':
    #         show_m_list_source(m_list[offset:], 1)
    #         output(' —— 返回数据')
    #         offset += 1
    #         offset += self.typedo.take_octect_string(m_list[offset:], '')
    #     return offset

    # def security_request(self, m_list):
    #     offset = 0
    #     security_choice = m_list[offset]
    #     if security_choice == '00':  # 明文
    #         octect_string_len, len_offset = get_len_of_octect_string(m_list[offset + 1:])
    #         show_m_list_source(m_list[offset:], 1 + len_offset)
    #         output(' —— 明文应用数据单元, 长度' + str(octect_string_len))
    #         offset += 1 + len_offset
    #         offset += self.typedo.take_security_APDU(m_list[offset:], '')
    #     else:   # 密文
    #         show_m_list_source(m_list[offset:], 1)
    #         offset += self.typedo.take_octect_string(m_list[offset + 1:], '密文应用数据单元') + 1
    #     security_choice = m_list[offset]
    #     print('security_choice:', security_choice)
    #     offset += 1
    #     offset += {
    #         '00': self.typedo.take_SID_MAC,
    #         '01': self.typedo.take_RN,
    #         '02': self.typedo.take_RN_MAC,
    #         '03': self.typedo.take_SID,
    #     }[security_choice](m_list[offset:], '(数据验证信息)')
    #     return offset


    # def security_response(self, m_list):
    #     offset = 0
    #     security_choice = m_list[offset]
    #     if security_choice == '00':
    #         octect_string_len, len_offset = get_len_of_octect_string(m_list[offset + 1:])
    #         show_m_list_source(m_list[offset:], 1 + len_offset)
    #         output(' —— 明文应用数据单元, 长度' + str(octect_string_len))
    #         offset += 1 + len_offset
    #         offset += self.typedo.take_security_APDU(m_list[offset:], '')
    #     elif security_choice == '01':
    #         show_m_list_source(m_list[offset:], 1)
    #         offset += self.typedo.take_octect_string(m_list[offset + 1:], '密文应用数据单元') + 1
    #     elif security_choice == '02':
    #         show_m_list_source(m_list[offset:], 1)
    #         offset += 1
    #         offset += self.typedo.take_DAR(m_list[offset:], '异常错误')
    #     optional = m_list[offset]
    #     offset += self.typedo.take_OPTIONAL(m_list[offset:], '数据验证信息')
    #     if optional == '01':
    #         check_choice = m_list[offset]
    #         show_m_list_source(m_list[offset:], 1)
    #         output(' —— 数据验证方式:数据MAC')
    #         offset += 1
    #         if check_choice == '00':
    #             offset += self.typedo.take_MAC(m_list[offset:], '')
    #     return offset


    # def self.typedo.take_security_APDU(m_list, add_text=''):
    #     offset = 0
    #     output('*' * 50 + '安全传输APDU')
    #     offset_temp, service_type = self.typedo.take_service_type(m_list[offset:], '')
    #     offset += offset_temp
    #     offset += {
    #         '01': link_request,
    #         '02': connect_request,
    #         '03': release_request,
    #         '81': link_response,
    #         '82': connect_response,
    #         '83': release_response,
    #         '0501': GetRequestNormal,
    #         '0502': GetRequestNormalList,
    #         '0503': GetRequestRecord,
    #         '0504': GetRequestRecordList,
    #         '0505': GetRequestNext,
    #         '8501': GetResponseNormal,
    #         '8502': GetResponseNormalList,
    #         '8503': GetResponseRecord,
    #         '8504': GetResponseRecordList,
    #         '8505': GetResponseNext,
    #         '0601': SetRequestNormal,
    #         '0602': SetRequestNormalList,
    #         '0603': SetThenGetRequestNormalList,
    #         '8601': SetResponseNormal,
    #         '8602': SetResponseNormalList,
    #         '8603': SetThenGetResponseNormalList,
    #         '0701': ActionRequest,
    #         '0702': ActionRequestList,
    #         '0703': ActionThenGetRequestNormalList,
    #         '8701': ActionResponseNormal,
    #         '8702': ActionResponseNormalList,
    #         '8703': ActionThenGetResponseNormalList,
    #         '0801': ReportResponseList,
    #         '0802': ReportResponseRecordList,
    #         '8801': ReportNotificationList,
    #         '8802': ReportNotificationRecordList,
    #         '0901': proxy_get_request_list,
    #         '0902': ProxyGetRequestRecord,
    #         '0903': ProxySetRequestList,
    #         '0904': ProxySetThenGetRequestList,
    #         '0905': ProxyActionRequestList,
    #         '0906': ProxyActionThenGetRequestList,
    #         '0907': ProxyTransCommandRequest,
    #         '8901': ProxyGetResponseList,
    #         '8902': ProxyGetResponseRecord,
    #         '8903': ProxySetResponseList,
    #         '8904': ProxySetThenGetResponseList,
    #         '8905': ProxyActionResponseList,
    #         '8906': ProxyActionThenGetResponseList,
    #         '8907': ProxyTransCommandResponse,
    #     }[service_type](m_list[offset:], '')
    #     if m_list[0] in ['82', '83', '84', '85', '86', '87', '88', '89']:
    #         offset += self.typedo.take_FollowReport(m_list[offset:], '')
    #         offset += self.typedo.take_TimeTag(m_list[offset:], '')
    #     elif m_list[0] in ['02', '03', '04', '05', '06', '07', '00', '09']:
    #         offset += self.typedo.take_TimeTag(m_list[offset:], '')
    #     output('*' * 50 + '安全传输APDU')
    #     return offset