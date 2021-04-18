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

def reverse(tf):
    init()
    # left wheele reverse
    gpio.output(33, True)
    gpio.output(31, False)
    # right wheele reverse
    gpio.output(35, True)
    gpio.output(37, False)
    # hold on
    time.sleep(tf)
    # send all pins low & cleanup
    gameover()
    gpio.cleanup()

def pivotleft(tf):
    init()
    # left wheele reverse
    gpio.output(33, True)
    gpio.output(31, False)
    # right wheele forward
    gpio.output(37, True)
    gpio.output(35, False)
    # hold on
    time.sleep(tf)
    # send all pins low & cleanup
    gameover()
    gpio.cleanup()

def pivotright(tf):
    init()
    # left wheele forward
    gpio.output(31, True)
    gpio.output(33, False)
    # right wheele reverse
    gpio.output(35, True)
    gpio.output(37, False)
    # hold on
    time.sleep(tf)
    # send all pins low & cleanup
    gameover()
    gpio.cleanup()




def drive(event, val):
    init()
    print("Key: ", event)
    key_press = event
    tf = 1
    tf = tf / val
    if key_press.lower() == 'w':
        forward(tf)
    elif key_press.lower() == 's':
        reverse(tf)
    elif key_press.lower() == 'a':
        pivotleft(tf)
    elif key_press.lower() == 'd':
        pivotright(tf)
    else:
        print("Invalid key presses!")

while True:
    key_press = input("Select driving mode: ")
    val_press = input('value')
    val_press = int(val_press)

    if key_press == 'q':
        break
    drive(key_press, val_press)



# forward(2)

