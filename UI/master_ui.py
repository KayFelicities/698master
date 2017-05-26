'''master ui'''
import config
from PyQt4 import QtCore
from PyQt4 import QtGui
from UI.master_window import Ui_MasterWindow
import traceback
import time
from commu import communication
from trans import common
from trans.translate import Translate
from UI.dialog_ui import TransPopDialog


class MasterWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_MasterWindow):
    '''serial window'''
    receive_signal = QtCore.pyqtSignal(str, str)
    send_signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(MasterWindow, self).__init__()
        self.setupUi(self)
        self.create_tables()
        self.setWindowTitle('698后台' + config.WINDOWS_TITLE_ADD)
        self.receive_signal.connect(self.re_message)
        self.send_signal.connect(self.se_message)
        self.test_b.clicked.connect(self.test_b_down)
        self.about_menu.triggered.connect(self.show_about_window)
        self.always_top_cb.clicked.connect(self.set_always_top)

        self.commu = communication.Serial('COM1')
        ret = self.commu.connect()
        print("connect com1: " + ret)

        self.pop = TransPopDialog()


    def create_tables(self):
        '''create tables'''
        for count in range(5):
            self.mes_table.insertColumn(count)
        self.mes_table.setHorizontalHeaderLabels(['时间', '终端', '通道/方向', '概览', '报文'])
        self.mes_table.setColumnWidth(0, 130)
        self.mes_table.setColumnWidth(1, 100)
        self.mes_table.setColumnWidth(2, 60)
        self.mes_table.setColumnWidth(3, 200)
        self.mes_table.setColumnWidth(4, 340)


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
        text_color = QtGui.QColor(220, 226, 241) if direction == '→' else\
                    QtGui.QColor(227, 237, 205) if direction == '←' else QtGui.QColor(255, 255, 255)
        row_pos = self.mes_table.rowCount()
        self.mes_table.insertRow(row_pos)

        item = QtGui.QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # item.setBackgroundColor(text_color)
        self.mes_table.setItem(row_pos, 0, item)

        item = QtGui.QTableWidgetItem(channel + direction)
        item.setBackgroundColor(text_color)
        self.mes_table.setItem(row_pos, 2, item)

        item = QtGui.QTableWidgetItem(brief)
        # item.setBackgroundColor(text_color)
        self.mes_table.setItem(row_pos, 3, item)

        item = QtGui.QTableWidgetItem(common.format_text(m_text))
        # item.setBackgroundColor(text_color)
        self.mes_table.setItem(row_pos, 4, item)

        self.mes_table.scrollToBottom()


    def test_b_down(self):
        '''test'''
        test_text = '682100434FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA10CC1C05010140000200007D1B16'
        self.send_mess(test_text)


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
        # config.ABOUT_WINDOW.show()
        # config.TRANS_WINDOW.show()
        self.pop.show()
