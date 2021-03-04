import RPi.GPIO as gpio
import time 

# define pin
trig = 16
echo = 18

def distance(num_measure=10):
    gpio.setmode(gpio.BOARD)
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    dis_mean = 0
    
    for _ in range(num_measure):

        time.sleep(1)

        # ensure output has no value 
        gpio.output(trig, False)
        time.sleep(0.01)
        
        # generate trigger pulse
        gpio.output(trig, True)
        time.sleep(0.00001)
        gpio.output(trig, False)
    
        # pulse_start, pulse_end = 0, 0
        
        # Generate echo time signal 
        while gpio.input(echo) == 0:
            pulse_start = time.time()

        while gpio.input(echo) == 1:
            pulse_end = time.time()

        pulse_dur = pulse_end - pulse_start
        
        # convert time to distance 
        dis = pulse_dur * 17150
        dis = round(dis, 2)
        dis_mean += dis/num_measure

        print(dis)

    # cleanup gpio pin & return distance estimation 
    gpio.cleanup()
    return dis_mean 

print("Distance: ", distance())

