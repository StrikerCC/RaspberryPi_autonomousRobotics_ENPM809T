import RPi.GPIO as gpio
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.getcwd()))

from RaspberryPi_autonomousRobotics_ENPM809T.utils.sensors import encoder, imu


class wheel():
    def __init__(self):
        # self.dis_move = 0
        self.__pin_upper_left_h_bridge = 31
        self._pin_in1 = 31
        self._pin_in2 = 33
        self._pin_in4 = 35
        self._pin_in3 = 37

        self._command_2_movement = {  # user input to drive wheel around
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
        gpio.setup(self._pin_in2, gpio.OUT)  # IN1
        gpio.setup(self._pin_in1, gpio.OUT)  # IN2
        gpio.setup(self._pin_in4, gpio.OUT)  # IN3
        gpio.setup(self._pin_in3, gpio.OUT)  # IN4

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

    def retrive_path(self):
        pass


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

        self.path = {
            'move_len': [0],
            'orientations': [0]
        }

        """sensors"""
        self.encoder_ = encoder()
        self.imu_ = imu()

        """motor control parameters for motor"""
        self.frequency = 10  # motor control frequency
        self.duty_cycle = 50  # duty cycle to control motor effect voltage
        """motor control parameters for encoder"""
        self.meter_2_ticks = 98  # number of ticks per meter of travelling
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
        print('moving forward', distance)

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in1, self.frequency)
        pwm_back_right = gpio.PWM(self._pin_in3, self.frequency)
        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        time.sleep(0.01)

        if self.encoder_.reach('left', int(distance * self.meter_2_ticks)):
            pwm_front_left.stop()
            pwm_back_right.stop()
            print('moved forward', distance)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def reverse(self, distance=1.0):
        self._init_ouput_pins()
        print('moving backward', distance)

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in2, self.frequency)
        pwm_back_right = gpio.PWM(self._pin_in4, self.frequency)
        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        time.sleep(0.01)

        if self.encoder_.reach('left', int(distance * self.meter_2_ticks)):
            pwm_front_left.stop()
            pwm_back_right.stop()
            print('moved backward', distance)
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def spin_start(self, pwm, duty_cycle=50):
        """
        start pwm signal to preset pins
        :param pwm:
        :type pwm:
        :param duty_cycle:
        :type duty_cycle:
        :return:
        :rtype:
        """
        pwm_left, pwm_right = pwm
        pwm_left.start(duty_cycle)
        pwm_right.start(duty_cycle)
        time.sleep(0.01)
        return pwm_left, pwm_right

    def spin_init(self):
        # independent motor control via pwm, move forward with half speed
        pwm_l_left_wheel = gpio.PWM(self._pin_in2, self.frequency)
        pwm_l_right_wheel = gpio.PWM(self._pin_in3, self.frequency)
        pwm_r_left_wheel = gpio.PWM(self._pin_in1, self.frequency)
        pwm_r_right_wheel = gpio.PWM(self._pin_in4, self.frequency)
        return (pwm_l_left_wheel, pwm_l_right_wheel), (pwm_r_left_wheel, pwm_r_right_wheel)

    def spin_end(self, pwm):
        pwm_left, pwm_right = pwm
        if pwm_left: pwm_left.stop()
        if pwm_right: pwm_right.stop()
        # self.stop()

        gpio.cleanup()

    def turn(self, angle=0.0):
        """
        turn the robot a specific angle
        :param angle:
        :type angle:
        :return:
        :rtype:
        """
        """measure the init orientation of robot"""
        angle_init = self.imu_.angle()

        """make a range of target for desired robot orientation"""
        angle_goal_left = angle % 180.0
        angle_goal_right = angle % 180.0
        if angle > 0.0:
            angle_goal_right += self._tolerance
        elif angle < 0.0:
            angle_goal_left -= self._tolerance
        else:
            angle_goal_left -= self._tolerance
            angle_goal_right += self._tolerance

        # angle_goal_left = (angle_goal_left + 360.0) % 360.0  # left limit
        # angle_goal_right = max((angle_goal_right + 360.0) % 360.0, angle_goal_right)  # right limit

        # if 270.0 < angle_goal_left:
        #     angle_goal_left -= 360.0
        # if 270.0 < angle_goal_right:
        #     angle_goal_right -= 360.0

        print('turn from', angle_init, 'to between', angle_init+angle_goal_left, 'and', angle_init+angle_goal_right)
        """start spin"""
        try:
            self._init_ouput_pins()
            pwm_l, pwm_r = self.spin_init()  # start pwm_l to turn left, likewise for turing right
            for _ in range(10000):
                angle_current = self.imu_.angle() - angle_init

                print(angle_goal_left, '<', angle_current, '<', angle_goal_right)
                if angle_current > angle_goal_left and angle_current > angle_goal_right:    # spin left if bigger than left and right limit
                    self.spin_start(pwm_l, 90)
                elif angle_current < angle_goal_left and angle_current < angle_goal_right:  # spin right if smaller than left and right limit
                    self.spin_start(pwm_r, 90)
                else:                                                                       # stop pin
                    break

            """stop spin"""
            if pwm_l or pwm_r:
                self.spin_end(pwm_l)
                self.spin_end(pwm_r)

            # send all pins low & cleanup
            # self.stop()
            gpio.cleanup()
            return True
        except ArithmeticError:
            # send all pins low & cleanup
            self.stop()
            gpio.cleanup()
            return False

    def pivotleft(self, angle=30.0):
        self._init_ouput_pins()
        angle_init = self.imu_.angle()
        angle_goal_left = ((angle_init - angle - self._tolerance) + 360.0) % 360.0  # left limit
        angle_goal_right = max(((angle_init - angle + self._tolerance) + 360.0) % 360.0,
                               angle_goal_left + 2 * self._tolerance)  # right limit
        print(angle_init, 'to range', angle_goal_left, angle_goal_right)

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in2, self.frequency)
        pwm_back_right = gpio.PWM(self._pin_in3, self.frequency)
        # gpio.output(self._pin_in1, False)
        # gpio.output(self._pin_in4, False)

        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        time.sleep(0.01)

        for _ in range(1000):
            print(angle_goal_left, '<', self.imu_.angle(), '<', angle_goal_right)
            if angle_goal_left <= self.imu_.angle() <= angle_goal_right:
                print('reach', self.imu_.angle())
                pwm_front_left.stop()
                pwm_back_right.stop()
                break
        # send all pins low & cleanup
        self.stop()
        gpio.cleanup()

    def pivotright(self, angle=30.0):
        self._init_ouput_pins()
        angle_init = self.imu_.angle()
        angle_goal = angle_init + angle
        print(angle_init, 'to', angle_goal)

        self._init_ouput_pins()
        angle_init = self.imu_.angle()
        angle_goal_left = ((angle_init + angle - self._tolerance) + 360.0) % 360.0  # left limit
        angle_goal_right = max(((angle_init + angle + self._tolerance) + 360.0) % 360.0,
                               angle_goal_left + 2 * self._tolerance)  # right limit
        print(angle_init, 'to range', angle_goal_left, angle_goal_right)

        # independent motor control via pwm, move forward with half speed
        pwm_front_left = gpio.PWM(self._pin_in1, self.frequency)
        pwm_back_right = gpio.PWM(self._pin_in4, self.frequency)
        pwm_front_left.start(self.duty_cycle)
        pwm_back_right.start(self.duty_cycle)
        gpio.output(self._pin_in2, False)
        gpio.output(self._pin_in3, False)

        time.sleep(0.01)

        for _ in range(1000):
            print(angle_goal_left, '<', self.imu_.angle(), '<', angle_goal_right)
            if angle_goal_left <= self.imu_.angle() <= angle_goal_right:
                print(angle_init, 'to', angle_goal)
                print('reach', self.imu_.angle())
                pwm_front_left.stop()
                pwm_back_right.stop()
                break
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

    def read_user_input_then_turn_acoordingly(self):
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            return False
        elif key_press == 't':
            value = float(input("enter value for this move: distance in cm, angle in degree "))
            self.turn(angle=value)
            return True
        else:
            print('couldn\'t recognize ', key_press, ' please enter ', str(self._command_2_movement))
            return True

    def rectangle(self, side0=0.5, side1=0.25):
        self._init_ouput_pins()

        """start transporting"""
        print('moving to injection area')
        self.forward(distance=side0)  # move forward side0
        self.turn(90)  # turn left 90
        self.forward(distance=side1)  # move forward side1

        """deliver vail"""
        print('delivering injection vial')

        """go back"""
        print('going back to storage area')
        self.turn(90)  # turn left 90
        self.forward(distance=side0)  # move forward side0
        self.turn(90)  # turn left 90
        self.forward(distance=side1)  # move forward side1

        """picking up"""
        print('picking up')

        """turn to transportation route"""
        self.turn(90)  # turn left 90

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
        if not driver.read_user_input_then_turn_acoordingly():
            break
    print('driving with distance done')
    driver.rectangle()


if __name__ == '__main__':
    main()
