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
        print('aiming vail')
        # camera_.view_some_frames(num_frames=8)

        gripper_.open_for_vail()  # open gripper
        while True:
            if not wheel_.read_user_input_then_move_acoordingly():
                break
        # turn to the vial
        # gripper_.open_for_vail()    # open gripper


        # move to the vail
        print('moving to vail')
        while True:
            if not wheel_.read_user_input_then_move_acoordingly():
                break
        gripper_.close_for_vail()   # close gripper to pick up
        # back up for same distance
        print('backing up with vail')
        while True:
            if not wheel_.read_user_input_then_move_acoordingly():
                break

        # turn to direction for transportation
        print('turn to transportation')
        while True:
            if not wheel_.read_user_input_then_move_acoordingly():
                break

        """start a transporting"""
        print('moving to injection area')
        wheel_.forward(distance=side0)  # move forward side0
        wheel_.rotate(90)  # turn left 90
        wheel_.forward(distance=side1)  # move forward side1

        """deliver vail"""
        print('delivering injection vial')
        # move forward to injection area
        while True:
            if not wheel_.read_user_input_then_move_acoordingly():
                break

        gripper_.open_for_vail()    # open gripper to put down vail

        # back up
        print('backing up from vail')
        while True:
            if not wheel_.read_user_input_then_move_acoordingly():
                break

        gripper_.close_for_vail()   # close gripper

        """go back"""
        print('going back to storage area')
        wheel_.rotate(90)  # turn left 90
        wheel_.forward(distance=side0)  # move forward side0
        wheel_.rotate(90)  # turn left 90
        wheel_.forward(distance=side1)  # move forward side1

        """picking up"""
        print('picking up again')

        """turn to transportation route"""
        # print()
        # wheel_.rotate(90)  # turn left 90

    return True



if __name__ == '__main__':
    main()