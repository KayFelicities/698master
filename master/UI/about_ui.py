"""about ui"""
import os
import sys
from master import config
if config.IS_USE_PYSIDE:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore


class AboutWindow(QtGui.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setup_ui()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


    def setup_ui(self):
        """layout"""
        self.setWindowTitle('关于')
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.SOFTWARE_PATH, config.MASTER_ICO_PATH)))

        self.head_img = QtGui.QLabel()
        self.head_img.setText('<img src="{master_logo}" height="72"></img><span> </span><img src="{trans_logo}" height="72"></img>'\
                            .format(master_logo=os.path.join(config.SOFTWARE_PATH, config.MASTER_ICO_PATH),\
                                    trans_logo=os.path.join(config.SOFTWARE_PATH, config.TRANS_ICO_PATH)))
        self.head_ver = QtGui.QLabel()
        self.head_ver.setText('<p style="font-family: 微软雅黑; font-size: 16px;" align="center">\
                                <b>698后台/698日志解析<br>{version}({dt})</b></p>'\
                                .format(version=config.MASTER_SOFTWARE_VERSION, dt=config.MASTER_SOFTWARE_DT))
        self.head_hbox = QtGui.QHBoxLayout()
        self.head_hbox.addStretch(1)
        self.head_hbox.addWidget(self.head_img)
        self.head_hbox.addWidget(self.head_ver)
        self.head_hbox.addStretch(1)

        self.about_box = QtGui.QTextBrowser()
        with open(os.path.join(config.SOFTWARE_PATH, 'docs/dev_log.html'), encoding='utf-8') as dev_log:
            text = dev_log.read() + '<h3>如果您喜欢这个软件，希望您能支持我:</h3>' +\
                    '<center><img src="{alipay}" height="350"></center>'.format(alipay=os.path.join(config.SOFTWARE_PATH, config.ALIPAY_IMG))
            self.about_box.setText(text)

        self.foot_text = QtGui.QLabel()
        self.foot_text.setText('<p align="center">Designed by Kay. Powered by SX Company.')
        self.foot_hbox = QtGui.QHBoxLayout()
        self.foot_hbox.addStretch(1)
        self.foot_hbox.addWidget(self.foot_text)
        self.foot_hbox.addStretch(1)

        self.main_vbox = QtGui.QVBoxLayout()
        self.main_vbox.setContentsMargins(1, 1, 1, 1)
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
    sys.exit(0)
