'''translate 698 messages'''
import trans.common as commonfun
import trans.linklayer as linklayer_do
import trans.applayer as applayer_do

class Translate():
    '''translate class'''
    def __init__(self):
        '''init'''
        self.trans_res = commonfun.TransRes()

    def trans_all(self, m_text):
        '''translate all messages'''
        offset = 0
        if not commonfun.chk_format(m_text):
            return False
        m_list = commonfun.text2list(m_text)
        offset += linklayer_do.take_linklayer(m_list[offset:], self.trans_res)
        offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
        res_list = self.trans_res.get_res()
        print(res_list)
        res_text = ''
        for row in res_list:
            res_text += '  '*row[2] + commonfun.list2text(row[0]) + ' ---- ' + row[1] + '\n'

        return res_text

