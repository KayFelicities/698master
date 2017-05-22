'''translate 698 messages'''
import traceback
import trans.common as commonfun
import trans.linklayer as linklayer_do
import trans.service as applayer_do
import config

class Translate():
    '''translate class'''
    def __init__(self):
        '''init'''
        self.trans_res = commonfun.TransRes()


    def trans_all(self, m_list):
        '''translate all messages'''
        offset = 0
        try:
            if m_list[0] == '68':
                offset += linklayer_do.take_linklayer1(m_list[offset:], self.trans_res)
                offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
                offset += linklayer_do.take_linklayer2(m_list[:], offset, self.trans_res)
            else:
                offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
        except Exception:
            traceback.print_exc()
            res_list = self.trans_res.get_res()
            return res_list, False
        else:
            res_list = self.trans_res.get_res()
            return res_list, True


    def get_full(self, m_text, is_show_level=True):
        '''get full translate'''
        m_list = commonfun.text2list(m_text)
        res_list, is_success = self.trans_all(m_list)
        m_chk = [byte for row in res_list for byte in row['m_list']]
        if is_success and m_chk == m_list:
            res_text = '<table style="table-layout:fixed; word-wrap:break-word;">'
        else:
            print('ERROR:\nm_chk: %s\n m_list: %s\n'%(m_chk, m_list))
            res_text = '<p style="color: red">报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！</p>'
        temp_row = None
        for row in res_list:
            if row['dtype'] in ['Data', 'CSD']:
                temp_row = row
                continue
            res_text += '<tr style="{color};">\
                            <td style="{padding} padding-right: 5px;">{messagerow}</td>\
                            <td>{brief}{value}{unit}{dtype}</td></tr>'\
                .format(color='color: %s;'%config.M_PRIORITY_COLOR[row['priority']],\
                padding='padding-left: %d px;'%(row['depth'] * 10) if is_show_level else '',\
                messagerow=commonfun.list2text(temp_row['m_list']+row['m_list']\
                                                if temp_row else row['m_list']),\
                brief=row['brief']+':' if row['brief'] else '',\
                dtype='('+temp_row['dtype']+'_'+row['dtype']+')' if temp_row\
                        else ('('+row['dtype']+')' if row['dtype'] else ''),\
                        value=row['value'], unit=row['unit'])
            temp_row = None
        res_text += '</table>'
        # print(res_text)
        return res_text


    def get_direction(self, m_text):
        '''get direction'''
        m_list = commonfun.text2list(m_text)
        res_list, is_success = self.trans_all(m_list)

        m_chk = [byte for row in res_list for byte in row['m_list']]
        if is_success is False or m_chk != m_list:
            print(m_chk, m_list)
            return '-'

        depth0_list = [row for row in res_list if row['depth'] == 0]
        service_type = commonfun.list2text(list(filter(lambda row: row['dtype'] == 'service'\
                                                        , depth0_list))[0]['m_list'])
        if service_type[1] == '8':
            return '←'
        else:
            return '→'



    def get_brief(self, m_text):
        '''get brief translate'''
        m_list = commonfun.text2list(m_text)
        res_list, is_success = self.trans_all(m_list)

        m_chk = [byte for row in res_list for byte in row['m_list']]
        if is_success is False or m_chk != m_list:
            return '<p style="color: red">无效报文</p>'

        depth0_list = [row for row in res_list if row['depth'] == 0]
        depth1_list = [row for row in res_list if row['depth'] == 1]
        depth2_list = [row for row in res_list if row['depth'] == 2]
        service_type = commonfun.list2text(list(filter(lambda row: row['dtype'] == 'service'\
                                                        , depth0_list))[0]['m_list'])
        if service_type[1] == '8':
            brief = {'dir': '应答' if service_type[0] == '0' else '主动'}
        else:
            brief = {'dir': '申请' if service_type[0] in ['0', '1'] else '回复'}
        if service_type[1] in ['1']:
            brief['service'] = '预连接'
            if brief['dir'] == '申请':
                brief['content'] = list(filter(lambda row: row['dtype'] == 'enum'\
                                        , depth0_list))[0]['value']
            else:
                brief['content'] = '结果' + list(filter(lambda row: row['dtype'] == 'Result'\
                        , depth0_list))[0]['value']

        elif service_type[1] in ['2']:
            brief['service'] = '建立应用连接'

        elif service_type[1] in ['3']:
            brief['service'] = '断开应用连接'

        elif service_type[1] in ['5']:
            brief['service'] = '读取记录' if service_type[-1] in ['3', '4'] else '读取'
            if service_type[-1] in ['2', '4']:
                brief['content'] = ','.join([row['value'].split('[索引')[0]\
                                    for row in depth1_list if row['dtype'] == 'OAD'])
            elif service_type[-1] in ['5']:
                brief['content'] = '分帧序号%d的数据块'%list(filter(lambda row: row['dtype'] \
                        == 'long-unsigned', depth0_list))[0]['value']
            else:
                brief['content'] = list(filter(lambda row: row['dtype'] == 'OAD'\
                        , depth0_list))[0]['value'].split('[索引')[0]

        elif service_type[1] in ['6']:
            brief['service'] = '设置后读取' if service_type[-1] == '3' else '设置'
            if service_type[-1] in ['2', '3']:
                brief['content'] = ','.join([row['value'].split('[索引')[0]\
                                for row in depth1_list if row['dtype'] == 'OAD'])
            else:
                brief['content'] = list(filter(lambda row: row['dtype'] == 'OAD'\
                        , depth0_list))[0]['value'].split('[索引')[0]

        elif service_type[1] in ['7']:
            brief['service'] = '操作后读取' if service_type[-1] == '3' else '操作'
            if service_type[-1] in ['2', '3']:
                brief['content'] = ','.join([row['value'].split('[操作模式')[0]\
                                for row in depth1_list if row['dtype'] == 'OMD'])
            else:
                brief['content'] = list(filter(lambda row: row['dtype'] == 'OMD'\
                        , depth0_list))[0]['value'].split('[操作模式')[0]

        elif service_type[1] in ['8']:
            brief['service'] = '上报'
            brief['content'] = ','.join([row['value'].split('[索引')[0]\
                                for row in depth1_list if row['dtype'] == 'OAD'])

        elif service_type[1] in ['9']:
            brief['service'] = {'1': '代理读取', '2': '代理读取记录', '3': '代理设置', '4': '代理设置后读取',\
                                '5': '代理操作', '6': '代理操作后读取', '7': '代理透明转发'}.get(service_type[-1])
            if service_type[-1] in ['1', '2', '3', '4']:
                brief['content'] = ','.join([row['value'].split('[索引')[0]\
                                for row in depth2_list if row['dtype'] == 'OAD'])

            if service_type[-1] in ['5', '6']:
                brief['content'] = ','.join([row['value'].split('[索引')[0]\
                                for row in depth2_list if row['dtype'] == 'OAD'])

            if service_type[-1] in ['7']:
                brief['content'] = '通道: ' + list(filter(lambda row: row['dtype'] == 'OAD'\
                        , depth0_list))[0]['value'].split('[索引')[0]

        elif service_type[1] in ['0']:
            brief['service'] = '安全传输'

        return '%s-%s %s'%(brief.get('dir', ''),\
                            brief.get('service', ''), brief.get('content', ''))
