"""msg reply"""
import time
from master.trans import common


def get_link_replay_apdu(trans_object):
    """get_link_replay_apdu"""
    tm1_text = common.list2text(list(filter(lambda row: row['dtype'] == 'date_time'\
                                                , trans_object.res_list))[0]['m_list'])
    tm_local = time.localtime()
    weekday = 0 if tm_local.tm_wday == 6 else tm_local.tm_wday + 1 
    tm2_text = '%04X %02X %02X %02X %02X %02X %02X 0000'\
                    % (tm_local[0], tm_local[1], tm_local[2],\
                        weekday, tm_local[3], tm_local[4], tm_local[5])
    reply_apdu_text = '81 %s %s'%(trans_object.get_piid(), '80') + tm1_text + tm2_text + tm2_text
    return reply_apdu_text


def get_rpt_replay_apdu(trans_object):
    """get_rpt_replay_apdu"""
    piid = trans_object.get_piid()
    service_choice = trans_object.get_service()[-2:]
    print('service_choice:', service_choice)
    if service_choice in ['01', '02']:
        oad_list = list(map(lambda x: common.list2text(x['m_list']),\
                        list(filter(lambda row: row['dtype'] == 'OAD' and row['depth'] == 1\
                                                , trans_object.res_list))))
        print('oad_list:', oad_list)
        oad_num = len(oad_list)
        reply_text = '08%s %s %02X %s 00'%(service_choice, piid, oad_num, ''.join(oad_list))
    if service_choice == '03':
        reply_text = '0803%s 00'%piid
    return reply_text


def get_rpt_replay_split(trans_object):
    """get_rpt_replay_apdu"""
    piid = trans_object.get_piid()
    split_no = trans_object.get_raw_msg('分帧序号')
    reply_text = '0505%s%s 00'%(piid, split_no)
    return reply_text
