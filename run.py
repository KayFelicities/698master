"""run app"""
import sys
from run_master import run_master
from run_trans import run_trans
from master import config


if __name__ == '__main__':
    print('software path: ', sys.argv[0])
    config.RUN_EXE_PATH = sys.argv[0]
    if len(sys.argv) > 1:
        run_trans(sys.argv[1])
    else:
        run_master()
