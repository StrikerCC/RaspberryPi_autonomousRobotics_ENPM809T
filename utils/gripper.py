import RPi.GPIO as gpio
import time


class gripper():
    def __init__(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(36, gpio.OUT)
        self.pwm = gpio.PWM(36, 50)
        self.pwm.start(3.5)  # start with close

    def __del__(self):
        # clean up GPIO
        self.pwm.stop()
        gpio.cleanup()

    def open(self, percent):
        # start from 0 to 100 percent, 0 is close, 100 is close
        if 0 <= percent <= 100: 
            duty_cycle = 0.75 * percent
            self.__change_dc__(duty_cycle)
            return True
        else:
            return False

    def __change_dc__(self, dc):
        if dc > 70 or dc < 35:
            print('servo duty cycle over range')
            return
        self.pwm.ChangeDutyCycle(i/10)
        time.sleep(0.1)

    def open_and_close(self):
        print('open and close')
        # move from close to open 
        for i in range(35, 70, 1):
            self.pwm.ChangeDutyCycle(i/10)
            time.sleep(0.1)

        # move from open to close
        for i in range(70, 35, -1):
            self.pwm.ChangeDutyCycle(i/10)
            time.sleep(0.1)

    def open_for_vail(self):
        print('open gripper for vail')
        for i in range(25, 70, 5):
            self.pwm.ChangeDutyCycle(i/10)
            time.sleep(0.1)

    def close_for_vail(self):
        print('open gripper for vail')
        for i in range(70, 25, -5):
            self.pwm.ChangeDutyCycle(i / 10)
            time.sleep(0.1)


def main():
    gripper_ = gripper()
    gripper_.open_for_vail()
    time.sleep(3)
    gripper_.close_for_vail()


if __name__ == '__main__':
    main()
