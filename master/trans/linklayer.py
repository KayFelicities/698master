"""handle with 698 link layer"""
import master.trans.common as commonfun
import master.trans.service as applayer_do


def take_linklayer1(m_list, trans_res):
    """translate linklayer"""
    offset = 0
    trans_res.add_row(m_list[offset : offset+1], '帧起始符', value=68, priority=0)
    offset += 1
    link_length = int(m_list[offset + 1] + m_list[offset], 16)
    if link_length == len(m_list) - 2:
        length_check = '(正确)'
    else:
        length_check = '(错误，正确值{0:d}({0:04X}))'.format(len(m_list) - 2)
    trans_res.add_row(m_list[offset : offset+2], '长度L', '',\
                      int(m_list[offset + 1] + m_list[offset], 16), '字节' + length_check, priority=0)
    offset += 2

    # 控制域
    ctrol = int(m_list[offset], 16)
    dir_prm_flag = ctrol >> 6
    frame_separation_flag = (ctrol >> 5) & 0x01
    function_flag = ctrol & 0x03
    frame_type = {
        0: '完整报文',
        1: '分帧报文'
    }.get(frame_separation_flag, '错误')
    function_type = ''
    if function_flag == 1:
        function_type = {
            0: '主站确认登录心跳',
            2: '终端登录心跳'
        }.get(dir_prm_flag, '错误')
    elif function_flag == 3:
        function_type = {
            0: '主站确认主动上报',
            1: '主站向终端下发命令',
            2: '终端主动上报',
            3: '终端响应主站命令'
        }.get(dir_prm_flag, '错误')
    else:
        function_type = '错误'
    trans_res.add_row(m_list[offset: offset+1], '控制域C', '', frame_type + ',' + function_type, priority=0)
    offset += 1

    # 地址域
    server_addr_type = {
        0: '单地址',
        1: '通配地址',
        2: '组地址',
        3: '广播地址'
    }.get(int(m_list[offset], 16) >> 6, '错误')
    server_logic_addr = (int(m_list[offset], 16) >> 4) & 0x03
    server_addr_len = (int(m_list[offset], 16) & 0x0f) + 1
    server_logic_len = 0
    if server_logic_addr > 1: # 扩展逻辑地址
        server_logic_len = 1
        server_logic_addr = int(m_list[offset + 1], 16)
    server_addr_reverse = m_list[offset + server_addr_len: offset + server_logic_len: -1]
    server_addr = ''.join(server_addr_reverse)
    trans_res.add_row(m_list[offset: offset+server_addr_len+1], '服务器地址', 'SA',\
                    '逻辑地址[%s], %s[%s]'%(server_logic_addr, server_addr_type, server_addr), priority=0)
    offset += server_addr_len + 1
    trans_res.add_row(m_list[offset: offset+1], '客户机地址', 'CA', '{0:02X}'.format(int(m_list[offset], 16)), priority=0)
    offset += 1

    # 帧头校验
    # print('hcs_calc:', m_list[1:offset], 'len', offset - 1)
    hcs_calc = commonfun.get_fcs(m_list[1:offset])
    hcs_calc = ((hcs_calc << 8) | (hcs_calc >> 8)) & 0xffff  # 低位在前
    # print('fcs test:', m_list[1:offset], 'cs:', hex(hcs_calc))
    fcs_now = int(m_list[offset] + m_list[offset + 1], 16)
    if fcs_now == hcs_calc:
        hcs_check = '(正确)'
    else:
        hcs_check = '(错误，正确值{0:04X})'.format(hcs_calc)
    trans_res.add_row(m_list[offset: offset+2], '帧头校验', '', '{0:04X}'.format(fcs_now) + hcs_check, priority=0)
    offset += 2

    # 分帧
    if frame_separation_flag == 1:
        frame_separation = int(m_list[offset + 1] + m_list[offset], 16)
        frame_separation_seq = frame_separation & 0x3f
        frame_separation_type = {
            0: '(起始帧)',
            1: '(最后帧)',
            2: '(确认帧)',
            3: '(中间帧)',
        }.get(frame_separation >> 14, '错误')
        trans_res.add_row(m_list[offset: offset+2], '分帧序号', '', str(frame_separation_seq) + frame_separation_type, priority=0)
        offset += 2
    return offset


