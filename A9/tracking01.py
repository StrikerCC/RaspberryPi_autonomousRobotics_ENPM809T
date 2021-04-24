#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tracking01.py    
@Github  :   https://github.com/StrikerCC

@Modify Time      @Author       @Version    @Desciption
------------      -------       --------    -----------
4/23/2021 6:43 PM   Cheng Chen    1.0         None
'''

# import lib
import numpy as np
import cv2
import sys
import os


sys.path.insert(0, os.path.dirname(os.getcwd()))


from RaspberryPi_autonomousRobotics_ENPM809T.utils.camera_pi import camera_pi
from RaspberryPi_autonomousRobotics_ENPM809T.utils.wheel import wheelControlled

from RaspberryPi_autonomousRobotics_ENPM809T.utils.image import find_ROI

def keep_tracking(camera_, color_limit_object):
    frames_out = 10000

    print('looking for object like ', object, 'for', frames_out, 'frames')

    """find object in current frame"""
    for i in range(frames_out):
        img = camera_.view_one_frame()

        """find a contour around the object"""
        center, area = find_ROI(img, color_limit_object)
        radius = np.sqrt(area/2/np.pi)

        cv2.circle(img, center, int(radius), (255, 155, 155), 1)
        cv2.imshow(str(center), img)
        cv2.waitKey(0)

        """calculate the pixel coord"""
        angle = camera_.coord_img_to_pose(center)
        if area > 5.0:    # if the pixel cluster is big enough

            """transform to img coord"""
            print('frame', i, 'found object at', angle, 'degree')
            return angle

        if i % 100 == 0:
            print('frame', i, 'haven\'t find object yet')

    return None


def rotate_to_object(wheel, angle):
    assert -360.0 < angle < 360.0, 'cannot rotate ' + str(angle) + ' degree'

    if angle == 0.0:
        return True
    elif angle < 0.0:
        print('go left', angle)
        wheel.pivotleft(abs(angle))
        return True
    elif angle > 0.0:
        print('go right', angle)
        wheel.pivotright(abs(angle))
        return True
    return False


def main():
    """object color info"""
    low_h, low_s, low_v = (0, 174, 50)
    high_h, high_s, high_v = (12, 255, 189)
    object_color = {    ### hsv filter for object
        'low_limit': (low_h, low_s, low_v),
        'up_limit': (high_h, high_s, high_v)
    }

    camera_ = camera_pi()
    wheel_ = wheelControlled()

    print('tracking obejct of color', object_color)
    while True:
        if input('continue? y?') == 'y':
            angle = keep_tracking(camera_, object_color)
            print('find object at', angle, 'degree')

            assert angle[1] < camera_.fov()[1]  # only rotate in horizontal
            rotate_to_object(wheel_, angle[1])
        else:
            break


if __name__ == '__main__':
    main()
