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
from utils.tracking import angle_of_object


command = 'chengc0611@gmail.com'
# command = 'ENPM809TS19@gmail.com'

vaccines = {   ### hsv filter for object
    'J&J': {
        'color': 'blue',
        'threshold': {
            'low_limit': (91, 124, 88),
            'up_limit': (108, 255, 255)
        }
    },
    'MODERNA': {
        'color': 'green',
        'threshold': {
            'low_limit': (53, 61, 34),
            'up_limit': (84, 255, 233)
        }
    },
    'PFIZER': {
        'color': 'red',
        'threshold': {
            'low_limit': (153, 29, 125),
            'up_limit': (183, 255, 255)
        }
    },
    'arrow': {
        'color': 'red',
        'threshold': {
            'low_limit': (153, 29, 125),
            'up_limit': (183, 255, 255)
        }
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


def move_to_object(wheel_, angle):
    assert -360.0 < angle < 360.0, 'cannot rotate ' + str(angle) + ' degree'
    step, dis = 0.05, 0.0

    for _ in range(1000):
        if angle > -10.0:
            wheel_.forward(step)
            dis += step
        else:
            break
    return dis


def main():
    names = ['J&J', 'MODERNA', 'PFIZER']

    """operation classes"""
    wheel_ = wheelControlled()    # dynamic units
    camera_ = camera_pi()  # perception units
    gripper_ = gripper()

    """field parameters"""
    side0, side1 = 0.8, 0.4
    dis_away_2_vail = 0.2

    """go live"""
    for i in range(3):

        """hold on for emails"""

        vail = names[i]
        vail_info = vaccines[vail]
        """looking for and pick up vail according to command"""
        print('aiming vail', vail_info['color'])
        # camera_.view_some_frames(num_frames=8)
        angle_vail = angle_of_object(camera_, vail_info['threshold'])

        gripper_.open_for_vail()                                # open gripper
        wheel_.rotate(angle_vail[0])                            # turn to the vial

        print('moving to vail')
        dis_move_2_vail = move_to_object(wheel_, angle_vail)    # move to the vail
        gripper_.close_for_vail()                               # close gripper to pick up
        print('backing up with vail')
        wheel_.reverse(dis_move_2_vail)                         # back up for same distance

        # turn to direction for transportation
        print('turn to transportation')
        wheel_.turn_to(90.0)

        """start a transporting"""
        print('moving to injection area')
        wheel_.forward(distance=side0)  # move forward side0
        wheel_.rotate(90)  # turn left 90
        wheel_.forward(distance=side1)  # move forward side1

        """deliver vail"""
        print('delivering injection vial')

        # move forward to injection area
        wheel_.forward(dis_away_2_vail)
        gripper_.open_for_vail()                                # open gripper to put down vail

        print('backing up from vail')
        wheel_.reverse(dis_away_2_vail)                         # back up to leave vail alone
        gripper_.close_for_vail()                               # close gripper

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