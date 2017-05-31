'''config'''
import os
import sys


SOFTWARE_VERSION = 'V5.0Beta2'
SOFTWARE_DT = '2017.05'
WINDOWS_TITLE_ADD = '_%s(%s)'%(SOFTWARE_VERSION, SOFTWARE_DT)

TRANS_WINDOW = None
ABOUT_WINDOW = None
MASTER_WINDOW = None

if getattr(sys, 'frozen', False):
    SORTWARE_PATH = sys._MEIPASS
else:
    SORTWARE_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..')

M_PRIORITY_COLOR = {0: 'grey', 1: 'black', 2: 'blue', 3: 'red'}
