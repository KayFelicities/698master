'''main'''
import sys
import os
from UI.trans_ui2 import TransWindow
from UI.about_ui import AboutWindow
from UI.master_ui import MasterWindow
from PyQt4 import QtGui
import config

if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    config.ABOUT_WINDOW = AboutWindow()
    config.TRANS_WINDOW = TransWindow()
    config.MASTER_WINDOW = MasterWindow()
    config.MASTER_WINDOW.show()
    APP.exec_()
    os._exit(0)
