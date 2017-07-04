'''run log file translate app'''
import sys
from master.app_trans import main


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
