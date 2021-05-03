#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   image.py    
@Github  :   https://github.com/StrikerCC

@Modify Time      @Author       @Version    @Desciption
------------      -------       --------    -----------
4/23/2021 9:20 PM   Cheng Chen    1.0         None
'''

# import lib
import cv2


def color_mask(img, limits):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV', img_HSV)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    ### hsv filter for green
    low_h, low_s, low_v = limits['low_limit']
    high_h, high_s, high_v = limits['up_limit']

    img_thresh = cv2.inRange(img_HSV, (low_h, low_s, low_v), (high_h, high_s, high_v))
    # cv2.imshow('mask', img_thresh)
    # cv2.waitKey(0)
    return img_thresh


def show_tracking(self, img):
    # frame = cv2.flip(img, 0)
    mask = self.color_mask(img)
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    # cv2.imshow('tracking', frame)
    # cv2.waitKey(0)
    return img


def find_ROI(img, limits):
    """
    find the center and area of pixels in limits
    :param img:
    :type img:
    :return:
    :rtype:
    """
    mask = color_mask(img, limits)

    # dilate the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    mask = cv2.dilate(mask, kernel)
    # cv2.imshow('dilated', mask)
    # cv2.waitKey(0)

    # get contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_biggest, area_biggest = contours[0], cv2.contourArea(contours[0])

    # biggest contour
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > area_biggest:
            contour_biggest = contour
            area_biggest = area

    # cv2.drawContours(img, [contour_biggest], -1, (0, 0, 255), 3)
    # cv2.imshow('tracking', img)
    # cv2.waitKey(0)
    
    M = cv2.moments(contour_biggest)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])

    # cv2.circle(mask, (cX, cY), 7, (255, 255, 255), -1)
    # cv2.putText(mask, str((cX, cY)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    # show the image
    # cv2.imshow('image', mask)
    # cv2.waitKey(0)

    return (cX, cY), area_biggest
