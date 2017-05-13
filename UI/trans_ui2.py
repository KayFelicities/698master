'''trans ui'''
import re
from PyQt4 import QtCore
from PyQt4 import QtGui
from UI.trans_window2 import Ui_TransWindow
from trans.translate import Translate
import config
import trans.common as commonfun


class TransWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_TransWindow):
    '''translate window'''
    def __init__(self):
        super(TransWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('698解析工具_' + config.version + '(' + config.DT + ')')
        config.show_level = self.show_level_cb.isChecked()
        self.input_box.cursorPositionChanged.connect(self.cursor_changed)
        self.input_box.textChanged.connect(self.take_input_text)
        self.clear_b.clicked.connect(self.clear_box)
        self.open_b.clicked.connect(self.openfile)
        self.show_level_cb.clicked.connect(self.set_level_visible)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.input_box.textChanged.connect(self.calc_len_box)
        self.about.triggered.connect(self.show_about_window)

        self.find_dict = []
        self.last_cursor_span = (0, 0)


    def openfile(self):
        '''open file'''
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', '*.txt *.log')
        with open(filepath, encoding='utf-8', errors='ignore') as file:
            text = file.read()
            self.input_box.setText(text)


    def cursor_changed(self):
        '''cursor changed to trans'''
        if self.last_cursor_span[0] <= int(self.input_box.textCursor().position()) <= self.last_cursor_span[1]:
            return
        for row in self.find_dict:
            # print(row)
            if row['span'][0] <= int(self.input_box.textCursor().position()) <= row['span'][1]:
                self.start_trans(row['message'])
                self.last_cursor_span = row['span']
                break
        else:
            self.output_box.setText('请点选一条报文')
            self.last_cursor_span = (0, 0)


    def take_input_text(self):
        '''handle with input text'''
        input_text = self.input_box.toPlainText()
        html_text = input_text
        # res = re.compile(r'68 ([0-9a-fA-F]{2} )+16')
        res = re.compile(r'([0-9a-fA-F]{2} ){5,}[0-9a-fA-F]{2}')
        all_match = res.finditer(html_text)
        offset = 0
        for mes in all_match:
            html_text = html_text[:mes.start()+offset] + '<b>'\
                            + html_text[mes.start()+offset:mes.end()+offset]\
                            + '</b>' + html_text[mes.end()+offset:]
            offset += 7
        html_text = '<!DOCTYPE HTML><html><body>'\
                        + html_text.replace('\n', '<br>') + '</body></html>'
        self.input_box.textChanged.disconnect(self.take_input_text)
        # self.input_box.setText(html_text)
        self.input_box.textChanged.connect(self.take_input_text)

        all_match = res.finditer(input_text)
        self.find_dict = []
        for mes in all_match:
            self.find_dict += [{'message': mes.group(), 'span': mes.span()}]
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
