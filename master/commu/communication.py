'''communication'''
import serial
import serial.tools.list_ports
import socket
import threading
import time
import traceback
import struct
from master import config
from master.trans import common


def serial_com_scan():
    '''scan com port'''
    return [com[0] for com in list(serial.tools.list_ports.comports())]


class Serial():
    '''serial communication class'''
    def __init__(self, com, baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=0.05):
        '''init'''
        self.port = com
        self.serial_handle = serial.Serial(com, baudrate, bytesize, parity, stopbits, timeout)
        self.is_serial_running = False


    def send_msg(self, m_text):
        '''send message'''
        m_list = common.text2list(m_text)
        send_b = b''.join(map(lambda x: struct.pack('B', int(x, 16)), m_list))
        if self.is_serial_running:
            self.serial_handle.write(send_b)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), self.port)


    def connect(self):
        '''connect serial'''
        try:
            self.serial_handle.close()
            self.serial_handle.open()
            self.is_serial_running = True
            threading.Thread(target=self.read_loop).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def disconnect(self):
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


    def read_loop(self):
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
                config.MASTER_WINDOW.receive_signal.emit(re_text, self.port)
            if self.is_serial_running is False:
                print('serial_run quit')
                break



class Frontend():
    '''frontend communication class'''
    def __init__(self, addr):
        '''init'''
        self.frontend_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_frontend_running = False
        port = int(addr.split(':')[1])
        self.frontend_addr = (addr.split(':')[0], port)


    def send_msg(self, m_text):
        '''send message'''
        m_list = common.text2list(m_text)
        send_b = b''.join(map(lambda x: struct.pack('B', int(x, 16)), m_list))
        if self.is_frontend_running:
            self.frontend_handle.sendall(send_b)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), '前置机')


    def connect(self):
        '''connect'''
        try:
            print(self.frontend_addr)
            self.frontend_handle.connect(self.frontend_addr)
            self.is_frontend_running = True
            threading.Thread(target=self.read_loop).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'

    def disconnect(self):
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


    def read_loop(self):
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


class Server():
    '''server communication class'''
    def __init__(self, server_port):
        '''init'''
        self.server_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_handle.bind(('0.0.0.0', server_port))
        self.client_list = []
        self.is_server_running = False


    def send_msg(self, m_text):
        '''send message'''
        m_list = common.text2list(m_text)
        send_b = b''.join(map(lambda x: struct.pack('B', int(x, 16)), m_list))
        def send_to_client(client_handle, client_addr):
            '''send'''
            try:
                client_handle.sendall(send_b)
                print('send to client', client_addr)
            except Exception:
                self.client_list.remove((client_handle, client_addr))
                print('del client', client_addr)

        if self.is_server_running:
            for client_handle, client_addr in self.client_list:
                send_to_client(client_handle, client_addr)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 'server')


    def start(self):
        '''connect server'''
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
                threading.Thread(target=self.read_loop, args=(client_handle, client_addr)).start()
            except Exception:
                print('server_run err quit')
                break
            if self.is_server_running is False:
                print('server_run quit')
                break


    def stop(self):
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


    def read_loop(self, client_handle, client_addr):
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
