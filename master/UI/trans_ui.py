'''log files trans ui'''
import re
import os
import sys
import threading
from PyQt4 import QtCore, QtGui
from master.trans.translate import Translate
from master import config
import master.trans.common as commonfun


class TransWindow(QtGui.QMainWindow):
    '''translate window'''
    load_file = QtCore.pyqtSignal(str)
    set_progress = QtCore.pyqtSignal(int)

    def __init__(self):
        super(TransWindow, self).__init__()
        self.setup_ui()
        self.setAcceptDrops(True)
        self.is_show_level = self.show_level_cb.isChecked()
        self.input_box.cursorPositionChanged.connect(self.cursor_changed)
        self.input_box.textChanged.connect(self.take_input_text)
        self.clr_b.clicked.connect(self.clear_box)
        self.open_b.clicked.connect(self.openfile)
        self.show_level_cb.clicked.connect(self.set_level_visible)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.about_action.triggered.connect(self.show_about_window)
        self.load_file.connect(self.load_text, QtCore.Qt.QueuedConnection)
        self.set_progress.connect(self.set_progressbar, QtCore.Qt.QueuedConnection)

        self.find_dict = []
        self.last_selection = (0, 0)


    def setup_ui(self):
        '''set layout'''
        self.setWindowTitle('698日志解析工具_{ver}'.format(ver=config.WINDOWS_TITLE_ADD))
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698_o.png')))
        self.menubar = self.menuBar()
        self.about_action = QtGui.QAction('&关于', self)
        self.help_menu = self.menubar.addMenu('&帮助')
        self.help_menu.addAction(self.about_action)

        self.open_b = QtGui.QPushButton()
        self.open_b.setText('打开日志...')
        self.open_b.setMinimumSize(QtCore.QSize(100, 0))
        self.open_b.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.clr_b = QtGui.QPushButton()
        self.clr_b.setText('清空')
        self.btn_hbox = QtGui.QHBoxLayout()
        self.btn_hbox.addWidget(self.open_b)
        self.btn_hbox.addWidget(self.clr_b)

        self.input_box = QtGui.QTextEdit()
        self.output_box = QtGui.QTextEdit()
        self.main_hsplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.main_hsplitter.addWidget(self.input_box)
        self.main_hsplitter.addWidget(self.output_box)
        self.main_hsplitter.setStretchFactor(0, 1)
        self.main_hsplitter.setStretchFactor(1, 1)

        self.show_level_cb = QtGui.QCheckBox()
        self.show_level_cb.setChecked(True)
        self.show_level_cb.setText('报文结构')
        self.always_top_cb = QtGui.QCheckBox()
        self.always_top_cb.setChecked(False)
        self.always_top_cb.setText('置顶')
        self.proc_bar = QtGui.QProgressBar()
        self.proc_bar.setEnabled(True)
        self.proc_bar.setMinimumSize(QtCore.QSize(200, 0))
        self.proc_bar.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.proc_bar.setTextVisible(False)
        self.proc_bar.setVisible(False)

        self.proc_l = QtGui.QLabel()
        self.proc_l.setText('就绪')
        self.foot_hbox = QtGui.QHBoxLayout()
        self.foot_hbox.addWidget(self.proc_bar)
        self.foot_hbox.addWidget(self.proc_l)
        self.foot_hbox.addStretch(1)
        self.foot_hbox.addWidget(self.show_level_cb)
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
        print(int(self.input_box.textCursor().position()))
        if self.last_selection[0] <= int(self.input_box.textCursor().position())\
                                    <= self.last_selection[1]:
            return
        else:
            self.trans_pos(int(self.input_box.textCursor().position()))


    def trans_pos(self, message_pos):
        '''trans message in position'''
        for row in self.find_dict:
            # print(row)
            if row['span'][0] <= message_pos <= row['span'][1]:
                self.start_trans(row['message'])
                cursor = self.input_box.textCursor()
                cursor.setPosition(row['span'][0])
                cursor.setPosition(row['span'][1], QtGui.QTextCursor.KeepAnchor)
                self.input_box.setTextCursor(cursor)
                self.last_selection = row['span']
                break
        else:
            self.output_box.setText('请点选一条报文')
            self.last_selection = (0, 0)


    def take_input_text(self):
        '''handle with input text'''
        input_text = self.input_box.toPlainText()
        res = re.compile(r'([0-9a-fA-F]{2} ){5,}[0-9a-fA-F]{2}')
        all_match = res.finditer(input_text)
        self.find_dict = []
        find_num = 0
        for mes in all_match:
            self.find_dict += [{'message': mes.group(), 'span': mes.span()}]
            find_num += 1
        self.proc_l.setText('找到报文%d条'%find_num)
        if len(self.find_dict) == 1 and self.find_dict[0]['message'].strip() == input_text.strip():
            self.start_trans(self.find_dict[0]['message'])


    def start_trans(self, input_text):
        '''start_trans'''
        trans = Translate(input_text)
        brief = trans.get_brief()
        full = trans.get_full(self.is_show_level)
        self.output_box.setText(r'<b>【概览】</b><p>%s</p><hr><b>【完整】</b>%s'%(brief, full))


    def clear_box(self):
        '''clear_box'''
        self.input_box.setText('')
        self.output_box.setText('')
        self.input_box.setFocus()


    def set_level_visible(self):
        '''set_level_visible'''
        self.is_show_level = self.show_level_cb.isChecked()
        self.trans_pos(int(self.input_box.textCursor().position()))


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



if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = TransWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
