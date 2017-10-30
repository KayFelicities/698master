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


class CommuPanel():
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
            self.serial_handle.write(send_b)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 0)
        if self.is_frontend_running and chan_index in [-1, 1]:
            self.frontend_handle.sendall(send_b)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 1)

        def send_to_client(client_handle, client_addr):
            """send"""
            try:
                client_handle.sendall(send_b)
                print('send to client', client_addr)
            except Exception:
                self.client_list.remove((client_handle, client_addr))
                print('del client', client_addr)

        if self.is_server_running and chan_index in [-1, 2]:
            for client_handle, client_addr in self.client_list:
                send_to_client(client_handle, client_addr)
            config.MASTER_WINDOW.send_signal.emit(common.format_text(m_text), 2)


    def receive_msg(self, m_text, chan_index):
        """receive msg to emit signal"""
        config.MASTER_WINDOW.receive_signal.emit(m_text, chan_index)


    def serial_connect(self, com, baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=0):
        """connect serial"""
        if self.is_serial_running:
            return 'err'
        try:
            self.serial_handle = serial.Serial(com, baudrate, bytesize, parity, stopbits, timeout)
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
                data_wait = self.serial_handle.inWaiting()
            except Exception:
                traceback.print_exc()
                print('serial_run err quit')
                break
            re_text = ''
            while data_wait > 0:
                re_data = self.serial_handle.read(256)
                for re_char in re_data:
                    re_text += '{0:02X} '.format(re_char)
                data_wait = self.serial_handle.inWaiting()
            if re_text != '':
                re_msg_buf += common.text2list(re_text)
                if re_msg_buf and re_msg_buf[0] == '68' and re_msg_buf[-1] != '16':  # in case of serial msg break
                    continue
                try:
                    msgs = common.search_msg(re_msg_buf)
                except IndexError:  # break in half of the msg but 16 is just the end byte
                    traceback.print_exc()
                    continue
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
            self.is_frontend_running = True
            threading.Thread(target=self.frontend_read_loop).start()
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


    def frontend_read_loop(self):
        """frontend loop"""
        self.frontend_handle.setblocking(False)
        re_msg_buf = []
        while True:
            try:
                re_byte = self.frontend_handle.recv(4096)
                re_text = ''.join(['%02X ' % x for x in re_byte])
            except Exception:
                # keep connect
                if self.is_frontend_running is False:
                    print('frontend quit')
                    break
                continue
            if re_text != '':
                re_msg_buf += common.text2list(re_text)
                if re_msg_buf and re_msg_buf[0] == '68' and re_msg_buf[-1] != '16':  # in case of msg break
                    continue
                try:
                    msgs = common.search_msg(re_msg_buf)
                except IndexError:  # break in half of the msg but 16 is just the end byte
                    traceback.print_exc()
                    continue
                for msg in msgs:
                    self.receive_msg(msg, 1)
                re_msg_buf = []


    def server_start(self, server_port):
        """connect server"""
        if self.is_server_running:
            return 'err'
        try:
            self.server_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_handle.bind(('0.0.0.0', server_port))
            self.server_handle.listen(1)
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


    def server_stop(self):
        """stop server"""
        if self.is_server_running is False:
            return 'ok'
        try:
            self.is_server_running = False
            # self.server_handle.shutdown(socket.SHUT_RDWR)
            self.server_handle.close()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def server_read_loop(self, client_handle, client_addr):
        """server loop"""
        client_handle.setblocking(False)
        re_msg_buf = []
        while True:
            try:
                re_byte = client_handle.recv(4096)
                re_text = ''.join(['%02X ' % x for x in re_byte])
            except Exception:
                if self.is_server_running is False:
                    client_handle.shutdown(socket.SHUT_RDWR)
                    client_handle.close()
                    self.client_list.remove((client_handle, client_addr))
                    print(client_addr, 'client quit')
                    break
                continue
            if re_text != '':
                re_msg_buf += common.text2list(re_text)
                if re_msg_buf and re_msg_buf[0] == '68' and re_msg_buf[-1] != '16':  # in case of msg break
                    continue
                try:
                    msgs = common.search_msg(re_msg_buf)
                except IndexError:  # break in half of the msg but 16 is just the end byte
                    traceback.print_exc()
                    continue
                for msg in msgs:
                    self.receive_msg(msg, 2)
                re_msg_buf = []


    def quit(self):
        """quit"""
        self.serial_disconnect()
        self.frontend_disconnect()
        self.server_stop()
        print('commu quit')
        time.sleep(0.2)
