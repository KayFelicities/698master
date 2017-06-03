'''dialog windows'''
import sys
import os
from PyQt4 import QtGui, QtCore
from master.trans import translate, linklayer
import master.trans.common as commonfun
from master import config
from master.commu import communication


class TransPopDialog(QtGui.QDialog):
    '''translate window'''
    def __init__(self):
        super(TransPopDialog, self).__init__()
        self.setup_ui()
        self.msg_box.textChanged.connect(self.trans_msg)
        self.show_level_cb.stateChanged.connect(self.trans_msg)
        self.always_top_cb.stateChanged.connect(self.set_always_top)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)


    def setup_ui(self):
        '''set layout'''
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('详细解析')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698_o.png')))
        self.msg_box = QtGui.QTextEdit()
        self.explain_box = QtGui.QTextEdit()
        self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.msg_box)
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


    def trans_msg(self):
        '''translate'''
        msg_text = self.msg_box.toPlainText()
        trans = translate.Translate(msg_text)
        brief = trans.get_brief()
        full = trans.get_full(self.show_level_cb.isChecked())
        self.explain_box.setText(r'<b>【概览】</b><p>%s</p><hr><b>【完整】</b>%s'%(brief, full))


    def set_always_top(self):
        '''set_always_top'''
        window_pos = self.pos()
        if self.always_top_cb.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


class CommuDialog(QtGui.QDialog):
    '''communication config window'''
    def __init__(self):
        super(CommuDialog, self).__init__()
        self.setup_ui()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.serial_combo.addItems(communication.serial_com_scan())
        self.serial_link_b.clicked.connect(self.connect_serial)
        self.serial_cut_b.clicked.connect(self.cut_serial)
        self.frontend_link_b.clicked.connect(self.connect_frontend)
        self.frontend_cut_b.clicked.connect(self.cut_frontend)
        self.server_link_b.clicked.connect(self.connect_server)
        self.server_cut_b.clicked.connect(self.cut_server)


    def setup_ui(self):
        '''set layout'''
        self.setWindowTitle('通信控制面板')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698_o.png')))
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
        self.dummy_l = QtGui.QLabel()
        self.commu_panel_gbox = QtGui.QGridLayout()
        self.commu_panel_gbox.setMargin(15)
        self.commu_panel_gbox.setSpacing(3)
        self.commu_panel_gbox.addWidget(self.serial_label, 0, 0)
        self.commu_panel_gbox.addWidget(self.serial_combo, 1, 0)
        self.commu_panel_gbox.addWidget(self.serial_link_b, 1, 1)
        self.commu_panel_gbox.addWidget(self.serial_cut_b, 1, 2)
        self.commu_panel_gbox.addWidget(self.dummy_l, 2, 0)
        self.commu_panel_gbox.addWidget(self.frontend_label, 3, 0)
        self.commu_panel_gbox.addWidget(self.frontend_box, 4, 0)
        self.commu_panel_gbox.addWidget(self.frontend_link_b, 4, 1)
        self.commu_panel_gbox.addWidget(self.frontend_cut_b, 4, 2)
        self.commu_panel_gbox.addWidget(self.dummy_l, 5, 0)
        self.commu_panel_gbox.addWidget(self.server_label, 6, 0)
        self.commu_panel_gbox.addWidget(self.server_box, 7, 0)
        self.commu_panel_gbox.addWidget(self.server_link_b, 7, 1)
        self.commu_panel_gbox.addWidget(self.server_cut_b, 7, 2)
        self.setLayout(self.commu_panel_gbox)

    def connect_serial(self):
        '''open serial'''
        serial_com = self.serial_combo.currentText()
        if config.COMMU.serial_connect(serial_com) == 'ok':
            self.serial_link_b.setText('已连接')
            self.serial_link_b.setEnabled(False)
            self.serial_combo.setEnabled(False)
            self.serial_cut_b.setText('断开')


    def cut_serial(self):
        '''close serial'''
        if self.serial_link_b.isEnabled() is False:
            if config.COMMU.serial_disconnect() == 'ok':
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
        if config.COMMU.frontend_connect(frontend_addr) == 'ok':
            self.frontend_link_b.setText('已连接')
            self.frontend_link_b.setEnabled(False)
            self.frontend_box.setEnabled(False)


    def cut_frontend(self):
        '''close frontend'''
        if config.COMMU.frontend_disconnect() == 'ok':
            self.frontend_link_b.setText('连接')
            self.frontend_link_b.setEnabled(True)
            self.frontend_box.setEnabled(True)


    def connect_server(self):
        '''open server'''
        server_port = self.server_box.text().replace(' ', '')
        if config.COMMU.server_start(int(server_port)) == 'ok':
            self.server_link_b.setText('已启动')
            self.server_link_b.setEnabled(False)
            self.server_box.setEnabled(False)


    def cut_server(self):
        '''close server'''
        if config.COMMU.server_stop() == 'ok':
            self.server_link_b.setText('启动')
            self.server_link_b.setEnabled(True)
            self.server_box.setEnabled(True)


class MsgDiyDialog(QtGui.QDialog):
    '''message DIY dialog class'''
    def __init__(self):
        super(MsgDiyDialog, self).__init__()
        self.setup_ui()

        self.clr_b.clicked.connect(self.clr_box)
        self.send_b.clicked.connect(self.send_msg)

        self.msg_box.textChanged.connect(self.trans_msg)
        self.show_level_cb.stateChanged.connect(self.trans_msg)
        self.always_top_cb.stateChanged.connect(self.set_always_top)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)


    def setup_ui(self):
        '''set layout'''
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('自定义报文')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698.png')))

        self.clr_b = QtGui.QPushButton()
        self.clr_b.setText('清空')
        self.logic_addr_box = QtGui.QLineEdit()
        self.logic_addr_box.setText('0')
        self.send_b = QtGui.QPushButton()
        self.send_b.setText('发送')
        self.btn_hbox = QtGui.QHBoxLayout()
        self.btn_hbox.addWidget(self.clr_b)
        self.btn_hbox.addWidget(self.logic_addr_box)
        self.btn_hbox.addWidget(self.send_b)

        self.msg_box = QtGui.QTextEdit()
        self.explain_box = QtGui.QTextEdit()
        self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.msg_box)
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
        self.main_vbox.addLayout(self.btn_hbox)
        self.main_vbox.addWidget(self.splitter)
        self.main_vbox.addLayout(self.cb_hbox)
        self.setLayout(self.main_vbox)
        self.resize(500, 700)


    def trans_msg(self):
        '''translate'''
        msg_text = self.msg_box.toPlainText()
        trans = translate.Translate(msg_text)
        full = trans.get_full(self.show_level_cb.isChecked())
        self.explain_box.setText(r'%s'%full)


    def send_msg(self):
        '''send message'''
        msg_text = self.msg_box.toPlainText()
        config.COMMU.send_msg(linklayer.add_linkLayer(commonfun.text2list(msg_text), SA_text='17370000'))


    def clr_box(self):
        '''clear input&output box'''
        self.msg_box.setText('')

    def set_always_top(self):
        '''set_always_top'''
        window_pos = self.pos()
        if self.always_top_cb.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = CommuDialog()
    dialog.show()
    APP.exec_()
    os._exit(0)
