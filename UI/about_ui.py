'''about ui'''
from PyQt4 import QtGui
from UI.about_window import Ui_AboutWindow
import config
from doc.dev_log import LOG


class AboutWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_AboutWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)
        self.about_box.setText(LOG)
        self.version_tag.setText('''<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;">
<p align="center" style=" margin-top:0px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; font-weight:600;">698解析工具_''' + config.SOFTWARE_VERSION + '''</span></p>
<p align="center" style=" margin-top:0px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; font-weight:600;">终端通信部内部测试版</span></p>
<p align="center" style=" margin-top:0px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; font-weight:600;">''' + config.SOFTWARE_DT + '''</span></p></body></html>''')
