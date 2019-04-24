"""handle with SSAL layer"""
import master.trans.common as commonfun

SSAL_PRIORITY = -1


def take_ssal_head(m_list, trans_res):
    """translate ssal head"""
    offset = 0
    trans_res.add_row(m_list[offset : offset+1], '帧起始符', value=98, priority=SSAL_PRIORITY)
    offset += 1
    link_length = int(m_list[offset + 1] + m_list[offset], 16)
    if link_length == len(m_list) - 4:
        length_check = '(正确)'
    else:
        length_check = '(错误，正确值{0:d}({0:04X}))'.format(len(m_list) - 4)
    trans_res.add_row(m_list[offset : offset+2], '长度L', '',\
                      link_length, '字节' + length_check, priority=SSAL_PRIORITY)
    offset += 2

    # seq
    seq = int(m_list[offset + 1] + m_list[offset], 16)
    trans_res.add_row(m_list[offset : offset+2], '帧序号', 'SEQ', seq, '', priority=SSAL_PRIORITY)
    offset += 2

    # 控制域
    ctrol = int(m_list[offset + 1] + m_list[offset], 16)
    ctrol_bin = bin(ctrol)[2:]
    ctrol_bin = '0'*(16 - len(ctrol_bin)) + ctrol_bin
    trans_res.add_row(m_list[offset: offset+2], '控制码', 'C', ctrol_bin, priority=SSAL_PRIORITY)
    offset += 2

    # 功能码
    if commonfun.is_bit(ctrol, 15):
        c_code = int(m_list[offset], 16)
        c_dir = '上行' if commonfun.is_bit(c_code, 7) else '下行'
        c_prm = '来自启动站' if commonfun.is_bit(c_code, 6) else '来自从动站'
        c_trig = '可能触发协商' if commonfun.is_bit(c_code, 4) else '不触发协商'
        c_type = {0: '应用数据报文', 1: '链路管理报文', 2: '获取终端基本信息报文', 3: '终端会话协商报文',
                        4: '更改时效门限', 5: '终端链路密钥更新', 6: '终端网关证书更新', 7: '查询网关链接状态', 
                        8: '安全接入区设备密钥协商触发', 9: '网关链路心跳', 10: '终端会话申请', 11: '终端会话确认',
                        12: '网关查询指令'}.get(c_code & 0x0f, '未知报文类型%d'%(c_code & 0x0f))
        trans_res.add_row(m_list[offset: offset+1], '功能码', 'FC', 
                '{dir}, {prm}, {trig}, {type}'.format(dir=c_dir, prm=c_prm, trig=c_trig, type=c_type), priority=SSAL_PRIORITY)
        offset += 1

    # 协议版本
    if commonfun.is_bit(ctrol, 14):
        sv_ver = '0x%02X'%int(m_list[offset + 1], 16)
        sv_etype = {0: '明文', 1: 'CBC密文', 2: '明文+MAC', 3: 'ECB密文', 4: 'CBC密文+MAC', 5: 'ECB密文+MAC'}\
                    .get(int(m_list[offset], 16), '未知%d'%(int(m_list[offset], 16) & 0x0f))
        trans_res.add_row(m_list[offset: offset+2], '协议版本', 'SV', 
                'SSAL协议版本:{ver}, 加密算法:{etype}'.format(ver=sv_ver, etype=sv_etype), priority=SSAL_PRIORITY)
        offset += 2

    # 设备地址类型
    if commonfun.is_bit(ctrol, 13):
        device_int = (int(m_list[offset + 1], 16) >> 3) & 0x1f
        device_type = {0: '采集前置/通信后置', 1: '采集设备', 2: '现场服务终端（掌机）', 3: '移动办公设备(营业办公设备)', 
                        4: '通信前置', 5: '3A认证服务器', 6: '在线性能检测服务器', 7: '接入区运维专用设备', 24: '网上国网APP终端', 25: '隔离装置'}\
                    .get(device_int, '未知%d'%device_int)
        addr_int = int(m_list[offset + 1], 16) & 0x07
        addr_type = {0: '单地址', 1: '组地址', 2: '广播地址'}\
                    .get(addr_int, '未知%d'%addr_int)
        app_int = int(m_list[offset], 16) & 0x1f
        app_ver = {0: '初始版本', 1: '698', 2: '1376.1', 3: '移动互联网APP'}\
                    .get(app_int, '未知%d'%app_int)
        trans_res.add_row(m_list[offset: offset+2], '设备地址类型', 'DAT', 
                '设备类型:{device}, 地址类型:{addr}, 应用协议版本:{app}'.format(device=device_type, addr=addr_type, app=app_ver), priority=SSAL_PRIORITY)
        offset += 2

    # 设备地址
    if commonfun.is_bit(ctrol, 12):
        addr_len = (int(m_list[offset], 16) >> 4) & 0x07
        logic_addr_len = int(m_list[offset], 16) & 0x0f
        if device_int not in [1, 2, 3, 24] and addr_len == 4:
            address = '%d.%d.%d.%d'%(int(m_list[offset+1 + 3], 16), int(m_list[offset+1 + 2], 16), int(m_list[offset+1 + 3], 16), int(m_list[offset+1], 16))
        else:
            address = ''.join(m_list[offset + 1: offset + 1 + logic_addr_len][::-1])
        trans_res.add_row(m_list[offset: offset+1+logic_addr_len], '设备地址', 'DA', address, priority=SSAL_PRIORITY)
        offset += 1 + logic_addr_len

    # 源地址SA
    if commonfun.is_bit(ctrol, 11):
        s_port_len = (int(m_list[offset], 16) >> 5) & 0x07
        s_addr_len = int(m_list[offset], 16) & 0x1f
        offset += 1
        if s_addr_len == 4: # 先这样判断是不是IP
            s_addr = '%d.%d.%d.%d'%(int(m_list[offset + 3], 16), int(m_list[offset + 2], 16), int(m_list[offset + 1], 16), int(m_list[offset], 16))
        else:
            s_addr = ''.join(m_list[offset: offset + s_addr_len][::-1])
        offset += s_addr_len
        s_port = ' : ' + ''.join(m_list[offset: offset + s_port_len][::-1]) if s_port_len else ''
        offset += s_port_len
        trans_res.add_row(m_list[offset - s_port_len - s_addr_len - 1: offset], '源地址', 'SA', s_addr + s_port, priority=SSAL_PRIORITY)

    # 目的地址TA
    if commonfun.is_bit(ctrol, 10):
        t_port_len = (int(m_list[offset], 16) >> 5) & 0x07
        t_addr_len = int(m_list[offset], 16) & 0x1f
        offset += 1
        if t_addr_len == 4: # 先这样判断是不是IP
            t_addr = '%d.%d.%d.%d'%(int(m_list[offset + 3], 16), int(m_list[offset + 2], 16), int(m_list[offset + 1], 16), int(m_list[offset], 16))
        else:
            t_addr = ''.join(m_list[offset: offset + t_addr_len][::-1])
        offset += t_addr_len
        t_port = ' : ' + ''.join(m_list[offset: offset + t_port_len][::-1]) if t_port_len else ''
        offset += t_port_len
        trans_res.add_row(m_list[offset - t_port_len - t_addr_len - 1: offset], '目的地址', 'TA', t_addr + t_port, priority=SSAL_PRIORITY)

    # 通信信息
    if commonfun.is_bit(ctrol, 9):
        ci_type_int = (int(m_list[offset], 16) >> 5) & 0x0f
        ci_type = {0: '无信道信息', 1: '无线公网', 2: '专网', 3: '230', 4: '短信', 5: '北斗'}\
                    .get(ci_type_int, '未知%d'%device_int)
        ci_len = int(m_list[offset], 16) & 0x0f
        ci_content = ''.join(m_list[offset+1: offset+1 + ci_len])
        trans_res.add_row(m_list[offset: offset+1 + ci_len], '通信信息', 'CI', '类型:%s, 内容:%s'%(ci_type, ci_content), priority=SSAL_PRIORITY)
        offset += 1 + ci_len

    # 时间标签
    if commonfun.is_bit(ctrol, 8):
        tp_str = '%d-%d-%d %d:%d:%d'%(int(m_list[offset] + m_list[offset+1], 16), int(m_list[offset+2], 16), 
                int(m_list[offset+3], 16), int(m_list[offset+4], 16), int(m_list[offset+5], 16), int(m_list[offset+6], 16))
        trans_res.add_row(m_list[offset: offset + 7], '时间标签', 'TP', tp_str, priority=SSAL_PRIORITY)
        offset += 7

    # 网关地址 
    if commonfun.is_bit(ctrol, 7):
        ga_len = int(m_list[offset], 16) & 0x1f
        if ga_len == 4:
            ga_content = '%d.%d.%d.%d'%(int(m_list[offset+1 + 3], 16), int(m_list[offset+1 + 2], 16), int(m_list[offset+1 + 1], 16), int(m_list[offset+1], 16))
        else:
            ga_content = ''.join(m_list[offset+1: offset+1 + ga_len])
        trans_res.add_row(m_list[offset: offset+1 + ga_len], '网关地址', 'GA', ga_content, priority=SSAL_PRIORITY)
        offset += 1 + ga_len

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
    trans_res.add_row(m_list[offset: offset+2], '帧头校验', 'HCS', '{0:04X}'.format(fcs_now) + hcs_check, priority=SSAL_PRIORITY)
    offset += 2
    return offset


def take_ssal_tail(m_list, offset, trans_res):
    """take_ssal_tail"""
    offset_temp = offset
    fcs_calc = commonfun.get_fcs(m_list[1:offset])
    fcs_calc = ((fcs_calc << 8) | (fcs_calc >> 8)) & 0xffff  # 低位在前
    # print('fcs test:', m_list[1:offset], 'cs:', hex(fcs_calc))
    fcs_now = int(m_list[offset] + m_list[offset + 1], 16)
    if fcs_now == fcs_calc:
        hcs_check = '(正确)'
    else:
        hcs_check = '(错误，正确值{0:04X})'.format(fcs_calc)
    trans_res.add_row(m_list[offset: offset+2], '帧校验', '', '{0:04X}'.format(fcs_now) + hcs_check, priority=SSAL_PRIORITY)
    offset += 2
    trans_res.add_row(m_list[offset: offset+1], '结束符%s'%('(错误)' if m_list[offset] != '16' else ''),\
                        value=m_list[offset], priority=SSAL_PRIORITY)
    offset += 1
    return offset - offset_temp


def add_ssal_layer(apdu_list):
    """add ssal_layer"""
    return apdu_list

