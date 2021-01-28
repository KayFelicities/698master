"""master ui"""
import sys
import os
from master import config
import traceback
import time
import threading
import urllib.request
from master.UI.ui_setup import MasterWindowUi
from master.trans import common
from master.trans import linklayer
from master.trans.translate import Translate
from master.UI import dialog_ui
from master.UI import param_ui
from master.reply import reply
from master.datas import k_data_s
from master.datas import collection
from master.others import msg_log
from master.others import master_config
if config.IS_USE_PYSIDE:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore


class MasterWindow(QtGui.QMainWindow, MasterWindowUi):
    """serial window"""
    receive_signal = QtCore.Signal(str, int) if config.IS_USE_PYSIDE else QtCore.pyqtSignal(str, int)
    send_signal = QtCore.Signal(str, int) if config.IS_USE_PYSIDE else QtCore.pyqtSignal(str, int)
    se_apdu_signal = QtCore.Signal(str) if config.IS_USE_PYSIDE else QtCore.pyqtSignal(str)

    def __init__(self):
        super(MasterWindow, self).__init__()
        self.setup_ui()
        # self.show_linklayer_cb.setVisible(False)
        self.show_level_cb.setVisible(False)
        self.plaintext_rn.setChecked(False)
        self.reply_rpt_cb.setChecked(True)
        self.reply_link_cb.setChecked(True)
        self.reply_split_cb.setChecked(True)
        self.show_level_cb.setChecked(True)
        self.is_reply_link = True if self.reply_link_cb.isChecked() else False
        self.is_reply_rpt = True if self.reply_rpt_cb.isChecked() else False
        self.is_reply_split = True if self.reply_split_cb.isChecked() else False
        self.is_plaintext_rn = True if self.plaintext_rn.isChecked() else False
        self.quick_read_panel.cnt_box_w.setVisible(True if self.quick_read_panel.oad_auto_r_cb.isChecked() else False)
        # self.tmn_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.set_b_red(self.serial_b)
        self.set_b_red(self.frontend_b)
        self.set_b_red(self.server_b)

        self.apply_config()

        self.setAcceptDrops(True)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint\
                if self.always_top_cb.isChecked() else QtCore.Qt.Widget)
        self.receive_signal.connect(self.re_msg_do)
        self.send_signal.connect(self.se_msg_do)
        self.se_apdu_signal.connect(self.send_apdu)

        self.tmn_table_scan_b.clicked.connect(self.tmn_scan)
        self.clr_b.clicked.connect(lambda: self.clr_table(self.msg_table))
        self.msg_table.currentCellChanged.connect(self.trans_row)
        self.msg_table.cellClicked.connect(self.trans_row)
        self.msg_table.cellDoubleClicked.connect(self.trans_msg)
        self.se_clr_b.clicked.connect(lambda: self.get_current_se_box().clear() or self.get_current_se_box().setFocus())
        self.se_send_b.clicked.connect(self.send_se_msg)
        self.auto_wrap_cb.stateChanged.connect(self.set_auto_wrap)
        self.show_linklayer_cb.stateChanged.connect(self.trans_se_msg)
        self.show_level_cb.stateChanged.connect(self.trans_se_msg)
        self.show_dtype_cb.stateChanged.connect(self.trans_se_msg)
        self.copy_b.clicked.connect(self.copy_to_clipboard)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.reply_link_cb.clicked.connect(self.set_reply_link)
        self.reply_rpt_cb.clicked.connect(self.set_reply_rpt)
        self.reply_split_cb.clicked.connect(self.set_reply_split)
        self.plaintext_rn.clicked.connect(self.set_plaintext_rn)
        self.quick_read_panel.read_oad_b.clicked.connect(self.send_read_oad)
        self.quick_read_panel.oad_auto_r_cb.clicked.connect(lambda: self.quick_read_panel.cnt_box_w.setVisible(True if self.quick_read_panel.oad_auto_r_cb.isChecked() else False))
        self.quick_read_panel.cnt_clr_b.clicked.connect(self.cnt_reset)
        self.quick_read_panel.oad_box.returnPressed.connect(self.send_read_oad)
        self.quick_read_panel.oad_box.textChanged.connect(self.explain_oad)
        self.se_msg_tab.installEventFilter(self)
        self.se_msg_tab.currentChanged.connect(self.set_auto_wrap)
        self.se_msg_tab.currentChanged.connect(self.trans_msg_box)
        self.quick_set_time_panel.read_dt_b.clicked.connect(lambda: self.send_apdu('0501004000020000'))
        self.quick_set_time_panel.set_dt_b.clicked.connect(lambda: self.set_time(False))
        self.quick_set_time_panel.set_current_dt_b.clicked.connect(lambda: self.set_time(True))
        self.quick_set_time_panel.dt_box.dateTimeChanged.connect(lambda: self.quick_set_time_panel.dt_sec_box.setText(str(self.quick_set_time_panel.dt_box.dateTime().toTime_t())))
        self.quick_set_time_panel.dt_sec_b.clicked.connect(lambda: self.quick_set_time_panel.dt_box.setDateTime(QtCore.QDateTime.fromTime_t(int(self.quick_set_time_panel.dt_sec_box.text()))))
        self.quick_set_time_panel.dt_box.setDateTime(QtCore.QDateTime.currentDateTime())

        self.serial_b.clicked.connect(lambda: self.commu_dialog.connect_serial() if not self.commu_dialog.is_serial_connect else self.commu_dialog.cut_serial())
        self.frontend_b.clicked.connect(lambda: self.commu_dialog.connect_frontend() if not self.commu_dialog.is_frontend_connect else self.commu_dialog.cut_frontend())
        self.server_b.clicked.connect(lambda: self.commu_dialog.connect_server() if not self.commu_dialog.is_server_connect else self.commu_dialog.cut_server())
        self.commu_set_b.clicked.connect(self.show_commu_window)

        for cnt in range(1, 7):
            se_box = self.add_se_box(' %s '%str(cnt))
            se_box.textChanged.connect(self.trans_msg_box)

            # scroll connect
            se_box.verticalScrollBar().valueChanged.connect(self.set_explain_box_vscroll_percent)
            self.explain_box.verticalScrollBar().valueChanged.connect(self.set_se_box_vscroll_percent)
            se_box.horizontalScrollBar().valueChanged.connect(self.set_explain_box_hscroll_percent)
            self.explain_box.horizontalScrollBar().valueChanged.connect(self.set_se_box_hscroll_percent)
        self.set_auto_wrap()

        # collection list
        self.collec = collection.Collection()
        self.se_collection_cbox.addItems(self.collec.get_name_list())
        self.se_collection_cbox.addItems(['刷新', '自定义'])
        self.se_collection_cbox.setCurrentIndex(-1)
        self.se_collection_cbox.activated.connect(self.collection_active)
        completer = QtGui.QCompleter(self.collec.get_name_list())
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.se_collection_cbox.setCompleter(completer)

        self.about_action.triggered.connect(lambda: config.ABOUT_WINDOW.show() or config.ABOUT_WINDOW.showNormal() or config.ABOUT_WINDOW.activateWindow())
        self.link_action.triggered.connect(self.show_commu_window)
        self.general_cmd_action.triggered.connect(lambda: self.general_cmd_dialog.show() or self.general_cmd_dialog.showNormal() or self.general_cmd_dialog.activateWindow())
        self.get_set_service_action.triggered.connect(self.show_get_service_window)
        self.apdu_diy_action.triggered.connect(lambda: self.apdu_diy_dialog.show() or self.apdu_diy_dialog.showNormal() or self.apdu_diy_dialog.activateWindow())
        self.msg_diy_action.triggered.connect(lambda: self.msg_diy_dialog.show() or self.msg_diy_dialog.showNormal() or self.msg_diy_dialog.activateWindow())
        self.remote_update_action.triggered.connect(lambda: self.remote_update_dialog.show() or self.remote_update_dialog.showNormal() or self.remote_update_dialog.activateWindow())
        self.trans_log_action.triggered.connect(lambda: self.trans_file(config.LOG_PATH))
        self.open_log_action.triggered.connect(lambda: os.system('start "" "{dir}"'.format(dir=config.MSG_LOG_DIR)))
        self.open_trans_action.triggered.connect(self.trans_file)

        self.tmn_table_add_b.clicked.connect(lambda:\
                            self.add_tmn_table_row('000000000001', 0, 1, is_checked=True))
        self.tmn_table_clr_b.clicked.connect(lambda: self.clr_table(self.tmn_table))

        qss_file = open(os.path.join(config.SOFTWARE_PATH, 'styles/white_blue.qss')).read()
        self.setStyleSheet(qss_file)
        self.pop_dialog = dialog_ui.TransPopDialog()
        self.pop_dialog.setStyleSheet(qss_file)
        self.commu_dialog = dialog_ui.CommuDialog()
        self.commu_dialog.setStyleSheet(qss_file)
        # self.get_set_service_dialog = dialog_ui.GetSetServiceDialog()
        self.apdu_diy_dialog = dialog_ui.ApduDiyDialog()
        self.apdu_diy_dialog.setStyleSheet(qss_file)
        self.msg_diy_dialog = dialog_ui.MsgDiyDialog()
        self.msg_diy_dialog.setStyleSheet(qss_file)
        self.remote_update_dialog = dialog_ui.RemoteUpdateDialog()
        self.remote_update_dialog.setStyleSheet(qss_file)
        self.general_cmd_dialog = param_ui.ParamWindow()
        self.general_cmd_dialog.setStyleSheet(qss_file)

        self.msg_log = msg_log.MsgLog()

        self.infol_cycle = 0
        self.update_infol()
        self.explain_oad()

        self.apdu_text = ''
        self.is_auto_r = False
        self.msg_now = ''

        self.timer = time.time()
        self.auto_r_piid = 63
        self.send_cnt = 0
        self.receive_cnt = 0


    def dragEnterEvent(self, event):
        """drag"""
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        """drop file"""
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            print('url:', links[0])
            self.trans_file(links[0])
        else:
            event.ignore()


    def apply_config(self):
        """apply config"""
        apply_config = master_config.MasterConfig()
        tmn_list = eval(apply_config.get_tmn_list())
        for tmn in tmn_list:
            self.add_tmn_table_row(is_checked=tmn[0], tmn_addr=tmn[1],\
                                    logic_addr=tmn[2], chan_index=tmn[3])
        self.always_top_cb.setChecked(apply_config.get_windows_top())
        self.quick_read_panel.oad_box.setText(apply_config.get_oad_r())


    def eventFilter(self, widget, event):
        """test"""
        # if event.type() == QtCore.QEvent.FocusIn:
        if event.type() == QtCore.QEvent.MouseButtonPress:
            scroll_hpos = self.get_current_se_box().horizontalScrollBar().value()
            scroll_vpos = self.get_current_se_box().verticalScrollBar().value()
            self.get_current_se_box().setPlainText(self.get_current_se_box().get_save_msg())
            self.trans_msg_box()
            self.get_current_se_box().horizontalScrollBar().setValue(scroll_hpos)
            self.get_current_se_box().verticalScrollBar().setValue(scroll_vpos)
            self.se_msg_tab.setEnabled(True)
            self.get_current_se_box().setFocus(True)
        return QtGui.QMainWindow.eventFilter(self, widget, event)


    def set_time(self, is_current_tm):
        DT = QtCore.QDateTime.currentDateTime() if is_current_tm else self.quick_set_time_panel.dt_box.dateTime()
        DT_list = DT.toString('yyyy.MM.dd.hh.mm.ss').split('.')
        DT_text = '1C%04X' % int(DT_list[0])
        for DT in DT_list[1:]:
            DT_text += '%02X' % int(DT)
        apdu_text = '06010D40000200' + DT_text + '00'
        self.send_apdu(apdu_text)


    def collection_active(self):
        """collection_active"""
        select = self.se_collection_cbox.currentText()
        if select in ['刷新']:
            self.collec.refresh_name_list()
            self.se_collection_cbox.clear()
            self.se_collection_cbox.addItems(self.collec.get_name_list())
            self.se_collection_cbox.addItems(['刷新', '自定义'])
            completer = QtGui.QCompleter(self.collec.get_name_list())
            completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
            self.se_collection_cbox.setCompleter(completer)
        elif select in ['自定义']:
            self.collec.open_collection_file()
        else:
            self.get_current_se_box().setPlainText(self.collec.get_msg(select))
        self.se_collection_cbox.setCurrentIndex(-1)


    def update_infol(self, tmout=1):
        """update"""
        try:
            info = urllib.request.urlopen('http://65.49.212.36/infol/' + config.MASTER_SOFTWARE_VERSION, timeout=tmout)
            if info:
                self.info_l.setText(info.read().decode())
                self.infol_cycle = 30*60
        except Exception:
            traceback.print_exc()
            self.infol_cycle += 1*60
            if self.infol_cycle > 30*60:
                self.infol_cycle = 0
            print('request failed.')


    # @QtCore.Slot(str, int)
    def re_msg_do(self, re_text, chan_index):
        """recieve text"""
        self.add_msg_table_row(re_text, chan_index, '←')
        if self.quick_read_panel.oad_auto_r_cb.isChecked() and common.get_msg_service_no(re_text) == self.auto_r_piid:
            self.receive_cnt += 1
            self.quick_read_panel.receive_cnt_l.setText('收%d'%self.receive_cnt)
        if time.time() - self.timer > self.infol_cycle:
            print('update info')
            self.timer = time.time()
            self.update_infol(tmout=2)
        apdu_list = common.get_apdu_list(common.text2list(re_text))
        if apdu_list and ''.join(apdu_list[0:2]) == '8501' and ''.join(apdu_list[3:7]) == '40000200' and apdu_list[7] == '01':
            offset = 9
            DT_read = QtCore.QDateTime(
                (int(apdu_list[offset], 16) << 8) | int(apdu_list[offset + 1], 16),
                int(apdu_list[offset + 2], 16),
                int(apdu_list[offset + 3], 16),
                int(apdu_list[offset + 4], 16),
                int(apdu_list[offset + 5], 16),
                int(apdu_list[offset + 6], 16),
            )
            self.quick_set_time_panel.dt_box.setDateTime(DT_read)


    # @QtCore.Slot(str, int)
    def se_msg_do(self, re_text, chan_index):
        """recieve text"""
        self.add_msg_table_row(re_text, chan_index, '→')
        if self.quick_read_panel.oad_auto_r_cb.isChecked() and common.get_msg_service_no(re_text) == self.auto_r_piid:
            self.send_cnt += 1
            self.quick_read_panel.send_cnt_l.setText('发%d'%self.send_cnt)


    def add_tmn_table_row(self, tmn_addr='000000000001', logic_addr=0, chan_index=1, is_checked=False):
        """add message row"""
        row_pos = self.tmn_table.rowCount()
        self.tmn_table.insertRow(row_pos)

        tmn_enable_cb = QtGui.QCheckBox()
        tmn_enable_cb.setChecked(is_checked)
        self.tmn_table.setCellWidget(row_pos, 0, tmn_enable_cb)

        item = QtGui.QTableWidgetItem(tmn_addr)
        self.tmn_table.setItem(row_pos, 1, item)

        logic_addr_box = QtGui.QSpinBox()
        logic_addr_box.setRange(0, 255)
        logic_addr_box.setValue(logic_addr)
        self.tmn_table.setCellWidget(row_pos, 2, logic_addr_box)

        channel_cb = QtGui.QComboBox()
        channel_cb.addItems(('串口', '前置机', '服务器'))
        channel_cb.setCurrentIndex(chan_index)
        self.tmn_table.setCellWidget(row_pos, 3, channel_cb)

        self.tmn_remove_cb = QtGui.QPushButton()
        self.tmn_remove_cb.setText('删')
        self.tmn_table.setCellWidget(row_pos, 4, self.tmn_remove_cb)
        self.tmn_remove_cb.clicked.connect(self.tmn_table_remove)

        self.tmn_table.scrollToBottom()


    def tmn_table_remove(self):
        """remove row in tmn table"""
        button = self.sender()
        index = self.tmn_table.indexAt(button.pos())
        self.tmn_table.removeRow(index.row())


    def add_msg_table_row(self, m_text, chan_index, direction):
        """add message row"""
        trans = Translate(m_text)
        brief = trans.get_brief()
        # direction = trans.get_direction()
        client_addr = trans.get_CA()
        if config.IS_FILETER_CA and client_addr != '00' and client_addr != config.COMMU.master_addr:
            print('过滤报文：CA不匹配')
            return
        server_addr = trans.get_SA()
        logic_addr = trans.get_logic_addr()
        chan_text = {0: '串口', 1: '前置机', 2: '服务器'}.get(chan_index)

        # chk to add tmn addr to table
        if direction == '←':
            for row_num in range(self.tmn_table.rowCount()):
                if server_addr == self.tmn_table.item(row_num, 1).text()\
                and logic_addr == self.tmn_table.cellWidget(row_num, 2).value()\
                and chan_index == self.tmn_table.cellWidget(row_num, 3).currentIndex():
                    break
            else:
                is_cb_checked = False if chan_index == 1 else True
                self.add_tmn_table_row(tmn_addr=server_addr, logic_addr=logic_addr,\
                                        chan_index=chan_index, is_checked=is_cb_checked)

        text_color = QtGui.QColor(220, 226, 241) if direction == '→' else\
                    QtGui.QColor(227, 237, 205) if direction == '←' else QtGui.QColor(255, 255, 255)
        row_pos = self.msg_table.rowCount()
        self.msg_table.insertRow(row_pos)

        item = QtGui.QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # item.setBackground(text_color)
        self.msg_table.setItem(row_pos, 0, item)

        addr_text = '{SA}:{logic}'.format(SA=server_addr, logic=logic_addr)
        item = QtGui.QTableWidgetItem(addr_text)
        # item.setBackground(text_color)
        self.msg_table.setItem(row_pos, 1, item)

        item = QtGui.QTableWidgetItem(chan_text + direction)
        item.setBackground(text_color)
        self.msg_table.setItem(row_pos, 2, item)

        item = QtGui.QTableWidgetItem(brief)
        if brief == '无效报文':
            item.setTextColor(QtCore.Qt.red)
        if brief.find('(访问失败)') == 0:
            item.setTextColor(QtGui.QColor(255, 140, 0))
        self.msg_table.setItem(row_pos, 3, item)

        msg_text = common.format_text(m_text)
        item = QtGui.QTableWidgetItem(msg_text)
        # item.setBackground(text_color)
        self.msg_table.setItem(row_pos, 4, item)

        if row_pos > config.MSG_TABLE_ROW_MAX:
            self.msg_table.removeRow(0)

        self.msg_table.scrollToBottom()

        # log
        self.msg_log.add_log(addr_text, chan_text, direction, brief, msg_text)

        service = trans.get_service()
        if service == '01' and self.is_reply_link:
            reply_apdu_text = reply.get_link_replay_apdu(trans)
            self.send_apdu(reply_apdu_text, tmn_addr=server_addr,\
                            logic_addr=logic_addr, chan_index=chan_index, C_text='01')
        if service[:2] == '88' and self.is_reply_rpt:
            reply_apdu_text = reply.get_rpt_replay_apdu(trans)
            self.send_apdu(reply_apdu_text, tmn_addr=server_addr,\
                            logic_addr=logic_addr, chan_index=chan_index, C_text='03')
        if service == '8505' and self.is_reply_split and trans.is_access_successed:
            reply_apdu_text = reply.get_rpt_replay_split(trans)
            self.send_apdu(reply_apdu_text, tmn_addr=server_addr,\
                            logic_addr=logic_addr, chan_index=chan_index, C_text='43')


    def trans_msg_box(self):
        """trans_msg_box"""
        self.msg_now = self.get_current_se_box().toPlainText()
        self.get_current_se_box().set_save_msg(self.msg_now)
        self.trans_se_msg()


    def trans_se_msg(self):
        """translate"""
        if len(self.msg_now) < 5:
            return
        trans = Translate(self.msg_now)
        structed_explain = trans.get_structed_explain(is_show_type=self.show_dtype_cb.isChecked(), has_linklayer=self.show_linklayer_cb.isChecked())
        self.explain_box.setText(r'%s'%structed_explain)
        self.se_send_b.setEnabled(True if trans.is_success else False)
        if self.se_send_b.isEnabled():
            self.apdu_text = trans.get_apdu_text()
        if trans.is_success:
            self.get_current_se_box().textChanged.disconnect(self.trans_msg_box)
            cursor = self.get_current_se_box().textCursor()
            cursor_pos = cursor.position()
            scroll_hpos = self.get_current_se_box().horizontalScrollBar().value()
            scroll_vpos = self.get_current_se_box().verticalScrollBar().value()
            self.get_current_se_box().setPlainText(trans.get_structed_msg(has_linklayer=self.show_linklayer_cb.isChecked()))
            cursor = self.get_current_se_box().textCursor()
            cursor.setPosition(cursor_pos)
            self.get_current_se_box().setTextCursor(cursor)
            self.get_current_se_box().horizontalScrollBar().setValue(scroll_hpos)
            self.get_current_se_box().verticalScrollBar().setValue(scroll_vpos)
            self.get_current_se_box().textChanged.connect(self.trans_msg_box)


    def set_se_box_vscroll_percent(self):
        """set_se_box_scroll_percent"""
        if self.explain_box.verticalScrollBar().maximum() != 0:
            value = self.explain_box.verticalScrollBar().value() / self.explain_box.verticalScrollBar().maximum() * self.get_current_se_box().verticalScrollBar().maximum()
            self.get_current_se_box().verticalScrollBar().valueChanged.disconnect(self.set_explain_box_vscroll_percent)
            self.get_current_se_box().verticalScrollBar().setValue(value)
            self.get_current_se_box().verticalScrollBar().valueChanged.connect(self.set_explain_box_vscroll_percent)



    def set_explain_box_vscroll_percent(self):
        """set_explain_box_scroll_percent"""
        if self.get_current_se_box().verticalScrollBar().maximum() != 0:
            value = self.get_current_se_box().verticalScrollBar().value() / self.get_current_se_box().verticalScrollBar().maximum() * self.explain_box.verticalScrollBar().maximum()
            self.explain_box.verticalScrollBar().valueChanged.disconnect(self.set_se_box_vscroll_percent)
            self.explain_box.verticalScrollBar().setValue(value)
            self.explain_box.verticalScrollBar().valueChanged.connect(self.set_se_box_vscroll_percent)


    def set_se_box_hscroll_percent(self):
        """set_se_box_scroll_percent"""
        if self.explain_box.horizontalScrollBar().maximum() != 0:
            value = self.explain_box.horizontalScrollBar().value() / self.explain_box.horizontalScrollBar().maximum() * self.get_current_se_box().horizontalScrollBar().maximum()
            self.get_current_se_box().horizontalScrollBar().valueChanged.disconnect(self.set_explain_box_hscroll_percent)
            self.get_current_se_box().horizontalScrollBar().setValue(value)
            self.get_current_se_box().horizontalScrollBar().valueChanged.connect(self.set_explain_box_hscroll_percent)


    def set_explain_box_hscroll_percent(self):
        """set_explain_box_scroll_percent"""
        if self.get_current_se_box().horizontalScrollBar().maximum() != 0:
            value = self.get_current_se_box().horizontalScrollBar().value() / self.get_current_se_box().horizontalScrollBar().maximum() * self.explain_box.horizontalScrollBar().maximum()
            self.explain_box.horizontalScrollBar().valueChanged.disconnect(self.set_se_box_hscroll_percent)
            self.explain_box.horizontalScrollBar().setValue(value)
            self.explain_box.horizontalScrollBar().valueChanged.connect(self.set_se_box_hscroll_percent)


    def send_se_msg(self):
        """send sendbox msg"""
        msg = self.get_current_se_box().toPlainText()
        if len(msg) < 5:
            return
        trans = Translate(msg)
        apdu_text = trans.get_apdu_text()
        self.se_apdu_signal.emit(apdu_text)


    # @QtCore.Slot(str)
    def send_apdu(self, apdu_text, tmn_addr='', logic_addr=-1, chan_index=-1, C_text='43'):
        """apdu to compelete msg to send"""
        if self.is_plaintext_rn:
            # 10 + 00 + len + apdu + 0110 5FE30D32D6A20288F9112B5C6052CFDB(fixme: 先固定一个随机数)
            apdu_len = len(common.text2list(apdu_text))
            apdu_head = '1000' #安全请求+明文应用数据单元

            if apdu_len < 128:
                apdu_head += "%02X"%apdu_len
            elif apdu_len < 256:
                apdu_head += "81%02X"%apdu_len
            else:
                apdu_head += "82%04X"%apdu_len

            apdu_text = apdu_head + apdu_text + '0110 5FE30D32D6A20288F9112B5C6052CFDB'
            # print('读取明文+随机{}:{}'.format(len(common.text2list(apdu_text)), apdu_text))

        for row in [x for x in range(self.tmn_table.rowCount())\
                        if self.tmn_table.cellWidget(x, 0).isChecked()]:
            if tmn_addr and tmn_addr != self.tmn_table.item(row, 1).text():
                continue
            # if logic_addr != -1 and logic_addr != self.tmn_table.cellWidget(row, 2).value():
            #     continue
            if chan_index != -1 and chan_index != self.tmn_table.cellWidget(row, 3).currentIndex():
                continue

            compelete_msg = linklayer.add_linkLayer(common.text2list(apdu_text),\
                                logic_addr=self.tmn_table.cellWidget(row, 2).value(),\
                                SA_text=self.tmn_table.item(row, 1).text(),\
                                CA_text=config.COMMU.master_addr, C_text=C_text)
            config.COMMU.send_msg(compelete_msg, self.tmn_table.cellWidget(row, 3).currentIndex())


    def send_msg(self, msg_text, chan_index):
        """msg to send"""
        config.COMMU.send_msg(msg_text, chan_index)


    def tmn_scan(self):
        """scan terminal"""
        wild_apdu = '0501014000020000'
        compelete_msg = linklayer.add_linkLayer(common.text2list(wild_apdu),\
                                SA_text='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',\
                                SA_type=1,\
                                CA_text=config.COMMU.master_addr,\
                                C_text='43')
        config.COMMU.send_msg(compelete_msg, -1)


    def trans_msg(self, row):
        """translate massage"""
        self.pop_dialog.msg_box.setPlainText(self.msg_table.item(row, 4).text())
        self.pop_dialog.show()
        self.pop_dialog.showNormal()
        self.pop_dialog.activateWindow()


    def trans_row(self, row):
         """translate row massage"""
         if self.msg_table.item(row, 4) is None: # fixme: 这里会出现None
             self.msg_now = ''
         else:
            self.msg_now = self.msg_table.item(row, 4).text()
         self.trans_se_msg()
         self.se_msg_tab.setEnabled(False)
         self.se_send_b.setEnabled(False)

    def clr_table(self, table):
        """clear table widget"""
        for _ in range(table.rowCount()):
            table.removeRow(0)
        # table.setRowCount(0)


    def set_auto_wrap(self):
        """set_auto_wrap"""
        self.get_current_se_box().setLineWrapMode(QtGui.QTextEdit.WidgetWidth\
                if self.auto_wrap_cb.isChecked() else QtGui.QTextEdit.NoWrap)
        self.explain_box.setLineWrapMode(QtGui.QTextEdit.WidgetWidth\
                if self.auto_wrap_cb.isChecked() else QtGui.QTextEdit.NoWrap)


    def set_always_top(self):
        """set_always_top"""
        window_pos = self.pos()
        if self.always_top_cb.isChecked() is True:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


    def set_reply_link(self):
        """set_reply_link"""
        self.is_reply_link = self.reply_link_cb.isChecked()


    def set_reply_rpt(self):
        """set_reply_rpt"""
        self.is_reply_rpt = self.reply_rpt_cb.isChecked()


    def set_reply_split(self):
        """set_reply_split"""
        self.is_reply_split = self.reply_split_cb.isChecked()


    def set_plaintext_rn(self):
        """set_plaintext_rn"""
        self.is_plaintext_rn = self.plaintext_rn.isChecked()


    def show_get_service_window(self):
        """show_get_service_window"""
        self.get_set_service_dialog.show()
        self.get_set_service_dialog.activateWindow()


    def show_commu_window(self):
        """show commu window"""
        self.commu_dialog.show()
        self.commu_dialog.showNormal()
        self.commu_dialog.activateWindow()

    def send_read_oad(self):
        """send message"""
        if self.is_auto_r:
            self.is_auto_r = False
            self.quick_read_panel.read_oad_b.setText('读取')
            self.quick_read_panel.oad_auto_r_cb.setEnabled(True)
            self.quick_read_panel.oad_auto_r_spin.setEnabled(True)
            self.quick_read_panel.oad_auto_unit_l.setEnabled(True)
            return
        oad_text = self.quick_read_panel.oad_box.text().replace(' ', '')
        if len(oad_text) == 8:
            apdu_text = '0501%02X %s 00'%(self.auto_r_piid, oad_text)
            if self.quick_read_panel.oad_auto_r_cb.isChecked():
                self.is_auto_r = True
                self.quick_read_panel.read_oad_b.setText('停止')
                self.quick_read_panel.oad_auto_r_cb.setEnabled(False)
                self.quick_read_panel.oad_auto_r_spin.setEnabled(False)
                self.quick_read_panel.oad_auto_unit_l.setEnabled(False)
                threading.Thread(target=self.auto_r_oad,\
                    args=(apdu_text,)).start()
            else:
                self.se_apdu_signal.emit(apdu_text)
        else:
            self.quick_read_panel.oad_explain_l.setTextFormat(QtCore.Qt.RichText)
            self.quick_read_panel.oad_explain_l.setText('<p style="color: red">请输入正确的OAD</p>')

    
    def auto_r_oad(self, apdu_text):
        """auto read oad thread"""
        delay_s = max(self.quick_read_panel.oad_auto_r_spin.value(), 0.05)
        if delay_s == 0:
            delay_s = 0.2
        while self.is_auto_r:
            self.se_apdu_signal.emit(apdu_text)
            time.sleep(delay_s)


    def cnt_reset(self):
        """reset cnt"""
        self.send_cnt = 0
        self.receive_cnt = 0
        self.quick_read_panel.send_cnt_l.setText('发0')
        self.quick_read_panel.receive_cnt_l.setText('收0')


    def explain_oad(self):
        """explain_oad"""
        oad_text = self.quick_read_panel.oad_box.text().replace(' ', '')
        if len(oad_text) == 8:
            explain = config.K_DATA.get_oad_explain(oad_text)
            self.quick_read_panel.oad_explain_l.setText(explain)
        else:
            self.quick_read_panel.oad_explain_l.setText('')


    def trans_file(self, file_path='1'):
        """file analysis"""
        cmd = 'start "" "{exe}" "{log}"'.format(exe=config.RUN_EXE_PATH, log=file_path)
        print(cmd)
        os.system(cmd)


    def copy_to_clipboard(self):
        """copy_to_clipboard"""
        trans = Translate(self.msg_now)
        text = trans.get_clipboard_text(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        clipboard = QtGui.QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(text)


    def closeEvent(self, event):
        """close event"""
        # save config
        save_config = master_config.MasterConfig()
        tmn_list = []
        for row_num in range(self.tmn_table.rowCount()):
            tmn_list.append([self.tmn_table.cellWidget(row_num, 0).isChecked(),\
                                self.tmn_table.item(row_num, 1).text(),\
                                self.tmn_table.cellWidget(row_num, 2).value(),\
                                self.tmn_table.cellWidget(row_num, 3).currentIndex()])
        save_config.set_tmn_list(tmn_list)
        save_config.set_windows_top(self.always_top_cb.isChecked())
        save_config.set_oad_r(self.quick_read_panel.oad_box.text().replace(' ', ''))
        save_config.commit()

        # quit
        config.COMMU.quit()
        event.accept()
        os._exit(0)

        # ask to quit
        # window_pos = self.pos()
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.show()
        # self.move(window_pos)
        # quit_box = QtGui.QMessageBox()
        # reply = quit_box.question(self, '698后台', '确定退出吗？'
        #                           , QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        # if reply == QtGui.QMessageBox.Yes:
        #     config.COMMU.quit()
        #     event.accept()
        #     os._exit(0)
        # else:
        #     self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint\
        #             if self.always_top_cb.isChecked() else QtCore.Qt.Widget)
        #     self.show()
        #     self.move(window_pos)
        #     event.ignore()


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = MasterWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
