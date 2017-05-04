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
        link_type = {
            '00': ' —— 登录',
            '01': ' —— 心跳',
            '02': ' —— 退出登录'
        }.get(m_list[offset], '错误')
        self.trans_res.add_row(m_list[offset:], 1, link_type, 0)
        offset += 1
        offset += self.typedo.take_long_unsigned(m_list[offset:], '心跳周期s:')
        offset += self.typedo.take_date_time(m_list[offset:], '请求时间:')
        return offset

    # def link_response(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:])
    #     time_credible_flag = int(m_list[offset], 16) >> 7
    #     if time_credible_flag == 1:
    #         output(m_list[offset] + ' —— 结果Result：可信')
    #     else:
    #         output(m_list[offset] + ' —— 结果Result：不可信')
    #     offset += 1
    #     offset += self.typedo.take_date_time(m_list[offset:], '请求时间:')
    #     offset += self.typedo.take_date_time(m_list[offset:], '收到时间:')
    #     offset += self.typedo.take_date_time(m_list[offset:], '响应时间:')
    #     return offset


    # def connect_request(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:])
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '期望的应用层协议版本号:')
    #     show_m_list_source(m_list[offset:], 8)
    #     output(' —— 期望的协议一致性块')
    #     offset += 8
    #     show_m_list_source(m_list[offset:], 16)
    #     offset += 16
    #     output(' —— 期望的功能一致性块')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '客户机发送帧最大尺寸:')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '客户机接收帧最大尺寸:')
    #     offset += self.typedo.take_unsigned(m_list[offset:], '客户机接收帧最大窗口尺寸:')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '客户机最大可处理APDU尺寸:')
    #     offset += self.typedo.take_double_long_unsigned(m_list[offset:], '期望的应用连接超时时间:')
    #     offset += self.typedo.take_ConnectMechanismInfo(m_list[offset:], '认证请求对象:')
    #     return offset


    # def connect_response(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:])
    #     offset += self.typedo.take_FactoryVersion(m_list[offset:])
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '商定的应用层协议版本号:')
    #     show_m_list_source(m_list[offset:], 8)
    #     output(' —— 期望的协议一致性块')
    #     offset += 8
    #     show_m_list_source(m_list[offset:], 16)
    #     offset += 16
    #     output(' —— 期望的功能一致性块')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '服务器发送帧最大尺寸:')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '服务器发送帧最大尺寸:')
    #     offset += self.typedo.take_unsigned(m_list[offset:], '服务器发送帧最大窗口尺寸:')
    #     offset += self.typedo.take_long_unsigned(m_list[offset:], '服务器最大可处理APDU尺寸:')
    #     offset += self.typedo.take_double_long_unsigned(m_list[offset:], '商定的应用连接超时时间:')
    #     offset += self.typedo.take_ConnectResponseInfo(m_list[offset:], '连接响应对象:')
    #     return offset


    # def release_request(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID(m_list[offset:])
    #     return offset


    # def release_response(self, m_list):
    #     offset = 0
    #     offset += self.typedo.take_PIID_ACD(m_list[offset:])
    #     if m_list[offset] == '00':
    #         output(m_list[offset] + ' —— 成功')
    #     else:
    #         output(m_list[offset] + ' —— 不成功')
    #     offset += 1
    #     return offset


    