#! /usr/bin/env python3
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

class ElectricCar:    
    def __init__(self):
        # 5km/h刻みの速度と周波数の係数とスペクトラム拡散可否、PWM変調周波数
        self.speed_profile = [
            [2.5, False, 0], # 0-5
            [2.0, False, 0], # 5-10
            [1.5, False, 0], # 10-15
            [1.5, False, 1], # 15-20
            [1.5, False, 1], # 20-25
            [1.5, False, 1], # 25-30
            [1.5, False, 1], # 30-35
            [1.5, False, 1], # 35-40
            [1.5, False, 1], # 40-45
            [1.5, False, 1], # 45-50
            [1.5, False, 1], # 50-55
            [1.5, False, 1], # 55-60
        ]
        
        self.speed = 0
        
        self.last_freq = 0
        self.last_spectram = False
        self.last_pwmfreq = 0
        
        self.max_speed = 60
        
        self.inverter = FREQROL()
        self.inverter.start()
        
    def getProfileFromSpeed(self, speed):
        freq = 0
        
        profile_num = int(speed // 5)
        profile_of_speed = self.speed_profile[profile_num]
        if profile_num > 0:
            for p in self.speed_profile[:profile_num]:
                freq += p[0] * 5
            
        freq += profile_of_speed[0] * (speed % 5)
        return {'freq':freq, 'spectram':profile_of_speed[1], 'pwmfreq':profile_of_speed[2]}
    
    def setSpeedAndStatus(self, speed):
        if speed > self.max_speed:
            print('Too fast')
            return
        
        profile = self.getProfileFromSpeed(speed)
        freq = profile['freq']
        if freq != self.last_freq:
            self.inverter.set_freq(freq)
            self.last_freq = freq
        print(freq)
        spectram = profile['spectram']
        if spectram != self.last_spectram:
            self.inverter.set_spectram(spectram)
            self.last_spectram = spectram
        
        pwmfreq = profile['pwmfreq']
        if pwmfreq != self.last_pwmfreq:
            self.inverter.set_PWMfreq()
            self.last_pwmfreq = pwmfreq

E = ElectricCar()
try:
    for i in range(500):
        E.setSpeedAndStatus(i * 0.1)
        time.sleep(0.07)
finally:
    E.setSpeed(0)

#f = FREQROL()
#f.start()
#f.set_spectram(False)
#f.set_freq(9)
#time.sleep(0.7)
#f.set_freq(100)
#time.sleep(3)
#f.set_spectram(True)
#time.sleep(5)
#f.set_spectram(False)
#f.set_freq(2)
#time.sleep(9)
#f.set_freq(0)
