'''dialog windows'''
import sys
import os
import threading
import time
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
        self.close_b.clicked.connect(self.close_window)


    def setup_ui(self):
        '''set layout'''
        self.setWindowTitle('通信控制面板')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698_o.png')))
        self.serial_label = QtGui.QLabel()
        self.serial_label.setText('串口：')
        self.serial_combo = QtGui.QComboBox()
        self.serial_baud = QtGui.QComboBox()
        self.serial_baud.addItems(('1200', '2400', '9600', '115200'))
        self.serial_baud.setCurrentIndex(2)
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
        self.close_b = QtGui.QPushButton()
        self.close_b.setText('关闭')
        self.dummy_l = QtGui.QLabel()
        self.commu_panel_gbox = QtGui.QGridLayout()
        self.commu_panel_gbox.setMargin(15)
        self.commu_panel_gbox.setSpacing(3)
        self.commu_panel_gbox.addWidget(self.serial_label, 0, 0)
        self.commu_panel_gbox.addWidget(self.serial_combo, 1, 0)
        self.commu_panel_gbox.addWidget(self.serial_baud, 1, 1)
        self.commu_panel_gbox.addWidget(self.serial_link_b, 1, 2)
        self.commu_panel_gbox.addWidget(self.serial_cut_b, 1, 3)
        self.commu_panel_gbox.addWidget(self.dummy_l, 2, 0)
        self.commu_panel_gbox.addWidget(self.frontend_label, 3, 0)
        self.commu_panel_gbox.addWidget(self.frontend_box, 4, 0, 1, 2)
        self.commu_panel_gbox.addWidget(self.frontend_link_b, 4, 2)
        self.commu_panel_gbox.addWidget(self.frontend_cut_b, 4, 3)
        self.commu_panel_gbox.addWidget(self.dummy_l, 5, 0)
        self.commu_panel_gbox.addWidget(self.server_label, 6, 0)
        self.commu_panel_gbox.addWidget(self.server_box, 7, 0, 1, 2)
        self.commu_panel_gbox.addWidget(self.server_link_b, 7, 2)
        self.commu_panel_gbox.addWidget(self.server_cut_b, 7, 3)
        self.commu_panel_gbox.addWidget(self.dummy_l, 8, 0)
        self.commu_panel_gbox.addWidget(self.close_b, 9, 0, 1, 4)
        self.setLayout(self.commu_panel_gbox)

    def connect_serial(self):
        '''open serial'''
        serial_com = self.serial_combo.currentText()
        if config.COMMU.serial_connect(serial_com, baudrate=int(self.serial_baud.currentText())) == 'ok':
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


    def close_window(self):
        '''close window'''
        self.close()


class MsgDiyDialog(QtGui.QDialog):
    '''message DIY dialog class'''
    def __init__(self):
        super(MsgDiyDialog, self).__init__()
        self.setup_ui()

        self.clr_b.clicked.connect(self.clr_box)
        self.send_b.clicked.connect(self.send_msg)

        self.msg_box.textChanged.connect(self.trans_msg)
        self.chk_valid_cb.stateChanged.connect(self.trans_msg)
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
        self.logic_addr_l = QtGui.QLabel()
        self.logic_addr_l.setText('逻辑地址:')
        self.logic_addr_box = QtGui.QSpinBox()
        self.logic_addr_box.setRange(0, 3)
        self.send_b = QtGui.QPushButton()
        self.send_b.setText('发送')
        self.send_b.setEnabled(False)
        self.btn_hbox = QtGui.QHBoxLayout()
        self.btn_hbox.addWidget(self.clr_b)
        self.btn_hbox.addStretch(1)
        self.btn_hbox.addWidget(self.logic_addr_l)
        self.btn_hbox.addWidget(self.logic_addr_box)
        self.btn_hbox.addStretch(1)
        self.btn_hbox.addWidget(self.send_b)

        self.msg_box = QtGui.QTextEdit()
        self.explain_box = QtGui.QTextEdit()
        self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.msg_box)
        self.splitter.addWidget(self.explain_box)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 6)

        self.chk_valid_cb = QtGui.QCheckBox()
        self.chk_valid_cb.setChecked(True)
        self.chk_valid_cb.setText('检查合法性')
        self.always_top_cb = QtGui.QCheckBox()
        self.always_top_cb.setChecked(True)
        self.always_top_cb.setText('置顶')
        self.show_level_cb = QtGui.QCheckBox()
        self.show_level_cb.setChecked(True)
        self.show_level_cb.setText('显示结构')
        self.cb_hbox = QtGui.QHBoxLayout()
        self.cb_hbox.addStretch(1)
        self.cb_hbox.addWidget(self.chk_valid_cb)
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
        if self.chk_valid_cb.isChecked():
            self.send_b.setEnabled(True if trans.is_success else False)
        else:
            self.send_b.setEnabled(True)


    def send_msg(self):
        '''send message'''
        msg_text = self.msg_box.toPlainText()
        logic_addr = self.logic_addr_box.value()
        config.MASTER_WINDOW.se_apdu_signal.emit(msg_text, logic_addr, 'all')


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


