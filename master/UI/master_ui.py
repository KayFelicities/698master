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
from master.UI.dialog_ui import TransPopDialog, CommuDialog


class MasterWindow(QtGui.QMainWindow):
    '''serial window'''
    receive_signal = QtCore.pyqtSignal(str, str)
    send_signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(MasterWindow, self).__init__()
        self.setup_ui(self)
        self.receive_signal.connect(self.re_msg_do)
        self.send_signal.connect(self.se_msg_do)

        self.test_b.clicked.connect(self.test_b_down)
        self.clr_b.clicked.connect(self.clr_table)
        self.msg_table.cellDoubleClicked.connect(self.trans_msg)
        self.about_action.triggered.connect(self.show_about_window)
        self.link_action.triggered.connect(self.show_commu_window)
        self.always_top_cb.clicked.connect(self.set_always_top)

        self.pop_dialog = TransPopDialog()
        self.commu_dialog = CommuDialog()

        config.COMMU = communication.CommuPanel()



    def setup_ui(self, master_window):
        '''set layout'''
        self.setWindowTitle('698后台_{ver}'.format(ver=config.WINDOWS_TITLE_ADD))
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698.png')))
        self.menubar = self.menuBar()
        self.about_action = QtGui.QAction('&关于', self)
        self.link_action = QtGui.QAction('&通信设置', self)
        self.link_action.setShortcut('F1')
        self.commu_menu = self.menubar.addMenu('&通信')
        self.commu_menu.addAction(self.link_action)
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
        for count in range(3):
            self.tmn_table.insertColumn(count)
        self.tmn_table.setHorizontalHeaderLabels(['', '终端地址', '通道'])
        self.tmn_table.setColumnWidth(0, 20)
        self.tmn_table.setColumnWidth(1, 120)
        self.tmn_table.setColumnWidth(2, 70)
        self.tmn_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tmn_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)

        self.info_view_box = QtGui.QTextBrowser()

        self.msg_table = QtGui.QTableWidget()
        for count in range(5):
            self.msg_table.insertColumn(count)
        self.msg_table.setHorizontalHeaderLabels(['时间', '终端', '通道/方向', '概览', '报文'])
        self.msg_table.setColumnWidth(0, 130)
        self.msg_table.setColumnWidth(1, 100)
        self.msg_table.setColumnWidth(2, 60)
        self.msg_table.setColumnWidth(3, 200)
        self.msg_table.setColumnWidth(4, 800)
        self.msg_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers) # 表格不可编辑

        self.left_vsplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.left_vsplitter.addWidget(self.tmn_table)
        self.left_vsplitter.addWidget(self.info_view_box)
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
        self.setCentralWidget(self.main_widget)
        self.resize(1000, 666)


    def re_msg_do(self, re_text, channel):
        '''recieve text'''
        self.add_msg_table_row(re_text, channel)


    def se_msg_do(self, re_text, channel):
        '''recieve text'''
        self.add_msg_table_row(re_text, channel)


    def add_tmn_table_row(self, tmn_addr, channel):
        '''add message row'''
        row_pos = self.tmn_table.rowCount()
        self.tmn_table.insertRow(row_pos)

        tmn_cb = QtGui.QCheckBox()
        tmn_cb.setChecked(True)
        self.tmn_table.setCellWidget(row_pos, 0, tmn_cb)

        item = QtGui.QTableWidgetItem(tmn_addr)
        self.tmn_table.setItem(row_pos, 1, item)

        item = QtGui.QTableWidgetItem(channel)
        self.tmn_table.setItem(row_pos, 2, item)

        self.tmn_table.scrollToBottom()


    def add_msg_table_row(self, m_text, channel):
        '''add message row'''
        trans = Translate(m_text)
        brief = trans.get_brief()
        direction = trans.get_direction()
        server_addr = trans.get_SA()

        # chk to add tmn addr to table
        if direction == '←':
            for row_num in range(self.tmn_table.rowCount()):
                if server_addr == self.tmn_table.item(row_num, 1).text():
                    break
            else:
                self.add_tmn_table_row(server_addr, channel)

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
        config.COMMU.send_msg(test_text)


    def trans_msg(self, row):
        '''translate massage'''
        self.pop_dialog.message_box.setText(self.msg_table.item(row, 4).text())
        self.pop_dialog.show()
        self.pop_dialog.activateWindow()


    def clr_table(self):
        '''clear table widget'''
        self.msg_table.setRowCount(0)


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


    def show_commu_window(self):
        '''show_commu_window'''
        self.commu_dialog.show()
        # config.TRANS_WINDOW.show()


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = MasterWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
