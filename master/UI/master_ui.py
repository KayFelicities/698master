'''master ui'''
from master import config
from PyQt4 import QtCore
from PyQt4 import QtGui
import traceback
import time
from commu import communication
from trans import common
from trans.translate import Translate
from UI.dialog_ui import TransPopDialog


class MasterWindow(QtGui.QMainWindow):
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
        self.test_b_2.clicked.connect(self.test_b_2_down)
        self.mes_table.cellDoubleClicked.connect(self.trans_msg)
        self.about_menu.triggered.connect(self.show_about_window)
        self.always_top_cb.clicked.connect(self.set_always_top)

        self.commu = communication.Serial('COM1')
        ret = self.commu.connect()
        print("connect com1: " + ret)

        self.pop_dialog = TransPopDialog()


    def setup_ui(self):
        '''set layout'''
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('详细解析')
        self.message_box = QtGui.QTextEdit()
        self.explain_box = QtGui.QTextEdit()
        self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.message_box)
        self.splitter.addWidget(self.explain_box)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 6)

        self.always_top_cb = QtGui.QCheckBox()
        self.always_top_cb.setChecked(True)
        self.always_top_cb.setText('置顶')
        self.show_level_cb = QtGui.QCheckBox()
        self.show_level_cb.setChecked(True)
        self.show_level_cb.setText('显示结构')
        self.cb_hbox = QtGui.QHBoxLayout()
        self.cb_hbox.addStretch(1)
        self.cb_hbox.addWidget(self.always_top_cb)
        self.cb_hbox.addWidget(self.show_level_cb)

        self.main_vbox = QtGui.QVBoxLayout()
        self.main_vbox.setMargin(1)
        self.main_vbox.setSpacing(1)
        self.main_vbox.addWidget(self.splitter)
        self.main_vbox.addLayout(self.cb_hbox)
        self.setLayout(self.main_vbox)
        self.resize(500, 700)
        self.setWindowIcon(QtGui.QIcon('img/698_o.png'))


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
        server_addr = trans.get_SA()
        text_color = QtGui.QColor(220, 226, 241) if direction == '→' else\
                    QtGui.QColor(227, 237, 205) if direction == '←' else QtGui.QColor(255, 255, 255)
        row_pos = self.mes_table.rowCount()
        self.mes_table.insertRow(row_pos)

        item = QtGui.QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # item.setBackgroundColor(text_color)
        self.mes_table.setItem(row_pos, 0, item)

        item = QtGui.QTableWidgetItem(server_addr)
        # item.setBackgroundColor(text_color)
        self.mes_table.setItem(row_pos, 1, item)

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
        self.pop_dialog.message_box.setText(self.mes_table.item(row, 4).text())
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
