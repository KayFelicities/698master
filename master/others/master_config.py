"""master config file"""
import os
import configparser
import random
from master import config


class MasterConfig:
    """master config class"""
    def __init__(self, config_path=config.CONFIG_FILE_PATH):
        self.config_path = config_path
        config_dir = os.path.dirname(self.config_path)
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
        try:
            self.config = configparser.ConfigParser()
            self.config.read(self.config_path)
        except Exception:
            os.remove(self.config_path)
            self.config = configparser.ConfigParser()
            self.config.read(self.config_path)
        if not self.config.has_section('master'):
            self.config.add_section('master')
        if not self.config.has_section('commu'):
            self.config.add_section('commu')
        if not self.config.has_section('trans'):
            self.config.add_section('trans')

    def set_tmn_list(self, tmn_list):
        """set_tmn_list"""
        self.config.set('master', 'tmn_list', str(tmn_list))

    def get_tmn_list(self):
        """get_tmn_list"""
        if not self.config.has_option('master', 'tmn_list'):
            self.config.set('master', 'tmn_list', '[]')
        return self.config.get('master', 'tmn_list')

    def set_windows_top(self, is_windows_top):
        """set_windows_top"""
        self.config.set('master', 'is_windows_top', 'true' if is_windows_top else 'false')

    def get_windows_top(self):
        """get_windows_top"""
        if not self.config.has_option('master', 'is_windows_top'):
            self.config.set('master', 'is_windows_top', 'false')
        return self.config.getboolean('master', 'is_windows_top')

    def set_oad_r(self, oad):
        """set_oad_r"""
        self.config.set('master', 'oad_r', oad)

    def get_oad_r(self):
        """get_oad_r"""
        if not self.config.has_option('master', 'oad_r'):
            self.config.set('master', 'oad_r', '40000200')
        return self.config.get('master', 'oad_r')

    def set_serial_com(self, com):
        """set_serial_com"""
        self.config.set('commu', 'serial_com', com)

    def get_serial_com(self):
        """get_serial_com"""
        if not self.config.has_option('commu', 'serial_com'):
            self.config.set('commu', 'serial_com', 'COM1')
        return self.config.get('commu', 'serial_com')

    def set_serial_band_index(self, baud_index):
        """set_serial_band_index"""
        self.config.set('commu', 'serial_baud', str(baud_index))

    def get_serial_band_index(self):
        """get_serial_band_index"""
        if not self.config.has_option('commu', 'serial_baud'):
            self.config.set('commu', 'serial_baud', '0')
        return int(self.config.get('commu', 'serial_baud'))

    def set_master_addr(self, addr):
        """set_master_addr"""
        self.config.set('commu', 'master_addr', addr)

    def get_master_addr(self):
        """get_windows_top"""
        if not self.config.has_option('commu', 'master_addr'):
            self.config.set('commu', 'master_addr', '%02X'%random.randint(0, 255))
        return self.config.get('commu', 'master_addr')

    def set_serial_baud_index(self, baud_index):
        """set_windows_top"""
        self.config.set('commu', 'serial_baud', str(baud_index))

    def get_serial_baud_index(self):
        """get_windows_top"""
        if not self.config.has_option('commu', 'serial_baud'):
            self.config.set('commu', 'serial_baud', '3')
        return self.config.getint('commu', 'serial_baud')

    def set_frontend_ip(self, frontend_ip):
        """set_fontend"""
        self.config.set('commu', 'frontend_ip', frontend_ip)

    def get_frontend_ip(self):
        """get_fontend"""
        if not self.config.has_option('commu', 'frontend_ip'):
            self.config.set('commu', 'frontend_ip', '127.0.0.1:2017')
        return self.config.get('commu', 'frontend_ip')

    def set_server_port(self, port):
        """set_server"""
        self.config.set('commu', 'server_port', port)

    def get_server_port(self):
        """get_server"""
        if not self.config.has_option('commu', 'server_port'):
            self.config.set('commu', 'server_port', '0')
        return self.config.get('commu', 'server_port')

    def add_last_file(self, file_path):
        """add_last_file"""
        file_list = self.get_last_file()
        if file_path in file_list:
            file_list.remove(file_path)
        file_list.append(file_path)
        if len(file_list) > 10:
            file_list.pop(0)
        self.config.set('trans', 'file_list', str(file_list))

    def get_last_file(self):
        """get_last_file"""
        if not self.config.has_option('trans', 'file_list'):
            self.config.set('trans', 'file_list', '[]')
        return eval(self.config.get('trans', 'file_list'))

    def set_font_size(self, size):
        """set_font_size"""
        self.config.set('trans', 'font_size', str(size))

    def get_font_size(self):
        """get_font_size"""
        if not self.config.has_option('trans', 'font_size'):
            self.config.set('trans', 'font_size', '9')
        return int(self.config.get('trans', 'font_size'))

    def commit(self):
        """commit config"""
        with open(self.config_path, 'w') as file:
            self.config.write(file)
