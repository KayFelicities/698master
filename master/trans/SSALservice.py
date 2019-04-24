"""handle with SSAL service"""
from master import config
import master.trans.linklayer as linklayer_do
import master.trans.service as applayer_do



def take_ssal_app(m_list, FC, trans_res):
    """take_ssal_applayer"""
    offset = 0
    service = SSALService(trans_res)
    offset += service.take_service(m_list[offset:], FC)
    return offset


class SSALService:
    """SSALService class"""
    def __init__(self, trans_res):
        """init"""
        self.trans_res = trans_res

    def take_service(self, m_list, FC):
        """take ssal app"""
        offset = 0
        msg_type = FC & 0x0f
        dir = (FC >> 7) & 1
        prm = (FC >> 6) & 1

        # 数据长度
        lud_len = int(m_list[offset + 1] + m_list[offset], 16)
        lud_len_right = len(m_list) - 4 if prm == 0 else len(m_list) - 2
        brief = '数据长度(%s)'%('正确' if lud_len == lud_len_right else '错误(正确值 %02X %02X)'%(lud_len_right & 0xff, lud_len_right >> 8))
        self.trans_res.add_row(m_list[offset: offset+2], brief, 'LUD', '%d'%lud_len)
        offset += 2

        if prm == 0:
            err_code = int(m_list[offset + 1] + m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+2], '返回信息',\
                        '', self.get_err_msg(err_code))
            offset += 2

        if lud_len == 0:
            pass
        elif msg_type == 2 and dir == 0:  # 下行获取终端基本信息
            pass
        elif msg_type == 2 and dir == 1:  # 上行获取终端基本信息
            offset += self.take_terminal_info(m_list[offset:])
        elif msg_type == 3:  # 上、下行会话密钥协商
            m_len = int(m_list[offset + 1] + m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+2 + m_len], '会话密钥素材',\
                        'SSAL-string[%d]'%m_len, ''.join(m_list[offset+2: offset+2 + m_len]))
            offset += 2 + m_len

            s_len = int(m_list[offset + 1] + m_list[offset], 16)
            self.trans_res.add_row(m_list[offset: offset+2 + s_len], '签名',\
                        'SSAL-string[%d]'%s_len, ''.join(m_list[offset+2: offset+2 + s_len]))
            offset += 2 + s_len
        else: # 698报文
            offset += self.take_698_full(m_list[offset:])
        return offset

    def take_698_full(self, m_list, brief='', depth=0):
        """take_698_full"""
        offset = 0
        if m_list[offset] == '68':  # todo: 先这样判断明文和密文
            offset += linklayer_do.take_linklayer1(m_list[offset:], self.trans_res)
            if (int(m_list[3], 16) >> 5) & 0x01 == 1: #linklayer sep
                self.is_linklayer_sep = True
                self.trans_res.add_row(m_list[offset : len(m_list) - 3], '链路层分帧片段', '', ''.join(m_list[offset : len(m_list) - 3]), priority=1)
                offset = len(m_list) - 3
            else:
                offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
            offset += linklayer_do.take_linklayer2(m_list[:], offset, self.trans_res)
        else:
            self.trans_res.add_row(m_list[:], 'SSAL密文', '', ''.join(m_list[:]), priority=1)
            offset += len(m_list)
        return offset

    def take_terminal_info(self, m_list, brief='', depth=0):
        """take_A_ResultNormal"""
        offset = 0
        len1 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len1], 'ESAM序列号',\
                    'SSAL-string[%d]'%len1, ''.join(m_list[offset+2: offset+2 + len1]))
        offset += 2 + len1

        len2 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len2], 'ESAM版本号',\
                    'SSAL-string[%d]'%len2, ''.join(m_list[offset+2: offset+2 + len2]))
        offset += 2 + len2

        len3 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len3], '链路对称密钥版本',\
                    'SSAL-string[%d]'%len3, ''.join(m_list[offset+2: offset+2 + len3]))
        offset += 2 + len3

        len4 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len4], '证书版本',\
                    'SSAL-string[%d]'%len4, ''.join(m_list[offset+2: offset+2 + len4]))
        offset += 2 + len4

        len5 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len5], '链路会话时效门限',\
                    'SSAL-string[%d]'%len5, ''.join(m_list[offset+2: offset+2 + len5]))
        offset += 2 + len5

        len6 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len6], '链路会话时效剩余时间',\
                    'SSAL-string[%d]'%len6, ''.join(m_list[offset+2: offset+2 + len6]))
        offset += 2 + len6

        len7 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len7], '当前计数器',\
                    'SSAL-string[%d]'%len7, ''.join(m_list[offset+2: offset+2 + len7]))
        offset += 2 + len7

        len8 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len8], '链路证书序列号',\
                    'SSAL-string[%d]'%len8, ''.join(m_list[offset+2: offset+2 + len8]))
        offset += 2 + len8

        len9 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len9], '链路证书',\
                    'SSAL-string[%d]'%len9, ''.join(m_list[offset+2: offset+2 + len9]))
        offset += 2 + len9

        len10 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len10], '网关证书序列号',\
                    'SSAL-string[%d]'%len10, ''.join(m_list[offset+2: offset+2 + len10]))
        offset += 2 + len10

        len11 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len11], '终端序列号',\
                    'SSAL-string[%d]'%len11, ''.join(m_list[offset+2: offset+2 + len11]))
        offset += 2 + len11

        len12 = int(m_list[offset + 1] + m_list[offset], 16)
        self.trans_res.add_row(m_list[offset: offset+2 + len12], '终端ESN号',\
                    'SSAL-string[%d]'%len12, ''.join(m_list[offset+2: offset+2 + len12]))
        offset += 2 + len12
        return offset


    def get_err_msg(self, err_code):
        """get_err_msg"""
        return {
            0x0000: '正确', 
            0x1001: '安全认证-终端解密错误', 
            0x1002: '安全认证-终端验签失败', 
            0x1003: '安全认证-终端MAC校验失败', 
            0x1004: '安全认证-会话计数器错误', 
            0x1005: '安全认证-网关解密错误', 
            0x1006: '安全认证-网关验签失败', 
            0x1007: '安全认证-网关MAC校验失败', 
            0x1008: '安全认证-网关密码单元故障', 
            0x1009: '安全认证-链路设备密码单元故障', 
            0x2001: '帧校验-协议版本错误', 
            0x2002: '帧校验-加解密算法标志不匹配', 
            0x2003: '帧校验-设备类型无法识别', 
            0x2004: '帧校验-控制码无法识别', 
            0x2005: '帧校验-传输方向位错误', 
            0x2006: '帧校验-数据域长度异常（小于4字节）', 
            0x2007: '帧校验-数据域长度不匹配', 
            0x3001: '链路-目标节点不存在', 
            0x3002: '链路-当前会话未建立', 
            0x3003: '链路-报文发送失败', 
            0x3004: '链路-信道错误', 
            0x3005: '链路-当前链路会话协商失败', 
            }.get(err_code, '未知错误码0x%X' % err_code)

