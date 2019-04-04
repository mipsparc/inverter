#coding:utf-8

import FREQROL
import time


class Motor: 
    # 5km/h刻みの速度と周波数の係数
    speed_profile = [
        0.6, # 0-5
        0.7, # 5-10
        0.7, # 10-15
        0.7, # 15-20
        0.8, # 20-25
        0.8, # 25-30
        0.9, # 30-35
        0.9, # 35-40
        1.0, # 40-45
        1.9, # 45-50
        1.0, # 50-55
        1.0, # 55-60
        1.0, # 60-65
        1.0, # 65-70
        1.0, # 70-75
        1.0, # 75-80
        1.0, # 80-85
        1.0, # 85-90
        1.0, # 90-95
    ]
    
    # 周波数閾値とPWM変調周波数
    pwmfreq_profile = [
        [0.0, 1],
        [7.0, 2],
        [35.0, 3],
        [999.9, None] # dummy
    ]
    
    # 周波数閾値とスペクトラム拡散
    spectram_profile = [
        [0.0, False],
        [45, True],
        [999.9, None] # dummy
    ]
    
    def __init__(self):
        self.last_freq = None
        self.last_spectram = None
        self.last_pwmfreq = None
        
        self.max_speed = 90
        
        self.inverter = FREQROL.FREQROL()
        self.inverter.start()
        
    def getFreqFromSpeed(self, speed):
        freq = 0
        
        profile_num = int(speed // 5)
        if profile_num > 0:
            for p in self.speed_profile[:profile_num]:
                freq += p * 5
            
        freq += self.speed_profile[profile_num] * (speed % 5)
        return freq
    
    def getPWMfrqFromFreq(self, freq):
        for i, p in enumerate(self.pwmfreq_profile):
            if p[0] > freq:
                return self.pwmfreq_profile[i-1][1]
            
    def getSpectramFromFreq(self, freq):
        for i, p in enumerate(self.spectram_profile):
            if p[0] > freq:
                return self.spectram_profile[i-1][1]
    
    def setSpeedAndStatus(self, speed):
        if speed > self.max_speed:
            print('Too fast')
            raise ValueError
        
        freq = self.getFreqFromSpeed(speed)
        if freq != self.last_freq:
            self.inverter.set_freq(freq)
            self.last_freq = freq
        
        spectram = self.getSpectramFromFreq(freq)
        if spectram != self.last_spectram:
            self.inverter.set_spectram(spectram)
            self.last_spectram = spectram
        
        pwmfreq = self.getPWMfrqFromFreq(freq)
        if pwmfreq != self.last_pwmfreq:
            self.inverter.set_PWMfreq(pwmfreq)
            self.last_pwmfreq = pwmfreq
            
    def stop(self):
        self.inverter.set_freq(0)
        time.sleep(0.5)
        self.inverter.set_freq(0)
        time.sleep(0.5)
        self.inverter.set_freq(0)

if __name__ == '__main__':
    M = Motor()
    try:
        for i in range(0, 600, 3):
            M.setSpeedAndStatus(i * 0.1)
            time.sleep(0.07)
            
        for i in range(600, 0, -3):
            M.setSpeedAndStatus(i * 0.1)
            time.sleep(0.07)
    finally:
        M.stop()
        

