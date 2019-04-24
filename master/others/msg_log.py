"""log class"""
import os
import datetime
from master import config


class MsgLog:
    """logger class"""
    def __init__(self, log_dir=config.MSG_LOG_DIR):
        now = datetime.datetime.now()
        self.log_dir = log_dir
        self.file_path = os.path.join(log_dir, now.strftime('%Y-%m-%d') + '_msg.log')
        print('LOG path: ', self.file_path)
        config.LOG_PATH = self.file_path
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)
        with open(self.file_path, 'a', encoding='gb2312') as log:
            log_time = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            log.write('\n' + '='*10 + log_time + '='*10 + '\n')

    def add_log(self, terminal_addr, chan_text, direction, brief, msg):
        """add msg row to log"""
        log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'a', encoding='gb2312') as log:
                log.write('\n' + '='*10 + log_time + '='*10 + '\n')

        with open(self.file_path, 'a', encoding='gb2312') as log:
            log.write('[{time}] [{addr}] [{chan}{dir}] ({brief}) <{msg}>\n'\
                        .format(time=log_time, addr=terminal_addr, chan=chan_text,\
                        brief=brief, dir=direction, msg=msg))

