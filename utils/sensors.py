import RPi.GPIO as gpio
import numpy as np
import time

class encoder():
    def __init__(self):
        self.pin_left_encoder_pin, self.pin_right_encoder_pin = 7, 12
        gpio.setup(self.pin_left_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # front left encoder pin
        gpio.setup(self.pin_right_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # back right encoder pin

    def __del__(self):
        gpio.cleanup()

    def count(self, left_or_right):
        if left_or_right not in ['left', 'right']:
            raise AttributeError()
        pin = self.pin_left_encoder_pin if left_or_right == 'left' else self.pin_right_encoder_pin

        counter = np.uint64(0)
        button = int(0)
        time.sleep(0.1)

        for i in range(0, 1000):
            print('counter = ', counter, "GPIO state: ", gpio.input(12))
            if int(gpio.input()) != int(button):
                button = int(gpio.input(pin))
                counter += 1
            print('encoder count to ', counter)
            if counter >= 960:
                print("endcoder count finished")
                break

    def reach(self, left_or_right, count):
        if left_or_right not in ['left', 'right']:
            raise AttributeError()
        pin = self.pin_left_encoder_pin if left_or_right == 'left' else self.pin_right_encoder_pin

        counter = np.uint64(0)
        button = int(0)
        time.sleep(0.1)

        for i in range(0, 1000):
            if int(gpio.input()) != int(button):
                button = int(gpio.input(pin))
                counter += 1
            print('encoder count to ', counter)
            if counter >= count:
                return True
        return False

if __name__ == '__name__':
    print('testing left encoder')
    encoder_ = encoder()
    encoder_.count('left')
    print('left encoder tested')

    print('testing right encoder')
    encoder_ = encoder()
    encoder_.count('left')
    print('right encoder tested')