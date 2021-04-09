import RPi.GPIO as gpio
import time


class drive():

    def __init__(self):
        self.dis_move = 0

    def __start__(self):
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

    def forward(self, tf):
        self.__start__()
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

    def reverse(self, tf):
        self.__start__()
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

    def pivotleft(self, tf):
        self.__start__()
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

    def pivotright(self, tf):
        self.__start__()
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


    def drive(self, event):
        self.__start__()
        print("Key: ", event)
        key_press = event
        tf = 1
        if key_press.lower() == 'w':
            self.forward(tf)
        elif key_press.lower() == 's':
            self.reverse(tf)
        elif key_press.lower() == 'a':
            self.pivotleft(tf)
        elif key_press.lower() == 'd':
            self.pivotright(tf)
        else:
            print("Invalid key presses!")


def main():
    driver = drive()
    while True:
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            break
        driver.drive(key_press)

if __name__ == '__main__':
    main()

# forward(2)

