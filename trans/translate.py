'''translate 698 messages'''
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
        if not commonfun.chk_format(m_text):
            return 'format error'
        m_list = commonfun.text2list(m_text)
        offset += linklayer_do.take_linklayer1(m_list[offset:], self.trans_res)
        offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
        offset += linklayer_do.take_linklayer2(m_list[:], offset, self.trans_res)
        res_list = self.trans_res.get_res()
        print(res_list)
        res_text = ''
        data_add = [[], '']
        for row in res_list:
            if row[2] == 'Data':
                data_add = [row[0], 'Data ']
                continue
            res_text += '  '*row[6] + commonfun.list2text(data_add[0] + row[0]) +\
                        ' ---- {brief}({data_add}{dtype}:{value}{unit})'\
                        .format(data_add=data_add[1], brief=row[1], dtype=row[2], value=row[3], unit=row[4]) + '\n'
            data_add = [[], '']
        return res_text

