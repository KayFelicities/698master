"""handle with 698 service"""
import copy
import master.trans.datatype as typedo
from master.datas import base_data
from master.datas import k_data_s
from master import config


def take_applayer(m_list, trans_res):
    """take_applayer"""
    offset = 0
    service = Service(trans_res)
    offset += service.take_service(m_list[offset:])
    return offset


class Service:
    """service class"""
    def __init__(self, trans_res):
        """init"""
        self.trans_res = trans_res
        self.typedo = typedo.TypeDo(trans_res)

    def take_service(self, m_list):
        """take app layer"""
        offset = 0
        service_type = m_list[offset]
        if service_type not in ['01', '02', '03', '10', '81', '82', '83', '84', '90', '6E', 'EE']:
            service_type += m_list[offset + 1]
            explain = base_data.get_service(service_type)
            offset += 2
        else:
            explain = base_data.get_service(service_type)
            offset += 1
        self.trans_res.add_row(m_list[:offset], '服务类型', 'service', explain, '', 0, 0)
        offset += {
            '01': self.link_request,
            '02': self.connect_request,
            '03': self.release_request,
            '81': self.link_response,
            '82': self.connect_response,
            '83': self.release_response,
            '84': self.release_connect_notification,
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
            '0701': self.ActionRequest,
            '0702': self.ActionRequestList,
            '0703': self.ActionThenGetRequestNormalList,
            '8701': self.ActionResponseNormal,
            '8702': self.ActionResponseNormalList,
            '8703': self.ActionThenGetResponseNormalList,
            '0801': self.ReportResponseList,
            '0802': self.ReportResponseRecordList,
            '0803': self.ReportResponseTransData,
            '8801': self.ReportNotificationList,
            '8802': self.ReportNotificationRecordList,
            '8803': self.ReportNotificationTransData,
            '0901': self.proxy_get_request_list,
            '0902': self.ProxyGetRequestRecord,
            '0903': self.ProxySetRequestList,
            '0904': self.ProxySetThenGetRequestList,
            '0905': self.ProxyActionRequestList,
            '0906': self.ProxyActionThenGetRequestList,
            '0907': self.ProxyTransCommandRequest,
            '8901': self.ProxyGetResponseList,
            '8902': self.ProxyGetResponseRecord,
            '8903': self.ProxySetResponseList,
            '8904': self.ProxySetThenGetResponseList,
            '8905': self.ProxyActionResponseList,
            '8906': self.ProxyActionThenGetResponseList,
            '8907': self.ProxyTransCommandResponse,
            '10': self.security_request,
            '90': self.security_response,
            '6E': self.ERRORResponse,
            'EE': self.ERRORResponse,
        }.get(service_type)(m_list[offset:])
        if m_list[0] in ['82', '83', '84', '85', '86', '87', '88', '89', 'EE']:
            offset += self.take_FollowReport(m_list[offset:])
            offset += self.take_TimeTag(m_list[offset:])
        elif m_list[0] in ['02', '03', '05', '06', '07', '08', '09', '6E']:
            offset += self.take_TimeTag(m_list[offset:])
        return offset

    def take_Get_Result(self, m_list, brief='', depth=0, oad=''):
        """take_Get_Result"""
        offset = 0
        result = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], brief, depth=depth,\
                                    choice_dict={'00': '错误信息', '01': '数据'})
        if result == '00':  # 错误信息
            self.trans_res.add_access_res(oad, m_list[offset])
            offset += self.typedo.take_DAR(m_list[offset:], '错误信息', depth=depth)
        elif result == '01':  # 数据
            self.trans_res.add_access_res(oad, '00')
            structure = []
            if oad:
                structure = config.K_DATA.get_structure('oad', oad)
            offset += self.typedo.take_Data(m_list[offset:], '', depth=depth, structure=structure)
        return offset

    def take_A_ResultNormal(self, m_list, brief='', depth=0):
        """take_A_ResultNormal"""
        offset = 0
        offset += self.typedo.take_OAD(m_list[offset:], 'OAD', depth=depth)
        oad = ''.join(m_list[offset - 4 : offset])
        offset += self.take_Get_Result(m_list[offset:], '结果', depth=depth, oad=oad)
        return offset

    def take_A_ResultRecord(self, m_list, brief='', depth=0):
        """take_A_ResultRecord"""
        offset = 0
        offset += self.typedo.take_OAD(m_list[offset:], '记录型OAD', depth=depth)
        oad = ''.join(m_list[offset - 4 : offset])
        csd_num = int(m_list[offset], 16)
        rcsd_structure = config.K_DATA.get_rcsd_structure(m_list[offset:])
        print('rcsd_structure:', rcsd_structure)
        offset += self.typedo.take_RCSD(m_list[offset:], '一行记录N列属性描述符', depth=depth)
        re_data_choice = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], '响应数据',\
                                            choice_dict={'00': '错误信息', '01': 'M条记录'})
        if re_data_choice == '00':
            self.trans_res.add_access_res(oad, m_list[offset])
            offset += self.typedo.take_DAR(m_list[offset:], '错误信息', depth=depth)
        elif re_data_choice == '01':  # M条记录
            self.trans_res.add_access_res(oad, '00')
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1], '记录',\
                                    'SEQUENCE OF A-RecordRow[%d]'%num, num, depth=depth, unit='条')
            offset += 1
            for _ in range(num):
                rcsd_copy = copy.deepcopy(rcsd_structure)
                for _ in range(csd_num):
                    offset += self.typedo.take_Data(m_list[offset:],\
                                    depth=depth+1, structure=rcsd_copy.pop(0))
        return offset

    def take_FollowReport(self, m_list, depth=0):
        """take_FollowReport"""
        offset = 0
        follow_report_option = m_list[offset]
        offset += self.typedo.take_OPTIONAL(m_list[offset:], '跟随上报信息域')
        if follow_report_option == '01':
            follow_report_choice = m_list[offset]
            offset += self.typedo.take_CHOICE(m_list[offset:], 'FollowReport', depth=depth,\
                                choice_dict={'01': '对象属性及其数据', '02': '记录型对象属性及其数据'})
            if follow_report_choice == '01':
                num = int(m_list[offset], 16)
                self.trans_res.add_row(m_list[offset: offset+1], '对象属性及其数据',\
                                        'SEQUENCE OF A-ResultNormal[%d]'%num, num, unit='个')
                offset += 1
                for _ in range(num):
                    offset += self.take_A_ResultNormal(m_list[offset:], depth=depth)
            elif follow_report_choice == '02':
                num = int(m_list[offset], 16)
                self.trans_res.add_row(m_list[offset: offset+1], '记录型对象属性及其数据',\
                                        'SEQUENCE OF A-ResultRecord[%d]'%num, num, unit='个')
                offset += 1
                for _ in range(num):
                    offset += self.take_A_ResultRecord(m_list[offset:], depth=depth)
        return offset

    def take_TimeTag(self, m_list, depth=0):
        """take_TimeTag"""
        offset = 0
        timetag_option = m_list[offset]
        offset += self.typedo.take_OPTIONAL(m_list[offset:], '时间标签', depth=depth)
        if timetag_option == '01':
            offset += self.typedo.take_date_time_s(m_list[offset:], '发送时标', depth=depth)
            offset += self.typedo.take_TI(m_list[offset:], '允许传输延时时间', depth=depth)
        return offset

    def link_request(self, m_list):
        """link_request"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:])
        link_type = {'00': '登录', '01': '心跳', '02': '退出登录'}
        offset += self.typedo.take_enum(m_list[offset:], brief='请求类型', enum_dict=link_type)
        offset += self.typedo.take_long_unsigned(m_list[offset:], '心跳周期s')
        offset += self.typedo.take_date_time(m_list[offset:], '请求时间')
        return offset

    def link_response(self, m_list):
        """link_response"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:])
        time_credible_flag = int(m_list[offset], 16) >> 7
        self.trans_res.add_row(m_list[offset: offset+1], '结果', 'Result',\
                                '可信' if time_credible_flag == 1 else '不可信')
        offset += 1
        offset += self.typedo.take_date_time(m_list[offset:], '请求时间')
        offset += self.typedo.take_date_time(m_list[offset:], '收到时间')
        offset += self.typedo.take_date_time(m_list[offset:], '响应时间')
        return offset

    def connect_request(self, m_list):
        """connect_request"""
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
        """connect_response"""
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
        """release_request"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:])
        return offset

    def release_response(self, m_list):
        """release_response"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:])
        offset += self.typedo.take_enum(m_list[offset:], '结果', enum_dict={'00': '成功'})
        return offset

    def release_connect_notification(self, m_list):
        """release_connect_notification"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:])
        offset += self.typedo.take_date_time_s(m_list[offset:], '应用连接建立时间')
        offset += self.typedo.take_date_time_s(m_list[offset:], '服务器当前时间')
        return offset

    def GetRequestNormal(self, m_list):
        """GetRequestNormal"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_OAD(m_list[offset:], 'OAD')
        return offset

    def GetRequestNormalList(self, m_list):
        """GetRequestNormalList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1], 'OAD', 'SEQUENCE OF OAD[%d]'%num, value=num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], depth=1)
        return offset

    def GetRequestRecord(self, m_list):
        """GetRequestRecord"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_OAD(m_list[offset:], 'OAD')
        offset += self.typedo.take_RSD(m_list[offset:], '记录选择描述符')
        offset += self.typedo.take_RCSD(m_list[offset:], '记录列选择描述符')
        return offset

    def GetRequestRecordList(self, m_list):
        """GetRequestRecordList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1], '读取记录型对象属性',\
                                'SEQUENCE OF GetRecord[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], 'OAD', depth=1)
            offset += self.typedo.take_RSD(m_list[offset:], '记录选择描述符', depth=1)
            offset += self.typedo.take_RCSD(m_list[offset:], '记录列选择描述符', depth=1)
        return offset

    def GetRequestNext(self, m_list):
        """GetRequestNext"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '正确接收的最近一次数据块序号')
        return offset

    def GetRequestMD5(self, m_list):
        """GetRequestNext"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_OAD(m_list[offset:], 'OAD')
        return offset

    def GetResponseNormal(self, m_list):
        """GetResponseNormal"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.take_A_ResultNormal(m_list[offset:])
        return offset

    def GetResponseNormalList(self, m_list):
        """GetResponseNormalList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1], '对象属性及其结果',\
                                'SEQUENCE OF A_ResultNormal[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.take_A_ResultNormal(m_list[offset:], depth=1)
        return offset

    def GetResponseRecord(self, m_list):
        """GetResponseRecord"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.take_A_ResultRecord(m_list[offset:])
        return offset

    def GetResponseRecordList(self, m_list):
        """GetResponseRecordList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                '记录型对象属性及其结果', 'SEQUENCE OF A_ResultNormal[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.take_A_ResultRecord(m_list[offset:], depth=1)
        return offset

    def GetResponseNext(self, m_list):
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.typedo.take_bool(m_list[offset:], '末帧标志')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '分帧序号')

        re_m_list_choice = m_list[offset]
        choice = {'00': '错误信息', '01': '对象属性', '02': '记录型对象属性'}
        offset += self.typedo.take_CHOICE(m_list[offset:], '分帧响应', choice_dict=choice)
        if re_m_list_choice == '00':
            self.trans_res.add_access_res('', m_list[offset])
            offset += self.typedo.take_DAR(m_list[offset:], '错误信息')
        elif re_m_list_choice == '01':  # SEQUENCE OF A-ResultNormal
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象属性', 'SEQUENCE OF A_ResultNormal[%d]'%num, num, unit='个')
            offset += 1
            for _ in range(num):
                offset += self.take_A_ResultNormal(m_list[offset:], depth=1)
        elif re_m_list_choice == '02':  # SEQUENCE OF A-ResultRecord
            num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                    '记录型对象属性', 'SEQUENCE OF A-ResultRecord[%d]'%num, num, unit='个')
            offset += 1
            for _ in range(num):
                offset += self.take_A_ResultRecord(m_list[offset:], depth=1)
        return offset

    def GetResponseMD5(self, m_list):
        """GetResponseMD5"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        re_choice = m_list[offset]
        choice = {'00': '错误信息', '01': 'MD5值'}
        offset += self.typedo.take_CHOICE(m_list[offset:], '结果', choice_dict=choice)
        if re_choice == '00':
            self.trans_res.add_access_res('', m_list[offset + 1])
            offset += self.typedo.take_DAR(m_list[offset + 1:], '错误信息')
        elif re_choice == '01':
            self.trans_res.add_access_res('', '00')
            offset += self.typedo.take_octect_string(m_list[offset + 1:], 'MD5值')
        return offset

    def SetRequestNormal(self, m_list):
        """SetRequestNormal"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_OAD(m_list[offset:], 'OAD')
        oad = ''.join(m_list[offset - 4: offset])
        structure = config.K_DATA.get_structure('oad', oad)
        offset += self.typedo.take_Data(m_list[offset:], '', structure=structure)
        return offset

    def SetRequestNormalList(self, m_list):
        """SetRequestNormalList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象属性', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], 'OAD', depth=1)
            oad = ''.join(m_list[offset - 4: offset])
            structure = config.K_DATA.get_structure('oad', oad)
            offset += self.typedo.take_Data(m_list[offset:], '', depth=1, structure=structure)
        return offset

    def SetThenGetRequestNormalList(self, m_list):
        """SetThenGetRequestNormalList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '设置后读取对象属性', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], '设置的对象属性', depth=1)
            oad = ''.join(m_list[offset - 4: offset])
            structure = config.K_DATA.get_structure('oad', oad)
            offset += self.typedo.take_Data(m_list[offset:], '', depth=1, structure=structure)
            offset += self.typedo.take_OAD(m_list[offset:], '读取的对象属性', depth=1)
            offset += self.typedo.take_unsigned(m_list[offset:], '延时读取时间(秒)', depth=1)
        return offset

    def SetResponseNormal(self, m_list):
        """SetResponseNormal"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.typedo.take_OAD(m_list[offset:], 'OAD')
        self.trans_res.add_access_res(''.join(m_list[offset - 4: offset]), m_list[offset])
        offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果')
        return offset

    def SetResponseNormalList(self, m_list):
        """SetResponseNormalList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象属性设置结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], 'OAD', depth=1)
            self.trans_res.add_access_res(''.join(m_list[offset - 4: offset]), m_list[offset])
            offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果', depth=1)
        return offset

    def SetThenGetResponseNormalList(self, m_list):
        """SetThenGetResponseNormalList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象属性设置后读取结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], '设置的OAD', depth=1)
            self.trans_res.add_access_res(''.join(m_list[offset - 4: offset]), m_list[offset])
            offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果', depth=1)
            offset += self.typedo.take_OAD(m_list[offset:], '读取的OAD', depth=1)
            oad = ''.join(m_list[offset - 4: offset])
            self.trans_res.add_access_res(oad, m_list[offset])
            offset += self.take_Get_Result(m_list[offset:], '读取响应数据', depth=1, oad=oad)
        return offset

    def ActionRequest(self, m_list):
        """ActionRequest"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_OMD(m_list[offset:], '对象方法描述符')
        omd = ''.join(m_list[offset - 4: offset])
        structure = config.K_DATA.get_structure('omd', omd)
        offset += self.typedo.take_Data(m_list[offset:], '方法参数', structure=structure)
        return offset

    def ActionRequestList(self, m_list):
        """ActionRequestList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象属性', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OMD(m_list[offset:], '对象方法描述符', depth=1)
            omd = ''.join(m_list[offset - 4: offset])
            structure = config.K_DATA.get_structure('omd', omd)
            offset += self.typedo.take_Data(m_list[offset:], '方法参数', depth=1, structure=structure)
        return offset

    def ActionThenGetRequestNormalList(self, m_list):
        """ActionThenGetRequestNormalList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '操作对象方法后读取对象属性', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OMD(m_list[offset:], '设置的对象方法描述符', depth=1)
            omd = ''.join(m_list[offset - 4: offset])
            structure = config.K_DATA.get_structure('omd', omd)
            offset += self.typedo.take_Data(m_list[offset:], '方法参数', depth=1, structure=structure)
            offset += self.typedo.take_OMD(m_list[offset:], '读取的OAD', depth=1)
            offset += self.typedo.take_unsigned(m_list[offset:], '读取延时(秒)', depth=1)
        return offset

    def ActionResponseNormal(self, m_list):
        """ActionResponseNormal"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.typedo.take_OMD(m_list[offset:], '对象方法描述符')
        self.trans_res.add_access_res(''.join(m_list[offset - 4: offset]), m_list[offset])
        offset += self.typedo.take_DAR(m_list[offset:], '操作执行结果')
        optional = m_list[offset]
        offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据')
        if optional == '01':
            offset += self.typedo.take_Data(m_list[offset:], '', depth=1)
        return offset

    def ActionResponseNormalList(self, m_list):
        """ActionResponseNormalList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象方法操作结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OMD(m_list[offset:], '对象方法描述符', depth=1)
            self.trans_res.add_access_res(''.join(m_list[offset - 4: offset]), m_list[offset])
            offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果', depth=1)
            optional = m_list[offset]
            offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据', depth=1)
            if optional == '01':
                offset += self.typedo.take_Data(m_list[offset:], depth=1)
        return offset

    def ActionThenGetResponseNormalList(self, m_list):
        """ActionThenGetResponseNormalList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '操作对象方法后读取属性的结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OMD(m_list[offset:], '设置的对象方法描述符', depth=1)
            self.trans_res.add_access_res(''.join(m_list[offset - 4: offset]), m_list[offset])
            offset += self.typedo.take_DAR(m_list[offset:], '设置执行结果', depth=1)
            optional = m_list[offset]
            offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据', depth=1)
            if optional == '01':
                offset += self.typedo.take_Data(m_list[offset:], '', depth=2)
            offset += self.typedo.take_OAD(m_list[offset:], '读取的OAD', depth=1)
            oad = ''.join(m_list[offset - 4: offset])
            self.trans_res.add_access_res(oad, m_list[offset])
            offset += self.take_Get_Result(m_list[offset:], depth=1, oad=oad)
        return offset

    def ReportResponseList(self, m_list):
        """ReportResponseList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '对应上报的OAD', 'SEQUENCE OF OAD[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_OAD(m_list[offset:], depth=1)
        return offset

    def ReportResponseRecordList(self, m_list):
        """ReportResponseRecordList"""
        return self.ReportResponseList(m_list)

    def ReportResponseTransData(self, m_list):
        """ReportResponseTransData"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        return offset

    def ReportNotificationList(self, m_list):
        """ReportNotificationList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '对象属性及其数据', 'SEQUENCE OF A-ResultNormal[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.take_A_ResultNormal(m_list[offset:], depth=1)
        return offset

    def ReportNotificationRecordList(self, m_list):
        """ReportNotificationRecordList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '记录型对象属性及其数据', 'SEQUENCE OF A-ResultNormal[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.take_A_ResultRecord(m_list[offset:], depth=1)
        return offset

    def ReportNotificationTransData(self, m_list):
        """ReportNotificationTransData"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.typedo.take_OAD(m_list[offset:], '数据来源端口')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '透明数据', 'SEQUENCE OF octet-string[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_octect_string(m_list[offset:], depth=1)
        return offset

    def proxy_get_request_list(self, m_list):
        """proxy_get_request_list"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间(秒)')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的对象属性读取', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            offset += self.typedo.take_long_unsigned(m_list[offset:], '代理服务器的超时时间(秒)', depth=1)
            oad_num = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        'OAD', 'SEQUENCE OF OAD[%d]'%oad_num, oad_num, depth=1, unit='个')
            offset += 1
            for _ in range(oad_num):
                offset += self.typedo.take_OAD(m_list[offset:], '', depth=2)
        return offset

    def ProxyGetRequestRecord(self, m_list):
        """ProxyGetRequestRecord"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '代理请求的超时时间(秒)')
        offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址')
        offset += self.typedo.take_OAD(m_list[offset:], 'OAD')
        offset += self.typedo.take_RSD(m_list[offset:], '记录选择描述符')
        offset += self.typedo.take_RCSD(m_list[offset:], '记录列选择描述符')
        return offset

    def ProxySetRequestList(self, m_list):
        """ProxySetRequestList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间(秒)')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的对象属性设置', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            offset += self.typedo.take_long_unsigned(m_list[offset:], '代理服务器的超时时间(秒)', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        'OAD及其数据', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OAD(m_list[offset:], 'OAD', depth=2)
                oad = ''.join(m_list[offset - 4: offset])
                structure = config.K_DATA.get_structure('oad', oad)
                offset += self.typedo.take_Data(m_list[offset:], '', depth=2, structure=structure)
        return offset

    def ProxySetThenGetRequestList(self, m_list):
        """ProxySetThenGetRequestList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间(秒)')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的对象属性设置后读取', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            offset += self.typedo.take_long_unsigned(m_list[offset:], '代理服务器的超时时间(秒)', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        '对象属性的设置后读取', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OAD(m_list[offset:], '设置的OAD', depth=2)
                oad = ''.join(m_list[offset - 4: offset])
                structure = config.K_DATA.get_structure('oad', oad)
                offset += self.typedo.take_Data(m_list[offset:], '及其设置数值', depth=2, structure=structure)
                offset += self.typedo.take_OAD(m_list[offset:], '读取的OAD', depth=2)
                offset += self.typedo.take_unsigned(m_list[offset:], '及其延时读取时间(秒)', depth=2)
        return offset

    def ProxyActionRequestList(self, m_list):
        """ProxyActionRequestList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间(秒)')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的对象方法操作', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            offset += self.typedo.take_long_unsigned(m_list[offset:], '代理服务器的超时时间(秒)', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        '对象方法描述符及其参数', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OMD(m_list[offset:], '对象方法描述符', depth=2)
                omd = ''.join(m_list[offset - 4: offset])
                structure = config.K_DATA.get_structure('omd', omd)
                offset += self.typedo.take_Data(m_list[offset:], '及其方法参数', depth=2, structure=structure)
        return offset

    def ProxyActionThenGetRequestList(self, m_list):
        """ProxyActionThenGetRequestList"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '整个代理请求的超时时间(秒)')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的操作后读取', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            offset += self.typedo.take_long_unsigned(m_list[offset:], '代理服务器的超时时间(秒)', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        '对象方法及属性的操作后读取', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OMD(m_list[offset:], '操作的对象方法描述符', depth=2)
                omd = ''.join(m_list[offset - 4: offset])
                structure = config.K_DATA.get_structure('omd', omd)
                offset += self.typedo.take_Data(m_list[offset:], '及其方法参数', depth=2, structure=structure)
                offset += self.typedo.take_OAD(m_list[offset:], '读取的OAD', depth=2)
                offset += self.typedo.take_unsigned(m_list[offset:], '延时读取时间(秒)', depth=2)
        return offset

    def ProxyTransCommandRequest(self, m_list):
        """ProxyTransCommandRequest"""
        offset = 0
        offset += self.typedo.take_PIID(m_list[offset:], 'PIID')
        offset += self.typedo.take_OAD(m_list[offset:], '数据转发端口')
        offset += self.typedo.take_COMDCB(m_list[offset:], '端口通信控制块')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '接收等待报文超时时间(秒)')
        offset += self.typedo.take_long_unsigned(m_list[offset:], '接收等待字节超时时间(毫秒)')
        offset += self.typedo.take_octect_string(m_list[offset:], '透明转发命令')
        return offset

    def ProxyGetResponseList(self, m_list):
        """ProxyGetResponseList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的读取结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        'OAD及其结果', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OAD(m_list[offset:], 'OAD', depth=2)
                oad = ''.join(m_list[offset - 4: offset])
                offset += self.take_Get_Result(m_list[offset:], '及其读取结果', depth=2, oad=oad)
        return offset

    def ProxyGetResponseRecord(self, m_list):
        """ProxyGetResponseRecord"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址')
        offset += self.take_A_ResultRecord(m_list[offset:], '记录型对象属性及其结果')
        return offset

    def ProxySetResponseList(self, m_list):
        """ProxySetResponseList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的读取结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        'OAD及其结果', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OAD(m_list[offset:], 'OAD', depth=2)
                offset += self.typedo.take_DAR(m_list[offset:], '及其设置结果', depth=2)
        return offset

    def ProxySetThenGetResponseList(self, m_list):
        """ProxySetThenGetResponseList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的设置后读取结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        '对象属性设置后读取结果', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OAD(m_list[offset:], '设置的OAD', depth=2)
                offset += self.typedo.take_DAR(m_list[offset:], '及其设置结果', depth=2)
                offset += self.typedo.take_OAD(m_list[offset:], '读取的OAD', depth=2)
                oad = ''.join(m_list[offset - 4: offset])
                offset += self.take_Get_Result(m_list[offset:], '及其读取结果', depth=2, oad=oad)
        return offset

    def ProxyActionResponseList(self, m_list):
        """ProxyActionResponseList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的操作结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        '对象属性设置后读取结果', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OMD(m_list[offset:], '对象方法描述符', depth=2)
                offset += self.typedo.take_DAR(m_list[offset:], '及其操作结果', depth=2)
                optional = m_list[offset]
                offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据', depth=2)
                if optional == '01':
                    offset += self.typedo.take_Data(m_list[offset:], '', depth=3)
        return offset

    def ProxyActionThenGetResponseList(self, m_list):
        """ProxyActionThenGetResponseList"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        num = int(m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+1],\
                    '代理服务器的操作后读取结果', 'SEQUENCE OF[%d]'%num, num, unit='个')
        offset += 1
        for _ in range(num):
            offset += self.typedo.take_TSA(m_list[offset:], '目标服务器地址', depth=1)
            num1 = int(m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+1],\
                        '对象方法和属性操作后读取结果', 'SEQUENCE OF[%d]'%num1, num1, depth=1, unit='个')
            offset += 1
            for _ in range(num1):
                offset += self.typedo.take_OMD(m_list[offset:], '操作的对象方法描述符', depth=2)
                offset += self.typedo.take_DAR(m_list[offset:], '及其操作结果', depth=2)
                optional = m_list[offset]
                offset += self.typedo.take_OPTIONAL(m_list[offset:], '操作返回数据', depth=2)
                if optional == '01':
                    offset += self.typedo.take_Data(m_list[offset:], '', depth=3)
                offset += self.typedo.take_OAD(m_list[offset:], '读取的OAD', depth=2)
                oad = ''.join(m_list[offset - 4: offset])
                offset += self.take_Get_Result(m_list[offset:], '及其读取结果', depth=2, oad=oad)
        return offset

    def ProxyTransCommandResponse(self, m_list):
        """ProxyTransCommandResponse"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.typedo.take_OAD(m_list[offset:], '数据转发端口')
        trans_result_choice = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], '透明转发命令返回结果',\
                                    choice_dict={'00': '错误信息', '01': '返回数据'})
        if trans_result_choice == '00':
            offset += self.typedo.take_DAR(m_list[offset:], '错误信息', depth=1)
        elif trans_result_choice == '01':
            offset += self.typedo.take_octect_string(m_list[offset:], '', depth=1)
        return offset

    def security_request(self, m_list):
        """security_request"""
        offset = 0
        security_choice = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], '应用数据单元',\
                        choice_dict={'00': '明文应用数据单元', '01': '密文应用数据单元'})
        if security_choice == '00':
            res = self.typedo.take_axdr_len(m_list[offset:])
            self.trans_res.add_row(m_list[offset: offset+res['offset']], '明文应用数据单元[%d]'%res['len'])
            offset += res['offset']
            offset += self.take_service(m_list[offset:])
        else:
            offset += self.typedo.take_octect_string(m_list[offset:], '密文应用数据单元')
        security_choice = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], '数据验证信息',\
                        choice_dict={'00': '数据验证码', '01': '随机数', '02': '随机数+数据MAC', '03': '安全标识',})
        offset += {
            '00': self.typedo.take_SID_MAC,
            '01': self.typedo.take_RN,
            '02': self.typedo.take_RN_MAC,
            '03': self.typedo.take_SID,
        }[security_choice](m_list[offset:])
        return offset

    def security_response(self, m_list):
        """security_response"""
        offset = 0
        security_choice = m_list[offset]
        offset += self.typedo.take_CHOICE(m_list[offset:], '应用数据单元',\
                        choice_dict={'00': '明文应用数据单元', '01': '密文应用数据单元'})
        if security_choice == '00':
            res = self.typedo.take_axdr_len(m_list[offset:])
            self.trans_res.add_row(m_list[offset: offset+res['offset']], '明文应用数据单元[%d]'%res['len'])
            offset += res['offset']
            offset += self.take_service(m_list[offset:])
        elif security_choice == '01':
            offset += self.typedo.take_octect_string(m_list[offset:], '密文应用数据单元')
        elif security_choice == '02':
            offset += self.typedo.take_DAR(m_list[offset:], '异常错误')
        optional = m_list[offset]
        offset += self.typedo.take_OPTIONAL(m_list[offset:], '数据验证信息')
        if optional == '01':
            check_choice = m_list[offset]
            offset += self.typedo.take_CHOICE(m_list[offset:], '数据验证信息',\
                            choice_dict={'00': '数据MAC'})
            if check_choice == '00':
                offset += self.typedo.take_MAC(m_list[offset:], '数据MAC')
        return offset

    def ERRORResponse(self, m_list):
        """ERRORResponse"""
        offset = 0
        offset += self.typedo.take_PIID_ACD(m_list[offset:], 'PIID-ACD')
        offset += self.typedo.take_enum(m_list[offset:], brief='异常类型',\
                        enum_dict={'01': 'APDU 无法解析', '02': '服务不支持', 'FF': '其他'})
        return offset
