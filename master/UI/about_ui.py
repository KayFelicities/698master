'''about ui'''
import os
import sys
from PyQt4 import QtGui, QtCore
from master import config


class AboutWindow(QtGui.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setup_ui()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


    def setup_ui(self):
        '''layout'''
        self.setWindowTitle('关于')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SORTWARE_PATH, 'imgs/698.png')))

        self.head_img = QtGui.QLabel()
        self.head_ver = QtGui.QLabel()
        about_img = '<img src="imgs/698.png" height="70" width="70"></img>'
        about_ver = '<p style="font-family: 微软雅黑; font-size: 16px; float: right" align="center">\
                        <b>698后台_{version}<br>{dt}</b></p>'\
                        .format(version=config.SOFTWARE_VERSION, dt=config.SOFTWARE_DT)
        self.head_img.setText(about_img)
        self.head_ver.setText(about_ver)
        self.head_hbox = QtGui.QHBoxLayout()
        self.head_hbox.addStretch(1)
        self.head_hbox.addWidget(self.head_img)
        self.head_hbox.addWidget(self.head_ver)
        self.head_hbox.addStretch(1)

        self.about_box = QtGui.QTextBrowser()
        with open(os.path.join(config.SORTWARE_PATH, 'docs/dev_log.html'), encoding='utf-8') as dev_log:
            self.about_box.setText(dev_log.read())

        self.foot_text = QtGui.QLabel()
        self.foot_text.setText('<p align="center">Designed by Kay. Powered by Qt Company.')
        self.foot_hbox = QtGui.QHBoxLayout()
        self.foot_hbox.addStretch(1)
        self.foot_hbox.addWidget(self.foot_text)
        self.foot_hbox.addStretch(1)

        self.main_vbox = QtGui.QVBoxLayout()
        self.main_vbox.setMargin(1)
        self.main_vbox.setSpacing(5)
        self.main_vbox.addLayout(self.head_hbox)
        self.main_vbox.addWidget(self.about_box)
        self.main_vbox.addLayout(self.foot_hbox)
        self.setLayout(self.main_vbox)
        self.resize(500, 600)


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    dialog = AboutWindow()
    dialog.show()
    APP.exec_()
    os._exit(0)
