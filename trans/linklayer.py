'''handle with 698 link layer'''
import trans.common as commonfun
import config

def take_linklayer(m_list, trans_res):
    '''translate linklayer'''
    offset = 0
    trans_res.add_row(m_list[offset:], 1, '帧起始符', 0)
    offset += 1
    trans_res.add_row(m_list[offset:], 2, '长度L:'
                      + str(int(m_list[offset + 1] + m_list[offset], 16)) + '字节', 0)
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
    trans_res.add_row(m_list[offset:], 1, '控制域C: ' + frame_type + ' ' + function_type, 0)
    offset += 1

    # 地址域
    server_addr_type = {
        0: ' 单地址',
        1: ' 通配地址',
        2: ' 组地址',
        3: ' 广播地址'
    }.get(int(m_list[offset], 16) >> 6, '错误')
    server_logic_addr = (int(m_list[offset], 16) >> 4) & 0x03
    server_addr_len = (int(m_list[offset], 16) & 0x0f) + 1
    server_addr_reverse = m_list[offset + server_addr_len: offset: -1]
    server_addr = ''
    for k in range(0, server_addr_len):
        server_addr += server_addr_reverse[k]
    trans_res.add_row(m_list[offset:], server_addr_len + 1,\
                    '服务器地址: 逻辑地址' + str(server_logic_addr) + server_addr_type + server_addr, 0)
    offset += server_addr_len + 1
    trans_res.add_row(m_list[offset:], 1, '客户机地址: ' + m_list[offset], 0)
    offset += 1

    # 帧头校验
    # print('hcs_calc:', data[1:offset], 'len', offset - 1)
    hcs_calc = commonfun.get_fcs(m_list[1:offset])
    hcs_calc = ((hcs_calc << 8) | (hcs_calc >> 8)) & 0xffff  # 低位在前
    # print('fcs test:', data[1:offset], 'cs:', hex(hcs_calc))
    fcs_now = int(m_list[offset] + m_list[offset + 1], 16)
    if fcs_now == hcs_calc:
        hcs_check = '(正确)'
        config.good_HCS = None
    else:
        hcs_check = '(错误，正确值{0:04X})'.format(hcs_calc)
        config.good_HCS = ['{0:02X}'.format(hcs_calc >> 8), '{0:02X}'.format(hcs_calc & 0xff)]
    trans_res.add_row(m_list[offset:], 2, '帧头校验:{0:04X}'.format(fcs_now) + hcs_check, 0)
    offset += 2

    # 分帧
    if frame_separation_flag == 1:
        frame_separation = int(m_list[offset] + m_list[offset + 1], 16)
        frame_separation_seq = frame_separation & 0x3f
        frame_separation_type = {
            0: '(起始帧)',
            1: '(最后帧)',
            2: '(确认帧)',
            3: '(中间帧)',
        }.get(frame_separation >> 14, '错误')
        trans_res.add_row(m_list[offset:], 2,
                          '分帧序号:' + str(frame_separation_seq) + frame_separation_type, 0)
        offset += 2
    return offset


