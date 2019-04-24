"""logfile translate"""
import sys
from master.UI.trans_ui import TransWindow
from master.UI.about_ui import AboutWindow
from master import config
from master.datas import k_data_s

if config.IS_USE_PYSIDE:
    from PySide2 import QtCore, QtWidgets
else:
    from PyQt5 import QtCore, QtWidgets


def main(file_path=''):
    """main"""
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    config.K_DATA = k_data_s.Data698('123456')
    app = QtWidgets.QApplication(sys.argv)
    config.ABOUT_WINDOW = AboutWindow()
    config.TRANS_WINDOW = TransWindow()
    config.TRANS_WINDOW.show()
    print(config.SOFTWARE_PATH)
    # if file_path:
    config.TRANS_WINDOW.openfile(file_path)
    app.exec_()
    sys.exit(0)


if __name__ == "__main__":
    main()
