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
from utils.wheel import wheel
from utils.camera_pi import camera_pi, recorder
from utils.ranger import sonar
from utils.gripper import gripper


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

def main():
    """video and image saving path"""
    path_ = './results/'
    path_video = path_ + 'drive.avi'
    path_img = path_ + 'drive.png'

    """operation classes"""
    wheel_ = wheel()    # dynamic units
    camera_ = camera_pi()  # perception units


    """go live"""
    while True:
        camera_.view_some_frames(num_frames=8)
        if not wheel_.read_user_input_then_move_acoordingly():   # break when user input q
            break



if __name__ == '__main__':
    main()