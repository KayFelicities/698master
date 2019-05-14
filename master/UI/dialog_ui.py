"""dialog windows"""
import sys
import os
import threading
import time
import re
import random
from master.UI import ui_setup
from master.trans import translate, linklayer
from master.trans import common
from master import config
from master.commu import communication
from master.datas import service_data
from master.trans import loadtype
from master.others import master_config
if config.IS_USE_PYSIDE:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore


class TransPopDialog(QtGui.QDialog, ui_setup.TransPopDialogUi):
    """translate window"""
    def __init__(self):
        super(TransPopDialog, self).__init__()
        self.setup_ui()
        self.show_level_cb.setChecked(True)

        self.msg_box.textChanged.connect(self.trans_msg)
        self.show_level_cb.stateChanged.connect(self.trans_msg)
        self.show_dtype_cb.stateChanged.connect(self.trans_msg)
        self.always_top_cb.stateChanged.connect(self.set_always_top)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)


    def trans_msg(self):
        """translate"""
        msg_text = self.msg_box.toPlainText()
        trans = translate.Translate(msg_text)
        brief = trans.get_brief()
        full = trans.get_full(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        self.explain_box.setText(r'<b>【概览】</b><p>%s</p><hr><b>【完整】</b>%s'%(brief, full))

    def set_always_top(self):
        """set_always_top"""
        window_pos = self.pos()
        if self.always_top_cb.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


class CommuDialog(QtGui.QDialog, ui_setup.CommuDialogUi):
    """communication config window"""
    def __init__(self):
        super(CommuDialog, self).__init__()
        self.setup_ui()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.master_addr_change_b.clicked.connect(lambda: self.master_addr_box.setText('%02X'%random.randint(0, 255)))
        self.master_addr_box.textChanged.connect(self.set_master_addr)
        self.serial_combo.addItems(communication.serial_com_scan())
        self.serial_link_b.clicked.connect(self.connect_serial)
        self.serial_cut_b.clicked.connect(self.cut_serial)
        self.frontend_link_b.clicked.connect(self.connect_frontend)
        self.frontend_cut_b.clicked.connect(self.cut_frontend)
        self.server_link_b.clicked.connect(self.connect_server)
        self.server_cut_b.clicked.connect(self.cut_server)
        self.close_b.clicked.connect(self.close)

        # apply config
        apply_config = master_config.MasterConfig()
        try:
            index = communication.serial_com_scan().index(apply_config.get_serial_com())
            self.serial_combo.setCurrentIndex(index)
        except ValueError:
            pass
        self.serial_baud.setCurrentIndex(apply_config.get_serial_baud_index())
        self.master_addr_box.setText(apply_config.get_master_addr())
        self.frontend_box.setText(apply_config.get_frontend_ip())
        self.server_box.setText(apply_config.get_server_port())
        self.master_addr_filter_cb.setChecked(True)

        self.close_b.setFocus()

        self.is_serial_connect = False
        self.is_frontend_connect = False
        self.is_server_connect = False


    def set_master_addr(self):
        """set_master_addr"""
        config.COMMU.master_addr = self.master_addr_box.text()
        config.IS_FILETER_CA = self.master_addr_filter_cb.isChecked()


    def connect_serial(self):
        """open serial"""
        serial_com = self.serial_combo.currentText()
        if config.COMMU.serial_connect(serial_com, baudrate=int(self.serial_baud.currentText())) == 'ok':
            self.serial_link_b.setText('已连接')
            self.serial_link_b.setEnabled(False)
            self.serial_combo.setEnabled(False)
            self.serial_baud.setEnabled(False)
            self.serial_cut_b.setText('断开')
            self.is_serial_connect = True
            config.MASTER_WINDOW.set_b_green(config.MASTER_WINDOW.serial_b)
        else:
            self.serial_link_b.setText('失败')
            config.MASTER_WINDOW.set_b_yellow(config.MASTER_WINDOW.serial_b)


    def cut_serial(self):
        """close serial"""
        if self.serial_link_b.isEnabled() is False:
            if config.COMMU.serial_disconnect() == 'ok':
                self.serial_link_b.setText('连接')
                self.serial_link_b.setEnabled(True)
                self.serial_combo.setEnabled(True)
                self.serial_baud.setEnabled(True)
                self.serial_cut_b.setText('刷新')
        else:
            self.serial_combo.clear()
            self.serial_combo.addItems(communication.serial_com_scan())
            self.serial_link_b.setText('连接')
        self.is_serial_connect = False
        config.MASTER_WINDOW.set_b_red(config.MASTER_WINDOW.serial_b)


    def connect_frontend(self):
        """open frontend"""
        frontend_addr = self.frontend_box.text().replace(' ', '')
        if config.COMMU.frontend_connect(frontend_addr) == 'ok':
            self.frontend_link_b.setText('已连接')
            self.frontend_link_b.setEnabled(False)
            self.frontend_box.setEnabled(False)
            self.is_frontend_connect = True
            config.MASTER_WINDOW.set_b_green(config.MASTER_WINDOW.frontend_b)
        else:
            self.frontend_link_b.setText('失败')
            config.MASTER_WINDOW.set_b_yellow(config.MASTER_WINDOW.frontend_b)


    def cut_frontend(self):
        """close frontend"""
        if config.COMMU.frontend_disconnect() == 'ok':
            self.frontend_link_b.setText('连接')
            self.frontend_link_b.setEnabled(True)
            self.frontend_box.setEnabled(True)
        self.is_frontend_connect = False
        config.MASTER_WINDOW.set_b_red(config.MASTER_WINDOW.frontend_b)


    def connect_server(self):
        """open server"""
        server_port = self.server_box.text().replace(' ', '')
        if config.COMMU.server_start(int(server_port)) == 'ok':
            self.server_link_b.setText('已启动')
            self.server_link_b.setEnabled(False)
            self.server_box.setEnabled(False)
            self.is_server_connect = True
            config.MASTER_WINDOW.set_b_green(config.MASTER_WINDOW.server_b)
        else:
            self.server_link_b.setText('失败')
            config.MASTER_WINDOW.set_b_yellow(config.MASTER_WINDOW.server_b)


    def cut_server(self):
        """close server"""
        if config.COMMU.server_stop() == 'ok':
            self.server_link_b.setText('启动')
            self.server_link_b.setEnabled(True)
            self.server_box.setEnabled(True)
        self.is_server_connect = False
        config.MASTER_WINDOW.set_b_red(config.MASTER_WINDOW.server_b)


    def closeEvent(self, event):
        """close event"""
        self.set_master_addr()
        # save config
        save_config = master_config.MasterConfig()
        save_config.set_serial_com(self.serial_combo.currentText())
        save_config.set_serial_band_index(self.serial_baud.currentIndex())
        save_config.set_master_addr(self.master_addr_box.text())
        save_config.set_serial_baud_index(self.serial_baud.currentIndex())
        save_config.set_frontend_ip(self.frontend_box.text())
        save_config.set_server_port(self.server_box.text())
        save_config.commit()
        event.accept()


class ApduDiyDialog(QtGui.QDialog, ui_setup.ApduDiyDialogUi):
    """apdu DIY dialog class"""
    def __init__(self):
        super(ApduDiyDialog, self).__init__()
        self.setup_ui()

        self.send_b.setEnabled(False)
        self.chk_valid_cb.setChecked(True)
        self.show_level_cb.setChecked(True)

        self.se_clr_b.clicked.connect(lambda: self.se_msg_box.clear() or self.se_msg_box.setFocus())
        self.re_clr_b.clicked.connect(lambda: self.re_msg_box.clear())
        self.send_b.clicked.connect(self.send_apdu)
        self.se_msg_box.textChanged.connect(self.trans_se_msg)
        self.re_msg_box.textChanged.connect(self.trans_re_msg)
        self.chk_valid_cb.stateChanged.connect(self.trans_se_msg)
        self.show_level_cb.stateChanged.connect(lambda: self.trans_se_msg() or self.trans_re_msg())
        self.show_dtype_cb.stateChanged.connect(lambda: self.trans_se_msg() or self.trans_re_msg())
        self.always_top_cb.stateChanged.connect(self.set_always_top)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)

        self.apdu_text = ''
        self.send_tm = 0

    def send_apdu(self):
        """send apdu"""
        config.MASTER_WINDOW.se_apdu_signal.emit(self.apdu_text)
        self.re_msg_box.clear()
        config.MASTER_WINDOW.receive_signal.connect(self.re_msg)

    def re_msg(self, msg_text):
        """re msg"""
        self.re_msg_box.setPlainText(msg_text)
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_msg)

    def trans_se_msg(self):
        """translate"""
        msg_text = self.se_msg_box.toPlainText()
        if len(msg_text) < 5:
            return
        trans = translate.Translate(msg_text)
        full = trans.get_full(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        self.se_explain_box.setText(r'%s'%full)
        if self.chk_valid_cb.isChecked():
            self.send_b.setEnabled(True if trans.is_success else False)
        else:
            self.send_b.setEnabled(True)
        if self.send_b.isEnabled():
            self.apdu_text = trans.get_apdu_text()

    def trans_re_msg(self):
        """translate"""
        msg_text = self.re_msg_box.toPlainText()
        if len(msg_text) < 5:
            return
        trans = translate.Translate(msg_text)
        full = trans.get_full(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        self.re_explain_box.setText(r'%s'%full)

    def set_always_top(self):
        """set_always_top"""
        window_pos = self.pos()
        if self.always_top_cb.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


class MsgDiyDialog(QtGui.QDialog, ui_setup.MsgDiyDialogUi):
    """apdu DIY dialog class"""
    def __init__(self):
        super(MsgDiyDialog, self).__init__()
        self.setup_ui()

        self.send_b.setEnabled(False)
        self.chk_valid_cb.setChecked(True)
        self.show_level_cb.setChecked(True)

        self.se_repair_b.clicked.connect(self.repair_msg)
        self.se_clr_b.clicked.connect(lambda: self.se_msg_box.clear() or self.se_msg_box.setFocus())
        self.re_clr_b.clicked.connect(lambda: self.re_msg_box.clear())
        self.send_b.clicked.connect(self.send_msg)
        self.se_msg_box.textChanged.connect(self.trans_se_msg)
        self.re_msg_box.textChanged.connect(self.trans_re_msg)
        self.chk_valid_cb.stateChanged.connect(self.trans_se_msg)
        self.show_level_cb.stateChanged.connect(lambda: self.trans_se_msg() or self.trans_re_msg())
        self.show_dtype_cb.stateChanged.connect(lambda: self.trans_se_msg() or self.trans_re_msg())
        self.always_top_cb.stateChanged.connect(self.set_always_top)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)

        self.apdu_text = ''

    def send_msg(self):
        """send full msg"""
        config.COMMU.send_msg(self.se_msg_box.toPlainText(), self.chan_cb.currentIndex())
        self.re_msg_box.clear()
        config.MASTER_WINDOW.receive_signal.connect(self.re_msg)

    def re_msg(self, msg_text):
        """re msg"""
        self.re_msg_box.setPlainText(msg_text)
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_msg)

    def repair_msg(self):
        """re msg"""
        msg_text = self.se_msg_box.toPlainText()
        if len(msg_text) < 5:
            return
        trans = translate.Translate(msg_text)
        if trans.is_success and trans.is_full_msg:
            repair_msg = linklayer.repair_cs(msg_text)
            self.se_msg_box.setPlainText(repair_msg)

    def trans_se_msg(self):
        """translate"""
        msg_text = self.se_msg_box.toPlainText()
        if len(msg_text) < 5:
            return
        trans = translate.Translate(msg_text)
        full = trans.get_full(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        self.se_explain_box.setText(r'%s'%full)
        if self.chk_valid_cb.isChecked():
            self.send_b.setEnabled(True if trans.is_success else False)
        else:
            self.send_b.setEnabled(True)
        if self.send_b.isEnabled():
            self.apdu_text = trans.get_apdu_text()

    def trans_re_msg(self):
        """translate"""
        msg_text = self.re_msg_box.toPlainText()
        if len(msg_text) < 5:
            return
        trans = translate.Translate(msg_text)
        full = trans.get_full(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        self.re_explain_box.setText(r'%s'%full)

    def set_always_top(self):
        """set_always_top"""
        window_pos = self.pos()
        if self.always_top_cb.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        self.move(window_pos)


class RemoteUpdateDialog(QtGui.QDialog, ui_setup.RemoteUpdateDialogUI):
    """remote update window"""
    update_signal = QtCore.Signal(int, int) if config.IS_USE_PYSIDE else QtCore.pyqtSignal(int, int)
    def __init__(self):
        super(RemoteUpdateDialog, self).__init__()
        self.setup_ui()
        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.file_open_b.clicked.connect(self.open_file)
        self.block_size_box.textChanged.connect(self.show_block_num)
        self.start_update_b.clicked.connect(self.start_update)
        self.stop_update_b.clicked.connect(self.stop_update)

        self.update_signal.connect(self.update_proc)

        self.file_path_box.setEnabled(False)
        self.start_update_b.setEnabled(False)
        self.stop_update_b.setEnabled(False)

        self.is_updating = False
        self.is_tmn_ready = False
        self.service_no = 0xff
        self.send_tm = 0

        self.tmout = 15
        self.retry = 3

    def dragEnterEvent(self, event):
        """drag"""
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        """drag"""
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
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
            self.open_file(links[0])
        else:
            event.ignore()


    def open_file(self, filepath=''):
        """open file"""
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
        """calc file info"""
        file_size = int(self.file_size_num_label.text().replace('字节', ''))
        try:
            block_size = int(self.block_size_box.text().replace('字节', ''))
        except ValueError:
            self.block_num_label.setText('格式错误')
            return
        block_num = file_size // block_size + (0 if file_size % block_size == 0 else 1)
        self.block_num_label.setText('{num}包'.format(num=block_num))


    def start_update(self):
        """start update"""
        filepath = self.file_path_box.text()
        try:
            block_size = int(self.block_size_box.text().replace('字节', ''))
            self.tmout = int(self.tmout_box.text())
            self.retry = int(self.retry_box.text())
        except ValueError:
            block_size = 1024
            self.tmout = 10
            self.retry = 3
            self.block_size_box.setText(str(block_size))
            self.tmout_box.setText(str(self.tmout))
            self.retry_box.setText(str(self.retry))
        if filepath:
            threading.Thread(target=self.send_file,\
                        args=(filepath, block_size)).start()


    def send_file(self, filepath, block_size):
        """send file thread"""
        config.MASTER_WINDOW.receive_signal.connect(self.re_msg)
        self.service_no = config.SERVICE.get_service_no()
        self.send_tm = time.time()
        self.send_cnt = 0
        start_apdu_text = '0701{piid:02X} f0010700 0203 0206 0a00 0a00 06 {filesize:08X}\
                        0403e0 0a00 1600 12 {blocksize:04X} 0202 1600 0900 00'\
                        .format(piid=self.service_no, filesize=os.path.getsize(filepath), blocksize=block_size)
        config.MASTER_WINDOW.se_apdu_signal.emit(start_apdu_text)
        self.status_label.setText('发送起始帧...')
        self.is_updating = True
        self.is_tmn_ready = False
        while not self.is_tmn_ready:
            if time.time() - self.send_tm > self.tmout:
                self.err_quit(err_msg='起始帧超时')
                return
            if not self.is_updating:
                self.err_quit(err_msg='意外终止')
                return
        self.file_open_b.setEnabled(False)
        self.block_size_box.setEnabled(False)
        self.retry_box.setEnabled(False)
        self.tmout_box.setEnabled(False)
        self.start_update_b.setEnabled(False)
        self.stop_update_b.setEnabled(True)

        file_size = os.path.getsize(filepath)
        block_num = file_size // block_size + (0 if file_size % block_size == 0 else 1)
        with open(filepath, 'rb') as file:
            file_text = file.read(file_size)
            file_text = ''.join(['%02X'%x for x in file_text])
            text_list = [file_text[x: x + block_size*2] for x in range(0, len(file_text), block_size*2)]
            for block_no, block_text in enumerate(text_list):
                # print('block:', block_no)
                send_len = (int)(len(block_text)/2)
                self.service_no = config.SERVICE.get_service_no()
                send_apdu_text = '0701{piid:02X} f0010800 0202 12{blockno:04X} 09'\
                                    .format(piid=self.service_no, blockno=block_no)\
                                    + ('%02X'%send_len if send_len < 128\
                                        else '82%04X'%send_len) + block_text + '00'
                config.MASTER_WINDOW.se_apdu_signal.emit(send_apdu_text)
                self.status_label.setText('正在升级...')
                self.update_signal.emit(block_no + 1, block_num)
                self.send_tm = time.time()
                self.send_cnt = 0
                self.is_tmn_ready = False
                while not self.is_tmn_ready:
                    time.sleep(0.05)
                    if time.time() - self.send_tm > self.tmout:
                        if self.send_cnt < self.retry:
                            self.status_label.setText('正在补发(%d/%d)...'%(self.send_cnt + 1, self.retry))
                            config.MASTER_WINDOW.se_apdu_signal.emit(send_apdu_text)
                            self.send_tm = time.time()
                            self.send_cnt += 1
                        else:
                            self.err_quit(err_msg='超时')
                            return
                    if not self.is_updating:
                        self.err_quit(err_msg='意外终止')
                        return
        self.ok_quit()

    def err_quit(self, err_msg = ''):
        """err_quit"""
        self.file_open_b.setEnabled(True)
        self.block_size_box.setEnabled(True)
        self.retry_box.setEnabled(True)
        self.tmout_box.setEnabled(True)
        self.stop_update_b.setEnabled(False)
        self.start_update_b.setEnabled(True)
        self.start_update_b.setText('开始升级')
        self.status_label.setText('升级失败 ' + err_msg)

    def ok_quit(self, ok_msg = ''):
        """ok_quit"""
        self.file_open_b.setEnabled(True)
        self.block_size_box.setEnabled(True)
        self.retry_box.setEnabled(True)
        self.tmout_box.setEnabled(True)
        self.stop_update_b.setEnabled(False)
        self.start_update_b.setEnabled(True)
        self.start_update_b.setText('开始升级')
        self.status_label.setText('升级成功 ' + ok_msg)


    def re_msg(self, msg_text):
        """re msg"""
        if self.service_no != common.get_msg_service_no(msg_text):
            return
        msg_trans = translate.Translate(msg_text)
        if msg_trans.is_access_successed:
            self.is_tmn_ready = True
        else:
            print('收到否认帧，重发...')
            return
        self.service_no = 0xff


    def update_proc(self, block_no, block_num):
        """update proc"""
        self.start_update_b.setText('升级中({no}/{all})'.format(no=block_no + 1, all=block_num))


    def stop_update(self):
        """stop update"""
        self.is_updating = False


class GetSetServiceDialog(QtGui.QDialog, ui_setup.GetSetServiceDialogUI):
    """get service dialog class"""
    def __init__(self):
        super(GetSetServiceDialog, self).__init__()
        self.setup_ui()

        self.class_cb.addItems(tuple(['收藏'] + service_data.get_base_class()))
        self.class_cb.setCurrentIndex(-1)

        self.object_table_add_b.clicked.connect(self.add_object_table_row)
        self.object_table_read_b.clicked.connect(self.clr_re_table)
        self.object_table_read_b.clicked.connect(self.send_read_apdu)
        self.re_table_clr_b.clicked.connect(self.clr_re_table)

        self.class_cb.currentIndexChanged.connect(self.load_class_oi)
        self.oi_cb.currentIndexChanged.connect(self.load_oi_attr)

        # self.show_level_cb.stateChanged.connect(self.trans_msg)
        self.always_top_cb.stateChanged.connect(self.set_always_top)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)

        self.class_cb.setCurrentIndex(0)

        self.service_no = 0xff
        self.send_tm = time.time()


    def load_class_oi(self):
        """load class oi"""
        self.oi_cb.clear()
        if self.class_cb.currentText() == '收藏':
            self.oi_cb.addItems(service_data.get_favorite_oi())
        else:
            add_list = config.K_DATA.get_class_oi(self.class_cb.currentText())
            self.oi_cb.addItems(add_list)


    def load_oi_attr(self):
        """load oi attr"""
        self.attr_cb.clear()
        self.attr_cb.addItems(config.K_DATA.get_oi_attr(self.oi_cb.currentText()[:4]))
        self.attr_cb.setCurrentIndex(1)


    def add_object_table_row(self):
        """add object row"""
        row_pos = self.object_table.rowCount()
        self.object_table.insertRow(row_pos)

        class_cb = QtGui.QComboBox()
        class_cb.addItems(('常用',))
        class_cb.setCurrentIndex(0)
        self.object_table.setCellWidget(row_pos, 0, class_cb)
        oad_cb = QtGui.QComboBox()
        # oad_cb.addItems(get_set_oads.ACTIVE_OADS)
        oad_cb.setCurrentIndex(0)
        self.object_table.setCellWidget(row_pos, 1, oad_cb)
        self.object_remove_cb = QtGui.QPushButton()
        self.object_remove_cb.setText('删')
        self.object_table.setCellWidget(row_pos, 2, self.object_remove_cb)
        self.object_remove_cb.clicked.connect(self.object_table_remove)

        self.object_table.scrollToBottom()


    def object_table_remove(self):
        """remove row in object table"""
        button = self.sender()
        index = self.object_table.indexAt(button.pos())
        self.object_table.removeRow(index.row())


    def send_read_apdu(self):
        """send_read_apdu"""
        oads = []
        for row in range(self.object_table.rowCount()):
            oads.append('%s%02d%02d'%\
                        (self.object_table.cellWidget(row, 1).currentText().split(' ')[0],\
                            int(self.object_table.cellWidget(row, 2).currentText().split(' ')[0]),\
                            int(self.object_table.cellWidget(row, 3).value())))
        print('oads', oads)
        if not oads:
            return
        service = '0501' if len(oads) == 1 else '0502'
        self.service_no = config.SERVICE.get_service_no()
        apdu_text = '{service}{piid:02X}{array}{oad}00'\
                        .format(service=service, piid=self.service_no,\
                                array='' if len(oads) == 1 else '%02X'%len(oads),\
                                oad=''.join(oads))
        print('apdu_text: ', apdu_text)
        self.send_tm = time.time()
        config.MASTER_WINDOW.se_apdu_signal.emit(apdu_text)
        config.MASTER_WINDOW.receive_signal.connect(self.re_msg)

    def re_msg(self, re_text):
        """recieve text"""
        if self.service_no != common.get_msg_service_no(re_text):
            return
        if abs(time.time() - self.send_tm) > config.RE_MSG_TIMEOUT:
            print('re msg timeout!')
            config.MASTER_WINDOW.receive_signal.disconnect(self.re_msg)
            self.service_no = 0xff
            return
        self.service_no = 0xff
        re_list = common.text2list(re_text)
        m_text = common.search_msg(re_list)[0]
        m_list = common.text2list(m_text)
        apdu_list = common.get_apdu_list(m_list)
        print('apdu_list', apdu_list)
        re_data_list = apdu_list[8:]
        loadtype.data2table(re_data_list, self.re_table)
        config.MASTER_WINDOW.receive_signal.disconnect(self.re_msg)

    def clr_re_table(self):
        """clear re msg table"""
        for _ in range(self.re_table.rowCount()):
            self.re_table.removeRow(0)

    def set_always_top(self):
        """set_always_top"""
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
    dialog = RemoteUpdateDialog()
    dialog.show()
    APP.exec_()
    sys.exit(0)
