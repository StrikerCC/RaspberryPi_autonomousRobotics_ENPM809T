import RPi.GPIO as gpio
import time
from sensors import encoder, imu


class wheel():
    def __init__(self):
        # self.dis_move = 0
        self.__pin_upper_left_h_bridge = 31
        self._pin_in1 = 31
        self._pin_in2 = 33
        self._pin_in4 = 35
        self._pin_in3 = 37

        self._command_2_movement = {    # user input to drive wheel around
            'w': self.forward,
            's': self.reverse,
            'a': self.pivotleft,
            'd': self.pivotright,
        }

    def __del__(self):
        # :self.shutdown()
        pass

    def _init_ouput_pins(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self._pin_in2, gpio.OUT)    # IN1
        gpio.setup(self._pin_in1, gpio.OUT)    # IN2
        gpio.setup(self._pin_in4, gpio.OUT)    # IN3
        gpio.setup(self._pin_in3, gpio.OUT)    # IN4

    def stop(self):
    # set all pins low
        gpio.setup(self._pin_in1, False)
        gpio.setup(self._pin_in2, False)
        gpio.setup(self._pin_in3, False)
        gpio.setup(self._pin_in4, False)

    def shutdown(self):
        self.stop()
        gpio.cleanup()

    def forward(self, move_time=1):
        self._init_ouput_pins()
        # left wheele
        gpio.output(self._pin_in1, True)
        gpio.output(self._pin_in2, False)
        # right wheele
        gpio.output(self._pin_in3, True)
        gpio.output(self._pin_in4, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def reverse(self, move_time=1):
        self._init_ouput_pins()
        # left wheele reverse
        gpio.output(self._pin_in2, True)
        gpio.output(self._pin_in1, False)
        # right wheele reverse
        gpio.output(self._pin_in4, True)
        gpio.output(self._pin_in3, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def pivotleft(self, move_time=1):
        self._init_ouput_pins()
        # left wheele reverse
        gpio.output(self._pin_in2, True)
        gpio.output(self._pin_in1, False)
        # right wheele forward
        gpio.output(self._pin_in3, True)
        gpio.output(self._pin_in4, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def pivotright(self, move_time=1):
        self._init_ouput_pins()
        # left wheele forward
        gpio.output(self._pin_in1, True)
        gpio.output(self._pin_in2, False)
        # right wheele reverse
        gpio.output(self._pin_in4, True)
        gpio.output(self._pin_in3, False)
        # hold on
        time.sleep(move_time)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def __moveIt(self, direction):
        print("Key: ", direction)
        key_press = direction
        if key_press in self._command_2_movement.keys():
            self._command_2_movement[key_press]()  # only move for one second
        else:
            print("Invalid key presses!")

    def read_user_input_then_move_acoordingly(self):
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            return False
        elif key_press in self._command_2_movement:
            self.__moveIt(key_press)
            return True
        else:
            print('couldn\'t recognize ', key_press, ' please enter ', str(self._command_2_movement))
            return True


class wheelControlled(wheel):
    def __init__(self):
        super().__init__()
        self._pin_left_encoder_pin = 7
        self._pin_right_encoder_pin = 12

        self._command_2_movement = {  # user input to drive wheel around
            'w': self.forward,
            's': self.reverse,
            'a': self.pivotleft,
            'd': self.pivotright
        }
        self.limit = {  # limit of distance and angle user can input each prompt
            'distance': (0.0, 2.5),
            'angle': (0.0, 360.5)
        }

        """sensors"""
        self.encoder_ = encoder()
        self.imu_ = imu()

        """motor control parameters for motor"""
        self.frequency = 50     # motor control frequency
        self.duty_cycle = 80    # duty cycle to control motor effect voltage
        """motor control parameters for encoder"""
        self.meter_2_ticks = 98 # number of ticks per meter of travelling
        """motor control parameters for imu"""
        self._tolerance = 2

    def __moveIt(self, direction='a', value=1.0):
        self._init_ouput_pins()
        print("Key: ", direction)
        key_press = direction
        if key_press in self._command_2_movement.keys():
            func_move = self._command_2_movement[key_press]  # only move for one second
            func_move(float(value))
        else:
            print("Invalid key presses!")

    def stop(self):
        # set all pins low
        super().stop()

    def forward(self, distance=1.0):
        self._init_ouput_pins()

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in1, 50)
        pwm_back_right = gpio.PWM(self._pin_in3, 50)
        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        time.sleep(0.01)

        if self.encoder_.reach('left', int(distance*self.meter_2_ticks)):
            pwm_front_left.stop()
            pwm_back_right.stop()
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def reverse(self, distance=1.0):
        self._init_ouput_pins()

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in2, 50)
        pwm_back_right = gpio.PWM(self._pin_in4, 50)
        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        time.sleep(0.01)

        if self.encoder_.reach('left', int(distance*self.meter_2_ticks)):
            pwm_front_left.stop()
            pwm_back_right.stop()
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def pivotleft(self, angle=30.0):
        self._init_ouput_pins()
        angle_init = self.imu_.angle()
        angle_goal = angle_init - angle
        print(angle_init, 'to', angle_goal)

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in1, 50)
        pwm_back_right = gpio.PWM(self._pin_in4, 50)
        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        time.sleep(0.01)

        for _ in range(1000):
            if 360.0 - angle_goal - self._tolerance <= self.imu_.angle() <= 360.0 - angle_goal + self._tolerance:
                print(angle_init, 'to', angle_goal)
                print('reach', self.imu_.angle())
                pwm_front_left.stop()
                pwm_back_right.stop()
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()


    def pivotright(self, angle=30.0):
        self._init_ouput_pins()
        angle_init = self.imu_.angle()
        angle_goal = angle_init + angle
        print(angle_init, 'to', angle_goal)

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in2, 50)
        pwm_back_right = gpio.PWM(self._pin_in3, 50)
        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        time.sleep(0.01)

        for _ in range(1000):
            if angle_goal-self._tolerance < self.imu_.angle() < angle_goal-self._tolerance:
                print(angle_init, 'to', angle_goal)
                print('reach', self.imu_.angle())
                pwm_front_left.stop()
                pwm_back_right.stop()
            # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def read_user_input_then_move_acoordingly(self):
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            return False
        elif key_press in self._command_2_movement.keys():
            value = float(input("enter value for this move: distance in cm, angle in degree"))
            self.__moveIt(direction=key_press, value=value)
            return True
        else:
            print('couldn\'t recognize ', key_press, ' please enter ', str(self._command_2_movement))
            return True


def main():
    driver = wheel()
    print('driving with time start')
    while True:
        if not driver.read_user_input_then_move_acoordingly():
            break
    print('driving with time done')
    driver.__del__()

    driver = wheelControlled()
    print('driving with distance start')
    while True:
        if not driver.read_user_input_then_move_acoordingly():
            break
    print('driving with distance done')


if __name__ == '__main__':
    main()

