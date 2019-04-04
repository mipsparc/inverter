#coding:utf-8

class Kumoha:
    # m/s, m/s^2
    accel_profile = [
        [0.0, 0.803],
        [3.6, 0.5],
        [8.3, 0.333],
        [11.6, 0.222],
        [15.0, 0.194],
        [21.0, 0.10],
        [23.0, 0.05],
        [23.5, 0],
        [999.9, None], #dummy
    ]
    
    bc_map = [0, 0.4, 0.5, 0.6, 0.70, 0.80, 0.90, 1.4, 2.0, 99] 
    
    def __init__(self):
        # 車速(m/s)
        self.speed = 0
        self.accel = 0
        self.mascon_level = 0
        # ブレーキシリンダ圧力(減速度)
        self.bc = 0
        # 最大ブレーキシリンダ圧力
        self.BC_MAX = 3.0
        # 非常ブレーキ状態
        self.eb = False
        # 乗客乗車時の加速度減少(単機: 1)
        self.freight = 0.8

    def getAccelFromSpeed(self, speed):
        for i, p in enumerate(self.accel_profile):
            if p[0] > speed:
                return self.accel_profile[i-1][1]
            
    # 外部でmascon_level, bc
    # 0.1秒進める
    def advanceTime(self):
        # 加速度を求める(m/s2)
        max_accel = self.getAccelFromSpeed(self.speed)
        self.accel = (max_accel / 5) * self.mascon_level
        
        # 減速度(m/s2 max ±5.0m/s2) ここは実物に則さない
        if self.bc < 0:
            self.bc = 0
        elif self.bc > self.BC_MAX:
            self.bc = self.BC_MAX
            
        # 加減速計算
        self.speed = self.speed + (self.accel - self.bc) * 0.1 * self.freight
        if self.speed < 0:
            self.speed = 0
            
        # OSR 85km/hを超えると非常ブレーキ
        if self.speed > 23.6:
            self.eb = True

        # 非常ブレーキ
        if self.eb:
            self.bc = 5.0
            # 十分に低速になったら自動で復位
            if self.speed < 1:
                self.eb = False

    def getSpeed(self):
        return self.speed
    
    # 0 ~ 5のマスコンノッチを入力 EB時は力行不可
    def setMascon(self, mascon_level):
        if not self.eb:
            self.mascon_level = mascon_level
        else:
            self.mascon_level = 0
    
    # ブレーキシリンダ圧力を入力
    def setBrake(self, brake_level):
        self.bc = self.bc_map[brake_level]
