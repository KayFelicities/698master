'''master ui'''
import sys
import os
from master import config
from PyQt4 import QtCore, QtGui
import traceback
import time

from master.trans import common
from master.trans import linklayer
from master.trans.translate import Translate
from master.UI import dialog_ui
from master.UI import param_ui
from master import config
from master.reply import reply


class MasterWindow(QtGui.QMainWindow):
    '''serial window'''
    receive_signal = QtCore.pyqtSignal(str, str)
    send_signal = QtCore.pyqtSignal(str, str)
    se_apdu_signal = QtCore.pyqtSignal(str)


    def __init__(self):
        super(MasterWindow, self).__init__()
        self.setup_ui(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)
        self.receive_signal.connect(self.re_msg_do)
        self.send_signal.connect(self.se_msg_do)
        self.se_apdu_signal.connect(self.send_apdu)

        self.tmn_table_scan_b.clicked.connect(self.tmn_scan)
        self.clr_b.clicked.connect(lambda: self.clr_table(self.msg_table))
        self.msg_table.cellDoubleClicked.connect(self.trans_msg)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.reply_link_cb.clicked.connect(self.set_reply_link)

        self.about_action.triggered.connect(self.show_about_window)
        self.link_action.triggered.connect(self.show_commu_window)
        self.general_cmd_action.triggered.connect(self.show_general_cmd_window)
        self.get_set_service_action.triggered.connect(self.show_get_service_window)
        self.msg_diy_action.triggered.connect(self.show_msg_diy_window)
        self.remote_update_action.triggered.connect(self.show_remote_update_window)

        self.tmn_table_add_b.clicked.connect(lambda:\
                            self.add_tmn_table_row('000000000001', 0, '', is_checked=True))
        self.tmn_table_clr_b.clicked.connect(lambda: self.clr_table(self.tmn_table))

        self.pop_dialog = dialog_ui.TransPopDialog()
        self.commu_dialog = dialog_ui.CommuDialog()
        self.get_set_service_dialog = dialog_ui.GetSetServiceDialog()
        self.msg_diy_dialog = dialog_ui.MsgDiyDialog()
        self.remote_update_dialog = dialog_ui.RemoteUpdateDialog()
        self.general_cmd_dialog = param_ui.ParamWindow()

        self.is_reply_link = True

        self.show_commu_window()


    def setup_ui(self, master_window):
        '''set layout'''
        self.setWindowTitle('698后台_{ver}'.format(ver=config.MASTER_WINDOW_TITLE_ADD))
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698.png')))
        self.menubar = self.menuBar()

        self.link_action = QtGui.QAction('&通信设置', self)
        self.link_action.setShortcut('F2')
        self.commu_menu = self.menubar.addMenu('&通信')
        self.commu_menu.addAction(self.link_action)

        self.general_cmd_action = QtGui.QAction('&常用命令', self)
        self.general_cmd_action.setShortcut('F5')
        self.get_set_service_action = QtGui.QAction('&读取/设置', self)
        self.get_set_service_action.setShortcut('F6')
        self.action_service_action = QtGui.QAction('&操作', self)
        self.action_service_action.setShortcut('F7')
        self.proxy_service_action = QtGui.QAction('&代理', self)
        self.proxy_service_action.setShortcut('F9')
        self.commu_menu = self.menubar.addMenu('&服务')
        self.commu_menu.addAction(self.general_cmd_action)
        self.commu_menu.addAction(self.get_set_service_action)
        self.commu_menu.addAction(self.action_service_action)
        self.commu_menu.addAction(self.proxy_service_action)

        self.msg_diy_action = QtGui.QAction('&自定义APDU', self)
        self.msg_diy_action.setShortcut('F10')
        self.remote_update_action = QtGui.QAction('&远程升级', self)
        self.remote_update_action.setShortcut('F11')
        self.msg_menu = self.menubar.addMenu('&报文')
        self.msg_menu.addAction(self.msg_diy_action)
        self.msg_menu.addAction(self.remote_update_action)

        self.about_action = QtGui.QAction('&关于', self)
        self.about_action.setShortcut('F1')
        self.help_menu = self.menubar.addMenu('&帮助')
        self.help_menu.addAction(self.about_action)

        self.tmn_list_w = QtGui.QWidget()
        self.tmn_table_vbox = QtGui.QVBoxLayout(self.tmn_list_w)
        self.tmn_table_vbox.setMargin(1)
        self.tmn_table_vbox.setSpacing(0)
        self.tmn_table = QtGui.QTableWidget(self.tmn_list_w)
        self.tmn_table.verticalHeader().setVisible(False)
        for count in range(5):
            self.tmn_table.insertColumn(count)
        self.tmn_table.setHorizontalHeaderLabels(['', '终端地址', '逻辑地址', '通道', ''])
        self.tmn_table.setColumnWidth(0, 15)
        self.tmn_table.setColumnWidth(1, 96)
        self.tmn_table.setColumnWidth(2, 40)
        self.tmn_table.setColumnWidth(3, 65)
        self.tmn_table.setColumnWidth(4, 25)
        self.tmn_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tmn_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tmn_table_scan_b = QtGui.QPushButton()
        self.tmn_table_scan_b.setText('扫描')
        self.tmn_table_add_b = QtGui.QPushButton()
        self.tmn_table_add_b.setText('新增')
        self.tmn_table_clr_b = QtGui.QPushButton()
        self.tmn_table_clr_b.setText('清空')
        self.tmn_table_clr_b.setMaximumWidth(70)
        self.tmn_table_btns_hbox = QtGui.QHBoxLayout()
        self.tmn_table_btns_hbox.addWidget(self.tmn_table_scan_b)
        self.tmn_table_btns_hbox.addWidget(self.tmn_table_add_b)
        self.tmn_table_btns_hbox.addWidget(self.tmn_table_clr_b)
        self.tmn_table_vbox.addWidget(self.tmn_table)
        self.tmn_table_vbox.addLayout(self.tmn_table_btns_hbox)

        self.info_view_box = QtGui.QTextBrowser()

        self.msg_table_w = QtGui.QWidget()
        self.msg_table_vbox = QtGui.QVBoxLayout(self.msg_table_w)
        self.msg_table_vbox.setMargin(1)
        self.msg_table_vbox.setSpacing(0)
        self.msg_table = QtGui.QTableWidget()
        for count in range(5):
            self.msg_table.insertColumn(count)
        self.msg_table.setHorizontalHeaderLabels(['时间', '终端', '通道/方向', '概览', '报文'])
        self.msg_table.setColumnWidth(0, 130)
        self.msg_table.setColumnWidth(1, 110)
        self.msg_table.setColumnWidth(2, 60)
        self.msg_table.setColumnWidth(3, 200)
        self.msg_table.setColumnWidth(4, 800)
        self.msg_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers) # 表格不可编辑
        self.msg_btn_hbox = QtGui.QHBoxLayout()
        self.clr_b = QtGui.QPushButton()
        self.clr_b.setText('清空报文')
        self.msg_btn_hbox.addWidget(self.clr_b)
        self.msg_btn_hbox.addStretch(1)
        self.msg_table_vbox.addWidget(self.msg_table)
        self.msg_table_vbox.addLayout(self.msg_btn_hbox)

        self.left_vsplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.left_vsplitter.addWidget(self.tmn_list_w)
        self.left_vsplitter.addWidget(self.info_view_box)
        self.left_vsplitter.setStretchFactor(0, 1)
        self.left_vsplitter.setStretchFactor(1, 1)

        self.main_hsplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.main_hsplitter.addWidget(self.left_vsplitter)
        self.main_hsplitter.addWidget(self.msg_table_w)
        self.main_hsplitter.setStretchFactor(0, 1)
        self.main_hsplitter.setStretchFactor(1, 3)

        self.reply_link_cb = QtGui.QCheckBox()
        self.reply_link_cb.setText('维护登录/心跳')
        self.reply_link_cb.setChecked(True)
        self.always_top_cb = QtGui.QCheckBox()
        self.always_top_cb.setText('置顶')
        self.foot_hbox = QtGui.QHBoxLayout()
        self.foot_hbox.addStretch(1)
        self.foot_hbox.addWidget(self.reply_link_cb)
        self.foot_hbox.addWidget(self.always_top_cb)

        self.main_vbox = QtGui.QVBoxLayout()
        self.main_vbox.setMargin(1)
        self.main_vbox.setSpacing(1)
        # self.main_vbox.addLayout(self.btn_hbox)
        self.main_vbox.addWidget(self.main_hsplitter)
        self.main_vbox.addLayout(self.foot_hbox)
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.main_vbox)
        self.setCentralWidget(self.main_widget)
        self.resize(1000, 666)


    def re_msg_do(self, re_text, channel):
        '''recieve text'''
        re_list = common.text2list(re_text)
        msgs = common.search_msg(re_list)
        for msg in msgs:
            self.add_msg_table_row(msg, channel, '←')


    def se_msg_do(self, re_text, channel):
        '''recieve text'''
        self.add_msg_table_row(re_text, channel, '→')


    def add_tmn_table_row(self, tmn_addr='000000000001', logic_addr=0, channel='', is_checked=False):
        '''add message row'''
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
        channel_cb.setCurrentIndex(0 if channel == '串口' else\
                                    1 if channel == '前置机' else\
                                    2 if channel == '服务器' else -1)
        self.tmn_table.setCellWidget(row_pos, 3, channel_cb)

        self.tmn_remove_cb = QtGui.QPushButton()
        self.tmn_remove_cb.setText('删')
        self.tmn_table.setCellWidget(row_pos, 4, self.tmn_remove_cb)
        self.tmn_remove_cb.clicked.connect(self.tmn_table_remove)

        self.tmn_table.scrollToBottom()


    def tmn_table_remove(self):
        '''remove row in tmn table'''
        button = self.sender()
        index = self.tmn_table.indexAt(button.pos())
        self.tmn_table.removeRow(index.row())


    def add_msg_table_row(self, m_text, channel, direction):
        '''add message row'''
        trans = Translate(m_text)
        brief = trans.get_brief()
        # direction = trans.get_direction()
        client_addr = trans.get_CA()
        if client_addr != '00' and client_addr != config.COMMU.master_addr:
            print('kay, CA 不匹配')
            return
        server_addr = trans.get_SA()
        logic_addr = trans.get_logic_addr()

        # chk to add tmn addr to table
        if direction == '←':
            for row_num in range(self.tmn_table.rowCount()):
                if server_addr == self.tmn_table.item(row_num, 1).text():
                    break
            else:
                self.add_tmn_table_row(tmn_addr=server_addr, logic_addr=logic_addr,\
                                        channel=channel, is_checked=True)

        text_color = QtGui.QColor(220, 226, 241) if direction == '→' else\
                    QtGui.QColor(227, 237, 205) if direction == '←' else QtGui.QColor(255, 255, 255)
        row_pos = self.msg_table.rowCount()
        self.msg_table.insertRow(row_pos)

        item = QtGui.QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 0, item)

        item = QtGui.QTableWidgetItem('{SA}:{logic}'.format(SA=server_addr, logic=logic_addr))
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 1, item)

        item = QtGui.QTableWidgetItem(channel + direction)
        item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 2, item)

        item = QtGui.QTableWidgetItem(brief)
        if brief == '无效报文':
            item.setTextColor(QtCore.Qt.red)
        self.msg_table.setItem(row_pos, 3, item)

        item = QtGui.QTableWidgetItem(common.format_text(m_text))
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 4, item)

        self.msg_table.scrollToBottom()

        if trans.get_service() == '01' and self.is_reply_link:
            reply_apdu_text = reply.get_link_replay_apdu(trans)
            self.send_apdu(reply_apdu_text, tmn_addr=server_addr,\
                            logic_addr=logic_addr, channel=channel, C_text='01')


    def send_apdu(self, apdu_text, tmn_addr='', logic_addr=-1, channel='', C_text='43'):
        '''apdu to compelete msg to send'''
        for row in [x for x in range(self.tmn_table.rowCount())\
                        if self.tmn_table.cellWidget(x, 0).isChecked()]:
            if tmn_addr and tmn_addr != self.tmn_table.item(row, 1).text():
                continue
            if logic_addr != -1 and logic_addr != self.tmn_table.cellWidget(row, 2).value():
                continue
            if channel and channel != {0: '串口', 1: '前置机', 2: '服务器'}\
                                        .get(self.tmn_table.cellWidget(row, 3).currentIndex(), ''):
                continue

            compelete_msg = linklayer.add_linkLayer(common.text2list(apdu_text),\
                                logic_addr=self.tmn_table.cellWidget(row, 2).value(),\
                                SA_text=self.tmn_table.item(row, 1).text(),\
                                CA_text=config.COMMU.master_addr, C_text=C_text)
            send_channel = {0: '串口', 1: '前置机', 2: '服务器'}\
                            .get(self.tmn_table.cellWidget(row, 3).currentIndex(), '')
            config.COMMU.send_msg(compelete_msg, send_channel)


    def tmn_scan(self):
        '''scan terminal'''
        wild_apdu = '0501014000020000'
        compelete_msg = linklayer.add_linkLayer(common.text2list(wild_apdu),\
                                SA_text='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',\
                                SA_type=1,\
                                CA_text=config.COMMU.master_addr,\
                                C_text='43')
        print('scan msg: ', compelete_msg)
        config.COMMU.send_msg(compelete_msg)


    def trans_msg(self, row):
        '''translate massage'''
        self.pop_dialog.msg_box.setText(self.msg_table.item(row, 4).text())
        self.pop_dialog.show()
        self.pop_dialog.activateWindow()


    def clr_table(self, table):
        '''clear table widget'''
        table.setRowCount(0)


    def set_always_top(self):
        '''set_always_top'''
        window_pos = self.pos()
        if self.always_top_cb.isChecked() is True:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


    def set_reply_link(self):
        '''set_reply_link'''
        self.is_reply_link = True if self.reply_link_cb.isChecked() else False


    def show_about_window(self):
        '''show_about_window'''
        config.ABOUT_WINDOW.show()
        config.ABOUT_WINDOW.activateWindow()


    def show_commu_window(self):
        '''show_commu_window'''
        self.commu_dialog.show()
        self.commu_dialog.activateWindow()


    def show_get_service_window(self):
        '''show_get_service_window'''
        self.get_set_service_dialog.show()
        self.get_set_service_dialog.activateWindow()


    def show_general_cmd_window(self):
        '''show_general_cmd_window'''
        self.general_cmd_dialog.show()
        self.general_cmd_dialog.activateWindow()


    def show_msg_diy_window(self):
        '''msg_diy_dialog'''
        self.msg_diy_dialog.show()
        self.msg_diy_dialog.activateWindow()


    def show_remote_update_window(self):
        '''remote_update_dialog'''
        self.remote_update_dialog.show()
        self.remote_update_dialog.activateWindow()


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = MasterWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
