#coding:utf-8

import serial
import time

class FREQROL:
    def __init__(self):
        self.ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        timeout=0.2,
        write_timeout=0.2
        )
        
    def start(self):
        self.send('FA02')
        
    def stop(self):
        self.send('FA00')
    
    def add_checksum(self, payload):
        sum = 0
        for c in payload:
            sum += ord(c)
        return payload + hex(sum)[-2:].upper()

    def send(self, data):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        header = '\x05'
        payload = '00' + data
        payload_with_checksum = self.add_checksum(payload)
        self.ser.write((header + payload_with_checksum).encode('ascii'))
        time.sleep(0.05)
        
    # 1桁のPWM周波数コード(0 - 9)
    def set_PWMfreq(self, freq):
        self.send('C8000' + str(freq)[0])
        
    # スペクトラム拡散を設定する
    def set_spectram(self, status):
        self.send('FF02')
        
        if status:
            self.send('B00001')
        else:
            self.send('B00000')

        self.send('FF00')
            
    # 周波数 (0 - 120)
    def set_freq(self, freq):
        if not 0 <= freq < 120:
            print("INVALID FREQ!")
            return
        
        freq_str = hex(int(freq * 100))[2:].upper()
        freq_zerofilled_str = freq_str.zfill(4)
        self.send('ED' + freq_zerofilled_str)
