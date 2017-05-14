'''trans ui'''
import re
import os
import threading
from PyQt4 import QtCore
from PyQt4 import QtGui
from UI.trans_window2 import Ui_TransWindow
from trans.translate import Translate
import config
import trans.common as commonfun


class TransWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_TransWindow):
    '''translate window'''
    load_file = QtCore.pyqtSignal(str)
    set_progress = QtCore.pyqtSignal(int)
    def __init__(self):
        super(TransWindow, self).__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.proc_bar.setVisible(False)
        self.setWindowTitle('698解析工具_' + config.version + '(' + config.DT + ')')
        config.show_level = self.show_level_cb.isChecked()
        self.input_box.cursorPositionChanged.connect(self.cursor_changed)
        self.input_box.textChanged.connect(self.take_input_text)
        self.clear_b.clicked.connect(self.clear_box)
        self.open_b.clicked.connect(self.openfile)
        self.show_level_cb.clicked.connect(self.set_level_visible)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.about.triggered.connect(self.show_about_window)
        self.load_file.connect(self.load_text, QtCore.Qt.QueuedConnection)
        self.set_progress.connect(self.set_progressbar, QtCore.Qt.QueuedConnection)

        self.find_dict = []


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
            if links[0].split('.')[-1] in ['txt', 'TXT', 'log', 'LOG']:
                self.openfile(links[0])
        else:
            event.ignore()

    def load_text(self, file_text):
        '''load text'''
        self.proc_bar.setVisible(False)
        self.open_b.setEnabled(True)
        self.setAcceptDrops(True)
        self.input_box.setText(file_text)


    def set_progressbar(self, percent):
        '''set progress bar in main process'''
        self.proc_bar.setValue(percent)


    def openfile(self, filepath=''):
        '''open file'''
        if not filepath:
            filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', '*.txt *.log')
        if filepath:
            print('filepath: ', filepath)
            file_size = os.path.getsize(filepath)
            if file_size > 3000000:
                reply = QtGui.QMessageBox.question(self, '警告', '打开大型文件会使用较长时间，确定打开吗？',\
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply != QtGui.QMessageBox.Yes:
                    return
            self.proc_bar.setVisible(True)
            self.open_b.setEnabled(False)
            self.setAcceptDrops(False)
            self.proc_l.setText('处理中')
            threading.Thread(target=self.read_file,\
                                args=(filepath,)).start()


    def read_file(self, filepath):
        '''read file thread'''
        with open(filepath, encoding='gb2312', errors='ignore') as file:
            count = 0
            for _ in file:
                count += 1
        print(count)
        with open(filepath, encoding='gb2312', errors='ignore') as file:
            file_text = ''
            for i, line in enumerate(file):
                file_text += line
                if i % 500 == 0:
                    self.set_progress.emit(i*95 / count)
        self.load_file.emit(file_text)
        print('read_file thread quit')


    def cursor_changed(self):
        '''cursor changed to trans'''
        for row in self.find_dict:
            # print(row)
            if row['span'][0] <= int(self.input_box.textCursor().position()) <= row['span'][1]:
                self.start_trans(row['message'])
                cursor = self.input_box.textCursor()
                cursor.setPosition(row['span'][0])
                cursor.setPosition(row['span'][1], QtGui.QTextCursor.KeepAnchor)
                self.input_box.setTextCursor(cursor)
                break
        else:
            self.output_box.setText('请点选一条报文')


    def take_input_text(self):
        '''handle with input text'''
        input_text = self.input_box.toPlainText()
        # html_text = input_text
        res = re.compile(r'([0-9a-fA-F]{2} ){5,}[0-9a-fA-F]{2}')
        # all_match = res.finditer(html_text)
        # offset = 0
        # for mes in all_match:
        #     html_text = html_text[:mes.start()+offset] + '<b>'\
        #                     + html_text[mes.start()+offset:mes.end()+offset]\
        #                     + '</b>' + html_text[mes.end()+offset:]
        #     offset += 7
        # html_text = '<!DOCTYPE HTML><html><body>'\
        #                 + html_text.replace('\n', '<br>') + '</body></html>'
        # self.input_box.textChanged.disconnect(self.take_input_text)
        # # self.input_box.setText(html_text)
        # self.input_box.textChanged.connect(self.take_input_text)

        all_match = res.finditer(input_text)
        self.find_dict = []
        find_num = 0
        for mes in all_match:
            self.find_dict += [{'message': mes.group(), 'span': mes.span()}]
            find_num += 1
        self.proc_l.setText('找到报文%d条'%find_num)
        if len(self.find_dict) == 1 and self.find_dict[0]['message'].strip() == input_text.strip():
            self.start_trans(self.find_dict[0]['message'])


    def start_trans(self, input_text, with_level=True):
        '''start_trans'''
        brief_trans = Translate()
        brief = brief_trans.get_brief(input_text)
        full_trans = Translate()
        full = full_trans.get_full(input_text)
        self.output_box.setText(r'<b>【概览】</b>%s<hr><b>【完整】</b>%s'%(brief, full))
        # print('Kay, ', self.output_box.toHtml())


    def clear_box(self):
        '''clear_box'''
        self.input_box.setFocus()


    def set_level_visible(self):
        '''set_level_visible'''
        config.show_level = self.show_level_cb.isChecked()
        self.start_trans()


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


    def calc_len_box(self):
        '''calc_len_box'''
        input_text = self.input_box.toPlainText()
        input_len = commonfun.calc_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        self.clear_b.setText('清空(' + len_message + ')')


    def show_about_window(self):
        '''show_about_window'''
        config.about_window.show()
