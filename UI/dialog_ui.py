'''dialog windows'''
import sys
import os
from PyQt4 import QtGui, QtCore


class TransPopDialog(QtGui.QWidget):
    '''translate window'''
    def __init__(self):
        # QtGui.QDialog.__init__(self, parent)
        super().__init__()
        self.setWindowTitle('详细解析')
        centralwidget = QtGui.QWidget()
        splitter = QtGui.QSplitter(centralwidget)
        splitter.setOrientation(QtCore.Qt.Vertical)
        message_box = QtGui.QTextEdit(splitter)
        message_box.setObjectName('message_box')
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        size_policy.setHintSize(QtCore.QSize(210, 0))
        message_box.setSizePolicy(size_policy)
        explain_box = QtGui.QTextEdit(splitter)
        explain_box.setObjectName('explain_box')
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        size_policy.setVerticalStretch(10)
        explain_box.setSizePolicy(size_policy)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(splitter)
        # vbox.addWidget(explain_box)
        self.setLayout(vbox)
        self.resize(500, 700)


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = TransPopDialog()
    dialog.show()
    APP.exec_()
    os._exit(0)


