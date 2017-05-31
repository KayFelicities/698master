'''master ui'''
import sys
import os
from master import config
from PyQt4 import QtCore, QtGui
import traceback
import time
from master.commu import communication
from master.trans import common
from master.trans.translate import Translate
from master.UI.dialog_ui import TransPopDialog


class MasterWindowLayout(QtGui.QMainWindow):
    '''master window layout'''
    def setup_ui(self, master_window):
        '''set layout'''
        master_window.setWindowTitle('698后台_{ver}'.format(ver=config.WINDOWS_TITLE_ADD))
        master_window.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698.png')))
        self.menubar = self.menuBar()
        self.about_action = QtGui.QAction('&关于', self)
        self.help_menu = self.menubar.addMenu('&帮助')
        self.help_menu.addAction(self.about_action)

        self.test_b = QtGui.QPushButton()
        self.test_b.setText('test')
        self.test_b_2 = QtGui.QPushButton()
        self.test_b_2.setText('test')
        self.clr_b = QtGui.QPushButton()
        self.clr_b.setText('清空')
        self.btn_hbox = QtGui.QHBoxLayout()
        self.btn_hbox.addWidget(self.test_b)
        self.btn_hbox.addWidget(self.test_b_2)
        self.btn_hbox.addWidget(self.clr_b)

        self.tmn_table = QtGui.QTableWidget()
        self.info_browser = QtGui.QTextBrowser()
        self.msg_table = QtGui.QTableWidget()

        self.left_vsplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.left_vsplitter.addWidget(self.tmn_table)
        self.left_vsplitter.addWidget(self.info_browser)
        self.left_vsplitter.setStretchFactor(0, 1)
        self.left_vsplitter.setStretchFactor(1, 1)

        self.main_hsplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.main_hsplitter.addWidget(self.left_vsplitter)
        self.main_hsplitter.addWidget(self.msg_table)
        self.main_hsplitter.setStretchFactor(0, 1)
        self.main_hsplitter.setStretchFactor(1, 3)

        self.always_top_cb = QtGui.QCheckBox()
        self.always_top_cb.setChecked(True)
        self.always_top_cb.setText('置顶')
        self.foot_hbox = QtGui.QHBoxLayout()
        self.foot_hbox.addStretch(1)
        self.foot_hbox.addWidget(self.always_top_cb)

        self.main_vbox = QtGui.QVBoxLayout()
        self.main_vbox.setMargin(1)
        self.main_vbox.setSpacing(1)
        self.main_vbox.addLayout(self.btn_hbox)
        self.main_vbox.addWidget(self.main_hsplitter)
        self.main_vbox.addLayout(self.foot_hbox)
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.main_vbox)
        master_window.setCentralWidget(self.main_widget)
        master_window.resize(1000, 666)

        self.create_msg_tables()


    def create_msg_tables(self):
        '''create tables'''
        for count in range(5):
            self.msg_table.insertColumn(count)
        self.msg_table.setHorizontalHeaderLabels(['时间', '终端', '通道/方向', '概览', '报文'])
        self.msg_table.setColumnWidth(0, 130)
        self.msg_table.setColumnWidth(1, 100)
        self.msg_table.setColumnWidth(2, 60)
        self.msg_table.setColumnWidth(3, 200)
        self.msg_table.setColumnWidth(4, 340)


class MasterWindow(MasterWindowLayout, QtGui.QMainWindow):
    '''serial window'''
    receive_signal = QtCore.pyqtSignal(str, str)
    send_signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(MasterWindow, self).__init__()
        self.setup_ui(self)
        self.msg_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers) # 表格不可编辑
        self.receive_signal.connect(self.re_message)
        self.send_signal.connect(self.se_message)
        self.test_b.clicked.connect(self.test_b_down)
        self.test_b_2.clicked.connect(self.test_b_2_down)
        self.msg_table.cellDoubleClicked.connect(self.trans_msg)
        self.about_action.triggered.connect(self.show_about_window)
        self.always_top_cb.clicked.connect(self.set_always_top)

        self.commu = communication.Serial('COM1')
        ret = self.commu.connect()
        print("connect com1: " + ret)

        self.pop_dialog = TransPopDialog()


    def open_serial(self):
        '''open serial'''


    def re_message(self, re_text, channel):
        '''recieve text'''
        self.add_mes_row(re_text, channel)


    def se_message(self, re_text, channel):
        '''recieve text'''
        self.add_mes_row(re_text, channel)


    def send_mess(self, se_text):
        '''test'''
        self.commu.send_mes(se_text)


    def add_mes_row(self, m_text, channel):
        '''add message row'''
        trans = Translate(m_text)
        brief = trans.get_brief()
        direction = trans.get_direction()
        server_addr = trans.get_SA()
        text_color = QtGui.QColor(220, 226, 241) if direction == '→' else\
                    QtGui.QColor(227, 237, 205) if direction == '←' else QtGui.QColor(255, 255, 255)
        row_pos = self.msg_table.rowCount()
        self.msg_table.insertRow(row_pos)

        item = QtGui.QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 0, item)

        item = QtGui.QTableWidgetItem(server_addr)
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 1, item)

        item = QtGui.QTableWidgetItem(channel + direction)
        item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 2, item)

        item = QtGui.QTableWidgetItem(brief)
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 3, item)

        item = QtGui.QTableWidgetItem(common.format_text(m_text))
        # item.setBackgroundColor(text_color)
        self.msg_table.setItem(row_pos, 4, item)

        self.msg_table.scrollToBottom()


    def test_b_down(self):
        '''test'''
        test_text = '682100434FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA10CC1C05010140000200007D1B16'
        self.send_mess(test_text)

    def test_b_2_down(self):
        '''test'''
        test_text = '68 7E 00 C3 03 01 00 00 00 10 31 7A 85 02 01 03 45 00 02 00 01 02 0C\
                     16 00 16 00 16 00 16 00 01 00 0A 06 74 65 73 74 31 32 0A 06 75 73 65\
                     72 31 32 0A 05 70 77 31 32 33 09 04 00 00 00 00 12 01 00 11 FC 12 01\
                     2C 45 00 03 00 01 01 01 02 02 09 04 79 28 50 9F 12 4E 73 45 00 04 00\
                     01 02 03 0A 06 01 02 03 04 05 06 01 01 0A 06 01 02 03 04 05 06 01 01\
                     0A 06 05 06 07 04 05 06 00 00 DC F5 16'
        self.send_mess(test_text)


    def trans_msg(self, row):
        '''translate massage'''
        self.pop_dialog.message_box.setText(self.msg_table.item(row, 4).text())
        self.pop_dialog.show()
        self.pop_dialog.activateWindow()

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


    def show_about_window(self):
        '''show_about_window'''
        config.ABOUT_WINDOW.show()
        # config.TRANS_WINDOW.show()


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = MasterWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
