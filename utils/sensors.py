import RPi.GPIO as gpio
import numpy as np
import time

class encoder():
    def __init__(self):
        self.pin_left_encoder_pin, self.pin_right_encoder_pin = 7, 12
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin_left_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # front left encoder pin
        gpio.setup(self.pin_right_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # back right encoder pin

    def __del__(self):
        gpio.cleanup()

    def count(self, left_or_right):
        if left_or_right not in ['left', 'right']:
            raise AttributeError('Wrong input given to encoder')
        pin = self.pin_left_encoder_pin if left_or_right == 'left' else self.pin_right_encoder_pin

        counter = np.uint64(0)
        button = int(0)
        time.sleep(0.01)

        for i in range(0, 1000):
            print('counter = ', counter, "GPIO state: ", gpio.input(pin))
            if int(gpio.input(pin)) != int(button):
                button = int(gpio.input(pin))
                counter += 1
            print('encoder count to ', counter)
            if counter >= 50:
                print("endcoder count finished")
                break

    def reach(self, left_or_right, count_goal):
        if left_or_right not in ['left', 'right']:
            raise AttributeError()
        pin = self.pin_left_encoder_pin if left_or_right == 'left' else self.pin_right_encoder_pin

        counter = np.uint64(0)
        button = int(0)
        time.sleep(0.01)

        for i in range(0, 1000):
            if int(gpio.input(pin)) != int(button):
                button = int(gpio.input(pin))
                counter += 1
            print('encoder count to ', counter)
            if counter >= count_goal:
                print('reach the goal count')
                return True
        return False


if __name__ == '__main__':
    print('testing left encoder')
    encoder_ = encoder()
    encoder_.count('left')
    print('left encoder tested')

    print('testing right encoder')
    encoder_ = encoder()
    encoder_.count('right')
    print('right encoder tested')
