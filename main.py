#! /usr/bin/env python3
#encoding: utf-8

from Motor import Motor
from Kumoha import Kumoha
from Mascon import Mascon
import time

kumoha = Kumoha()
motor = Motor()
mascon = Mascon()

# メインループを0.1秒おきに回す
last_counter = time.time()

joy = mascon.getMasconAndBrake()


while True:
    try:
        mascon_data = joy.__next__()
        print(mascon_data)
        mascon_level, brake_level = mascon.convertJoyToMascon(mascon_data)
        
        kumoha.setMascon(mascon_level)
        kumoha.setBrake(brake_level)
        
        kumoha.advanceTime()
        # m/s
        speed = kumoha.getSpeed()
   
        kph = speed * 3600 / 1000
        
        motor.setSpeedAndStatus(kph)
        
        # 0.1秒経過するまでwaitする
        while (time.time() < last_counter + 0.1):
            time.sleep(0.001)
        last_counter = time.time()
        
        print('{}km/h'.format(int(speed)))
        
    except:
        motor.stop()
        raise
        


