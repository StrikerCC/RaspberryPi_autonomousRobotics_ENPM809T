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
import cv2
import os

from utils.wheel import wheelControlled
from utils.camera_pi import camera_pi, recorder
from utils.ranger import sonar
from utils.gripper import gripper
from utils.tracking import face_detect, get_qrcode #, angle_of_object
from utils.communication import email_pi


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
paths_img = {
    'vail_qr': path_ + 'vail_prcode.jpg',
    'vail': path_ + 'vail.jpg',
    'qrcode': path_ + 'qrcode.jpg',
    'arrow': path_ + 'arrow.jpg',
    'face': path_ + 'face.jpg'
}


def save_img(img, name, email_):
    if name in paths_img.keys():
        cv2.imwrite(paths_img[name], img)
        email_.send('', paths_img[name])
        return True
    print('image saving path not found')
    return False


def email_img(email_):
    for file in os.listdir(path_):
        email_.send('', file)
    return True


def move_to_object(wheel_, step, angle=0.0):
    assert isinstance(angle, float), angle
    assert -360.0 < angle < 360.0, 'cannot rotate ' + str(angle) + ' degree'
    dis = 0.0
    # step, dis = 0.05, 0.0
    wheel_.forward(step)
    dis += step
    return dis


def main():
    names = ['J&J', 'MODERNA', 'PFIZER']

    """operation classes"""
    wheel_ = wheelControlled()    # dynamic units
    camera_ = camera_pi()  # perception units
    gripper_ = gripper()
    email_ = email_pi()
    """field parameters"""
    arrow_info = vaccines['arrow']  # arrow info

    # side0, side1 = 0.8, 0.4
    side0, side1 = 0.45, 0.3
    step = 0.12
    dis_away_2_vail = 0.15

    """go live"""
    for i in range(3):

        """hold on for emails"""

        """hold on for qrcode"""
        vail_name = names[i]
        # vail_name, img_qrcode_vail = get_qrcode(camera_, last=100)
        # save_img(img_qrcode_vail, 'vail_qr')

        vail_info = vaccines[vail_name]

        """looking for and pick up vail according to command"""
        print('aiming vail', vail_info['color'])
        angle_vail, img_vail = camera_.angle_of_object(color_limit_object=vail_info['threshold'])
        save_img(img_vail, 'vail', email_)

        gripper_.open_for_vail()                                # open gripper
        wheel_.rotate(angle_vail[0])                            # turn to the vial

        print('moving to vail')
        dis_move_2_vail = move_to_object(wheel_, step)    # move to the vail
        gripper_.close_for_vail()                               # close gripper to pick up
        print('backing up with vail')
        wheel_.reverse(dis_move_2_vail)                         # back up for same distance

        # turn to direction for transportation
        print('turn to transportation')
        wheel_.turn_to(90.0)

        """start a transporting"""
        print('moving to injection area')
        wheel_.forward(distance=side0)                          # move forward side0
        # wheel_.rotate(90)                                       # turn left 90
        angle_vail, img_arrow = camera_.angle_of_object(color_limit_object=arrow_info['threshold'])
        save_img(img_arrow, 'arrow', email_)
        wheel_.turn_to(180)                                       # turn left 90
        wheel_.forward(distance=side1)                          # move forward side1

        """deliver vail"""
        print('delivering injection vial')
        data, img_loc_qrcode = get_qrcode(camera_, last=15)
        save_img(img_loc_qrcode, 'qrcode', email_)

        # move forward to injection area
        wheel_.forward(dis_away_2_vail)
        img_face = face_detect(camera_)                         # holding for face detection
        save_img(img_face, 'face', email_)

        gripper_.open_for_vail()                                # open gripper to put down vail

        print('backing up from vail')
        wheel_.reverse(dis_away_2_vail)                         # back up to leave vail alone
        gripper_.close_for_vail()                               # close gripper

        """go back"""
        print('going back to storage area')
        wheel_.rotate(90)  # turn left 90
        wheel_.forward(distance=side0)  # move forward side0

        # use qrcode to adjust direction
        wheel_.rotate(0)  # turn left 90
        wheel_.forward(distance=side1)  # move forward side1

        """save resultant images"""


        # email_img(email_)

        """picking up"""
        print('picking up again')

        """turn to transportation route"""
        # print()
        # wheel_.rotate(90)  # turn left 90
    return True



if __name__ == '__main__':
    main()