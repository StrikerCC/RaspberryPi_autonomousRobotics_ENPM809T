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

from ..utils.camera_pi import camera_pi
from ..utils.wheel import wheelControlled

from ..utils.image import find_ROI

def keep_tracking(camera_, color_limit_object):
    frames_out = 10000

    print('looking for object like ', object, 'for', frames_out, 'frames')

    """find object in current frame"""
    for i in range(frames_out):
        img = camera_.view_one_frame()

        """find a contour around the object"""
        center, area = find_ROI(img, color_limit_object)

        """calculate the pixel coord"""
        angle = camera_.coord_img_to_pose(center)
        if area > 5.0:    # if the pixel cluster is big enough

            cv2.circle(img, center, 7, (255, 255, 255), -1)
            cv2.imshow(str(center), img)
            cv2.waitKey(0)

            """transform to img coord"""
            return angle

        if i % 100 == 0:
            print('frame', i, 'haven\'t find object yet')

    return None


def rotate(wheel, angle):
    assert -360.0 < angle < 360.0, 'cannot rotate ' + str(angle) + ' degree'

    if angle == 0.0:
        return True
    elif angle < 0.0:
        wheel.pivotleft(abs(angle))
        return True
    elif angle > 0.0:
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

            assert angle < camera_.fov()
            rotate(wheel_, angle)
        else:
            break


if __name__ == '__main__':
    main()
