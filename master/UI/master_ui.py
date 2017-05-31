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


class MasterWindow(QtGui.QMainWindow):
    '''serial window'''
    receive_signal = QtCore.pyqtSignal(str, str)
    send_signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(MasterWindow, self).__init__()
        self.setup_ui(self)
        self.msg_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.msg_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers) # 表格不可编辑
        self.receive_signal.connect(self.re_msg_do)
        self.send_signal.connect(self.se_msg_do)

        self.serial_combo.addItems(communication.serial_com_scan())
        self.serial_link_b.clicked.connect(self.connect_serial)
        self.serial_cut_b.clicked.connect(self.cut_serial)
        self.frontend_link_b.clicked.connect(self.connect_frontend)
        self.frontend_cut_b.clicked.connect(self.cut_frontend)
        self.server_link_b.clicked.connect(self.connect_server)
        self.server_cut_b.clicked.connect(self.cut_server)

        self.test_b.clicked.connect(self.test_b_down)
        self.clr_b.clicked.connect(self.clr_table)
        self.msg_table.cellDoubleClicked.connect(self.trans_msg)
        self.about_action.triggered.connect(self.show_about_window)
        self.always_top_cb.clicked.connect(self.set_always_top)

        self.pop_dialog = TransPopDialog()

        self.serial_handle = None
        self.frontend_handle = None
        self.server_handle = None


    def setup_ui(self, master_window):
        '''set layout'''
        self.setWindowTitle('698后台_{ver}'.format(ver=config.WINDOWS_TITLE_ADD))
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698.png')))
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

        self.serial_label = QtGui.QLabel()
        self.serial_label.setText('串口：')
        self.serial_combo = QtGui.QComboBox()
        self.serial_link_b = QtGui.QPushButton()
        self.serial_link_b.setMaximumWidth(50)
        self.serial_link_b.setText('连接')
        self.serial_cut_b = QtGui.QPushButton()
        self.serial_cut_b.setMaximumWidth(50)
        self.serial_cut_b.setText('刷新')
        self.frontend_label = QtGui.QLabel()
        self.frontend_label.setText('前置机：')
        self.frontend_box = QtGui.QLineEdit()
        self.frontend_box.setText('121.40.80.159:20084')
        self.frontend_link_b = QtGui.QPushButton()
        self.frontend_link_b.setMaximumWidth(50)
        self.frontend_link_b.setText('连接')
        self.frontend_cut_b = QtGui.QPushButton()
        self.frontend_cut_b.setMaximumWidth(50)
        self.frontend_cut_b.setText('断开')
        self.server_label = QtGui.QLabel()
        self.server_label.setText('服务器：')
        self.server_box = QtGui.QLineEdit()
        self.server_box.setText('20083')
        self.server_link_b = QtGui.QPushButton()
        self.server_link_b.setMaximumWidth(50)
        self.server_link_b.setText('启动')
        self.server_cut_b = QtGui.QPushButton()
        self.server_cut_b.setMaximumWidth(50)
        self.server_cut_b.setText('停止')
        self.commu_panel_w = QtGui.QWidget()
        self.commu_panel_w.setMinimumHeight(200)
        self.commu_panel_gbox = QtGui.QGridLayout(self.commu_panel_w)
        self.commu_panel_gbox.setMargin(1)
        self.commu_panel_gbox.setSpacing(3)
        self.commu_panel_gbox.addWidget(self.serial_label, 0, 0)
        self.commu_panel_gbox.addWidget(self.serial_combo, 1, 0)
        self.commu_panel_gbox.addWidget(self.serial_link_b, 1, 1)
        self.commu_panel_gbox.addWidget(self.serial_cut_b, 1, 2)
        self.commu_panel_gbox.addWidget(self.frontend_label, 3, 0)
        self.commu_panel_gbox.addWidget(self.frontend_box, 4, 0)
        self.commu_panel_gbox.addWidget(self.frontend_link_b, 4, 1)
        self.commu_panel_gbox.addWidget(self.frontend_cut_b, 4, 2)
        self.commu_panel_gbox.addWidget(self.server_label, 6, 0)
        self.commu_panel_gbox.addWidget(self.server_box, 7, 0)
        self.commu_panel_gbox.addWidget(self.server_link_b, 7, 1)
        self.commu_panel_gbox.addWidget(self.server_cut_b, 7, 2)
        self.commu_panel_area = QtGui.QScrollArea()
        self.commu_panel_area.setWidget(self.commu_panel_w)

        self.msg_table = QtGui.QTableWidget()
        for count in range(5):
            self.msg_table.insertColumn(count)
        self.msg_table.setHorizontalHeaderLabels(['时间', '终端', '通道/方向', '概览', '报文'])
        self.msg_table.setColumnWidth(0, 130)
        self.msg_table.setColumnWidth(1, 100)
        self.msg_table.setColumnWidth(2, 60)
        self.msg_table.setColumnWidth(3, 200)
        self.msg_table.setColumnWidth(4, 340)

        self.left_vsplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.left_vsplitter.addWidget(self.tmn_table)
        self.left_vsplitter.addWidget(self.commu_panel_area)
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


    def connect_serial(self):
        '''open serial'''
        serial_com = self.serial_combo.currentText()
        self.serial_handle = communication.Serial(serial_com)
        if self.serial_handle.connect() == 'ok':
            self.serial_link_b.setText('已连接')
            self.serial_link_b.setEnabled(False)
            self.serial_combo.setEnabled(False)
            self.serial_cut_b.setText('断开')


    def cut_serial(self):
        '''close serial'''
        if self.serial_link_b.isEnabled() is False:
            if self.serial_handle.disconnect() == 'ok':
                self.serial_link_b.setText('连接')
                self.serial_link_b.setEnabled(True)
                self.serial_combo.setEnabled(True)
                self.serial_cut_b.setText('刷新')
        else:
            self.serial_combo.clear()
            self.serial_combo.addItems(communication.serial_com_scan())


    def connect_frontend(self):
        '''open frontend'''
        frontend_addr = self.frontend_box.text().replace(' ', '')
        self.frontend_handle = communication.Frontend(frontend_addr)
        if self.frontend_handle.connect() == 'ok':
            self.frontend_link_b.setText('已连接')
            self.frontend_link_b.setEnabled(False)
            self.frontend_box.setEnabled(False)


    def cut_frontend(self):
        '''close frontend'''
        if self.frontend_handle.disconnect() == 'ok':
            self.frontend_link_b.setText('连接')
            self.frontend_link_b.setEnabled(True)
            self.frontend_box.setEnabled(True)


    def connect_server(self):
        '''open server'''
        server_port = self.server_box.text().replace(' ', '')
        self.server_handle = communication.Server(int(server_port))
        if self.server_handle.start() == 'ok':
            self.server_link_b.setText('已启动')
            self.server_link_b.setEnabled(False)
            self.server_box.setEnabled(False)


    def cut_server(self):
        '''close server'''
        if self.server_handle.stop() == 'ok':
            self.server_link_b.setText('启动')
            self.server_link_b.setEnabled(True)
            self.server_box.setEnabled(True)


    def re_msg_do(self, re_text, channel):
        '''recieve text'''
        self.add_msg_row(re_text, channel)


    def se_msg_do(self, re_text, channel):
        '''recieve text'''
        self.add_msg_row(re_text, channel)


    def add_msg_row(self, m_text, channel):
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
        if self.serial_handle:
            self.serial_handle.send_msg(test_text)
        if self.frontend_handle:
            self.frontend_handle.send_msg(test_text)
        if self.server_handle:
            self.server_handle.send_msg(test_text)


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


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = MasterWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
