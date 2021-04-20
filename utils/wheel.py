import RPi.GPIO as gpio
import time


class wheel():
    def __init__(self):
        # self.dis_move = 0
        self.__command_set = set()    # user input to drive wheel around
        for char in ['w', 'a', 's', 'd']:
            self.__command_set.add(char)

    def __init_ouput_pins(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(31, gpio.OUT)    # IN1
        gpio.setup(33, gpio.OUT)    # IN2
        gpio.setup(35, gpio.OUT)    # IN3
        gpio.setup(37, gpio.OUT)    # IN4

    def __del__(self):
        self.shutdown()

    def stop(self):
    # set all pins low
        gpio.setup(31, False)
        gpio.setup(33, False)
        gpio.setup(35, False)
        gpio.setup(37, False)

    def shutdown(self):
        self.stop()
        gpio.cleanup()

    def __forward(self, tf):
        self.__init_ouput_pins()
        # left wheele
        gpio.output(31, True)
        gpio.output(33, False)
        # right wheele
        gpio.output(37, True)
        gpio.output(35, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __reverse(self, tf):
        self.__init_ouput_pins()
        # left wheele reverse
        gpio.output(33, True)
        gpio.output(31, False)
        # right wheele reverse
        gpio.output(35, True)
        gpio.output(37, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotleft(self, tf):
        self.__init_ouput_pins()
        # left wheele reverse
        gpio.output(33, True)
        gpio.output(31, False)
        # right wheele forward
        gpio.output(37, True)
        gpio.output(35, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotright(self, tf):
        self.__init_ouput_pins()
        # left wheele forward
        gpio.output(31, True)
        gpio.output(33, False)
        # right wheele reverse
        gpio.output(35, True)
        gpio.output(37, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __move(self, event):
        print("Key: ", event)
        key_press = event
        tf = 1
        if key_press.lower() == 'w':
            self.__forward(tf)
        elif key_press.lower() == 's':
            self.__reverse(tf)
        elif key_press.lower() == 'a':
            self.__pivotleft(tf)
        elif key_press.lower() == 'd':
            self.__pivotright(tf)
        else:
            print("Invalid key presses!")

    def move_with_ui(self):
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            return False
        elif key_press in self.__command_set:
            self.__move(key_press)
            return True
        else:
            print('couldn\'t recognize ', key_press, ' please enter ', str(self.__command_set))
            return True


class wheel_controlled_by_encoder(wheel):
    def __init_ouput_pins(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(31, gpio.OUT)    # IN1
        gpio.setup(33, gpio.OUT)    # IN2
        gpio.setup(35, gpio.OUT)    # IN3
        gpio.setup(37, gpio.OUT)    # IN4
        gpio.setup(7, gpio.IN, pull_up_down=gpio.PUD_UP)    # front left encoder pin
        gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_UP)   # back right encoder pin

    def move_with_ui(self):
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            return False
        elif key_press in self.__command_set:
            value = int(input("enter value for this move: distance in cm, angle in degree"))
            if value > 0:
                self.__move(key_press, value)
            return True
        else:
            print('couldn\'t recognize ', key_press, ' please enter ', str(self.__command_set))
            return True

    def __move(self, event, value):
        self.__init_ouput_pins()
        print("Key: ", event)
        key_press = event

        if key_press.lower() == 'w':
            self.__forward(tf)
        elif key_press.lower() == 's':
            self.__reverse(tf)
        elif key_press.lower() == 'a':
            self.__pivotleft(tf)
        elif key_press.lower() == 'd':
            self.__pivotright(tf)
        else:
            print("Invalid key presses!")

    def stop(self):
        # set all pins low
        gpio.setup(31, False)
        gpio.setup(33, False)
        gpio.setup(35, False)
        gpio.setup(37, False)

    def __forward(self, tf):
        self.__init_ouput_pins()
        # left wheele
        gpio.output(31, True)
        gpio.output(33, False)
        # right wheele
        gpio.output(37, True)
        gpio.output(35, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __reverse(self, tf):
        self.__init_ouput_pins()
        # left wheele reverse
        gpio.output(33, True)
        gpio.output(31, False)
        # right wheele reverse
        gpio.output(35, True)
        gpio.output(37, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotleft(self, tf):
        self.__init_ouput_pins()
        # left wheele reverse
        gpio.output(33, True)
        gpio.output(31, False)
        # right wheele forward
        gpio.output(37, True)
        gpio.output(35, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotright(self, tf):
        self.__init_ouput_pins()
        # left wheele forward
        gpio.output(31, True)
        gpio.output(33, False)
        # right wheele reverse
        gpio.output(35, True)
        gpio.output(37, False)
        # hold on
        time.sleep(tf)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()






def main():
    driver = wheel()
    print('driving start')
    while True:
        if not driver.move_with_ui():
            break
    print('driving done')


if __name__ == '__main__':
    main()

