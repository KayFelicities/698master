"""master config file"""
import configparser
import random
from master import config


class MasterConfig:
    """master config class"""
    def __init__(self, config_path=config.CONFIG_FILE_PATH):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        if not self.config.has_section('master'):
            self.config.add_section('master')
        if not self.config.has_section('commu'):
            self.config.add_section('commu')


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


    def commit(self):
        """commit config"""
        with open(self.config_path, 'w') as file:
            self.config.write(file)
