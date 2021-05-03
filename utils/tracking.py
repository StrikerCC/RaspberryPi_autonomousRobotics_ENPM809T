#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tracking.py    
@Github  :   https://github.com/StrikerCC

@Modify Time      @Author       @Version    @Desciption
------------      -------       --------    -----------
5/3/2021 7:24 AM   Cheng Chen    1.0         None
'''

# import lib
import sys, os
sys.path.insert(0, os.path.dirname(os.getcwd()))

import numpy as np
import cv2


from RaspberryPi_autonomousRobotics_ENPM809T.utils.image import find_ROI


def angle_of_object(camera_, color_limit_object):
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
        cv2.destroyAllWindows()

        """calculate the pixel coord"""
        angle = camera_.coord_img_to_pose(center)
        angle[0] = -angle[0]

        if area > 5.0:    # if the pixel cluster is big enough
            """transform to img coord"""
            print('frame', i, 'found object at', angle, 'degree')
            return angle

        if i % 100 == 0:
            print('frame', i, 'haven\'t find object yet')

    return None