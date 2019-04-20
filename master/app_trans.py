"""logfile translate"""
import sys
import os
from master.UI.trans_ui import TransWindow
from master.UI.about_ui import AboutWindow
from master import config
from master.datas import k_data_s

if config.IS_USE_PYSIDE:
    from PySide2 import QtWidgets
else:
    from PyQt5 import QtWidgets


def main(file_path=''):
    """main"""
    config.K_DATA = k_data_s.Data698('123456')
    app = QtWidgets.QApplication(sys.argv)
    config.ABOUT_WINDOW = AboutWindow()
    config.TRANS_WINDOW = TransWindow()
    config.TRANS_WINDOW.show()
    print(config.SORTWARE_PATH)
    # if file_path:
    config.TRANS_WINDOW.openfile(file_path)
    app.exec_()
    os._exit(0)


if __name__ == "__main__":
    main()
