'''dialog windows'''
import sys
import os
from PyQt4 import QtGui, QtCore
from trans import translate


class TransPopDialog(QtGui.QDialog):
    '''translate window'''
    def __init__(self):
        # QtGui.QDialog.__init__(self, parent)
        super(TransPopDialog, self).__init__()
        self.setup_ui()
        self.message_box.textChanged.connect(self.trans_msg)
        self.show_level_cb.stateChanged.connect(self.trans_msg)
        self.always_top_cb.stateChanged.connect(self.set_always_top)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint if self.always_top_cb.isChecked() else QtCore.Qt.Widget)


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


    def trans_msg(self):
        '''translate'''
        msg_text = self.message_box.toPlainText()
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


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = TransPopDialog()
    dialog.show()
    APP.exec_()
    os._exit(0)


