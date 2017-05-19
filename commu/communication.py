'''communication'''
import serial
import threading
import time
import traceback


class Communication():
    '''communication class'''
    def __init__(self):
        '''init'''
        self.serial_handle = None
        self.is_serial_running = False


    def connect_serial(self, com, baudrate=9600, parity='E', stopbits=1, timeout=0.05):
        '''connect serial'''
        try:
            self.serial_handle = serial.Serial(com, baudrate, parity, stopbits, timeout)
            self.serial_handle.close()
            self.serial_handle.open()
            self.is_serial_running = True
            threading.Thread(target=self.serial_loop).start()
            return 'ok'
        except Exception:
            traceback.print_exc()
            return 'err'


    def disconnect_serial(self):
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


    def serial_loop(self):
        '''serial loop'''
        while True:
            try:
                data_wait = self.serial_handle.inWaiting()
            except Exception:
                traceback.print_exc()
                break
            re_text = ''
            while data_wait > 0:
                re_data = self.serial_handle.readline()
                for re_char in re_data:
                    re_text += '{0:02X} '.format(re_char)
                time.sleep(0.03)
                data_wait = self.serial_handle.inWaiting()
            if re_text != '':
                config.serial_window._receive_signal.emit(re_text)
            if self.is_serial_running is False:
                print('serial_run quit')
                break


    def connect_front_server(self):
        '''connect_front_server'''
        pass


    def disconnect_front_server(self):
        '''stop front_server'''
        pass


    def start_server(self):
        '''connect server'''
        pass


    def stop_server(self):
        '''stop server'''
        pass

