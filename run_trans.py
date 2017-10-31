"""run log file translate app"""
import sys
from master.app_trans import main


def run_trans(file_path=''):
    """run master"""
    main(file_path)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_trans(sys.argv[1])
    else:
        run_trans()
