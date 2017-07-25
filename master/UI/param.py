"""param"""
from master.trans import common
from master.datas import base_data


def read_set_dar(re_text):
    m_data = common.text2list(re_text)
    data = common.get_apdu_list(m_data)
    offset = 1
    if data[offset] == '01':
        offset += 6
        if data[offset] == '00':
            return 'ok'
        else:
            return base_data.get_dar(int(data[offset], 16))
    if data[offset] == '02':
        offset += 2
        dar_sum = int(data[offset], 16)
        offset += 5
        for _ in range(dar_sum):
            if data[offset] != '00':
                return base_data.get_dar(int(data[offset], 16))
            else:
                offset += 5
        return 'ok'


def get_long_unsigned(data, with_type=True):
    offset = 0
    if with_type is True:
        offset += 1
    return int(data[offset] + data[offset + 1], 16)


def get_double_long_unsigned(data, with_type=True):
    offset = 0
    if with_type is True:
        offset += 1
    return int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16)


def format_long_unsigned(text):
    long_unsigned_text = text.replace(' ', '')
    val = int(long_unsigned_text)
    val = val if val < 65535 else 65535
    return '12' + '%04X' % val


def get_ip(data):
    ip_text = ''
    for ip_section in data[0: 4]:
        ip_text += str(int(ip_section, 16)) + '.'
    return ip_text[: -1]


def format_ip(ip_text):
    ip_list = ip_text.replace(' ', '').split('.')
    text = ''
    for ip in ip_list:
        text += str('%02X' % int(ip))
    return text


def get_octet(data):
    offset = 1
    len_flag = int(data[offset], 16)
    offset += 1
    if len_flag >> 7 == 0:  # 单字节长度
        octet_len = len_flag
    else:
        len_of_len = len_flag & 0x7f
        string_len = ''
        for count in range(len_of_len):
            string_len += data[offset + count]
        offset += len_of_len
        octet_len = int(string_len, 16)
    octet_text = ''
    for i in range(octet_len):
        octet_text += data[offset + i]
    offset += octet_len
    return {'octet': octet_text, 'offset': offset, 'len': octet_len}


def get_visible(data):
    offset = 1  # type
    visible_len = int(data[offset], 16)
    offset += 1
    visible_text = ''
    for char in data[offset: offset + visible_len]:
        visible_text += chr(int(char, 16))
    offset += visible_len
    return {'visible': visible_text, 'offset': offset}


def format_visible_string(text):
    visible_text = text.replace(' ', '')
    visible_len = len(visible_text)
    text = ''
    for char in visible_text:
        text += '%02X' % ord(char)
    return '0A' + '%02X' % visible_len + text


def format_octet(octet_text):
    octet = octet_text.replace(' ', '')
    if len(octet) % 2 == 1:
        octet += 'F'
    octet_len_text = '%02X' % (len(octet) // 2)
    text = '09' + octet_len_text + octet
    return text
