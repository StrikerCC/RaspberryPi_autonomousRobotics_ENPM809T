import RPi.GPIO as gpio
import time

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31, gpio.OUT)    # IN1
    gpio.setup(33, gpio.OUT)    # IN2
    gpio.setup(35, gpio.OUT)    # IN3
    gpio.setup(37, gpio.OUT)    # IN4

def gameover():
    # set all pins low

    gpio.setup(31, False)
    gpio.setup(33, False)
    gpio.setup(35, False)
    gpio.setup(37, False)

def forward(tf):
    init()
    # left wheele
    gpio.output(31, True)
    gpio.output(33, False)
    # right wheele
    gpio.output(37, True)
    gpio.output(35, False)
    # hold on
    time.sleep(tf)
    # send all pins low & cleanup
    gameover()
    gpio.cleanup()

forward(2)

