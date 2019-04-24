"""communication"""
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
    """scan com port"""
    return [com[0] for com in list(serial.tools.list_ports.comports())]


class CommuPanel:
    """communication control panel class"""
    def __init__(self):
        self.serial_handle = None
        self.is_serial_running = False
        self.frontend_handle = None
        self.is_frontend_running = False
        self.server_handle = None
        self.is_server_running = False
        self.client_list = []

        self.master_addr = '00'

    def send_msg(self, m_text, chan_index):
        """send message"""
        m_list = common.text2list(m_text)
        send_b = b''.join(map(lambda x: struct.pack('B', int(x, 16)), m_list))
        if self.is_serial_running and chan_index in [-1, 0]:
            try:
                self.serial_handle.write(send_b)
                config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 0)
            except Exception:
                print('serial send err')
                self.serial_disconnect()
        if self.is_frontend_running and chan_index in [-1, 1]:
            try:
                self.frontend_handle.sendall(send_b)
                config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 1)
            except Exception:
                print('frontend send err')
                self.frontend_disconnect()

        if self.is_server_running and chan_index in [-1, 2]:
            for client_handle, client_addr in self.client_list:
                try:
                    client_handle.sendall(send_b)
                    print('send to client', client_addr)
                except Exception:
                    traceback.print_exc()
                    client_handle.close()
                    self.client_list.remove((client_handle, client_addr))
                    print('del client', client_addr)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 2)

    @staticmethod
    def receive_msg(m_text, chan_index):
        """receive msg to emit signal"""
        config.MASTER_WINDOW.receive_signal.emit(m_text, chan_index)

    def serial_connect(self, com, baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=0.05):
        """connect serial"""
        if self.is_serial_running:
            return 'err'
        try:
            self.serial_handle = serial.Serial(port=com, baudrate=baudrate, bytesize=bytesize,\
                                                parity=parity, stopbits=stopbits, timeout=timeout)
            self.serial_handle.close()
            self.serial_handle.open()
            self.is_serial_running = True
            threading.Thread(target=self.serial_read_loop).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'

    def serial_disconnect(self):
        """stop serial"""
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
        """serial loop"""
        re_msg_buf = []
        while True:
            try:
                new_data = self.serial_handle.read(1)
            except Exception:
                traceback.print_exc()
                print('serial_run err quit')
                break
            if new_data in [b'\x68', b'\x98']:
                re_data = b''
                while new_data:
                    re_data += new_data
                    new_data = self.serial_handle.read(4096)
                re_msg_buf += common.text2list(' '.join(['{0:02X}'.format(x) for x in re_data]))
                msgs = common.search_msg(re_msg_buf)
                for msg in msgs:
                    self.receive_msg(msg, 0)
                re_msg_buf = []
            if self.is_serial_running is False:
                print('serial_run quit')
                break

    def frontend_connect(self, addr):
        """connect"""
        if self.is_frontend_running:
            return 'err'
        port = int(addr.split(':')[1].replace(' ', ''))
        frontend_addr = (addr.split(':')[0].replace(' ', ''), port)
        try:
            self.frontend_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(frontend_addr)
            self.frontend_handle.connect(frontend_addr)
            # self.frontend_handle.settimeout(0.001)
            self.is_frontend_running = True
            threading.Thread(target=self.frontend_read_loop).start()
            threading.Thread(target=self.frontend_keep_alive).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'

    def frontend_disconnect(self):
        """stop serial"""
        if self.is_frontend_running is False:
            return 'ok'
        try:
            self.frontend_handle.shutdown(socket.SHUT_RDWR)
            self.frontend_handle.close()
            self.is_frontend_running = False
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'

    def frontend_keep_alive(self):
        """keep frontend server connect"""
        timer = time.time()
        while self.is_frontend_running:
            time.sleep(1)
            if time.time() - timer > 120:
                timer = time.time()
                m_list = common.text2list('FFFFFFFFFF')
                send_b = b''.join(map(lambda x: struct.pack('B', int(x, 16)), m_list))
                self.frontend_handle.sendall(send_b)

    def frontend_read_loop(self):
        """frontend loop"""
        re_msg_buf = []
        while True:
            try:
                re_byte = self.frontend_handle.recv(1)
            except Exception:
                print('frontend err quit')
                break
            if not re_byte:
                print('frontend disconnected')
                break
            if re_byte in [b'\x68', b'\x98']:
                re_byte += self.frontend_handle.recv(20480)
                re_msg_buf += common.text2list(''.join(['%02X ' % x for x in re_byte]))
                msgs = common.search_msg(re_msg_buf)
                for msg in msgs:
                    self.receive_msg(msg, 1)
                re_msg_buf = []
            if self.is_frontend_running is False:
                print('frontend_run quit')
                break
        self.frontend_disconnect()

    def server_start(self, server_port):
        """connect server"""
        if self.is_server_running:
            return 'err'
        try:
            self.server_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_handle.bind(('0.0.0.0', server_port))
            self.server_handle.listen(5)
            self.is_server_running = True
            threading.Thread(target=self.server_accept).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'

    def server_accept(self):
        """accept tcp client"""
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
        self.client_list = []

    def server_stop(self):
        """stop server"""
        if self.is_server_running is False:
            return 'ok'
        try:
            self.is_server_running = False
            for client in self.client_list:
                client[0].shutdown(socket.SHUT_RDWR)
                client[0].close()
            self.server_handle.close()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'

    def server_read_loop(self, client_handle, client_addr):
        """server loop"""
        re_msg_buf = []
        # client_handle.settimeout(0.001)
        while True:
            try:
                re_byte = client_handle.recv(1)
            except Exception:
                print(client_addr, 'client err quit')
                break
            if not re_byte:
                print('clint err quit')
                break
            if re_byte in [b'\x68', b'\x98']:
                re_byte += client_handle.recv(20480)
                re_msg_buf += common.text2list(''.join(['%02X ' % x for x in re_byte]))
                msgs = common.search_msg(re_msg_buf)
                for msg in msgs:
                    self.receive_msg(msg, 2)
                re_msg_buf = []
            if self.is_server_running is False:
                print('server_run quit')
                break
        client_handle.shutdown(socket.SHUT_RDWR)
        client_handle.close()
        self.client_list.remove((client_handle, client_addr))

    def quit(self):
        """quit"""
        self.serial_disconnect()
        self.frontend_disconnect()
        self.server_stop()
        print('commu quit')
        time.sleep(0.2)
