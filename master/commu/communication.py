'''communication'''
import socket
import threading
import time
import traceback
import struct
import serial
import serial.tools.list_ports
from master import config
from master.trans import common


def serial_com_scan():
    '''scan com port'''
    return [com[0] for com in list(serial.tools.list_ports.comports())]


class CommuPanel():
    '''communication control panel class'''
    def __init__(self):
        self.serial_handle = None
        self.is_serial_running = False
        self.frontend_handle = None
        self.is_frontend_running = False
        self.server_handle = None
        self.is_server_running = False
        self.client_list = []


    def send_msg(self, m_text, chanel='all'):
        '''send message'''
        m_list = common.text2list(m_text)
        send_b = b''.join(map(lambda x: struct.pack('B', int(x, 16)), m_list))
        if self.is_serial_running and chanel in ['all', 'serial']:
            self.serial_handle.write(send_b)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), '串口')
        if self.is_frontend_running and chanel in ['all', 'frontend']:
            self.frontend_handle.sendall(send_b)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), '前置机')

        def send_to_client(client_handle, client_addr):
            '''send'''
            try:
                client_handle.sendall(send_b)
                print('send to client', client_addr)
            except Exception:
                self.client_list.remove((client_handle, client_addr))
                print('del client', client_addr)

        if self.is_server_running and chanel in ['all', 'server']:
            for client_handle, client_addr in self.client_list:
                send_to_client(client_handle, client_addr)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 'server')


    def serial_connect(self, com, baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=0.05):
        '''connect serial'''
        if self.is_serial_running:
            return 'err'
        self.serial_handle = serial.Serial(com, baudrate, bytesize, parity, stopbits, timeout)
        try:
            self.serial_handle.close()
            self.serial_handle.open()
            self.is_serial_running = True
            threading.Thread(target=self.serial_read_loop).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def serial_disconnect(self):
        '''stop serial'''
        if self.is_serial_running is False:
            return 'ok'
        try:
            self.serial_handle.close()
            self.is_serial_running = False
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def serial_read_loop(self):
        '''serial loop'''
        while True:
            try:
                data_wait = self.serial_handle.inWaiting()
            except Exception:
                traceback.print_exc()
                print('serial_run err quit')
                break
            re_text = ''
            while data_wait > 0:
                re_data = self.serial_handle.readline()
                for re_char in re_data:
                    re_text += '{0:02X} '.format(re_char)
                time.sleep(0.03)
                data_wait = self.serial_handle.inWaiting()
            if re_text != '':
                config.MASTER_WINDOW.receive_signal.emit(re_text, '串口')
            if self.is_serial_running is False:
                print('serial_run quit')
                break


    def frontend_connect(self, addr):
        '''connect'''
        if self.is_frontend_running:
            return 'err'
        port = int(addr.split(':')[1])
        frontend_addr = (addr.split(':')[0], port)
        self.frontend_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(frontend_addr)
            self.frontend_handle.connect(frontend_addr)
            self.is_frontend_running = True
            threading.Thread(target=self.frontend_read_loop).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'

    def frontend_disconnect(self):
        '''stop serial'''
        if self.is_frontend_running is False:
            return 'ok'
        try:
            self.frontend_handle.close()
            self.is_frontend_running = False
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def frontend_read_loop(self):
        '''frontend loop'''
        while True:
            try:
                re_byte = self.frontend_handle.recv(4096)
                re_text = ''.join(['%02X ' % x for x in re_byte])
            except Exception:
                traceback.print_exc()
                print('frontend err quit')
                break
            if re_text != '':
                config.MASTER_WINDOW.receive_signal.emit(re_text, '前置机')
            if self.is_frontend_running is False:
                print('frontend quit')
                break


    def server_start(self, server_port):
        '''connect server'''
        if self.is_server_running:
            return 'err'
        self.server_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_handle.bind(('0.0.0.0', server_port))
        try:
            self.server_handle.listen(1)
            self.is_server_running = True
            threading.Thread(target=self.server_accept).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def server_accept(self):
        '''accept tcp client'''
        while True:
            try:
                client_handle, client_addr = self.server_handle.accept()
                self.client_list.append((client_handle, client_addr))
                print(client_addr, "connected")
                threading.Thread(target=self.server_read_loop, args=(client_handle, client_addr)).start()
            except Exception:
                print('server_run err quit')
                break
            if self.is_server_running is False:
                print('server_run quit')
                break


    def server_stop(self):
        '''stop server'''
        if self.is_server_running is False:
            return 'ok'
        try:
            self.server_handle.close()
            self.is_server_running = False
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def server_read_loop(self, client_handle, client_addr):
        '''server loop'''
        while True:
            try:
                re_byte = client_handle.recv(4096)
                re_text = ''.join(['%02X ' % x for x in re_byte])
            except Exception:
                traceback.print_exc()
                print(client_addr, 'client err quit')
                self.client_list.remove((client_handle, client_addr))
                break
            if re_text != '':
                config.MASTER_WINDOW.receive_signal.emit(re_text, 'server')
            if self.is_server_running is False:
                print(client_addr, 'client quit')
                self.client_list.remove((client_handle, client_addr))
                break
