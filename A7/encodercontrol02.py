import time
import RPi.GPIO as gpio
import numpy as np


#### initialize GPIO pins ####


def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31, gpio.OUT)	# in 1
    gpio.setup(33, gpio.OUT)	# in 2
    gpio.setup(35, gpio.OUT)	# in 3
    gpio.setup(37, gpio.OUT)	# in 4
    
    gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_UP)


def shutdown():
    gpio.output(31, False)	# close in 1
    gpio.output(33, False)	# close in 2
    gpio.output(35, False)	# close in 3
    gpio.output(37, False)	# close in 4
    
    gpio.cleanup()


def main():
    init()
    counter = np.uint64(0)
    button = int(0)

    pwm = gpio.PWM(37, 50)
    val = 14
    pwm.start(val)
    time.sleep(0.1)
    
    for i in range(0, 100000):
        print('counter = ', counter, "GPIO state: ", gpio.input(12))
        
        if int(gpio.input(12)) != int(button):
            button = int(gpio.input(12))
            counter += 1

        if counter >= 960:
            pwm.stop()
            shutdown()
            print("endcoder count finished")
            break


if __name__ == '__main__':
    main()
