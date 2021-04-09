import sys
#sys.path.append("..")
sys.path.append('/home/pi/ENPM809T/RaspberryPi_autonomousRobotics_ENPM809T')

for path in sys.path:
    print(path)

from utils.gripper import gripper
from utils.camera import recorder
import time 

def main():
    print('start ')
    recorder_ = recorder('a6 move.avi')
    gripper_ = gripper()
    dur = 20
    wait = 15
    
    
    
    recorder_.record(dur, 'oepn ' + str(0))
    time.sleep(wait)
    recorder_.record(dur, 'open ' + str(0))
    time.sleep(wait)
    recorder_.record(dur, 'open ' + str(0))
    time.sleep(wait)
    recorder_.record(dur, 'open ' + str(50))
    time.sleep(wait)
    recorder_.record(dur, 'open ' + str(50))
    
    return 
    
    for i in range(1, 100):
        gripper_.open(i)
        recorder_.record(10, 'duty cycle' + str(i))
        

    for i in range(100, 1, -1):
        gripper_.open(i)
        recorder_.record(10, 'duty cycle' + str(i))

if __name__ == '__main__':
    main()
