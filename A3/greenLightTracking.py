import numpy as np
import cv2
import imutils


# img = cv2.imread('green_light.jpg')

class tracking:
    def __init__(self):
        print("tracker ready")

    def colorMask(self, img):

        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # cv2.imshow('HSV', frame)
        # cv2.waitKey(0)

        ### hsv filter for green 
        low_h, low_s, low_v = (39, 113, 67)
        high_h, high_s, high_v = (87, 255, 91)
        ### hsv filter for red 
        # low_h, low_s, low_v = (106, 117, 92)
        # high_h, high_s, high_v = (255, 255, 255)

        img_thresh = cv2.inRange(img_HSV, (low_h, low_s, low_v), (high_h, high_s, high_v))
        # cv2.imshow('mask', frame_thresh)
        # cv2.waitKey(0)
        return img_thresh

    def showTracking(self, img):
        # frame = cv2.flip(img, 0)
        mask = self.colorMask(img)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0,0,255), 3)
        # cv2.imshow('tracking', frame)
        # cv2.waitKey(0)
        return img

