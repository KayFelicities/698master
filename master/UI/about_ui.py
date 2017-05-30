'''about ui'''
import sys
from PyQt4 import QtGui, QtCore
from master import config


class AboutWindow(QtGui.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setup_ui()


    def setup_ui(self):
        '''layout'''
        self.setWindowTitle('关于')
        self.setWindowIcon(QtGui.QIcon('imgs/698.png'))

        self.about_box = QtGui.QTextBrowser()
        with open('docs/dev_log.html', mode='r', encoding='utf-8') as dev_log:
            self.about_box.setText(dev_log.read())

        self.main_vbox = QtGui.QVBoxLayout()
        self.main_vbox.setMargin(1)
        self.main_vbox.setSpacing(1)
        self.main_vbox.addWidget(self.about_box)
        self.setLayout(self.main_vbox)
        self.resize(500, 600)


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = AboutWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
