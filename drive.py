#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   drive.py    
@Github  :   https://github.com/StrikerCC

@Modify Time      @Author       @Version    @Desciption
------------      -------       --------    -----------
4/18/2021 11:21 AM   Cheng Chen    1.0         None
'''

# import lib
from utils.wheel import wheelControlled
from utils.camera_pi import camera_pi, recorder
from utils.ranger import sonar
from utils.gripper import gripper

command = 'chengc0611@gmail.com'
# command = 'ENPM809TS19@gmail.com'

vaccines = {   ### hsv filter for object
    'J&J': {
        'color': 'blue',
        'low_limit': (91, 124, 88),
        'up_limit': (108, 255, 255)
    },
    'MODERNA': {
        'color': 'green',
        'low_limit': (53, 61, 34),
        'up_limit': (84, 255, 233)
    },
    'PFIZER': {
        'color': 'red',
        'low_limit': (153, 29, 125),
        'up_limit': (183, 255, 255)
    }
}

qrcode = {

}

"""video and image saving path"""
path_ = './grand_results/'
paths_img = [
    path_ + 'vail.jpg',
    path_ + 'qrcode.jpg',
    path_ + 'arrow.jpg',
    path_ + 'face.jpg'
]


def main():
    """operation classes"""
    wheel_ = wheelControlled()    # dynamic units
    camera_ = camera_pi()  # perception units
    gripper_ = gripper()

    """field parameters"""
    side0, side1 = 0.5, 0.25

    """go live"""
    for i in range(3):
        """hold on for emails"""

        """looking for and pick up vail according to command"""
        camera_.view_some_frames(num_frames=8)

        # turn to the vial
        gripper_.open_for_vail()    # open gripper
        # move to the vail
        gripper_.close_for_vail()   # close gripper to pick up
        # back up for same distance
        # turn to direction for transportation


        """start a transporting"""
        print('moving to injection area')
        wheel_.forward(distance=side0)  # move forward side0
        wheel_.turn(90)  # turn left 90
        wheel_.forward(distance=side1)  # move forward side1

        """deliver vail"""
        print('delivering injection vial')
        # move forward to injection area
        gripper_.open_for_vail()    # open gripper to put down vail
        # back up
        gripper_.close_for_vail()   # close gripper

        """go back"""
        print('going back to storage area')
        wheel_.turn(90)  # turn left 90
        wheel_.forward(distance=side0)  # move forward side0
        wheel_.turn(90)  # turn left 90
        wheel_.forward(distance=side1)  # move forward side1

        """picking up"""
        print('picking up again')

        """turn to transportation route"""
        wheel_.turn(90)  # turn left 90

    return True



if __name__ == '__main__':
    main()