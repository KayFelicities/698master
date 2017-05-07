'''translate 698 messages'''
import traceback
import trans.common as commonfun
import trans.linklayer as linklayer_do
import trans.service as applayer_do

class Translate():
    '''translate class'''
    def __init__(self):
        '''init'''
        self.trans_res = commonfun.TransRes()

    def trans_all(self, m_text):
        '''translate all messages'''
        offset = 0
        m_list = commonfun.text2list(m_text)
    # try:
        if commonfun.chk_format(m_text):
            offset += linklayer_do.take_linklayer1(m_list[offset:], self.trans_res)
            offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
            offset += linklayer_do.take_linklayer2(m_list[:], offset, self.trans_res)
        else:
            offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
    # finally:
        # traceback.print_exc()

        res_list = self.trans_res.get_res()
        print(res_list)
        m_chk = [byte for row in res_list for byte in row['m_list']]
        res_text = '' if m_chk == m_list else 'Kay, sth missing!\n'

        temp_row = None
        for row in res_list:
            if row['dtype'] in ['Data', 'CSD']:
                temp_row = row
                continue
            res_text += '{depth}{messagerow} --  {brief}{value}{unit}{dtype}\n'\
                .format(depth='  '*row['depth'],\
                messagerow=commonfun.list2text(temp_row['m_list']+row['m_list'] if temp_row else row['m_list']),\
                brief=row['brief']+':' if row['brief'] else '',\
                dtype='('+temp_row['dtype']+'-'+row['dtype']+')' if temp_row else ('('+row['dtype']+')' if row['dtype'] else ''),\
                value=row['value'], unit=row['unit'])
            temp_row = None
        return res_text