class RemoteUpdateDialog(QtGui.QDialog):
    '''remote update window'''
    update_signal = QtCore.pyqtSignal(int, int)
    def __init__(self):
        super(RemoteUpdateDialog, self).__init__()
        self.setup_ui()
        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.file_open_b.clicked.connect(self.open_file)
        self.block_size_combo.currentIndexChanged.connect(self.show_block_num)
        self.start_update_b.clicked.connect(self.start_update)
        self.stop_update_b.clicked.connect(self.stop_update)

        self.update_signal.connect(self.update_proc)

        self.is_updating = False


    def setup_ui(self):
        '''set layout'''
        self.setWindowTitle('远程文件升级')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698.png')))

        self.file_label = QtGui.QLabel()
        self.file_label.setText('文件:')
        self.file_open_b = QtGui.QPushButton()
        self.file_open_b.setMaximumWidth(50)
        self.file_open_b.setText('打开...')
        self.file_path_box = QtGui.QLineEdit()
        self.file_path_box.setEnabled(False)
        self.file_path_box.setPlaceholderText('请选择或拖入文件')

        self.logic_addr_l = QtGui.QLabel()
        self.logic_addr_l.setText('逻辑地址:')
        self.logic_addr_box = QtGui.QSpinBox()
        self.logic_addr_box.setRange(0, 3)

        self.block_size_label = QtGui.QLabel()
        self.block_size_label.setText('传输块大小:')
        self.block_size_combo = QtGui.QComboBox()
        self.block_size_combo.addItem('128字节')
        self.block_size_combo.addItem('256字节')
        self.block_size_combo.addItem('512字节')
        self.block_size_combo.addItem('1024字节')

        self.file_size_label = QtGui.QLabel()
        self.file_size_label.setText('文件大小')
        self.file_size_num_label = QtGui.QLabel()
        self.file_size_num_label.setText('0字节')
        self.block_label = QtGui.QLabel()
        self.block_label.setText('共计')
        self.block_num_label = QtGui.QLabel()
        self.block_num_label.setText('0包')

        self.start_update_b = QtGui.QPushButton()
        self.start_update_b.setText('开始升级')
        self.start_update_b.setEnabled(False)
        self.stop_update_b = QtGui.QPushButton()
        self.stop_update_b.setText('停止')
        self.stop_update_b.setEnabled(False)

        self.dummy_l = QtGui.QLabel()
        self.remote_update_gbox = QtGui.QGridLayout()
        self.remote_update_gbox.setMargin(15)
        self.remote_update_gbox.setSpacing(3)
        self.remote_update_gbox.addWidget(self.file_label, 1, 0)
        self.remote_update_gbox.addWidget(self.file_open_b, 1, 1)

        self.remote_update_gbox.addWidget(self.file_path_box, 2, 0, 1, 5)

        self.remote_update_gbox.addWidget(self.dummy_l, 3, 0)

        self.remote_update_gbox.addWidget(self.logic_addr_l, 4, 0)
        self.remote_update_gbox.addWidget(self.logic_addr_box, 4, 1)
        self.remote_update_gbox.addWidget(self.block_size_label, 4, 3)
        self.remote_update_gbox.addWidget(self.block_size_combo, 4, 4)

        self.remote_update_gbox.addWidget(self.dummy_l, 5, 0)

        self.remote_update_gbox.addWidget(self.file_size_label, 6, 0)
        self.remote_update_gbox.addWidget(self.file_size_num_label, 6, 1)
        self.remote_update_gbox.addWidget(self.block_label, 6, 3)
        self.remote_update_gbox.addWidget(self.block_num_label, 6, 4)

        self.remote_update_gbox.addWidget(self.dummy_l, 7, 0)

        self.remote_update_gbox.addWidget(self.start_update_b, 8, 0, 1, 4)
        self.remote_update_gbox.addWidget(self.stop_update_b, 8, 4)
        self.setLayout(self.remote_update_gbox)


    def dragEnterEvent(self, event):
        '''drag'''
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        '''drag'''
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        '''drop file'''
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.open_file(links[0])
        else:
            event.ignore()


    def open_file(self, filepath=''):
        '''open file'''
        if not filepath:
            filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', '*.*')
        if filepath:
            print('filepath: ', filepath)
            file_type = filepath.split('.')[-1]
            if file_type not in ['sp4']:
                reply = QtGui.QMessageBox.question(self, '警告', '确定升级非sp4文件吗？',\
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply != QtGui.QMessageBox.Yes:
                    return
            self.file_path_box.setText(filepath)
            file_size = os.path.getsize(filepath)
            self.file_size_num_label.setText('{size}字节'.format(size=file_size))
            self.show_block_num()
            self.start_update_b.setEnabled(True)


    def show_block_num(self):
        '''calc file info'''
        file_size = int(self.file_size_num_label.text().replace('字节', ''))
        block_size = int(self.block_size_combo.currentText().replace('字节', ''))
        block_num = file_size // block_size + (0 if file_size % block_size == 0 else 1)
        self.block_num_label.setText('{num}包'.format(num=block_num))


    def start_update(self):
        '''start update'''
        filepath = self.file_path_box.text()
        logic_addr = self.logic_addr_box.value()
        block_size = int(self.block_size_combo.currentText().replace('字节', ''))
        if filepath:
            threading.Thread(target=self.send_file,\
                        args=(filepath, logic_addr, block_size)).start()


    def send_file(self, filepath, logic_addr, block_size):
        '''send file thread'''
        start_apdu_text = '070100 f0010700 0203 0206 0a00 0a00 06 {filesize:08X}\
                        0403e0 0a00 1600 12 {blocksize:04X} 0202 1600 0900 00'\
                        .format(filesize=os.path.getsize(filepath), blocksize=block_size)
        config.MASTER_WINDOW.se_apdu_signal.emit(start_apdu_text, logic_addr, 'all')
        time.sleep(6)
        self.start_update_b.setEnabled(False)
        self.stop_update_b.setEnabled(True)
        self.is_updating = True

        file_size = os.path.getsize(filepath)
        block_num = file_size // block_size + (0 if file_size % block_size == 0 else 1)
        with open(filepath, 'rb') as file:
            file_text = file.read(file_size)
            file_text = ''.join(['%02X'%x for x in file_text])
            text_list = [file_text[x: x + block_size*2] for x in range(0, len(file_text), block_size*2)]
            for block_no, block_text in enumerate(text_list):
                send_len = len(block_text)/2
                send_apdu_text = '0701{piid:02X} f0010800 0202 12{blockno:04X} 09'\
                                    .format(piid=block_no % 64, blockno=block_no)\
                                    + ('%02X'%send_len if send_len < 128\
                                        else '82%04X'%send_len) + block_text + '00'
                config.MASTER_WINDOW.se_apdu_signal.emit(send_apdu_text, logic_addr, 'all')
                self.update_signal.emit(block_no + 1, block_num)
                time.sleep(2)
                if not self.is_updating:
                    break
        self.stop_update_b.setEnabled(False)
        self.start_update_b.setEnabled(True)
        self.start_update_b.setText('开始升级')
        print('send file thread quit')


    def update_proc(self, block_no, block_num):
        '''update proc'''
        self.start_update_b.setText('升级中({no}/{all})'.format(no=block_no + 1, all=block_num))


    def stop_update(self):
        '''stop update'''
        self.is_updating = False


    def close_window(self):
        '''close window'''
        self.close()


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = RemoteUpdateDialog()
    dialog.show()
    APP.exec_()
    os._exit(0)