def take_linklayer2(m_list, offset, trans_res):
    """take_linklayer2"""
    offset_temp = offset
    fcs_calc = commonfun.get_fcs(m_list[1:offset])
    fcs_calc = ((fcs_calc << 8) | (fcs_calc >> 8)) & 0xffff  # 低位在前
    # print('fcs test:', m_list[1:offset], 'cs:', hex(fcs_calc))
    fcs_now = int(m_list[offset] + m_list[offset + 1], 16)
    if fcs_now == fcs_calc:
        hcs_check = '(正确)'
    else:
        hcs_check = '(错误，正确值{0:04X})'.format(fcs_calc)
    trans_res.add_row(m_list[offset: offset+2], '帧校验', '', '{0:04X}'.format(fcs_now) + hcs_check, priority=0)
    offset += 2
    trans_res.add_row(m_list[offset: offset+1], '结束符%s'%('(错误)' if m_list[offset] != '16' else ''),\
                        value=m_list[offset], priority=0)
    offset += 1
    return offset - offset_temp


def add_linkLayer(apdu_list, CA_text='00', SA_text='00000001', logic_addr=0, SA_type=0, C_text='43'):
    """add linklayer"""
    SA_list = commonfun.text2list(SA_text)
    SA_list.reverse()  # 小端
    SA_text = ''.join(SA_list)
    if len(SA_text) % 2 == 1:
        SA_text += '0'
    if logic_addr > 1:  # 扩展逻辑地址
        SA_param_text = '{0:02X}'.format(((len(SA_text) // 2) & 0x0f) | (0x02 << 4) | ((SA_type & 0x03) << 6))
        SA_param_text += '%02X'%logic_addr
    else:
        SA_param_text = '{0:02X}'.format(((len(SA_text) // 2 - 1) & 0x0f) | ((logic_addr & 0x03) << 4) | ((SA_type & 0x03) << 6))
    L_text = '{0:04X}'.format(len(SA_text) // 2 + (10 if logic_addr > 1 else 9) + len(apdu_list))
    L_text = L_text[2:4] + L_text[0:2]
    hcs_clac_aera_text = L_text + C_text + SA_param_text + SA_text + CA_text
    hcs_calc = commonfun.get_fcs(commonfun.text2list(hcs_clac_aera_text))
    hcs_calc = ((hcs_calc << 8) | (hcs_calc >> 8)) & 0xffff  # 低位在前
    fcs_calc_aera_text = hcs_clac_aera_text + '{0:04X}'.format(hcs_calc) + commonfun.list2text(apdu_list)
    fcs_calc = commonfun.get_fcs(commonfun.text2list(fcs_calc_aera_text))
    fcs_calc = ((fcs_calc << 8) | (fcs_calc >> 8)) & 0xffff  # 低位在前

    return commonfun.format_text('68' + fcs_calc_aera_text + '{0:04X}'.format(fcs_calc) + '16')

def repair_cs(m_text):
    """repair_cs"""
    m_list = commonfun.text2list(m_text)
    offset = 1
    link_length = int(m_list[offset + 1] + m_list[offset], 16)
    if link_length != len(m_list) - 2:
        right_len = len(m_list) - 2
        m_list[offset + 1] = '{0:02X}'.format(right_len >> 8)
        m_list[offset] = '{0:02X}'.format(right_len & 0xff)
    offset += 2

    # 控制域
    ctrol = int(m_list[offset], 16)
    frame_separation_flag = (ctrol >> 5) & 0x01

    # 控制域
    offset += 1

    # 地址域
    server_addr_len = (int(m_list[offset], 16) & 0x0f) + 1
    offset += server_addr_len + 1

    # 客户机地址
    offset += 1

    # 帧头校验
    hcs_calc = commonfun.get_fcs(m_list[1:offset])
    hcs_calc = ((hcs_calc << 8) | (hcs_calc >> 8)) & 0xffff  # 低位在前
    hcs_now = int(m_list[offset] + m_list[offset + 1], 16)
    if hcs_now != hcs_calc:
        m_list[offset] = '{0:02X}'.format(hcs_calc >> 8)
        m_list[offset + 1] = '{0:02X}'.format(hcs_calc & 0xff)
    offset += 2

    # 分帧
    if frame_separation_flag == 1:
        offset += 2

    trans_res = commonfun.TransRes()
    offset += applayer_do.take_applayer(m_list[offset:], trans_res)

    fcs_calc = commonfun.get_fcs(m_list[1:offset])
    fcs_calc = ((fcs_calc << 8) | (fcs_calc >> 8)) & 0xffff  # 低位在前
    fcs_now = int(m_list[offset] + m_list[offset + 1], 16)
    if fcs_now != fcs_calc:
        m_list[offset] = '{0:02X}'.format(fcs_calc >> 8)
        m_list[offset + 1] = '{0:02X}'.format(fcs_calc & 0xff)

    m_text = commonfun.list2text(m_list)
    return m_text


if __name__ == "__main__":
    msg = '68 17 00 43 05 33 33 22 22 00 00 32 56 2E 05 01 3F 31 06 09 00 00 84 99 16'
    res = repair_cs(msg)
    print(res)