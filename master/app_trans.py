"""logfile translate"""
import sys
from master.UI.trans_ui import TransWindow
from master.UI.about_ui import AboutWindow
from master import config
from master.datas import k_data_s

if config.IS_USE_PYSIDE:
    from PySide import QtGui
else:
    from PyQt4 import QtGui


def main(file_path=''):
    """main"""
    config.K_DATA = k_data_s.Data698('123456')
    APP = QtGui.QApplication(sys.argv)
    config.ABOUT_WINDOW = AboutWindow()
    config.TRANS_WINDOW = TransWindow()
    config.TRANS_WINDOW.show()
    print(config.SOFTWARE_PATH)
    # if file_path:
    config.TRANS_WINDOW.openfile(file_path)
    APP.exec_()
    sys.exit(0)


if __name__ == "__main__":
    main()
