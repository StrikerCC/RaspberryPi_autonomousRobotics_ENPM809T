import RPi.GPIO as gpio
import numpy as np
import time
import serial


class encoder():
    def __init__(self):
        self.pin_left_encoder_pin, self.pin_right_encoder_pin = 7, 12
        self.meter_2_count = 96

    def __pins_init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin_left_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # front left encoder pin
        gpio.setup(self.pin_right_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # back right encoder pin

    def __del__(self):
        gpio.cleanup()

    def count_ticks(self, left_or_right):
        self.__pins_init()
        if left_or_right not in ['left', 'right']:
            raise AttributeError('Wrong input given to encoder')
        pin = self.pin_left_encoder_pin if left_or_right == 'left' else self.pin_right_encoder_pin

        counter = np.uint64(0)
        button = int(0)
        time.sleep(0.01)

        for i in range(0, 1000):
            print('counter = ', counter, "GPIO state: ", gpio.input(pin))
            if int(gpio.input(pin)) != int(button):
                button = int(gpio.input(pin))
                counter += 1
            print('encoder count to ', counter)
            if counter >= 50:
                print("endcoder count finished")
                break

    def reach(self, left_or_right, count_goal):
        self.__pins_init()
        if left_or_right not in ['left', 'right']:
            raise AttributeError()
        pin = self.pin_left_encoder_pin if left_or_right == 'left' else self.pin_right_encoder_pin

        counter = np.uint64(0)
        button = int(0)
        time.sleep(0.01)

        for i in range(0, 100000):
            if int(gpio.input(pin)) != int(button):
                button = int(gpio.input(pin))
                counter += 1

            if counter >= count_goal:
                print('reach the goal count')
                return True

            # if counter % self.meter_2_count == 0:
            print('encoder count to ', counter)
        return False


class imu():
    def __init__(self):
        # Indentify serial connection
        self.port = '/dev/ttyUSB0'
        self.ser = serial.Serial(self.port, 9600)
        
        print('waiting for imu to respond')
        while True:
            if self.ser.in_waiting > 0:
                print('imu ok, read \n', self.ser.readline())
                for i in range(5):  # keep reading 5 imu output
                    print(self.ser.readline())
                break
       
    def __init__serial(self):
        self.ser = serial.Serial(self.port, 9600)

    def angles(self):
        angle = 0.0
        for i in range(100):
            count = 0
            if self.ser.in_waiting > 0:
                count += 1
                # Read serial stream
                line = self.ser.readline()

                # avoid first n-line of serial information
                if count > 5:
                    angle = self.__line_to_angle(line)
                # print(angle)
            else:
                print('cannot listen to imu')

        return angle

    def angle(self):
        while True:
            if self.ser.in_waiting > 0:
                angle = 0.0
                for _ in range(3):
                    # Read serial stream
                    line = self.ser.readline()
                    angle = self.__line_to_angle(line)
                return angle


    def reach(self, angle_goal):
        # ser = serial.Serial(self.port, 9600)
        for i in range(10000000):
            count = 0
            if self.ser.in_waiting > 0:
                count += 1
                # Read serial stream
                line = self.ser.readline()

                # avoid first n-line of serial information
                if count > 5:
                    angle = self.__line_to_angle(line)
                    if line >= abs(angle):
                        return True
        return False

    def __line_to_angle(self, line):
        # setup serial stream of extra chars
        line = line.rstrip().lstrip()
        line = str(line)
        #line = line.strip(' ')
        line = line.strip(',')
        line = line.strip("b'")
        line = line.strip('X:')
        #line = line.strip(' ')
        # print(line)
        # return float
        try:
            line = float(line)
        except:
            print('cannot convert', line, 'to float')

        return line if isinstance(line, float) else None

if __name__ == '__main__':
    print('testing left encoder')
    encoder_ = encoder()
    encoder_.count_ticks('left')
    print('left encoder tested')

    print('testing right encoder')
    encoder_.count_ticks('left')
    print('right encoder tested')

    imu_ = imu()
    #imu_.angles()
    print('testing imu')
    for _ in range(20):
        print(imu_.angle())
    print('imu tested')


