'''trans ui'''
from PyQt4 import QtCore
from PyQt4 import QtGui
from UI.trans_window import Ui_TransWindow
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
        config.auto_trans = self.auto_trans_cb.isChecked()
        if config.auto_trans is True:
            self.input_box.textChanged.connect(self.start_trans)
            self.translate_button.setVisible(False)
        else:
            self.input_box.textChanged.disconnect(self.start_trans)
            self.translate_button.setVisible(True)
        self.quick_fix_button.clicked.connect(self.quick_fix)
        self.translate_button.clicked.connect(self.start_trans)
        self.clear_button.clicked.connect(self.clear_box)
        self.show_level_cb.clicked.connect(self.set_level_visible)
        self.auto_trans_cb.clicked.connect(self.set_auto_trans)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.input_box.textChanged.connect(self.calc_len_box)
        self.about.triggered.connect(self.show_about_window)
        self.serial_mode_button.clicked.connect(self.shift_serial_window)

    def start_trans(self):
        '''start_trans'''
        input_text = self.input_box.toPlainText()
        brief_trans = Translate()
        brief = brief_trans.get_brief(input_text)
        full_trans = Translate()
        full = full_trans.get_full(input_text)
        self.output_box.setText(r'<b>【概览】</b>%s<hr><b>【完整】</b>%s'%(brief, full))

    def clear_box(self):
        '''clear_box'''
        self.input_box.setFocus()

    def set_level_visible(self):
        '''set_level_visible'''
        config.show_level = self.show_level_cb.isChecked()
        self.start_trans()

    def quick_fix(self):
        '''quick_fix'''
        pass
        # input_text = self.input_box.toPlainText()
        # data_in = data_format(input_text)
        # if config.good_L is not None:
        #     data_in[1], data_in[2] = config.good_L[0], config.good_L[1]
        # else:
        #     if config.good_HCS is not None:
        #         ret_dict = link_layer.get_SA_CA(data_in)
        #         hcs_pos = 6 + int(ret_dict['SA_len'])
        #         data_in[hcs_pos], data_in[hcs_pos + 1] = config.good_HCS[0], config.good_HCS[1]
        #         input_text = ''
        #         for data in data_in:
        #             input_text += data + ' '
        #         self.input_box.setText(input_text)
        #         self.start_trans()
        #     if config.good_FCS is not None:
        #         data_in[-3], data_in[-2] = config.good_FCS[0], config.good_FCS[1]
        # input_text = ''
        # for data in data_in:
        #     input_text += data + ' '
        # self.input_box.setText(input_text)

    def set_auto_trans(self):
        '''set_auto_trans'''
        config.auto_trans = self.auto_trans_cb.isChecked()
        if config.auto_trans is True:
            self.input_box.textChanged.connect(self.start_trans)
            self.translate_button.setVisible(False)
        else:
            self.input_box.textChanged.disconnect(self.start_trans)
            self.translate_button.setVisible(True)
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
        self.clear_button.setText('清空(' + len_message + ')')

    def show_about_window(self):
        '''show_about_window'''
        config.about_window.show()

    def shift_serial_window(self):
        '''shift_serial_window'''
        pass
        # self.hide()
        # config.serial_window.show()
