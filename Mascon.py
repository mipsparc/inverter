import pygame
from time import sleep

class Mascon:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

    def getMasconAndBrake(self):
        buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while True:
            pygame.event.get()
            buttons[0] = self.joy.get_button(0)
            buttons[4] = self.joy.get_button(4)
            buttons[5] = self.joy.get_button(5)
            buttons[6] = self.joy.get_button(6)
            buttons[7] = self.joy.get_button(7)

            ax = self.joy.get_axis(0)
            if ax < 0:
                axis = -1
            elif ax == 0.0:
                axis = 0
            elif ax > 0:
                axis = 1
            yield [buttons, axis]

    def convertJoyToMascon(self, joy):
        if joy == [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], -1]:
            return [0, 9]
        if joy == [[0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], -1]:
            return [0, 8]
        if joy == [[0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0], -1]:
            return [0, 7]
        if joy == [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], -1]:
            return [0, 6]
        if joy == [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], -1]:
            return [0, 5]
        if joy == [[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], -1]:
            return [0, 4]
        if joy == [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], -1]:
            return [0, 3]
        if joy == [[0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0], -1]:
            return [0, 2]
        if joy == [[0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], -1]:
            return [0, 1]
        if joy == [[1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], 1]:
            return [1, 0]
        if joy == [[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], 1]:
            return [2, 0]
        if joy == [[1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], -1]:
            return [3, 0]
        #if joy == [[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], -1]:
        #    return [4, 0]
        if joy == [[1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], 0]:
            return [5, 0]

        return [0,0]

if __name__ == '__main__':
    m = Mascon()
    joy = m.getMasconAndBrake()
    while True:
        data = joy.__next__()
        print(m.convertJoyToMascon(data))
        print(data)
        sleep(0.5)
