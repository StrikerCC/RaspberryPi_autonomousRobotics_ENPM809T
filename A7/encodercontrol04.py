### 4
import time
import RPi.GPIO as gpio
import numpy as np

#### initialize GPIO pins ####


def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31, gpio.OUT)    # in 1
    gpio.setup(33, gpio.OUT)    # in 2
    gpio.setup(35, gpio.OUT)    # in 3
    gpio.setup(37, gpio.OUT)    # in 4
    
    gpio.setup(7, gpio.IN, pull_up_down=gpio.PUD_UP) 
    gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_UP)


def shutdown():
    gpio.output(31, False)  # close in 1
    gpio.output(33, False)  # close in 2
    gpio.output(35, False)  # close in 3
    gpio.output(37, False)  # close in 4
    
    gpio.cleanup()


def main():
    init()
    counter_front_left = np.uint64(0)
    counter_back_right = np.uint64(0)
    
    button_front_left = int(0)
    button_back_right = int(0)
    
    # independent motor control via pwm
    pwm_back_right = gpio.PWM(31, 50)
    pwm_front_left = gpio.PWM(37, 50)
    val = 22
    pwm_back_right.start(val)
    pwm_front_left.start(val)
    time.sleep(0.1)
    
    ### save encoder state to txt file 
    filename_br = 'encoderStateBR.txt' 
    filename_fl = 'encoderStateFL.txt'
    file_br = open(filename_br, 'w')
    file_fl = open(filename_fl, 'w')
    for i in range(0, 100000):
        
        print('counter back right', counter_back_right, 'counter front left', counter_front_left, "BR state: ", gpio.input(12), "FL state: ", gpio.input(7))
        file_br.write(str(int(gpio.input(12))) + ' ' + str(counter_back_right)+' \n')
        file_fl.write(str(int(gpio.input(7))) + ' ' + str(counter_front_left)+ ' \n')
        
        if int(gpio.input(12)) != int(button_back_right):
            button_back_right = int(gpio.input(12))
            button_back_right += 1
        
        if int(gpio.input(7)) != int(button_front_left):
            button_front_left = int(gpio.input(7))
            button_front_left += 1

        if button_front_left >= 960:
            pwm_front_left.stop()
        
        if button_back_right >= 960:
            pwm_back_right.stop()

        if button_front_left >= 960 and button_back_right >= 960:
            shutdown()          
            print("endcoder count finished, encoder state recorded at", filename_br)
            break
    file_br.close()
    file_fl.close()

if __name__ == '__main__':
    main()
