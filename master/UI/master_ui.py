"""master ui"""
import sys
import os
from master import config
from PyQt4 import QtCore, QtGui
import traceback
import time

from master.UI.ui_setup import MasterWindowUi
from master.trans import common
from master.trans import linklayer
from master.trans.translate import Translate
from master.UI import dialog_ui
from master.UI import param_ui
from master import config
from master.reply import reply
from master.datas import oad_omd
from master.others import msg_log
from master.others import master_config


class MasterWindow(QtGui.QMainWindow, MasterWindowUi):
    """serial window"""
    receive_signal = QtCore.pyqtSignal(str, int)
    send_signal = QtCore.pyqtSignal(str, int)
    se_apdu_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MasterWindow, self).__init__()
        self.setup_ui()
        self.reply_rpt_cb.setChecked(True)
        self.reply_link_cb.setChecked(True)
        self.is_reply_link = True if self.reply_link_cb.isChecked() else False
        self.is_reply_rpt = True if self.reply_rpt_cb.isChecked() else False

        self.apply_config()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint\
                if self.always_top_cb.isChecked() else QtCore.Qt.Widget)
        self.receive_signal.connect(self.re_msg_do)
        self.send_signal.connect(self.se_msg_do)
        self.se_apdu_signal.connect(self.send_apdu)

        self.tmn_table_scan_b.clicked.connect(self.tmn_scan)
        self.clr_b.clicked.connect(lambda: self.clr_table(self.msg_table))
        self.open_log_b.clicked.connect(self.open_log_dir)
        self.msg_table.cellDoubleClicked.connect(self.trans_msg)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.reply_link_cb.clicked.connect(self.set_reply_link)
        self.reply_rpt_cb.clicked.connect(self.set_reply_rpt)
        self.read_oad_b.clicked.connect(self.send_read_oad)
        self.connect(self.oad_box, QtCore.SIGNAL("returnPressed()"), self.send_read_oad)
        self.oad_box.textChanged.connect(self.explain_oad)

        self.about_action.triggered.connect(self.show_about_window)
        self.link_action.triggered.connect(self.show_commu_window)
        self.general_cmd_action.triggered.connect(self.show_general_cmd_window)
        self.get_set_service_action.triggered.connect(self.show_get_service_window)
        self.apdu_diy_action.triggered.connect(lambda: self.apdu_diy_dialog.show() or self.apdu_diy_dialog.activateWindow())
        self.msg_diy_action.triggered.connect(lambda: self.msg_diy_dialog.show() or self.msg_diy_dialog.activateWindow())

        self.remote_update_action.triggered.connect(self.show_remote_update_window)

        self.tmn_table_add_b.clicked.connect(lambda:\
                            self.add_tmn_table_row('000000000001', 0, 1, is_checked=True))
        self.tmn_table_clr_b.clicked.connect(lambda: self.clr_table(self.tmn_table))

        self.pop_dialog = dialog_ui.TransPopDialog()
        self.commu_dialog = dialog_ui.CommuDialog()
        self.get_set_service_dialog = dialog_ui.GetSetServiceDialog()
        self.apdu_diy_dialog = dialog_ui.ApduDiyDialog()
        self.msg_diy_dialog = dialog_ui.MsgDiyDialog()
        self.remote_update_dialog = dialog_ui.RemoteUpdateDialog()
        self.general_cmd_dialog = param_ui.ParamWindow()

        self.msg_log = msg_log.MsgLog()


    def apply_config(self):
        """apply config"""
        apply_config = master_config.MasterConfig()
        tmn_list = eval(apply_config.get_tmn_list())
        for tmn in tmn_list:
            self.add_tmn_table_row(is_checked=tmn[0], tmn_addr=tmn[1],\
                                    logic_addr=tmn[2], chan_index=tmn[3])
        self.always_top_cb.setChecked(apply_config.get_windows_top())

    def re_msg_do(self, re_text, chan_index):
        """recieve text"""
        re_list = common.text2list(re_text)
        msgs = common.search_msg(re_list)
        for msg in msgs:
            self.add_msg_table_row(msg, chan_index, '←')


    def se_msg_do(self, re_text, chan_index):
        """recieve text"""
        self.add_msg_table_row(re_text, chan_index, '→')


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
        logic_addr_box.setRange(0, 3)
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
        if client_addr != '00' and client_addr != config.COMMU.master_addr:
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
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 0, item)

        addr_text = '{SA}:{logic}'.format(SA=server_addr, logic=logic_addr)
        item = QtGui.QTableWidgetItem(addr_text)
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 1, item)

        item = QtGui.QTableWidgetItem(chan_text + direction)
        item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 2, item)

        item = QtGui.QTableWidgetItem(brief)
        if brief == '无效报文':
            item.setTextColor(QtCore.Qt.red)
        self.msg_table.setItem(row_pos, 3, item)

        msg_text = common.format_text(m_text)
        item = QtGui.QTableWidgetItem(msg_text)
        # item.setBackgroundColor(text_color)
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


    def send_apdu(self, apdu_text, tmn_addr='', logic_addr=-1, chan_index=-1, C_text='43'):
        """apdu to compelete msg to send"""
        for row in [x for x in range(self.tmn_table.rowCount())\
                        if self.tmn_table.cellWidget(x, 0).isChecked()]:
            if tmn_addr and tmn_addr != self.tmn_table.item(row, 1).text():
                continue
            if logic_addr != -1 and logic_addr != self.tmn_table.cellWidget(row, 2).value():
                continue
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
        self.pop_dialog.activateWindow()


    def clr_table(self, table):
        """clear table widget"""
        for _ in range(table.rowCount()):
            table.removeRow(0)
        # table.setRowCount(0)


    def open_log_dir(self):
        """open_log_dir"""
        os.system('start {dir}'.format(dir=config.MSG_LOG_DIR))


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
        self.is_reply_link = True if self.reply_link_cb.isChecked() else False


    def set_reply_rpt(self):
        """set_reply_rpt"""
        self.is_reply_rpt = True if self.reply_rpt_cb.isChecked() else False


    def show_about_window(self):
        """show_about_window"""
        config.ABOUT_WINDOW.show()
        config.ABOUT_WINDOW.activateWindow()


    def show_commu_window(self):
        """show_commu_window"""
        self.commu_dialog.show()
        self.commu_dialog.activateWindow()


    def show_get_service_window(self):
        """show_get_service_window"""
        self.get_set_service_dialog.show()
        self.get_set_service_dialog.activateWindow()


    def show_general_cmd_window(self):
        """show_general_cmd_window"""
        self.general_cmd_dialog.show()
        self.general_cmd_dialog.activateWindow()


    def show_remote_update_window(self):
        """remote_update_dialog"""
        self.remote_update_dialog.show()
        self.remote_update_dialog.activateWindow()


    def send_read_oad(self):
        """send message"""
        oad_text = self.oad_box.text().replace(' ', '')
        if len(oad_text) == 8:
            apdu_text = '050100 %s 00'%oad_text
            self.se_apdu_signal.emit(apdu_text)
        else:
            self.oad_explain_l.setTextFormat(QtCore.Qt.RichText)
            self.oad_explain_l.setText('<p style="color: red">请输入正确的OAD</p>')


    def explain_oad(self):
        """explain_oad"""
        oad_text = self.oad_box.text().replace(' ', '')
        if len(oad_text) == 8:
            explain = oad_omd.get_oad_explain(oad_text)
            self.oad_explain_l.setText(explain)
        else:
            self.oad_explain_l.setText('')


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
        save_config.commit()

        # ask to quit
        window_pos = self.pos()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()
        self.move(window_pos)
        quit_box = QtGui.QMessageBox()
        reply = quit_box.question(self, '698后台', '确定退出吗？'
                                  , QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            config.COMMU.quit()
            event.accept()
            os._exit(0)
        else:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint\
                    if self.always_top_cb.isChecked() else QtCore.Qt.Widget)
            self.show()
            self.move(window_pos)
            event.ignore()


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = MasterWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
