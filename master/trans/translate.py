"""translate 698 messages"""
import traceback
import master.trans.common as commonfun
import master.trans.linklayer as linklayer_do
import master.trans.service as applayer_do
import master.trans.SSALlayer as SSAL_do
import master.trans.SSALservice as SSALapp_do
from master import config

class Translate:
    """translate class"""
    def __init__(self, m_text):
        """init"""
        self.is_ssal = False
        self.is_empty_ssal = False
        self.is_full_msg = True
        self.is_linklayer_sep = False
        self.trans_res = commonfun.TransRes()
        self.source_msg = commonfun.format_text(m_text)
        m_list = commonfun.text2list(m_text)
        self.res_list, self.is_success = self.__trans_all(m_list)
        self.is_access_successed = self.get_access_res()

    def __trans_all(self, m_list):
        """translate all messages"""
        offset = 0
        try:
            if m_list[0] == '98':
                self.is_ssal = True
                self.is_full_msg = True
                offset += SSAL_do.take_ssal_head(m_list[offset:], self.trans_res)
                offset += SSALapp_do.take_ssal_app(m_list[offset:-3], int(m_list[7], 16), self.trans_res)
                offset += SSAL_do.take_ssal_tail(m_list[:], offset, self.trans_res)
            elif m_list[0] == '68':
                offset += linklayer_do.take_linklayer1(m_list[offset:], self.trans_res)
                if (int(m_list[3], 16) >> 5) & 0x01 == 1:  # linklayer sep
                    self.is_linklayer_sep = True
                    self.trans_res.add_row(m_list[offset : len(m_list) - 3], '链路层分帧片段', '', ''.join(m_list[offset : len(m_list) - 3]), priority=1)
                    offset = len(m_list) - 3
                else:
                    offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
                offset += linklayer_do.take_linklayer2(m_list[:], offset, self.trans_res)
                self.is_full_msg = True
            else:
                self.is_full_msg = False
                offset += applayer_do.take_applayer(m_list[offset:], self.trans_res)
        except Exception:
            traceback.print_exc()
            res_list = self.trans_res.get_trans_res()
            return res_list, False
        else:
            res_list = self.trans_res.get_trans_res()
            m_chk = [byte for row in res_list for byte in row['m_list']]
            if m_chk == m_list:
                chk_res = True
            else:
                chk_res = False
                print('chk ERROR:\nm_chk: %s\n m_list: %s\n'%(m_chk, m_list))
            # print('res_list:', res_list)
            return res_list, chk_res

    def get_res_list(self):
        """get result list"""
        return self.res_list

    def get_access_res(self):
        """get access res"""
        access_res = self.trans_res.get_access_res()
        print('access_res: ', access_res)
        for oad_res in access_res:
            if access_res[oad_res] != '00':
                return False
        return True

    def get_access_dict(self):
        """get access result dict"""
        access_res = self.trans_res.get_access_res()
        return access_res

    def get_full(self, is_show_level=True, is_show_type=True, is_output_html=True, has_linklayer=True):
        """get full translate"""
        if self.is_success:
            res_text = '<table style="table-layout:fixed; word-wrap:break-word; border-style:solid;">' if is_output_html else ''
        else:
            if is_output_html:
                res_text = '<p style="color: red">报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！</p><p> </p>'
            else:
                res_text = '报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！\n\n'
        temp_row = None
        for row in self.res_list:
            if not has_linklayer and row['priority'] <= 0:
                continue
            if row['dtype'] in ['Data']:
                temp_row = row
                continue
            value = row['value']
            if isinstance(value, int):
                value *= 10**int(row['scaler'])
            if int(row['scaler']) < 0:
                format_str = '{val:.%df}'%(abs(int(row['scaler'])))
                value = format_str.format(val=value)
                print('value:', value)
            
            dtype = ''
            if is_show_type:
                dtype = '('+temp_row['dtype']+'_'+row['dtype']+')' if temp_row\
                    else ('('+row['dtype']+')' if row['dtype'] else '')

            if is_output_html:
                res_text += '<tr style="{color};">\
                                <td style="{padding} padding-right: 5px;">{messagerow}</td>\
                                <td style="{padding} padding-right: 5px;">{brief}{value}{unit}{dtype}</td></tr>'\
                    .format(color='color: %s;'%config.M_PRIORITY_COLOR[row['priority']],\
                    padding='padding-left: %d px;'%(row['depth'] * 10) if is_show_level else '',\
                    messagerow=commonfun.list2text(temp_row['m_list']+row['m_list']\
                                                    if temp_row else row['m_list']),\
                    brief=row['brief'].replace('<', '(').replace('>', ')') +':'\
                                if row['brief'] else '', dtype=dtype, value=value, unit=row['unit'])
            else:
                res_text += '{padding}{messagerow} —— {brief}{value}{unit}{dtype}\n'\
                    .format(padding='  '*row['depth'] if is_show_level else '',\
                    messagerow=commonfun.list2text(temp_row['m_list']+row['m_list']\
                                                    if temp_row else row['m_list']),\
                    brief=row['brief'].replace('<', '(').replace('>', ')') +':'\
                                if row['brief'] else '', dtype=dtype, value=value, unit=row['unit'])

            temp_row = None
        if is_output_html:
            res_text += '</table>'
        # print(res_text)
        return res_text
    

    def get_structed_msg(self, has_linklayer=True):
        """get_structed_msg"""
        res_text = '' if self.is_success else '\n\n'
        temp_row = None
        for row in self.res_list:
            if not has_linklayer and row['priority'] <= 0:
                continue
            if row['dtype'] in ['Data']:
                temp_row = row
                continue

            res_text += '{padding}{messagerow}\n'\
                .format(padding='  '*row['depth'],\
                messagerow=commonfun.list2text(temp_row['m_list']+row['m_list'] if temp_row else row['m_list']))
            temp_row = None
        return res_text[:-1]  #remove last \n


    def get_structed_explain(self, has_linklayer=True, is_show_type=False):
        """get_structed_explain"""
        res_text = '' if self.is_success else '<p style="color: red">报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！</p><p> </p>'
        temp_row = None
        for row in self.res_list:
            if not has_linklayer and row['priority'] <= 0:
                continue
            if row['dtype'] in ['Data']:
                temp_row = row
                continue
            value = row['value']
            if isinstance(value, int):
                value *= 10**int(row['scaler'])
            if int(row['scaler']) < 0:
                format_str = '{val:.%df}'%(abs(int(row['scaler'])))
                value = format_str.format(val=value)
            
            dtype = ''
            if is_show_type:
                dtype = '('+temp_row['dtype']+'_'+row['dtype']+')' if temp_row\
                    else ('('+row['dtype']+')' if row['dtype'] else '')

            res_text += '<p style="margin:0; {color}; {padding};">{brief}{value}{unit}{dtype}</p>'\
                    .format(color='color: %s'%config.M_PRIORITY_COLOR[row['priority']],\
                    padding='margin-left: %d px'%(row['depth'] * 10),\
                    brief=row['brief'].replace('<', '(').replace('>', ')') +':'\
                                if row['brief'] else '', dtype=dtype, value=value, unit=row['unit'])
            temp_row = None
        # print('res_text:', res_text)
        return res_text

    def get_structed_msg(self, has_linklayer=True):
        """get_structed_msg"""
        res_text = '' if self.is_success else '\n\n'
        temp_row = None
        for row in self.res_list:
            if not has_linklayer and row['priority'] <= 0:
                continue
            if row['dtype'] in ['Data']:
                temp_row = row
                continue

            res_text += '{padding}{messagerow}\n'\
                .format(padding='  '*row['depth'],\
                messagerow=commonfun.list2text(temp_row['m_list']+row['m_list'] if temp_row else row['m_list']))
            temp_row = None
        return res_text[:-1]  #remove last \n

    def get_structed_explain(self, has_linklayer=True, is_show_type=False):
        """get_structed_explain"""
        res_text = '' if self.is_success else '<p style="color: red">报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！</p><p> </p>'
        temp_row = None
        for row in self.res_list:
            if not has_linklayer and row['priority'] <= 0:
                continue
            if row['dtype'] in ['Data']:
                temp_row = row
                continue
            value = row['value']
            if isinstance(value, int):
                value *= 10**int(row['scaler'])
            if int(row['scaler']) < 0:
                format_str = '{val:.%df}'%(abs(int(row['scaler'])))
                value = format_str.format(val=value)
            
            dtype = ''
            if is_show_type:
                dtype = '('+temp_row['dtype']+'_'+row['dtype']+')' if temp_row\
                    else ('('+row['dtype']+')' if row['dtype'] else '')

            res_text += '<p style="margin:0; {color}; {padding};">{brief}{value}{unit}{dtype}</p>'\
                    .format(color='color: %s'%config.M_PRIORITY_COLOR[row['priority']],\
                    padding='margin-left: %d px'%(row['depth'] * 10),\
                    brief=row['brief'].replace('<', '(').replace('>', ')') +':'\
                                if row['brief'] else '', dtype=dtype, value=value, unit=row['unit'])
            temp_row = None
        # print('res_text:', res_text)
        return res_text

    def get_apdu_text(self):
        """get_apdu_text"""
        apdu_text = ''.join([commonfun.list2text(row['m_list'])\
                                for row in self.res_list if row['priority'] > 0])
        return apdu_text

    def get_direction(self):
        """get direction"""
        if not self.is_success:
            return '-'

        depth0_list = [row for row in self.res_list if row['depth'] == 0]
        service_type = commonfun.list2text(list(filter(lambda row: row['dtype'] == 'service'\
                                                        , depth0_list))[0]['m_list'])
        if service_type[0] in ['0', '1'] and service_type != '01':
            return '→'
        else:
            return '←'

    def get_SA(self):
        """get server address"""
        for row in self.res_list:
            if row['dtype'] == 'SA':
                return row['value'].split('[')[2].split(']')[0]
        return '-'

    def get_CA(self):
        """get client address"""
        for row in self.res_list:
            if row['dtype'] == 'CA':
                return row['value']
        return '-'

    def get_logic_addr(self):
        """get logic address"""
        for row in self.res_list:
            if row['dtype'] == 'SA':
                return int(row['value'].split('[')[1].split(']')[0])
        return 0

    def get_service(self):
        """get service"""
        if self.is_ssal:
            return 'ssal'
        return commonfun.list2text(list(filter(lambda row: row['dtype'] == 'service'\
                                    , self.res_list))[0]['m_list']).replace(' ', '')

    def get_piid(self):
        """get_piid"""
        return commonfun.list2text(list(filter(lambda row: row['dtype'] in ['PIID', 'PIID_ACD']\
                            , self.res_list))[0]['m_list']).replace(' ', '')
    
    def get_raw_msg(self, brief):
        """get_raw_msg"""
        return commonfun.list2text(list(filter(lambda row: row['brief'].strip() == brief.strip()\
                            , self.res_list))[0]['m_list']).replace(' ', '').strip()


    def get_brief(self):
        """get brief translate"""
        if not self.is_success:
            return '无效报文'
        
        if self.is_linklayer_sep:
            return '链路层分帧报文'

        brief = {}
        if not self.is_access_successed:
            brief['access_res'] = '(访问失败)'

        depth0_list = [row for row in self.res_list if row['depth'] == 0]
        depth1_list = [row for row in self.res_list if row['depth'] == 1]
        depth2_list = [row for row in self.res_list if row['depth'] == 2]
        try:
            service_type = commonfun.list2text(list(filter(lambda row: row['dtype'] == 'service'\
                                                            , depth0_list))[0]['m_list'])
        except IndexError:
            if self.is_ssal:
                return 'SSAL报文'
            else:
                return '错误报文'

        if service_type[1] == '8':
            brief['dir'] = '应答' if service_type[0] == '0' else '主动'
        else:
            brief['dir'] = '申请' if service_type[0] in ['0', '1'] else '回复'
        if service_type[1] in ['1']:
            if brief['dir'] == '申请':
                brief['service'] = ''
                brief['content'] = list(filter(lambda row: row['dtype'] == 'enum'\
                                        , depth0_list))[0]['value']
            else:
                brief['service'] = '登录/心跳'
                brief['content'] = '结果' + list(filter(lambda row: row['dtype'] == 'Result'\
                        , depth0_list))[0]['value']

        elif service_type[1] in ['2']:
            brief['service'] = '建立应用连接'

        elif service_type[1] in ['3']:
            brief['service'] = '断开应用连接'

        elif service_type[1] in ['5']:
            brief['service'] = '读取记录' if service_type[-1] in ['3', '4'] else '读取'  # todo 读取(成功/失败:原因)
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
            if service_type[-1] == '3':
                brief['content'] = '透明数据'

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

        elif service_type[1] in ['E']:
            brief['service'] = '异常响应'

        return '%s%s%s %s'%(brief.get('access_res', ''), brief.get('dir', ''),\
                            brief.get('service', ''), brief.get('content', ''))

    def get_clipboard_text(self, is_show_level=True, is_show_type=True):
        """get_clipboard_text"""
        msg = self.source_msg
        full = self.get_full(is_show_level, is_show_type, is_output_html=False)
        brief = self.get_brief()

        line_list = full.split('\n')
        explain = ''
        for cnt, line in enumerate(line_list, start=0):
            if cnt % 2 == 1:
                explain += line + '  ——  '
            else:
                explain += line + '\n'
        text = '【报文】\n{msg}\n\n【概览】\n{brief}\n\n【完整解析】\n{full}'.format(msg=msg, brief=brief, full=full)
        return text
