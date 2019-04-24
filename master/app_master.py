"""master app"""
import sys
from master.UI.trans_ui import TransWindow
from master.UI.about_ui import AboutWindow
from master.UI.master_ui import MasterWindow
from master.commu import communication
from master import config
from master.datas import k_data_s
if config.IS_USE_PYSIDE:
    from PySide import QtGui
else:
    from PyQt4 import QtGui


def main():
    """main"""
    config.K_DATA = k_data_s.Data698('123456')
    APP = QtGui.QApplication(sys.argv)
    config.COMMU = communication.CommuPanel()
    config.ABOUT_WINDOW = AboutWindow()
    config.TRANS_WINDOW = TransWindow()
    config.MASTER_WINDOW = MasterWindow()
    config.MASTER_WINDOW.show()
    config.MASTER_WINDOW.show_commu_window()
    APP.exec_()
    os._exit(0)


if __name__ == "__main__":
    main()
