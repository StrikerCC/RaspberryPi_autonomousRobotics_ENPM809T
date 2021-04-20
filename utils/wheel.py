import RPi.GPIO as gpio
import time


class wheel():
    def __init__(self):
        # self.dis_move = 0
        self.pin_upper_left_h_bridge = 31
        self.pin_in1 = 31
        self.pin_in2 = 33
        self.pin_in4 = 35
        self.pin_in3 = 37

        self.__command_2_movement = {    # user input to drive wheel around
            'w': self.__forward,
            's': self.__reverse,
            'a': self.__pivotleft,
            'd': self.__pivotright
        }

    def __del__(self):
        self.shutdown()

    def _init_ouput_pins(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin_in2, gpio.OUT)    # IN1
        gpio.setup(self.pin_in1, gpio.OUT)    # IN2
        gpio.setup(self.pin_in4, gpio.OUT)    # IN3
        gpio.setup(self.pin_in3, gpio.OUT)    # IN4

    def stop(self):
    # set all pins low
        gpio.setup(31, False)
        gpio.setup(33, False)
        gpio.setup(35, False)
        gpio.setup(37, False)

    def shutdown(self):
        self.stop()
        gpio.cleanup()

    def __forward(self, move_time=1):
        self._init_ouput_pins()
        # left wheele
        gpio.output(self.pin_in1, True)
        gpio.output(self.pin_in2, False)
        # right wheele
        gpio.output(self.pin_in3, True)
        gpio.output(self.pin_in4, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __reverse(self, move_time=1):
        self._init_ouput_pins()
        # left wheele reverse
        gpio.output(self.pin_in2, True)
        gpio.output(self.pin_in1, False)
        # right wheele reverse
        gpio.output(self.pin_in4, True)
        gpio.output(self.pin_in3, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotleft(self, move_time=1):
        self._init_ouput_pins()
        # left wheele reverse
        gpio.output(self.pin_in2, True)
        gpio.output(self.pin_in1, False)
        # right wheele forward
        gpio.output(self.pin_in3, True)
        gpio.output(self.pin_in4, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotright(self, move_time=1):
        self._init_ouput_pins()
        # left wheele forward
        gpio.output(self.pin_in1, True)
        gpio.output(self.pin_in2, False)
        # right wheele reverse
        gpio.output(self.pin_in4, True)
        gpio.output(self.pin_in3, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __move(self, direction):
        print("Key: ", direction)
        key_press = direction
        if key_press in self.__command_2_movement.keys():
            self.__command_2_movement[key_press]()  # only move for one second
        else:
            print("Invalid key presses!")

    def read_user_input_then_move_acoordingly(self):
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            return False
        elif key_press in self.__command_2_movement:
            self.__move(key_press)
            return True
        else:
            print('couldn\'t recognize ', key_press, ' please enter ', str(self.__command_2_movement))
            return True


class wheelControlled(wheel):
    def __init__(self):
        super().__init__()
        self.__command_2_movement = {  # user input to drive wheel around
            'w': self.__forward,
            's': self.__reverse,
            'a': self.__pivotleft,
            'd': self.__pivotright
        }
        self.limit = {  # limit of distance and angle user can input each prompt
            'distance': (0.0, 2.5),
            'angle': (0.0, 360.5)
        }
        self.pin_left_encoder_pin = 7
        self.pin_right_encoder_pin = 12

    def _init_ouput_pins(self):
        super(wheelControlled, self)._init_ouput_pins()
        gpio.setup(self.pin_left_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)    # front left encoder pin
        gpio.setup(self.pin_right_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)   # back right encoder pin

    def __move(self, direction='a', value=50):
        self._init_ouput_pins()
        print("Key: ", direction)
        key_press = direction
        if key_press in self.__command_2_movement.keys():
            self.__command_2_movement[key_press]()  # only move for one second
        else:
            print("Invalid key presses!")

    def stop(self):
        # set all pins low
        gpio.setup(31, False)
        gpio.setup(33, False)
        gpio.setup(35, False)
        gpio.setup(37, False)

    def __forward(self, distance=0.5):
        self._init_ouput_pins()

        # left wheele
        gpio.output(31, True)
        gpio.output(33, False)
        # right wheele
        gpio.output(37, True)
        gpio.output(35, False)
        # hold on
        time.sleep(distance)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __reverse(self, distance=0.5):
        self._init_ouput_pins()
        # left wheele reverse
        gpio.output(33, True)
        gpio.output(31, False)
        # right wheele reverse
        gpio.output(35, True)
        gpio.output(37, False)
        # hold on
        time.sleep(distance)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotleft(self, angle=30):
        self._init_ouput_pins()
        # left wheele reverse
        gpio.output(33, True)
        gpio.output(31, False)
        # right wheele forward
        gpio.output(37, True)
        gpio.output(35, False)
        # hold on
        time.sleep(angle)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __pivotright(self, angle=30):
        self._init_ouput_pins()
        # left wheele forward
        gpio.output(31, True)
        gpio.output(33, False)
        # right wheele reverse
        gpio.output(35, True)
        gpio.output(37, False)
        # hold on
        time.sleep(angle)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def read_user_input_then_move_acoordingly(self):
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            return False
        elif key_press in self.__command_2_movement:
            value = int(input("enter value for this move: distance in cm, angle in degree"))
            self.__move(key_press, value)
            return True
        else:
            print('couldn\'t recognize ', key_press, ' please enter ', str(self.__command_2_movement))
            return True





def main():
    driver = wheel()
    print('driving start')
    while True:
        if not driver.read_user_input_then_move_acoordingly():
            break
    print('driving done')


if __name__ == '__main__':
    main()

