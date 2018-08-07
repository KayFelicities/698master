"""log files trans ui"""
import re
import os
import sys
import threading
import chardet
from master.UI.trans_ui_setup import TransWindowUi
from master.trans.translate import Translate
from master.others import master_config
from master import config
if config.IS_USE_PYSIDE:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore


class TransWindow(QtGui.QMainWindow, TransWindowUi):
    """translate window"""
    load_file = QtCore.Signal(str) if config.IS_USE_PYSIDE else QtCore.pyqtSignal(str)
    set_progress = QtCore.Signal(int) if config.IS_USE_PYSIDE else QtCore.pyqtSignal(int)

    def __init__(self):
        super(TransWindow, self).__init__()
        qss_file = open(os.path.join(config.SORTWARE_PATH, 'styles/white_blue.qss')).read()
        self.setStyleSheet(qss_file)
        self.setup_ui()
        self.proc_bar.setVisible(False)
        self.show_level_cb.setChecked(True)
        self.auto_wrap_cb.setChecked(False)

        apply_config = master_config.MasterConfig()
        file_list = apply_config.get_last_file()[::-1]
        for file_name in file_list:
            self.file_action = QtGui.QAction('%s'%file_name, self)
            self.file_menu.addAction(self.file_action)
            self.file_action.triggered.connect(self.openfile)
        font_size = apply_config.get_font_size()
        self.input_box.set_font_size(font_size)
        self.update_wrap_mode()

        self.setAcceptDrops(True)
        self.input_box.cursorPositionChanged.connect(self.cursor_changed)
        self.input_box.textChanged.connect(self.take_input_text)
        self.msg_box.textChanged.connect(self.start_trans)
        self.find_last_b.clicked.connect(lambda: self.find_last(True))
        self.find_next_b.clicked.connect(lambda: self.find_next(True))
        self.msg_next_b.clicked.connect(lambda: self.jump_to_msg('next'))
        self.msg_priv_b.clicked.connect(lambda: self.jump_to_msg('priv'))
        self.input_zoom_in_b.clicked.connect(self.input_box.zoomIn)
        self.input_zoom_out_b.clicked.connect(self.input_box.zoomOut)
        self.output_zoom_in_b.clicked.connect(self.output_box.zoomIn)
        self.output_zoom_out_b.clicked.connect(self.output_box.zoomOut)
        self.output_copy_b.clicked.connect(self.copy_to_clipboard)
        self.auto_wrap_cb.clicked.connect(self.update_wrap_mode)
        self.show_level_cb.clicked.connect(self.start_trans)
        self.show_dtype_cb.clicked.connect(self.start_trans)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.open_action.triggered.connect(self.openfile)
        self.reload_action.triggered.connect(lambda: self.openfile(filepath=self.file_now))
        self.clear_action.triggered.connect(self.clear_box)
        self.about_action.triggered.connect(config.ABOUT_WINDOW.show)
        self.find_action.triggered.connect(lambda: self.find_box.setFocus() or self.find_box.selectAll())
        self.next_msg_action.triggered.connect(lambda: self.jump_to_msg('next'))
        self.priv_msg_action.triggered.connect(lambda: self.jump_to_msg('priv'))
        self.load_file.connect(self.load_text, QtCore.Qt.QueuedConnection)
        self.set_progress.connect(self.set_progressbar, QtCore.Qt.QueuedConnection)
        self.find_box.returnPressed.connect(lambda: self.find_next(False))

        self.file_now = ''
        self.msg_find_dict = []
        self.last_selection = (0, 0)
        self.text_find_list = []
        self.last_find_text = ''


    def dragEnterEvent(self, event):
        """drag"""
        if event.mimeData().hasUrls:
            print('has')
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
            print('url:', links[0])
            self.openfile(links[0])
        else:
            event.ignore()


    def load_text(self, file_text):
        """load text"""
        self.proc_bar.setVisible(False)
        self.open_action.setEnabled(True)
        self.setAcceptDrops(True)
        self.input_box.setPlainText(file_text)


    def set_progressbar(self, percent):
        """set progress bar in main process"""
        self.proc_bar.setValue(percent)


    def openfile(self, filepath=''):
        """open file"""
        action = self.sender()
        if isinstance(action, QtGui.QAction) and os.path.isfile(action.text()):
            filepath = action.text()
        if not os.path.isfile(filepath):
            filepath = QtGui.QFileDialog.getOpenFileName(self, caption='请选择698日志文件', filter='*')
        if filepath:
            print('filepath: ', filepath)
            save_config = master_config.MasterConfig()
            save_config.add_last_file(filepath)
            save_config.commit()
            file_size = os.path.getsize(filepath)
            if file_size > 3000000:
                reply = QtGui.QMessageBox.question(self, '警告', '打开大型文件会使用较长时间，确定打开吗？',\
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply != QtGui.QMessageBox.Yes:
                    return
            self.proc_bar.setVisible(True)
            self.open_action.setEnabled(False)
            self.setAcceptDrops(False)
            self.proc_l.setText('处理中')
            self.setWindowTitle('698日志解析工具_{ver} - {file}'.\
                        format(ver=config.MASTER_WINDOW_TITLE_ADD, file=filepath))
            self.file_now = filepath
            threading.Thread(target=self.read_file,\
                                args=(filepath,)).start()


    def read_file(self, filepath):
        """read file thread"""
        # get file encoding
        with open(filepath, "rb") as file:
            encoding = chardet.detect(file.read(65535))
            print(encoding)
            if encoding['confidence'] > 0.95:
                file_encoding = encoding['encoding']
            else:
                file_encoding = 'gb2312'

        with open(filepath, encoding=file_encoding, errors='ignore') as file:
            count = 0
            for _ in file:
                count += 1
        with open(filepath, encoding=file_encoding, errors='ignore') as file:
            file_text = ''
            for i, line in enumerate(file):
                file_text += line
                if i % 500 == 0:
                    self.set_progress.emit(i*95 / count)
        self.load_file.emit(file_text)
        print('read_file thread quit')


    def cursor_changed(self):
        """cursor changed to trans"""
        document = self.input_box.document()
        cursor = self.input_box.textCursor()
        scroll = self.input_box.verticalScrollBar()
        print('cursor: %d, scroll: %d, document: %d'\
            %(cursor.blockNumber(), scroll.value(), document.findBlock(cursor.position()).blockNumber()))

        if self.last_selection[0] <= int(self.input_box.textCursor().position())\
                                    <= self.last_selection[1]:
            return
        else:
            self.msg_box.clear()
            for row in self.msg_find_dict:
                if row['span'][0] <= int(self.input_box.textCursor().position()) <= row['span'][1]:
                    self.msg_box.setPlainText(row['message'])
                    cursor = self.input_box.textCursor()
                    cursor.setPosition(row['span'][1])
                    cursor.setPosition(row['span'][0], QtGui.QTextCursor.KeepAnchor)
                    self.input_box.setTextCursor(cursor)
                    self.last_selection = row['span']
                    break
            else:
                # self.output_box.setText('请点选一条报文')
                self.last_selection = (0, 0)


    def take_input_text(self):
        """handle with input text"""
        input_text = self.input_box.toPlainText()
        res = re.compile(r'([0-9a-fA-F]{2} ){5,}[0-9a-fA-F]{2}')
        all_match = res.finditer(input_text)
        self.msg_find_dict = []
        find_num = 0
        for mes in all_match:
            self.msg_find_dict += [{'message': mes.group(), 'span': mes.span()}]
            find_num += 1
        self.proc_l.setText('找到报文%d条'%find_num)
        if len(self.msg_find_dict) == 1 and self.msg_find_dict[0]['message'].strip() == input_text.strip():
            self.msg_box.setPlainText(self.msg_find_dict[0]['message'])

        self.find_l.setText('')


    def start_trans(self):
        """start_trans"""
        if len(self.msg_box.toPlainText()) < 5:
            self.output_box.setText('请点选一条报文。\n若软件无法识别请手动复制到上方框中。')
            return
        trans = Translate(self.msg_box.toPlainText())
        brief = trans.get_brief()
        full = trans.get_full(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        self.output_box.setText(r'<b>【概览】</b><p>%s</p><hr><b>【完整】</b>%s'%(brief, full))


    def clear_box(self):
        """clear_box"""
        self.input_box.setPlainText('')
        self.output_box.setText('')
        self.setWindowTitle('698日志解析工具_{ver}'.format(ver=config.MASTER_WINDOW_TITLE_ADD))
        self.input_box.setFocus()


    def search_text(self, text):
        """search_text"""
        input_text = self.input_box.toPlainText()
        res = re.compile(r'%s'%text)
        all_match = res.finditer(input_text)
        self.text_find_list = [mes.span() for mes in all_match]
        if self.text_find_list:
            self.find_l.setText('0/%d'%len(self.text_find_list))
        else:
            self.find_l.setText('未找到！')


    def find_next(self, is_setfocus=True):
        """find_next"""
        find_text = self.find_box.text()
        if not find_text:
            return
        if self.find_l.text() == '' or find_text != self.last_find_text:
            self.search_text(find_text)
        if self.find_l.text() == '未找到！':
            return
        cursor = self.input_box.textCursor()
        position = cursor.position()
        for count, text_find in enumerate(self.text_find_list, 1):
            if text_find[0] >= position:
                self.find_l.setText('%d/'%count + self.find_l.text().split('/')[1])
                cursor.setPosition(text_find[0])
                cursor.setPosition(text_find[1], QtGui.QTextCursor.KeepAnchor)
                self.input_box.setTextCursor(cursor)
                break
        else:
            self.find_l.setText('1/' + self.find_l.text().split('/')[1])
            cursor.setPosition(self.text_find_list[0][0])
            cursor.setPosition(self.text_find_list[0][1], QtGui.QTextCursor.KeepAnchor)
            self.input_box.setTextCursor(cursor)
        if is_setfocus:
            self.input_box.setFocus()

    def find_last(self, is_setfocus=True):
        """find_last"""
        find_text = self.find_box.text()
        if not find_text:
            return
        if self.find_l.text() or find_text != self.last_find_text:
            self.search_text(find_text)
        if self.find_l.text() == '未找到！':
            return
        cursor = self.input_box.textCursor()
        position = cursor.position()
        for count, text_find in enumerate(self.text_find_list[::-1], 0):
            if text_find[1] < position:
                self.find_l.setText('%d/'%(len(self.text_find_list) - count)\
                                        + self.find_l.text().split('/')[1])
                cursor.setPosition(text_find[0])
                cursor.setPosition(text_find[1], QtGui.QTextCursor.KeepAnchor)
                self.input_box.setTextCursor(cursor)
                break
        else:
            self.find_l.setText('%d/%d'%(len(self.text_find_list),\
                                    len(self.text_find_list)))
            cursor.setPosition(self.text_find_list[::-1][0][0])
            cursor.setPosition(self.text_find_list[::-1][0][1], QtGui.QTextCursor.KeepAnchor)
            self.input_box.setTextCursor(cursor)
        if is_setfocus:
            self.input_box.setFocus()


    def jump_to_msg(self, mode='next'):
        """go to next or privious msg"""
        cursor = self.input_box.textCursor()
        pos_now = int(cursor.position())
        last_msg_pos = 0
        for row in self.msg_find_dict:
            if mode == 'priv':
                if row['span'][1] < pos_now:
                    last_msg_pos = row['span'][0]
                else:
                    cursor.setPosition(last_msg_pos)
                    self.input_box.setTextCursor(cursor)
                    break
            if mode == 'next':
                if row['span'][0] > pos_now:
                    cursor.setPosition(row['span'][1] if self.auto_wrap_cb.isChecked() else row['span'][0])
                    self.input_box.setTextCursor(cursor)
                    break
        self.input_box.setFocus()


    def copy_to_clipboard(self):
        """copy_to_clipboard"""
        trans = Translate(self.msg_box.toPlainText())
        text = trans.get_clipboard_text(self.show_level_cb.isChecked(), self.show_dtype_cb.isChecked())
        clipboard = QtGui.QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(text)


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


    def update_wrap_mode(self):
        """update_wrap_mode"""
        self.input_box.setLineWrapMode(QtGui.QPlainTextEdit.WidgetWidth\
                if self.auto_wrap_cb.isChecked() else QtGui.QPlainTextEdit.NoWrap)


    def closeEvent(self, event):
        """close event"""
        # save config
        save_config = master_config.MasterConfig()
        save_config.set_font_size(self.input_box.get_font_size())
        save_config.commit()

        # quit
        event.accept()
        os._exit(0)


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = TransWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
