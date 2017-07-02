'''config'''
import os
import sys


MASTER_SOFTWARE_VERSION = 'V5.1Beta1'
MASTER_SOFTWARE_DT = '2017.06'
MASTER_WINDOW_TITLE_ADD = '_%s(%s)'%(MASTER_SOFTWARE_VERSION, MASTER_SOFTWARE_DT)
TRANS_SOFTWARE_VERSION = 'VT1.0'
TRANS_SOFTWARE_DT = '2017.05'
TRANS_WINDOW_TITLE_ADD = '_%s(%s)'%(TRANS_SOFTWARE_VERSION, TRANS_SOFTWARE_DT)

TRANS_WINDOW = None
ABOUT_WINDOW = None
MASTER_WINDOW = None

COMMU = None

if getattr(sys, 'frozen', False):
    SORTWARE_PATH = sys._MEIPASS
else:
    SORTWARE_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..')

M_PRIORITY_COLOR = {0: 'grey', 1: 'black', 2: 'blue', 3: 'red'}

MSG_TABLE_ROW_MAX = 1024

CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.698master/698master.conf')
MSG_LOG_DIR = os.path.join(os.path.expanduser('~'), '.698master/logs/')
