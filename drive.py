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
from utils.camera import camera, recorder
from utils.ranger import sonar
from utils.gripper import gripper


def main():
    """video and image saving path"""
    path_ = './results/'
    path_video = path_ + 'drive.avi'
    path_img = path_ + 'drive.png'

    """operation classes"""
    wheel_ = wheel()    # dynamic units
    camera_ = camera()  # perception units


    """go live"""
    while True:

        camera_.view_some_frames(num_frames=8)
        if not wheel_.move_with_ui():
            break






if __name__ == '__main__':
    main()