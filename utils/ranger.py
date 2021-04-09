import RPi.GPIO as gpio
import time 

class sonar():
    def __init__(self, trig=16, echo=18):
        # define pin
        self.trig = trig
        self.echo = echo

    def __measure__(self):

        # ensure output has no value 
        gpio.output(self.trig, False)
        time.sleep(0.01)
        
        # generate trigger pulse
        gpio.output(self.trig, True)
        time.sleep(0.00001)
        gpio.output(self.trig, False)
    
        # pulse_start, pulse_end = 0, 0
        
        # Generate echo time signal 
        while gpio.input(self.echo) == 0:
            pulse_start = time.time()

        while gpio.input(self.echo) == 1:
            pulse_end = time.time()

        pulse_dur =   pulse_end - pulse_start
        # convert time to distance 
        dis = pulse_dur * 17150
        dis = round(dis, 2)
        return dis

    def distance(self):
        #gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

        time.sleep(0.5)
        dis = self.__measure__()
        # cleanup gpio pin & return distance estimation 
        gpio.cleanup()
        return dis
        
    def distance_mean(self, num_measure=5):
        #gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN) 
        dis_mean = 0

        for _ in range(num_measure):
            dis = self.__measure__()
            dis_mean += dis/num_measure
        # print(dis_mean)

        # cleanup gpio pin & return distance estimation 
        gpio.cleanup()
        return dis_mean 


def main():
    ranger = sonar()
    print("Distance: ", ranger.distance())
    print('average distance: ', ranger.distance_mean())

if __name__ == '__main__':
    main()
