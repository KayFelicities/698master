"""param ui"""
import os
from master import config
from master.trans import common
from master.UI.param_window import Ui_ParamWindow
from master.UI import param
from master.datas import base_data
if config.IS_USE_PYSIDE:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore


class ParamWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_ParamWindow):
    def __init__(self):
        super(ParamWindow, self).__init__()
        self.setupUi(self)
        self.always_top_cb.setChecked(False)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.res_b.clicked.connect(self.clear_res)
        self.DT_read_b.clicked.connect(self.DT_read)
        self.DT_set_b.clicked.connect(self.DT_set)
        self.DT_set_now_b.clicked.connect(self.DT_set_now)
        self.DT_param_r_b.clicked.connect(self.DT_param_read)
        self.DT_param_set_b.clicked.connect(self.DT_param_set)
        self.SA_read_b.clicked.connect(self.SA_read)
        self.SA_set_b.clicked.connect(self.SA_set)
        self.S_ip_read_b.clicked.connect(self.ip_read)
        self.S_ip_set_b.clicked.connect(self.ip_set)
        self.local_read_b.clicked.connect(self.local_net_read)
        self.local_set_b.clicked.connect(self.local_net_set)
        self.C_read_b.clicked.connect(self.communication_read)
        self.C_set_b.clicked.connect(self.communication_set)
        self.esam_r_info_b.clicked.connect(self.esam_info_read)
        self.esam_r_certi_b.clicked.connect(self.esam_certi_read)
        self.evt_r_b.clicked.connect(self.evt_read)
        self.evt_set_b.clicked.connect(self.evt_set)
        self.evt_valid_all_left_cb.clicked.connect(self.evt_select_all_left_valid)
        self.evt_rpt_all_left_cb.clicked.connect(self.evt_select_all_left_rpt)
        self.evt_valid_all_right_cb.clicked.connect(self.evt_select_all_right_valid)
        self.evt_rpt_all_right_cb.clicked.connect(self.evt_select_all_right_rpt)
        self.rpt_r_b.clicked.connect(self.rpt_read)
        self.rpt_set_b.clicked.connect(self.rpt_set)

        self.setWindowTitle('常用命令')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SOFTWARE_PATH, config.MASTER_ICO_PATH)))
        self.label_22.setText("无线公网IP")
        self.label_23.setText("端口")
        self.label_134.setText("以太网IP")
        self.label_145.setText("端口")


    def clear_res(self):
        self.res_b.setText('')


    def set_always_top(self):
        window_pos = self.pos()
        if (self.always_top_cb.isChecked() is True):
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


    def DT_read(self):
        self.res_b.setText('')
        apdu_text = '0501014000020000'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_DT)


    def DT_set(self):
        self.res_b.setText('')
        DT_box_content = self.DT_box.dateTime()
        self.set_DT(DT_box_content)


    def DT_set_now(self):
        self.res_b.setText('')
        DT_now = QtCore.QDateTime.currentDateTime()
        # print('DT_now', DT_now)
        self.set_DT(DT_now)


    def set_DT(self, DT):
        # self.DT_box.setDateTime(DT)
        DT_list = DT.toString('yyyy.MM.dd.hh.mm.ss').split('.')
        DT_text = '1C%04X' % int(DT_list[0])
        for DT in DT_list[1:]:
            DT_text += '%02X' % int(DT)
        apdu_text = '06010D40000200' + DT_text + '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res)


    def re_DT(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 7
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 2
            DT_read = QtCore.QDateTime(
                (int(data[offset], 16) << 8) | int(data[offset + 1], 16),
                int(data[offset + 2], 16),
                int(data[offset + 3], 16),
                int(data[offset + 4], 16),
                int(data[offset + 5], 16),
                int(data[offset + 6], 16),
            )
            # print('DT_read', DT_read)
            self.DT_box.setDateTime(DT_read)
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_DT)


    def SA_read(self):
        self.res_b.setText('')
        apdu_text = '0501004001020000'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_SA)


    def SA_set(self, DT):
        self.res_b.setText('')
        SA_text = self.SA_box.text().replace(' ', '')
        if len(SA_text) % 2 == 1:
            SA_text += 'F'
        self.SA_box.setText(SA_text)
        SA_len = len(SA_text) // 2
        apdu_text = '06010D4001020009' + '%02X' % (SA_len) + SA_text + '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res_SA)


    def re_SA(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 7
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 2
            SA_len = int(data[offset], 16)
            self.SA_len_box.setText(str(SA_len))
            SA_text = ''
            for d in data[offset + 1: offset + 1 + SA_len]:
                SA_text += d
            self.SA_box.setText(SA_text)
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_SA)


    def DT_param_read(self):
        self.res_b.setText('')
        apdu_text = '0502 0102 40000300 40000400 00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_DT_param)


    def DT_param_set(self, DT):
        self.res_b.setText('')
        mode_text = '16' + {0: '00', 1: '01', 2: '02', 3: '03', 4: 'FF'}[self.DT_mode_l.currentIndex()]
        tot_num_text = '11' + '%02X' % int(self.DT_tot_num_box.text().replace(' ', ''))
        biggest_num_text = '11' + '%02X' % int(self.DT_biggest_num_box.text().replace(' ', ''))
        smallest_num_text = '11' + '%02X' % int(self.DT_smallest_num_box.text().replace(' ', ''))
        dly_max_text = '11' + '%02X' % int(self.DT_dly_max_box.text().replace(' ', ''))
        valid_num_min_text = '11' + '%02X' % int(self.DT_valid_num_min_box.text().replace(' ', ''))
        apdu_text = '060200 02 40000300' + mode_text + '40000400 0205' + tot_num_text + biggest_num_text + smallest_num_text + dly_max_text + valid_num_min_text + '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res)


    def re_DT_param(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 8
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 2
            self.DT_mode_l.setCurrentIndex({'00': 0, '01': 1, '02': 2, 'FF': 3}[data[offset]])
            offset += 9
            self.DT_tot_num_box.setText(str(int(data[offset], 16)))
            offset += 2
            self.DT_biggest_num_box.setText(str(int(data[offset], 16)))
            offset += 2
            self.DT_smallest_num_box.setText(str(int(data[offset], 16)))
            offset += 2
            self.DT_dly_max_box.setText(str(int(data[offset], 16)))
            offset += 2
            self.DT_valid_num_min_box.setText(str(int(data[offset], 16)))
            offset += 2
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_DT_param)


    def ip_read(self):
        self.res_b.setText('')
        apdu_text = '050200 02 45000300 45100300 00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_ip)


    def ip_set(self, DT):
        self.res_b.setText('')
        gprs_ip_text = self.S_ip_box.text()
        if gprs_ip_text:
            gprs_ip_text = param.format_ip(gprs_ip_text)
            gprs_port_text = '%04X' % int(self.S_port_box.text().replace(' ', ''))
        eth_ip_text = self.S_ip_box_2.text()
        if eth_ip_text:
            eth_ip_text = param.format_ip(eth_ip_text)
            eth_port_text = '%04X' % int(self.S_port_box_2.text().replace(' ', ''))

        if gprs_ip_text and (not eth_ip_text):
            apdu_text = '060100 45000300 0101 0202 0904' + gprs_ip_text + '12' + gprs_port_text
        if (not gprs_ip_text) and eth_ip_text:
            apdu_text = '060100 45100300 0101 0202 0904' + eth_ip_text + '12' + eth_port_text
        if gprs_ip_text and eth_ip_text:
            apdu_text = '060200 02 45000300 0101 0202 0904' + gprs_ip_text + '12' + gprs_port_text\
                            + '45100300 0101 0202 0904' + eth_ip_text + '12' + eth_port_text
        apdu_text += '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res)


    def re_ip(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        gprs_pos = common.list2text(data).replace(' ', '').find('45000300') // 2
        eth_pos = common.list2text(data).replace(' ', '').find('45100300') // 2
        if gprs_pos >= 0:
            offset = gprs_pos + 4
            if data[offset] == '01':
                self.res_b.setStyleSheet('color: green')
                self.res_b.setText('成功')
                offset += 7
                ip_text = param.get_ip(data[offset:])
                self.S_ip_box.setText(ip_text)
                port_text = str(int(data[offset + 5] + data[offset + 6], 16))
                self.S_port_box.setText(port_text)
        if eth_pos >= 0:
            offset = eth_pos + 4
            if data[offset] == '01':
                self.res_b.setStyleSheet('color: green')
                self.res_b.setText('成功')
                offset += 7
                ip_text = param.get_ip(data[offset:])
                self.S_ip_box_2.setText(ip_text)
                port_text = str(int(data[offset + 5] + data[offset + 6], 16))
                self.S_port_box_2.setText(port_text)
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_ip)


    def local_net_read(self):
        self.res_b.setText('')
        apdu_text = '0501004510040000'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_local_net)


    def local_net_set(self, DT):
        self.res_b.setText('')
        ip_mode = '%02X' % self.local_ip_mode_l.currentIndex()
        ip_text = param.format_ip(self.local_ip_box.text())
        ip_mask = param.format_ip(self.local_mask_box.text())
        gate = param.format_ip(self.local_gate_addr_box.text())
        ppp_usr = param.format_visible_string(self.ppp_usr_box.text())
        ppp_pw = param.format_visible_string(self.ppp_pw_box.text())
        apdu_text = '06010D45100400 0206 16' + ip_mode + '0904' + ip_text + '0904' + ip_mask + '0904'\
                    + gate + ppp_usr + ppp_pw + '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res)


    def re_local_net(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 7
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 4
            self.local_ip_mode_l.setCurrentIndex({'00': 0, '01': 1, '02': 2}[data[offset]])
            offset += 3
            self.local_ip_box.setText(param.get_ip(data[offset:]))
            offset += 6
            self.local_mask_box.setText(param.get_ip(data[offset:]))
            offset += 6
            self.local_gate_addr_box.setText(param.get_ip(data[offset:]))
            offset += 4
            ret = param.get_visible(data[offset:])
            self.ppp_usr_box.setText(ret['visible'])
            offset += ret['offset']
            ret = param.get_visible(data[offset:])
            self.ppp_pw_box.setText(ret['visible'])
            offset += ret['offset']
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_local_net)


    def communication_read(self):
        self.res_b.setText('')
        apdu_text = '0501004500020000'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_communication)


    def communication_set(self, DT):
        self.res_b.setText('')
        work_mode_text = '16' + '%02X' % self.C_work_mode_l.currentIndex()
        online_mode_text = '16' + '%02X' % self.C_online_mode_l.currentIndex()
        connect_mode_text = '16' + '%02X' % self.C_connect_mode_l.currentIndex()
        connect_app_mode_text = '16' + '%02X' % self.C_connect_app_mode_l.currentIndex()
        listen_port_text = '0100'   # 暂时不可设置
        APN_text = param.format_visible_string(self.C_APN_box.text())
        usr_text = param.format_visible_string(self.C_usr_box.text())
        pw_text = param.format_visible_string(self.C_pw_box.text())
        proxy_addr_text = param.format_octet(self.C_proxy_addr_box.text())
        proxy_port_text = param.format_long_unsigned(self.C_proxy_prot_box.text())
        overtm_retry_num_text = '11' + '%02X' % ((int(self.C_retry_box.text()) << 6)
                                                 | int(self.C_over_tm_box.text()))
        heart_tm_text = param.format_long_unsigned(self.C_heart_tm_box.text())
        apdu_text = '06010D45000200 020C' + work_mode_text + online_mode_text + \
                    connect_mode_text + connect_app_mode_text + listen_port_text + APN_text + \
                    usr_text + pw_text + proxy_addr_text + proxy_port_text +\
                    overtm_retry_num_text + heart_tm_text + '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res)


    def re_communication(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 7
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 4
            self.C_work_mode_l.setCurrentIndex({'00': 0, '01': 1, '02': 2}[data[offset]])
            offset += 2
            self.C_online_mode_l.setCurrentIndex({'00': 0, '01': 1}[data[offset]])
            offset += 2
            self.C_connect_mode_l.setCurrentIndex({'00': 0, '01': 1}[data[offset]])
            offset += 2
            self.C_connect_app_mode_l.setCurrentIndex({'00': 0, '01': 1}[data[offset]])
            offset += 2
            array_num = int(data[offset], 16)
            offset += 1
            listen_port_text = ''
            for count in range(array_num):
                listen_port_text += str(param.get_long_unsigned(data[offset:])) + ' '
                offset += 3
            self.C_listen_port_box.setText(listen_port_text)
            ret = param.get_visible(data[offset:])
            self.C_APN_box.setText(ret['visible'])
            offset += ret['offset']
            ret = param.get_visible(data[offset:])
            self.C_usr_box.setText(ret['visible'])
            offset += ret['offset']
            ret = param.get_visible(data[offset:])
            self.C_pw_box.setText(ret['visible'])
            offset += ret['offset']
            ret = param.get_octet(data[offset:])
            self.C_proxy_addr_box.setText(ret['octet'])
            offset += ret['offset']
            self.C_proxy_prot_box.setText(str(param.get_long_unsigned(data[offset:])))
            offset += 3
            offset += 1
            overtm_retry_num_byte = int(data[offset], 16)
            self.C_retry_box.setText(str(overtm_retry_num_byte & 0x03))
            self.C_over_tm_box.setText(str(overtm_retry_num_byte >> 2))
            offset += 1
            self.C_heart_tm_box.setText(str(param.get_long_unsigned(data[offset:])))
            offset += 3
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_communication)


    def esam_info_read(self):
        self.res_b.setText('')
        apdu_text = '0502 0107 F1000200 F1000300 F1000400 F1000500 F1000600 F1000700 F1000800 00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_esam_info)


    def re_esam_info(self, re_text):
        res_sum = True
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = common.list2text(data).replace(' ', '').find('F1000200') // 2 + 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_no_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            res_sum = False
            self.esam_no_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        offset = common.list2text(data).replace(' ', '').find('F1000300') // 2 + 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_ver_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            res_sum = False
            self.esam_ver_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        offset = common.list2text(data).replace(' ', '').find('F1000400') // 2 + 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_key_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            res_sum = False
            self.esam_key_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        offset = common.list2text(data).replace(' ', '').find('F1000500') // 2 + 4
        if data[offset] == '01':
            offset += 1
            self.esam_dialog_tm_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
        else:
            res_sum = False
            self.esam_dialog_tm_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        offset = common.list2text(data).replace(' ', '').find('F1000600') // 2 + 4
        if data[offset] == '01':
            offset += 1
            self.esam_dialog_remain_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
        else:
            res_sum = False
            self.esam_dialog_remain_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        offset = common.list2text(data).replace(' ', '').find('F1000700') // 2 + 4
        if data[offset] == '01':
            offset += 3
            self.esam_addr_ctr_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
            self.esam_rpt_ctr_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
            self.esam_app_radio_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
        else:
            res_sum = False
            self.esam_addr_ctr_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
            self.esam_rpt_ctr_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
            self.esam_app_radio_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        offset = common.list2text(data).replace(' ', '').find('F1000800') // 2 + 4
        if data[offset] == '01':
            offset += 3
            ret = param.get_octet(data[offset:])
            self.esam_terminal_ver_box.setText(ret['octet'])
            offset += ret['offset']
            ret = param.get_octet(data[offset:])
            self.esam_host_ver_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            res_sum = False
            self.esam_terminal_ver_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
            self.esam_host_ver_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        if res_sum is True:
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_esam_info)


    def esam_certi_read(self):
        self.res_b.setText('')
        if self.esam_certi_l.currentIndex() == 0:
            apdu_text = '0502 0102 F1000900 F1000A00 00'
        else:
            apdu_text = '0502 0102 F1000B00 F1000C00 00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_esam_certi)


    def re_esam_certi(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 4
        res_sum = True
        offset += 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_certi_ver_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_certi_ver_box.setText('失败：' + base_data.get_dar(int(data[offset], 16)))
        offset += 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_certi_box.setText(ret['octet'])
            self.esam_certi_len_box.setText(str(ret['len']) + '字节')
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_certi_box.setText('失败：' + base_data.get_dar(int(data[offset], 16)))
        if res_sum is True:
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_esam_certi)


    def evt_read(self):
        self.res_b.setText('')
        self.clr_all_cb()
        apdu_text = '0501003FFF020000'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_evt)


    def evt_set(self, DT):
        self.res_b.setText('')
        bit_string_text = ''
        for byte_index in range(11):
            for bit_index in range(8):
                evt_no = byte_index * 8 + bit_index + 1
                bit_val = 0
                if evt_no <= 85:
                    if eval('self.valid_c_' + str(evt_no) + '.isChecked()') is True:
                        bit_val = 1
                bit_string_text += str(bit_val)
        bit_string_text = hex(int(bit_string_text, 2)).split('x')[1].rjust(22, '0')
        valid_text = '0455' + bit_string_text
        bit_string_text = ''
        for byte_index in range(11):
            for bit_index in range(8):
                evt_no = byte_index * 8 + bit_index + 1
                bit_val = 0
                if evt_no <= 85:
                    if eval('self.rpt_c_' + str(evt_no) + '.isChecked()') is True:
                        bit_val = 1
                bit_string_text += str(bit_val)
        bit_string_text = hex(int(bit_string_text, 2)).split('x')[1].rjust(22, '0')
        rpt_text = '0455' + bit_string_text
        apdu_text = '060101 3FFF0200 0202' + valid_text + rpt_text + '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res)


    def re_evt(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 7
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 4
            bit_string_len = int(data[offset], 16)
            byte_len = bit_string_len // 8 if bit_string_len % 8 == 0 else bit_string_len // 8 + 1
            offset += 1
            for byte_index in range(byte_len):
                byte_int = int(data[offset], 16)
                offset += 1
                for bit_index in range(8):
                    evt_no = byte_index * 8 + bit_index + 1
                    if evt_no <= 85:
                        if (byte_int >> (7 - bit_index)) & 0x01 == 1:
                            eval('self.valid_c_' + str(evt_no) + '.setChecked(True)')
                        else:
                            eval('self.valid_c_' + str(evt_no) + '.setChecked(False)')
            offset += 1
            bit_string_len = int(data[offset], 16)
            byte_len = bit_string_len // 8 if bit_string_len % 8 == 0 else bit_string_len // 8 + 1
            offset += 1
            for byte_index in range(byte_len):
                byte_int = int(data[offset], 16)
                offset += 1
                for bit_index in range(8):
                    evt_no = byte_index * 8 + bit_index + 1
                    if evt_no <= 85:
                        if (byte_int >> (7 - bit_index)) & 0x01 == 1:
                            eval('self.rpt_c_' + str(evt_no) + '.setChecked(True)')
                        else:
                            eval('self.rpt_c_' + str(evt_no) + '.setChecked(False)')
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_evt)


    def clr_all_cb(self):
        for count in range(1, 86):
            self.evt_valid_all_left_cb.setChecked(False)
            self.evt_rpt_all_left_cb.setChecked(False)
            self.evt_valid_all_right_cb.setChecked(False)
            self.evt_rpt_all_right_cb.setChecked(False)
            eval('self.valid_c_' + str(count) + '.setChecked(False)')
            eval('self.rpt_c_' + str(count) + '.setChecked(False)')

    def evt_select_all_left_valid(self):
        if self.evt_valid_all_left_cb.isChecked() is True:
            for count in range(1, 49):
                eval('self.valid_c_' + str(count) + '.setChecked(True)')
        else:
            for count in range(1, 49):
                eval('self.valid_c_' + str(count) + '.setChecked(False)')

    def evt_select_all_left_rpt(self):
        if self.evt_rpt_all_left_cb.isChecked() is True:
            for count in range(1, 49):
                eval('self.rpt_c_' + str(count) + '.setChecked(True)')
        else:
            for count in range(1, 49):
                eval('self.rpt_c_' + str(count) + '.setChecked(False)')

    def evt_select_all_right_valid(self):
        if self.evt_valid_all_right_cb.isChecked() is True:
            for count in range(49, 86):
                eval('self.valid_c_' + str(count) + '.setChecked(True)')
        else:
            for count in range(49, 86):
                eval('self.valid_c_' + str(count) + '.setChecked(False)')

    def evt_select_all_right_rpt(self):
        if self.evt_rpt_all_right_cb.isChecked() is True:
            for count in range(49, 86):
                eval('self.rpt_c_' + str(count) + '.setChecked(True)')
        else:
            for count in range(49, 86):
                eval('self.rpt_c_' + str(count) + '.setChecked(False)')


    def rpt_read(self):
        self.clear_res()
        apdu_text = '0502 0104 43000700 43000800 43000900 43000A00 00'
        self.rpt_follow_cb.setCurrentIndex(-1)
        self.rpt_cb.setCurrentIndex(-1)
        self.conn_sever_cb.setCurrentIndex(-1)
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_rpt)


    def rpt_set(self, DT):
        self.res_b.setText('')
        rpt_follow_text = '03' + '%02X' % self.rpt_follow_cb.currentIndex()
        rpt_text = '03' + '%02X' % self.rpt_cb.currentIndex()
        conn_sever_text = '03' + '%02X' % self.conn_sever_cb.currentIndex()
        rpt_channel_text = self.rpt_channel_box.text()
        rpt_channel_text = list(filter(str.isdigit, rpt_channel_text))
        rpt_channel_text = ''.join(rpt_channel_text)
        array_sum = len(rpt_channel_text) // 8
        rpt_channel_array_text = '01' + '%02X' % array_sum
        offset = 0
        for _ in range(array_sum):
            rpt_channel_array_text += '51' + rpt_channel_text[offset:offset + 8]
            offset += 8
        apdu_text = '060200 04 43000700' + rpt_follow_text + '43000800' + rpt_text +\
                    '43000900' + conn_sever_text + '43000A00' + rpt_channel_array_text + '00'
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.read_res)


    def re_rpt(self, re_text):
        m_data = common.text2list(re_text)
        data = common.get_apdu_list(m_data)
        offset = 4
        res_sum = True
        offset += 4
        if data[offset] == '01':
            offset += 2
            self.rpt_follow_cb.setCurrentIndex(1 if data[offset] == '01' else 0)
            offset += 1
        else:
            offset += 1
            res_sum = False
            self.esam_no_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        offset += 4
        if data[offset] == '01':
            offset += 2
            self.rpt_cb.setCurrentIndex(1 if data[offset] == '01' else 0)
            offset += 1
        else:
            offset += 1
            res_sum = False
            self.esam_ver_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        offset += 4
        if data[offset] == '01':
            offset += 2
            self.conn_sever_cb.setCurrentIndex(1 if data[offset] == '01' else 0)
            offset += 1
        else:
            offset += 1
            res_sum = False
            self.esam_key_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))
        offset += 4
        if data[offset] == '01':
            offset += 2
            array_sum = int(data[offset], 16)
            offset += 1
            channel = ''
            for array_count in range(array_sum):
                offset += 1
                channel += data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3]
                if array_count < array_sum - 1:
                    channel += ','
                offset += 4
            self.rpt_channel_box.setText(channel)
        else:
            offset += 1
            res_sum = False
            self.esam_dialog_tm_box.setText('失败：' + base_data.get_dar(int(data[offset + 1], 16)))

        if res_sum is True:
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_rpt)


    def read_res(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + res)
        config.MASTER_WINDOW.receive_signal.disconnect(self.read_res)


    def read_res_SA(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            config.serial_window.SA_box.setText(self.SA_box.text())
            config.serial_window.SA_len_box.setText(str(len(self.SA_box.text()) // 2))
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + res)
        config.MASTER_WINDOW.receive_signal.disconnect(self.read_res_SA)
